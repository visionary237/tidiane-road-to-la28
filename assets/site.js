(function () {
  "use strict";
  var cfg = window.SITE_CONFIG || {};

  // Menu mobile
  var btn = document.querySelector(".menu-btn");
  var mnav = document.getElementById("mobile-nav");
  if (btn && mnav) {
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!open));
      mnav.hidden = open;
      btn.querySelector(".txt").textContent = open ? "Menu" : "Fermer";
    });
  }

  // Année du pied de page
  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  // Compte à rebours LA28 (cérémonie d'ouverture le 14 juillet 2028, heure de Los Angeles)
  var cd = document.querySelectorAll("[data-countdown]");
  if (cd.length) {
    var target = Date.UTC(2028, 6, 15, 3, 0, 0); // 14/07/2028 20:00 PDT
    var days = Math.max(0, Math.ceil((target - Date.now()) / 86400000));
    cd.forEach(function (el) { el.textContent = days.toLocaleString("fr-FR"); });
  }

  // Galerie : visionneuse
  var gallery = document.querySelector(".gallery");
  var lb = document.getElementById("lightbox");
  if (gallery && lb) {
    var lbImg = lb.querySelector("img"), lbCap = lb.querySelector("figcaption"), closeBtn = lb.querySelector(".close"), lastFocus = null;
    function close() { lb.hidden = true; lbImg.removeAttribute("src"); if (lastFocus) lastFocus.focus(); }
    gallery.addEventListener("click", function (e) {
      var b = e.target.closest("button[data-full]");
      if (!b) return;
      lastFocus = b;
      lbImg.src = b.getAttribute("data-full");
      lbImg.alt = b.querySelector("img").alt;
      lbCap.textContent = b.getAttribute("data-caption") || "";
      lb.hidden = false;
      closeBtn.focus();
    });
    closeBtn.addEventListener("click", close);
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !lb.hidden) close(); });
  }

  // Copier un numéro ou une adresse
  document.querySelectorAll("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var text = b.getAttribute("data-copy");
      var done = function () { var t = b.textContent; b.textContent = "Copié"; setTimeout(function () { b.textContent = t; }, 1600); };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () { selectNext(b); });
      } else { selectNext(b); }
    });
  });
  function selectNext(b) {
    var code = b.parentElement.querySelector("code");
    if (!code) return;
    var r = document.createRange(); r.selectNodeContents(code);
    var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
  }

  // Formulaire de contact qualifiant
  var form = document.getElementById("contact-form");
  if (form) {
    var started = Date.now();
    var status = document.getElementById("form-status");
    var type = document.getElementById("f-type");
    var h = (location.hash || "").replace("#", "");
    if (type && h) { for (var i = 0; i < type.options.length; i++) { if (type.options[i].value === h) type.value = h; } }

    function show(msg, isError) {
      status.hidden = false;
      status.className = "notice" + (isError ? " error" : "");
      status.textContent = msg;
      status.focus();
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.checkValidity()) { form.reportValidity(); return; }
      // Anti-spam : champ piège et délai minimal de saisie
      if (form.website.value !== "" || Date.now() - started < 3000) {
        show("Votre demande n'a pas pu être envoyée. Merci de réessayer dans quelques secondes.", true);
        return;
      }
      var data = {
        entreprise: form.entreprise.value.trim(),
        secteur: form.secteur.value,
        nom: form.nom.value.trim(),
        fonction: form.fonction.value.trim(),
        email: form.email.value.trim(),
        type_partenariat: form.type.value,
        budget: form.budget.value,
        message: form.message.value.trim(),
        consentement: form.consent.checked,
        texte_consentement: document.getElementById("consent-text").textContent.trim(),
        page: location.pathname,
        date: new Date().toISOString(),
        source: "site-tidiane-road-to-la28"
      };
      if (!cfg.crmEndpoint) {
        show("Aperçu : le formulaire fonctionne, mais l'envoi vers le CRM " + (cfg.crmName || "") + " n'est pas encore branché. En attendant, contactez le management par téléphone ou à marinefordmanagement@gmail.com.", false);
        return;
      }
      var submit = form.querySelector("[type=submit]");
      submit.disabled = true; submit.textContent = "Envoi…";
      fetch(cfg.crmEndpoint, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) })
        .then(function (r) { if (!r.ok) throw new Error(r.status); form.reset(); show("Merci, votre demande est bien arrivée. Le management vous répond sous 72 heures ouvrées.", false); })
        .catch(function () { show("L'envoi a échoué. Vérifiez votre connexion puis réessayez, ou appelez le management.", true); })
        .then(function () { submit.disabled = false; submit.textContent = "Envoyer la demande"; });
    });
  }
})();
