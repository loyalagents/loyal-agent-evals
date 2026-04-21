(function () {
  var toggle = document.querySelector(".site-nav__toggle");
  var list = document.querySelector(".site-nav__list");
  if (toggle && list) {
    toggle.addEventListener("click", function () {
      var open = list.getAttribute("data-open") === "true";
      list.setAttribute("data-open", open ? "false" : "true");
      toggle.setAttribute("aria-expanded", open ? "false" : "true");
    });
  }

  var path = window.location.pathname.replace(/\/+$/, "/");
  var links = document.querySelectorAll(".site-nav__list a[href]");
  links.forEach(function (a) {
    var href = a.getAttribute("href");
    var resolved;
    try {
      resolved = new URL(href, window.location.href).pathname.replace(/\/+$/, "/");
    } catch (e) {
      return;
    }
    if (resolved === path) {
      a.setAttribute("aria-current", "page");
    }
  });
})();
