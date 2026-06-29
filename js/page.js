/* Veblen v2 inner pages — lead form + reveal. ~2KB, no dependencies. */
(function () {
  "use strict";

  var ENDPOINT = "https://veblen-platform-production.up.railway.app/api/webhooks/intake/website-contact-us";

  // reveal
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "60px" });
    document.querySelectorAll("[data-fade]").forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll("[data-fade]").forEach(function (el) { el.classList.add("in"); });
  }


  // in-place testimonial players on case pages
  document.querySelectorAll(".vcard__play[data-vplay]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var frame = btn.closest(".vcard__frame");
      var v = document.createElement("video");
      v.src = btn.dataset.vplay;
      v.controls = true; v.autoplay = true; v.playsInline = true;
      v.style.cssText = "position:absolute;inset:0;width:100%;height:100%;object-fit:cover;";
      frame.appendChild(v);
      btn.style.display = "none";
      v.addEventListener("ended", function () { v.remove(); btn.style.display = ""; });
    });
  });

  // lead form (one per page; entryPath carries the page slug)
  var form = document.getElementById("pform");
  if (!form) return;

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.checkValidity()) { form.reportValidity(); return; }
    var btn = form.querySelector("button[type=submit]");
    btn.disabled = true;
    btn.textContent = "Sending…";

    var raw = {};
    new FormData(form).forEach(function (v, k) { raw[k] = v; });
    var params = new URLSearchParams(location.search);
    var payload = {
      email: (raw.email || "").trim(),
      firstName: (raw.first_name || "").trim(),
      lastName: (raw.last_name || "").trim(),
      phone: (raw.phone || "").trim(),
      company: (raw.business || "").trim(),
      annualRevenue: raw.revenue || undefined,
      monthlyAdSpend: raw.ad_spend || undefined,
      entryPath: form.getAttribute("data-entrypath") || "website-page",
      landingPageUrl: location.href,
      utm_source: params.get("utm_source") || undefined,
      utm_medium: params.get("utm_medium") || undefined,
      utm_campaign: params.get("utm_campaign") || undefined,
      utm_content: params.get("utm_content") || undefined
    };

    var done = function () {
      form.querySelectorAll("label, button").forEach(function (el) { el.hidden = true; });
      document.getElementById("pform-success").hidden = false;
      if (typeof gtag === "function") gtag("event", "generate_lead", { page_path: location.pathname });
    };
    var fail = function () {
      window.location.href = "mailto:admin@veblengroup.com.au?subject=Website%20enquiry%20(" +
        encodeURIComponent(payload.company || "") + ")&body=" + encodeURIComponent(JSON.stringify(payload, null, 2));
    };

    fetch(ENDPOINT, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
      .then(function (r) { if (r.ok) { done(); } else { fail(); } })
      .catch(fail);
  });
})();
