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

    // Click-to-play: Cloudflare Workers assets often lack HTTP Range support,
    // which breaks progressive MP4 playback — load via blob when needed.
    document.querySelectorAll(".video-poster-play").forEach(function (wrap) {
      var busy = false;

      var reveal = function (video, container) {
        wrap.hidden = true;
        video.hidden = false;
        if (container) container.classList.add("is-playing");
        var p = video.play();
        if (p && typeof p.catch === "function") {
          p.catch(function () {
            video.setAttribute("controls", "");
          });
        }
      };

      var playFromBlob = function (video, container, src, btn) {
        return fetch(src)
          .then(function (res) {
            if (!res.ok) throw new Error("video fetch failed");
            return res.blob();
          })
          .then(function (blob) {
            video.src = URL.createObjectURL(blob);
            video.load();
            reveal(video, container);
          })
          .catch(function () {
            busy = false;
            if (btn) btn.textContent = "Play preview";
          });
      };

      var play = function (e) {
        if (e) {
          e.preventDefault();
          e.stopPropagation();
        }
        if (busy) return;
        busy = true;

        var src = wrap.getAttribute("data-video-src");
        var container = wrap.parentElement;
        if (!container || !src) {
          busy = false;
          return;
        }
        var video = container.querySelector(".hero-lazy-video");
        if (!video) {
          busy = false;
          return;
        }

        var btn = wrap.querySelector(".video-play-btn");
        if (btn) btn.textContent = "Loading…";

        // Prefer direct URL first (fast on caches that support it)
        video.removeAttribute("src");
        while (video.firstChild) video.removeChild(video.firstChild);
        video.src = src;
        video.setAttribute("playsinline", "");
        video.setAttribute("webkit-playsinline", "");
        video.controls = true;

        var settled = false;
        var finishOk = function () {
          if (settled) return;
          settled = true;
          reveal(video, container);
        };
        var finishBlob = function () {
          if (settled) return;
          settled = true;
          playFromBlob(video, container, src, btn);
        };

        video.addEventListener("loadeddata", finishOk, { once: true });
        video.addEventListener("error", finishBlob, { once: true });
        video.load();

        // If the file hangs (common without Accept-Ranges), fall back to blob
        setTimeout(function () {
          if (!settled && video.readyState < 2) finishBlob();
        }, 1800);
      };

      wrap.addEventListener("click", play);
      var btn = wrap.querySelector(".video-play-btn");
      if (btn) btn.addEventListener("click", play);
    });
  });
})();
