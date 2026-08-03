/* stuffaboutcode.com — theme toggle, code copy buttons, client-side search.
   Vanilla, no dependencies. The theme is applied inline in <head>; this only
   wires the button. */

(function () {
  "use strict";

  /* ------------------------------------------------------------ theme */

  var root = document.documentElement;

  // The button names the mode it switches TO. The word goes in its own span so
  // a narrow header can drop it and keep the glyph; the aria-label carries the
  // full meaning either way.
  function setLabel(btn, theme) {
    var word = theme === "dark" ? "light" : "dark";
    var glyph = theme === "dark" ? "☀" : "☾";
    var span = document.createElement("span");
    span.className = "toggle-word";
    span.textContent = word + " ";  // space inside, so hiding the word hides it too
    btn.textContent = "";
    btn.appendChild(span);
    btn.appendChild(document.createTextNode(glyph));
    btn.setAttribute("aria-label", "Switch to " + word + " theme");
  }

  var toggle = document.querySelector("[data-theme-toggle]");
  if (toggle) {
    setLabel(toggle, root.dataset.theme || "dark");
    toggle.addEventListener("click", function () {
      var next = (root.dataset.theme === "light") ? "dark" : "light";
      root.dataset.theme = next;
      setLabel(toggle, next);
      try { localStorage.setItem("theme", next); } catch (e) { /* ignore */ }
    });
  }

  /* ------------------------------------------------------------ code blocks

     Rouge emits <div class="language-x highlighter-rouge"><div class="highlight">
     <pre>. The design wants a header strip above it carrying the language and a
     copy button, so build that here rather than post-processing the Markdown. */

  document.querySelectorAll(".prose div.highlighter-rouge").forEach(function (block) {
    var m = block.className.match(/language-([\w+-]+)/);
    var lang = m ? m[1] : "text";
    if (lang === "plaintext") lang = "text";

    var head = document.createElement("div");
    head.className = "code-head";

    var name = document.createElement("span");
    name.className = "code-lang";
    name.textContent = lang;
    head.appendChild(name);

    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy-btn";
    btn.textContent = "copy";
    head.appendChild(btn);

    block.insertBefore(head, block.firstChild);

    btn.addEventListener("click", function () {
      var pre = block.querySelector("pre");
      if (!pre) return;
      var done = function () {
        btn.textContent = "copied";
        setTimeout(function () { btn.textContent = "copy"; }, 1200);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(pre.innerText).then(done, function () {
          btn.textContent = "failed";
          setTimeout(function () { btn.textContent = "copy"; }, 1200);
        });
      } else {
        // http:// or an older browser: no clipboard API
        var sel = window.getSelection();
        var range = document.createRange();
        range.selectNodeContents(pre);
        sel.removeAllRanges();
        sel.addRange(range);
        try { document.execCommand("copy"); done(); } catch (e) { /* ignore */ }
        sel.removeAllRanges();
      }
    });
  });

  /* ------------------------------------------------------------ search */

  var input = document.querySelector("[data-search-input]");
  if (!input) return;

  var tagBase = input.getAttribute("data-tag-base") || "/tags/";
  var results = document.querySelector("[data-list-results]");
  var kicker = document.querySelector("[data-list-kicker]");
  var subEl = document.querySelector("[data-list-sub]");
  var countEl = document.querySelector("[data-list-count]");
  var pager = document.querySelector(".pagination");

  // No list on this page (a post, or a static page): hand off to the home list.
  if (!results) {
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter" && input.value.trim()) {
        var base = document.querySelector(".wordmark").getAttribute("href") || "/";
        location.href = base + "?q=" + encodeURIComponent(input.value.trim());
      }
    });
    return;
  }

  var original = {
    html: results.innerHTML,
    kicker: kicker ? kicker.textContent : "",
    sub: subEl ? subEl.textContent : "",
    count: countEl ? countEl.textContent : ""
  };

  var index = null;
  var loading = null;

  function loadIndex() {
    if (index) return Promise.resolve(index);
    if (loading) return loading;
    var url = input.getAttribute("data-search-url") || "/search.json";
    loading = fetch(url)
      .then(function (r) { return r.json(); })
      .then(function (data) { index = data; return index; })
      .catch(function () { index = []; return index; });
    return loading;
  }

  function restore() {
    results.innerHTML = original.html;
    if (kicker) kicker.textContent = original.kicker;
    if (subEl) subEl.textContent = original.sub;
    if (countEl) countEl.textContent = original.count;
    if (pager) pager.hidden = false;
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  function render(hits, query) {
    if (kicker) kicker.textContent = "search results";
    if (subEl) subEl.textContent = 'matching “' + query + '”';
    if (countEl) countEl.textContent = hits.length + (hits.length === 1 ? " post" : " posts");
    if (pager) pager.hidden = true;

    if (!hits.length) {
      results.innerHTML =
        '<div class="empty-state">no posts matched “' + esc(query) + '”. try ' +
        '<a href="' + tagBase + 'minecraft/">minecraft</a>, ' +
        '<a href="' + tagBase + 'gpio/">gpio</a> or ' +
        '<a href="' + tagBase + 'python/">python</a></div>';
      return;
    }

    var html = ['<ul class="post-list">'];
    hits.forEach(function (p) {
      html.push(
        '<li><a class="post-link" href="' + esc(p.u) + '">' +
          '<div class="post-row">' +
            '<span class="post-date">' + esc(p.d) + "</span>" +
            '<h2 class="post-list-title">' + esc(p.t) + "</h2>" +
          "</div>" +
          '<p class="post-excerpt">' + esc(p.x.slice(0, 200)) + (p.x.length > 200 ? "…" : "") + "</p>" +
        "</a>" +
        ((p.g && p.g.length)
          ? '<div class="chips">' + p.g.map(function (t) {
              return '<a class="chip" href="' + tagBase + esc(t) + '/">#' + esc(t) + "</a>";
            }).join("") + "</div>"
          : "") +
        "</li>"
      );
    });
    html.push("</ul>");
    results.innerHTML = html.join("");
  }

  function search(query) {
    var terms = query.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) { restore(); return; }

    loadIndex().then(function (data) {
      var hits = data.filter(function (p) {
        var hay = (p.t + " " + (p.g || []).join(" ") + " " + p.x).toLowerCase();
        return terms.every(function (t) { return hay.indexOf(t) !== -1; });
      });
      // title matches first, then by date descending (the index is already
      // date-ordered, so a stable partition is enough)
      var titled = [], rest = [];
      hits.forEach(function (p) {
        var t = p.t.toLowerCase();
        (terms.every(function (q) { return t.indexOf(q) !== -1; }) ? titled : rest).push(p);
      });
      render(titled.concat(rest), query);
    });
  }

  var timer = null;
  input.addEventListener("input", function () {
    clearTimeout(timer);
    var q = input.value.trim();
    timer = setTimeout(function () { search(q); }, 120);
  });

  // arriving from another page with ?q=
  var q0 = new URLSearchParams(location.search).get("q");
  if (q0) {
    input.value = q0;
    search(q0.trim());
  }
})();
