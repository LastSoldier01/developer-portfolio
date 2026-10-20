/* ==========================================================================
   main.js — small vanilla JS for the portfolio.
   Behaviors: loader, nav hide-on-scroll, active section highlight,
   scroll reveals, mobile menu (focus trap + Escape).
   Everything degrades gracefully when this file fails to load.
   ========================================================================== */
(function () {
  "use strict";

  var prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Loader (home page only) ---------- */
  function initLoader() {
    var loader = document.getElementById("loader");
    var isHome = document.querySelector(".hero") !== null;
    if (!loader || !isHome || prefersReducedMotion) {
      if (loader) {
        loader.remove();
      }
      return;
    }
    loader.classList.add("show");
    window.setTimeout(function () {
      loader.remove();
    }, 1500);
  }

  /* ---------- Hero entrance (staggered fade-up) ---------- */
  function initHeroFade() {
    var items = document.querySelectorAll(".fade-item");
    if (!items.length) {
      return;
    }
    window.setTimeout(
      function () {
        items.forEach(function (item) {
          item.classList.add("is-visible");
        });
      },
      prefersReducedMotion ? 0 : 150
    );
  }

  /* ---------- Header: shrink on scroll, hide going down ---------- */
  function initNavScroll() {
    var header = document.getElementById("site-header");
    if (!header) {
      return;
    }
    var lastScrollY = window.scrollY;
    var ticking = false;

    function update() {
      var currentScrollY = window.scrollY;
      var goingDown = currentScrollY > lastScrollY;

      header.classList.toggle("scrolled", currentScrollY > 50);

      if (!prefersReducedMotion && goingDown && currentScrollY > 300) {
        header.classList.add("nav-hidden");
      } else {
        header.classList.remove("nav-hidden");
      }

      lastScrollY = currentScrollY;
      ticking = false;
    }

    window.addEventListener(
      "scroll",
      function () {
        if (!ticking) {
          window.requestAnimationFrame(update);
          ticking = true;
        }
      },
      { passive: true }
    );
  }

  /* ---------- Active section highlight in the nav ---------- */
  function initActiveSection() {
    var sections = document.querySelectorAll("section[data-nav-section]");
    if (!sections.length || !("IntersectionObserver" in window)) {
      return;
    }
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) {
            return;
          }
          var id = entry.target.id;
          document.querySelectorAll("[data-nav-link]").forEach(function (link) {
            link.classList.toggle("active", link.getAttribute("data-nav-link") === id);
          });
        });
      },
      { rootMargin: "-50% 0px -50% 0px" }
    );
    sections.forEach(function (section) {
      observer.observe(section);
    });
  }

  /* ---------- Scroll reveals (with stagger via inline delays) ---------- */
  function initReveals() {
    var elements = document.querySelectorAll(".reveal");
    if (!elements.length) {
      return;
    }
    if (prefersReducedMotion || !("IntersectionObserver" in window)) {
      elements.forEach(function (el) {
        el.classList.add("is-visible");
      });
      return;
    }
    var observer = new IntersectionObserver(
      function (entries, obs) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );
    elements.forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ---------- Mobile menu ---------- */
  function initMenu() {
    var toggle = document.querySelector(".menu-toggle");
    var menu = document.getElementById("mobile-menu");
    if (!toggle || !menu) {
      return;
    }

    function setOpen(open) {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      menu.classList.toggle("open", open);
      menu.setAttribute("aria-hidden", open ? "false" : "true");
      document.body.classList.toggle("menu-open", open);
      if (open) {
        var firstLink = menu.querySelector("a");
        if (firstLink) {
          firstLink.focus();
        }
      }
    }

    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });

    // Close when a menu link is chosen
    menu.addEventListener("click", function (event) {
      if (event.target.closest("a")) {
        setOpen(false);
      }
    });

    // Close on Escape and keep Tab focus inside the open menu
    document.addEventListener("keydown", function (event) {
      var isOpen = toggle.getAttribute("aria-expanded") === "true";
      if (!isOpen) {
        return;
      }
      if (event.key === "Escape") {
        setOpen(false);
        toggle.focus();
        return;
      }
      if (event.key === "Tab") {
        var focusables = [toggle].concat(Array.prototype.slice.call(menu.querySelectorAll("a")));
        var first = focusables[0];
        var last = focusables[focusables.length - 1];
        if (event.shiftKey && document.activeElement === first) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && document.activeElement === last) {
          event.preventDefault();
          first.focus();
        }
      }
    });

    // Close when resizing back to the desktop layout
    window.addEventListener("resize", function () {
      if (window.innerWidth > 768 && toggle.getAttribute("aria-expanded") === "true") {
        setOpen(false);
      }
    });
  }

  /* ---------- Init ---------- */
  function init() {
    initLoader();
    initHeroFade();
    initNavScroll();
    initActiveSection();
    initReveals();
    initMenu();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
