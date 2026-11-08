/* Ascendera shared behaviour */
(function () {
  'use strict';
  var nav = document.querySelector('.nav');
  var button = nav && nav.querySelector('.nav__toggle');
  if (!button) return;
  var ar = document.documentElement.lang === 'ar';
  button.hidden = false;
  nav.classList.add('nav--enhanced');
  function setOpen(open) {
    nav.classList.toggle('is-open', open);
    button.setAttribute('aria-expanded', String(open));
    button.textContent = ar ? (open ? 'إغلاق القائمة' : 'القائمة') : (open ? 'Close menu' : 'Menu');
  }
  button.addEventListener('click', function () { setOpen(button.getAttribute('aria-expanded') !== 'true'); });
  nav.querySelectorAll('.nav__links a').forEach(function (a) { a.addEventListener('click', function () { setOpen(false); }); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && button.getAttribute('aria-expanded') === 'true') { setOpen(false); button.focus(); }
  });
  document.addEventListener('click', function (e) { if (!nav.contains(e.target)) setOpen(false); });
  var mobile = window.matchMedia('(max-width:1000px)');
  mobile.addEventListener('change', function () { setOpen(false); });
})();

/* Decorative motion can be paused independently of narrated watch pages. */
(function () {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  document.querySelectorAll('.hero__video').forEach(function (video) {
    var ar = document.documentElement.lang === 'ar';
    var button = document.createElement('button');
    button.type = 'button'; button.className = 'motion-toggle';
    function label() { button.textContent = ar ? (video.paused ? 'تشغيل الخلفية المتحركة' : 'إيقاف الخلفية المتحركة') : (video.paused ? 'Play background motion' : 'Pause background motion'); }
    video.closest('.hero').appendChild(button);
    button.addEventListener('click', function () { if (video.paused) video.play().catch(label); else video.pause(); });
    video.addEventListener('play', label); video.addEventListener('pause', label);
    if (reduced.matches) video.pause();
    reduced.addEventListener('change', function (e) { if (e.matches) video.pause(); });
    label();
  });
})();

(function () {
  "use strict";

  /* Marquee: constant pixel speed on every device.
     The CSS animates the track by -50% over a fixed duration, so a wider
     track (big system font settings, zoomed displays, fallback fonts)
     scrolls proportionally faster. Measure the real width and derive the
     duration from it so the pace is identical everywhere. */
  (function () {
    var SPEED = 60; // px per second, matches the designed desktop pace
    function tune() {
      document.querySelectorAll(".marquee__track").forEach(function (t) {
        var w = t.scrollWidth / 2;
        if (w > 0) t.style.animationDuration = (w / SPEED).toFixed(2) + "s";
      });
    }
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(tune);
    tune();
    var rt;
    window.addEventListener("resize", function () {
      clearTimeout(rt);
      rt = setTimeout(tune, 200);
    });
  })();

  /* Split headline words into masked spans for the word-by-word reveal.
     Handles plain text and inline <em> accents. */
  var wordIndex = 0;
  function splitWords(el) {
    var frag = document.createDocumentFragment();
    Array.from(el.childNodes).forEach(function (node) {
      if (node.nodeType === Node.TEXT_NODE) {
        node.textContent.split(/(\s+)/).forEach(function (piece) {
          if (!piece) return;
          if (/^\s+$/.test(piece)) { frag.appendChild(document.createTextNode(" ")); return; }
          frag.appendChild(makeWord(piece, null));
        });
      } else if (node.nodeType === Node.ELEMENT_NODE) {
        node.textContent.split(/(\s+)/).forEach(function (piece) {
          if (!piece) return;
          if (/^\s+$/.test(piece)) { frag.appendChild(document.createTextNode(" ")); return; }
          frag.appendChild(makeWord(piece, node.tagName.toLowerCase()));
        });
      }
    });
    el.innerHTML = "";
    el.appendChild(frag);
  }

  function makeWord(word, wrapTag) {
    var w = document.createElement("span");
    w.className = "w";
    var s = document.createElement("span");
    s.style.setProperty("--d", (0.08 + wordIndex++ * 0.085) + "s");
    s.textContent = word;
    w.appendChild(s);
    if (wrapTag) {
      var outer = document.createElement(wrapTag);
      outer.appendChild(w);
      return outer;
    }
    return w;
  }

  document.querySelectorAll("[data-words]").forEach(function (el) {
    wordIndex = 0;
    splitWords(el);
  });

  /* Trigger hero reveal after fonts settle */
  window.addEventListener("load", function () {
    requestAnimationFrame(function () { document.body.classList.add("loaded"); });
  });
  setTimeout(function () { document.body.classList.add("loaded"); }, 900);

  /* Scroll progress bar + nav state */
  var bar = document.querySelector(".progress");
  function onScroll() {
    var h = document.documentElement;
    var max = h.scrollHeight - h.clientHeight;
    if (bar) bar.style.transform = "scaleX(" + (max > 0 ? h.scrollTop / max : 0) + ")";
    var nav = document.querySelector(".nav");
    if (nav) nav.classList.toggle("scrolled", h.scrollTop > 40);
  }
  document.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* IntersectionObserver reveals with per-sibling stagger */
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        e.target.classList.add("revealed");
        io.unobserve(e.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -8% 0px" });

  document.querySelectorAll("[data-reveal]").forEach(function (el) {
    var sibs = el.parentElement ? el.parentElement.querySelectorAll(":scope > [data-reveal]") : [el];
    var n = Array.prototype.indexOf.call(sibs, el);
    el.style.setProperty("--rd", (Math.max(0, n) * 0.09) + "s");
    io.observe(el);
  });

  /* Count-up stats */
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var cio = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target, target = parseFloat(el.dataset.count), suffix = el.dataset.suffix || "", prefix = el.dataset.prefix || "";
      if (reduceMotion) { el.textContent = prefix + target + suffix; cio.unobserve(el); return; }
      var dur = 1600, t0 = null;
      function tick(t) {
        if (!t0) t0 = t;
        var p = Math.min(1, (t - t0) / dur);
        var eased = 1 - Math.pow(1 - p, 4);
        el.textContent = prefix + Math.round(target * eased) + suffix;
        if (p < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
      cio.unobserve(el);
    });
  }, { threshold: 0.35 });
  document.querySelectorAll("[data-count]").forEach(function (el) {
    el.textContent = (el.dataset.prefix || "") + "0" + (el.dataset.suffix || "");
    cio.observe(el);
  });
})();

