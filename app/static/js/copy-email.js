/* Email contact popup: click the footer envelope -> a small dialog shows the address
 * with a one-click Copy button (so visitors can copy it, not just trigger mailto). */
(function () {
  "use strict";

  function init() {
    var trigger = document.getElementById("email-trigger");
    var popup = document.getElementById("email-popup");
    if (!trigger || !popup) return;

    var addr = document.getElementById("email-addr");
    var copyBtn = document.getElementById("email-copy");
    var closeBtn = popup.querySelector(".email-popup-close");

    function open(e) {
      if (e) e.preventDefault();
      popup.classList.add("is-open");
    }
    function close() {
      popup.classList.remove("is-open");
      if (copyBtn) copyBtn.textContent = "Copy";
    }

    trigger.addEventListener("click", open);
    if (closeBtn) closeBtn.addEventListener("click", close);
    popup.addEventListener("click", function (e) {
      if (e.target === popup) close(); // click on the backdrop
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") close();
    });

    if (copyBtn) {
      copyBtn.addEventListener("click", function () {
        var text = addr ? addr.textContent.trim() : "";
        function done() {
          copyBtn.textContent = "Copied!";
          setTimeout(function () { copyBtn.textContent = "Copy"; }, 1500);
        }
        function selectFallback() {
          // Select the address so the visitor can copy it manually (Ctrl+C).
          try {
            var range = document.createRange();
            range.selectNodeContents(addr);
            var sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
            document.execCommand("copy");
            done();
          } catch (_) {
            copyBtn.textContent = "Press Ctrl+C";
          }
        }
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(text).then(done).catch(selectFallback);
        } else {
          selectFallback();
        }
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
