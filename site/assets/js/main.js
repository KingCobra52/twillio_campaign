/* Siddarth Thota Personal Alerts - progressive enhancement only.
   No analytics, no cookies, no storage, no network requests.
   Every page works fully with JavaScript disabled. */

(function () {
  "use strict";

  /* 1. Mark the current page in the navigation.
        The markup already sets aria-current; this keeps it correct if a
        page is reached through a path variant such as "/sms/index.html". */
  function markCurrentNavLink() {
    var here = window.location.pathname.replace(/index\.html$/, "");
    var links = document.querySelectorAll(".site-nav a");

    for (var i = 0; i < links.length; i++) {
      var target = new URL(links[i].getAttribute("href"), window.location.href);
      var path = target.pathname.replace(/index\.html$/, "");
      if (path === here) {
        links[i].setAttribute("aria-current", "page");
      } else {
        links[i].removeAttribute("aria-current");
      }
    }
  }

  /* 2. Move keyboard focus to the heading an in-page link points at, so
        screen-reader and keyboard users land where sighted users look. */
  function focusAnchorTargets() {
    document.addEventListener("click", function (event) {
      var link = event.target.closest ? event.target.closest('a[href^="#"]') : null;
      if (!link) {
        return;
      }

      var id = link.getAttribute("href").slice(1);
      if (!id) {
        return;
      }

      var target = document.getElementById(id);
      if (!target) {
        return;
      }

      if (!target.hasAttribute("tabindex")) {
        target.setAttribute("tabindex", "-1");
      }
      target.focus({ preventScroll: true });
    });
  }

  try {
    markCurrentNavLink();
    focusAnchorTargets();
  } catch (error) {
    /* Enhancement only - never break the page. */
  }
})();
