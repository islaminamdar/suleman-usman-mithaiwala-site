(() => {
  'use strict';

  // Footer year
  const yr = document.getElementById('yr');
  if (yr) yr.textContent = new Date().getFullYear();

  // Sticky nav shadow on scroll
  const nav = document.getElementById('nav');
  if (nav) {
    const onScroll = () => {
      if (window.scrollY > 8) nav.classList.add('is-scrolled');
      else nav.classList.remove('is-scrolled');
    };
    document.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // Mobile menu
  const burger = document.querySelector('.nav__burger');
  const mobile = document.getElementById('mobileMenu');
  if (burger && mobile) {
    const setOpen = (open) => {
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (open) {
        mobile.hidden = false;
        mobile.style.display = 'flex';
      } else {
        mobile.style.display = 'none';
        mobile.hidden = true;
      }
    };
    burger.addEventListener('click', () => {
      const open = burger.getAttribute('aria-expanded') === 'true';
      setOpen(!open);
    });
    mobile.addEventListener('click', (e) => {
      if (e.target.tagName === 'A') setOpen(false);
    });
    window.addEventListener('resize', () => {
      if (window.innerWidth > 980) setOpen(false);
    });
  }

  // Reveal on scroll
  const revealTargets = document.querySelectorAll('.section, .card, .loc, .order__card, .timeline li');
  revealTargets.forEach((el) => el.setAttribute('data-reveal', ''));
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-in');
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
    );
    revealTargets.forEach((el) => io.observe(el));
  } else {
    revealTargets.forEach((el) => el.classList.add('is-in'));
  }

  // Smooth-scroll with sticky-nav offset
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener('click', (e) => {
      const id = a.getAttribute('href');
      if (id.length > 1) {
        const target = document.querySelector(id);
        if (target) {
          e.preventDefault();
          const top = target.getBoundingClientRect().top + window.scrollY - 70;
          window.scrollTo({ top, behavior: 'smooth' });
          history.replaceState(null, '', id);
        }
      }
    });
  });
})();
