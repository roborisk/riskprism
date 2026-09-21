// Copy-to-clipboard for the BibTeX block.
document.querySelectorAll('.copybtn').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var target = document.getElementById(btn.dataset.target);
    if (!target) return;

    navigator.clipboard.writeText(target.innerText.trim()).then(function () {
      var original = btn.textContent;
      btn.textContent = 'Copied';
      btn.classList.add('done');
      setTimeout(function () {
        btn.textContent = original;
        btn.classList.remove('done');
      }, 1600);
    });
  });
});

// Videos autoplay muted only while on screen, so a page full of clips stays light.
var lazyVideos = document.querySelectorAll('video[data-autoplay]');
if (lazyVideos.length && 'IntersectionObserver' in window) {
  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) entry.target.play().catch(function () {});
      else entry.target.pause();
    });
  }, { threshold: 0.25 });

  lazyVideos.forEach(function (v) { observer.observe(v); });
}

// Section rail. Built from the sections themselves rather than a hand-kept
// list, so adding a <section id> to index.md is enough to put it on the rail.
(function () {
  var nav = document.getElementById('railnav');
  if (!nav) return;

  var sections = Array.prototype.slice.call(document.querySelectorAll('main section[id]'));
  if (sections.length < 2) return;

  var list = document.createElement('ol');
  var links = sections.map(function (section) {
    var kicker = section.querySelector('.section-kicker');
    var heading = section.querySelector('h2');
    var label = section.dataset.nav
      || (kicker && kicker.textContent.trim())
      || (heading && heading.textContent.trim())
      || section.id;

    var link = document.createElement('a');
    link.href = '#' + section.id;
    // The label is hidden below 1380px, so the name has to survive without it.
    link.title = label;
    link.setAttribute('aria-label', label);
    link.innerHTML = '<span class="dot"></span>';

    var text = document.createElement('span');
    text.className = 'lbl';
    text.textContent = label;
    link.appendChild(text);

    var item = document.createElement('li');
    item.appendChild(link);
    list.appendChild(item);
    return link;
  });
  nav.appendChild(list);

  // A section counts as current once its top passes a third of the way up the
  // viewport, which matches where the eye sits while reading.
  var active = -1;
  function update() {
    var mark = window.innerHeight * 0.34;
    var index = 0;
    for (var i = 0; i < sections.length; i++) {
      if (sections[i].getBoundingClientRect().top <= mark) index = i;
    }
    // A short trailing section never reaches the mark, so pin it at the bottom.
    if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) {
      index = sections.length - 1;
    }

    if (index === active) return;
    active = index;
    links.forEach(function (link, i) {
      link.classList.toggle('on', i === index);
      if (i === index) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });
    nav.style.setProperty('--p', index / (sections.length - 1));
  }

  var queued = false;
  function onScroll() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(function () {
      queued = false;
      update();
    });
  }

  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', onScroll);
  update();
})();
