(function () {
  function curFile() {
    try { return decodeURIComponent(location.pathname.split("/").pop()); }
    catch (e) { return location.pathname.split("/").pop(); }
  }
  function go() {
    var data = window.__CQM_BACKLINKS, file = curFile();
    if (!data || !data[file]) return;
    var art = document.querySelector("article");
    if (!art) { setTimeout(go, 200); return; }
    if (art.querySelector(".cqm-backlinks")) return;
    var box = document.createElement("section");
    box.className = "cqm-backlinks md-typeset";
    var h = document.createElement("h2");
    h.textContent = "被引用（" + data[file].length + "）";
    box.appendChild(h);
    var ul = document.createElement("ul");
    data[file].forEach(function (it) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = "./" + it.file;
      a.textContent = it.title + (it.sid ? " [" + it.sid + "]" : "");
      li.appendChild(a);
      ul.appendChild(li);
    });
    box.appendChild(ul);
    art.appendChild(box);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", go);
  else go();
})();
