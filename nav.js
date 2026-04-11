(async function () {
  const mount = document.getElementById('nav-mount');
  if (!mount) return;

  try {
    const res = await fetch('/nav.html');
    if (!res.ok) throw new Error('nav fetch failed');
    mount.innerHTML = await res.text();
  } catch (e) {
    console.warn('Canopy nav: could not load nav.html', e);
    return;
  }

  const path = window.location.pathname;
  const isIndex = /\/(index\.html)?$/.test(path);

  // Logo - home nav on index, href on other pages
  const logo = document.getElementById('nav-logo');
  if (isIndex) {
    logo.style.cursor = 'pointer';
    logo.addEventListener('click', function () {
      if (typeof showView === 'function') showView('home');
    });
  } else {
    logo.style.cursor = 'pointer';
    logo.addEventListener('click', function () {
      window.location.href = 'index.html';
    });
  }

  // Hamburger toggle
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobile-menu');

  hamburger.addEventListener('click', function () {
    hamburger.classList.toggle('open');
    mobileMenu.classList.toggle('open');
  });

  // Close menu on outside click
  document.addEventListener('click', function (e) {
    if (!e.target.closest('#mobile-menu') && !e.target.closest('#hamburger')) {
      hamburger.classList.remove('open');
      mobileMenu.classList.remove('open');
    }
  });

  // On index, intercept section links and use mobileNav() instead of navigating
  if (isIndex) {
    document.querySelectorAll('.mobile-menu-item[data-section], .mobile-menu-sub[data-section]').forEach(function (item) {
      var section = item.dataset.section;
      var href = item.getAttribute('href');
      // Only intercept items that point to index (not cairn/keystones)
      if (!href || href === 'index.html') {
        item.addEventListener('click', function (e) {
          e.preventDefault();
          hamburger.classList.remove('open');
          mobileMenu.classList.remove('open');
          if (typeof mobileNav === 'function') mobileNav(section);
        });
      }
    });
  }

  // Render logo map now that the SVG element exists in the DOM
  if (typeof renderLogoMap === 'function') {
    renderLogoMap();
  }
})();
