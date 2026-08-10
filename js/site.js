(function () {
  "use strict";

  function ready(fn) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", fn);
    } else {
      fn();
    }
  }

  ready(function () {
    var toggle = document.querySelector(".menu-toggle");
    var links = document.querySelector(".nav-links");

    if (toggle && links) {
      toggle.addEventListener("click", function () {
        var open = links.classList.toggle("open");
        toggle.setAttribute("aria-expanded", open ? "true" : "false");
      });

      links.querySelectorAll("a").forEach(function (anchor) {
        anchor.addEventListener("click", function () {
          links.classList.remove("open");
          toggle.setAttribute("aria-expanded", "false");
        });
      });
    }

    var filterButtons = document.querySelectorAll("[data-filter]");
    var cards = document.querySelectorAll("[data-category]");

    if (filterButtons.length && cards.length) {
      filterButtons.forEach(function (btn) {
        btn.addEventListener("click", function () {
          var filter = btn.getAttribute("data-filter");
          filterButtons.forEach(function (item) {
            item.classList.toggle("active", item === btn);
          });
          cards.forEach(function (card) {
            var category = card.getAttribute("data-category");
            var show = filter === "all" || category === filter;
            card.classList.toggle("hidden", !show);
          });
        });
      });
    }

    var faqList = document.querySelector(".faq-list");
    if (faqList) {
      faqList.addEventListener(
        "toggle",
        function (e) {
          var t = e.target;
          if (!t || t.tagName !== "DETAILS" || !t.open) return;
          faqList.querySelectorAll("details[open]").forEach(function (d) {
            if (d !== t) d.removeAttribute("open");
          });
        },
        true
      );
    }

    var lazyFrames = document.querySelectorAll("iframe[data-src]");
    if (lazyFrames.length) {
      var loadFrame = function (el) {
        var src = el.getAttribute("data-src");
        if (!src) return;
        el.setAttribute("src", src);
        el.removeAttribute("data-src");
      };

      if ("IntersectionObserver" in window) {
        var io = new IntersectionObserver(
          function (entries) {
            entries.forEach(function (entry) {
              if (!entry.isIntersecting) return;
              loadFrame(entry.target);
              io.unobserve(entry.target);
            });
          },
          { rootMargin: "200px 0px" }
        );
        lazyFrames.forEach(function (frame) {
          io.observe(frame);
        });
      } else {
        lazyFrames.forEach(loadFrame);
      }
    }

    // Click-to-play keeps heavy MP4 off the initial load (Core Web Vitals)
    document.querySelectorAll(".video-poster-play").forEach(function (wrap) {
      var play = function () {
        var src = wrap.getAttribute("data-video-src");
        var container = wrap.parentElement;
        if (!container || !src) return;
        var video = container.querySelector(".hero-lazy-video");
        if (!video) return;
        var source = video.querySelector("source");
        if (source && !source.getAttribute("src")) {
          source.setAttribute("src", source.getAttribute("data-src") || src);
        }
        wrap.hidden = true;
        video.hidden = false;
        try {
          video.load();
          var p = video.play();
          if (p && typeof p.catch === "function") p.catch(function () {});
        } catch (e) {}
      };
      wrap.addEventListener("click", play);
      var btn = wrap.querySelector(".video-play-btn");
      if (btn) {
        btn.addEventListener("click", function (e) {
          e.preventDefault();
          play();
        });
      }
    });
  });
})();
