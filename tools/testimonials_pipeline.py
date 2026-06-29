# -*- coding: utf-8 -*-
"""Download Bali-finished testimonial masters from Drive, compress for web,
generate posters, upload to R2 (media.veblengroup.com.au). Idempotent."""
import json, os, subprocess, sys, urllib.request

TOKEN_FILE = r"C:\Users\admin\.gdrive-sync\token_readonly.json"
FFMPEG = r"C:\Users\admin\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin\ffmpeg.exe"
FFPROBE = FFMPEG.replace("ffmpeg.exe", "ffprobe.exe")
WORK = r"C:\Users\admin\veblen-website-v2\_video_src"
OUT = r"C:\Users\admin\veblen-website-v2\_video_out"

FILES = [
    ("1khf0Yp2HIXZ5XansxO6WUDtLkHbkTE1S", "luke-lcmb"),
    ("1kMyToOefuwSXYSVieMfpuJgJ32yrO9TN", "josh-nt-trailers"),
    ("1oE2KYhVM5LsXAI_dWodvCrViFAX0VCOS", "ardy-crown-realty"),
    ("1PNDzB_IXE700elYmTXe9x5J9MENcOI9j", "kento-crown-realty"),
    ("1McpNXlz1kRpsVVd8uOIfAsAIUox4Dbk0", "bish-talentport"),
    ("1GIZQAeTl7rLnHePRsxdZcPvRhbpOclOx", "david-adv-painting"),
    ("1mXW4UEgvphf8u5dBXW1ULLn22WRPn7Dx", "extra-clip"),
]

os.makedirs(WORK, exist_ok=True)
os.makedirs(OUT, exist_ok=True)

tok = json.load(open(TOKEN_FILE))
data = urllib.parse.urlencode({
    "client_id": tok["client_id"], "client_secret": tok["client_secret"],
    "refresh_token": tok["refresh_token"], "grant_type": "refresh_token",
}).encode()
req = urllib.request.Request(tok.get("token_uri", "https://oauth2.googleapis.com/token"), data=data)
access = json.load(urllib.request.urlopen(req))["access_token"]
print("token ok")

for fid, name in FILES:
    dst = os.path.join(WORK, name + ".mp4")
    if os.path.exists(dst) and os.path.getsize(dst) > 1000:
        print("have", name); continue
    url = f"https://www.googleapis.com/drive/v3/files/{fid}?alt=media&supportsAllDrives=true"
    r = urllib.request.Request(url, headers={"Authorization": "Bearer " + access})
    with urllib.request.urlopen(r) as resp, open(dst, "wb") as f:
        while True:
            chunk = resp.read(1 << 20)
            if not chunk: break
            f.write(chunk)
    print("downloaded", name, os.path.getsize(dst) // (1 << 20), "MB")

def probe(p):
    out = subprocess.check_output([FFPROBE, "-v", "quiet", "-print_format", "json",
                                   "-show_streams", "-show_format", p]).decode()
    j = json.loads(out)
    v = next(s for s in j["streams"] if s["codec_type"] == "video")
    return int(v["width"]), int(v["height"]), float(j["format"]["duration"])

results = []
for fid, name in FILES:
    src = os.path.join(WORK, name + ".mp4")
    mp4 = os.path.join(OUT, name + ".mp4")
    jpg = os.path.join(OUT, name + ".jpg")
    w, h, dur = probe(src)
    scale = "scale=1280:-2" if w >= h else "scale=-2:1280"
    if not os.path.exists(mp4):
        cmd = [FFMPEG, "-y", "-i", src, "-vf", scale,
               "-c:v", "h264_nvenc", "-preset", "p5", "-rc", "vbr", "-cq", "29",
               "-b:v", "0", "-maxrate", "3M", "-bufsize", "6M",
               "-c:a", "aac", "-b:a", "96k", "-ac", "2",
               "-movflags", "+faststart", "-pix_fmt", "yuv420p", mp4]
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not os.path.exists(jpg):
        subprocess.check_call([FFMPEG, "-y", "-ss", "1", "-i", mp4, "-frames:v", "1",
                               "-q:v", "4", jpg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    results.append((name, w, h, round(dur), os.path.getsize(mp4) // (1 << 20)))
    print(f"encoded {name}: {w}x{h} {round(dur)}s -> {os.path.getsize(mp4)//(1<<20)}MB")

# upload
import boto3
env = {}
with open(r"C:\Users\admin\.r2-social.env") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1); env[k] = v
s3 = boto3.client("s3",
    endpoint_url=f"https://{env['R2_ACCOUNT_ID']}.r2.cloudflarestorage.com",
    aws_access_key_id=env["R2_ACCESS_KEY_ID"],
    aws_secret_access_key=env["R2_SECRET_ACCESS_KEY"], region_name="auto")
base = env["R2_PUBLIC_BASE_URL"].rstrip("/")
for fid, name in FILES:
    for ext, ctype in [(".mp4", "video/mp4"), (".jpg", "image/jpeg")]:
        key = f"site/testimonials/{name}{ext}"
        s3.upload_file(os.path.join(OUT, name + ext), env["R2_BUCKET"], key,
                       ExtraArgs={"ContentType": ctype, "CacheControl": "public, max-age=31536000, immutable"})
        print("uploaded", base + "/" + key)
print("DONE")