/* Barrier film-synced hero: hide hero copy while the film plays, reveal it
   when the film ends, then let it stay while the film loops behind it. */
(function () {
  // SPA body class is brand-veriso; the barrier page sections are
  // #p-veriso-barrier (EN) and #p-ar-veriso-barrier (AR).
  var videos = [];
  ["p-veriso-barrier", "p-ar-veriso-barrier"].forEach(function (id) {
    var sec = document.getElementById(id);
    if (!sec) return;
    var v = sec.querySelector(".hero__video");
    if (v) videos.push(v);
  });
  if (!videos.length) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  function onBarrierRoute() { return location.hash.indexOf("veriso/barrier") !== -1; }
  function arm() {
    if (document.body.classList.contains("film-ended")) return;
    document.body.classList.add("film-armed");
  }
  if (onBarrierRoute()) arm();
  window.addEventListener("hashchange", function () {
    if (onBarrierRoute()) arm();
    else document.body.classList.remove("film-armed");
  });
  function endFilm() {
    if (document.body.classList.contains("film-ended")) return;
    document.body.classList.add("film-ended");
    videos.forEach(function (v) {
      v.removeEventListener("ended", endFilm);
      v.removeEventListener("timeupdate", onTime);
    });
  }
  function onTime() {
    videos.forEach(function (v) {
      if (v.duration && v.currentTime > v.duration - 1.4) endFilm();
    });
  }
  videos.forEach(function (v) {
    v.addEventListener("ended", endFilm);
    v.addEventListener("timeupdate", onTime);
  });
  // safety: never trap the page without copy
  setTimeout(endFilm, 36000);
})();

/* Contact form: after FormSubmit redirects back with ?sent=1, show the
   thank-you panel and hide the form. */
(function () {
  if (!/[?&]sent=1/.test(location.search)) return;
  var done = document.getElementById("form-sent");
  var form = document.querySelector("form.form");
  if (!done) return;
  done.hidden = false;
  if (form) form.style.display = "none";
  window.scrollTo(0, 0);
})();

/* Carry the selected HSSE service into the enquiry without overwriting user input. */
(function () {
  var select = document.getElementById('f-need');
  if (!select) return;
  var service = new URLSearchParams(window.location.search).get('service');
  var option = Array.from(select.options).find(function (item) { return item.value === service; });
  if (option && !select.value) select.value = option.value;
  function updateService() {
    var detail = document.getElementById('service-detail');
    if (detail) detail.value = /^hsse(?:-\d+)?$/.test(select.value) ? select.options[select.selectedIndex].text : '';
    var language = document.querySelector('.lang-toggle');
    if (language) {
      var target = new URL(language.href);
      if (/^hsse(?:-\d+)?$/.test(select.value)) target.searchParams.set('service', select.value);
      else target.searchParams.delete('service');
      language.href = target.href;
    }
  }
  select.addEventListener('change', updateService);
  updateService();
})();
