(function () {
  'use strict';

  // Sticky nav shadow
  const nav = document.getElementById('nav');
  const onScroll = () => {
    if (window.scrollY > 12) nav.classList.add('is-scrolled');
    else nav.classList.remove('is-scrolled');
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu
  const toggle = document.querySelector('.nav__toggle');
  const links = document.getElementById('navLinks');
  toggle.addEventListener('click', () => {
    const isOpen = links.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
  });
  links.querySelectorAll('a').forEach(a =>
    a.addEventListener('click', () => {
      links.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    })
  );

  // Menu filter chips
  const chips = document.querySelectorAll('.chip');
  const dishes = document.querySelectorAll('.dish');
  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      const filter = chip.dataset.filter;
      chips.forEach(c => c.classList.toggle('is-active', c === chip));
      dishes.forEach(d => {
        const show = filter === 'all' || d.dataset.cat === filter;
        d.classList.toggle('is-hidden', !show);
      });
    });
  });

  // Partner form — open WhatsApp with composed message
  const partnerForm = document.getElementById('partnerForm');
  if (partnerForm) {
    partnerForm.addEventListener('submit', e => {
      e.preventDefault();
      const data = new FormData(partnerForm);
      const lines = [
        '*New Partnership Enquiry*',
        '',
        `Name: ${data.get('name') || '-'}`,
        `Phone: ${data.get('phone') || '-'}`,
        `Email: ${data.get('email') || '-'}`,
        `City: ${data.get('city') || '-'}`,
        `Budget: ${data.get('budget') || '-'}`,
        `Intent: ${data.get('intent') || '-'}`,
        `Note: ${data.get('note') || '-'}`,
      ];
      const msg = encodeURIComponent(lines.join('\n'));
      window.open(`https://wa.me/971557133786?text=${msg}`, '_blank', 'noopener');
      const sent = partnerForm.querySelector('.partner__sent');
      if (sent) sent.hidden = false;
      partnerForm.reset();
    });
  }

  // Reveal on scroll
  const revealEls = document.querySelectorAll(
    '.section__head, .legacy__media, .legacy__copy, .timeline__item, .presence__card, .dish, .order__card, .why__item, .lead__card, .tech__copy, .tech__pill, .loc, .vision__card, .partner__copy, .partner__form, .contact__card'
  );
  revealEls.forEach(el => el.classList.add('reveal'));

  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -40px 0px' }
    );
    revealEls.forEach(el => io.observe(el));
  } else {
    revealEls.forEach(el => el.classList.add('is-visible'));
  }

  // Footer year
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
