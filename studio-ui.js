/* Small, progressive navigation additions for Portfolio 6 · Studio. */
(() => {
  'use strict';

  const root = document.documentElement;
  const arabic = () => root.lang === 'ar';
  const text = (en, ar) => arabic() ? ar : en;
  const mobileMenu = matchMedia('(max-width: 720px)');
  const smallGallery = matchMedia('(max-width: 900px)');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const bilingual = (en, ar) => {
    const fragment = document.createDocumentFragment();
    [['en', en], ['ar', ar]].forEach(([language, label]) => {
      const span = document.createElement('span');
      span.dataset.l = language;
      span.textContent = label;
      fragment.append(span);
    });
    return fragment;
  };
  const languageUpdates = [];

  // The existing navigation remains a normal list on larger screens.
  const nav = document.querySelector('nav');
  const navLinks = nav && nav.querySelector('ul');
  const languageButton = nav && nav.querySelector('.lang');
  if (nav && navLinks && languageButton) {
    navLinks.id = 'nav-links';
    const toggle = document.createElement('button');
    toggle.className = 'menu-toggle';
    toggle.type = 'button';
    toggle.setAttribute('aria-controls', navLinks.id);
    toggle.setAttribute('aria-expanded', 'false');
    const icon = document.createElement('span');
    icon.className = 'menu-toggle-icon';
    icon.setAttribute('aria-hidden', 'true');
    icon.textContent = '☰';
    toggle.append(icon, bilingual('Menu', 'القائمة'));
    languageButton.before(toggle);

    const isOpen = () => toggle.getAttribute('aria-expanded') === 'true';
    const setOpen = (open, restoreFocus = false) => {
      nav.classList.toggle('menu-open', open);
      if (open) nav.classList.remove('hide');
      toggle.setAttribute('aria-expanded', String(open));
      icon.textContent = open ? '×' : '☰';
      if (restoreFocus) toggle.focus({ preventScroll: true });
    };
    toggle.addEventListener('click', () => setOpen(!isOpen()));
    navLinks.addEventListener('click', event => {
      if (event.target.closest('a[href^="#"]')) setOpen(false);
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && isOpen()) {
        event.preventDefault();
        setOpen(false, true);
      }
    });
    document.addEventListener('pointerdown', event => {
      if (isOpen() && !nav.contains(event.target)) setOpen(false);
    });
    mobileMenu.addEventListener('change', event => {
      if (!event.matches) setOpen(false);
    });
    languageUpdates.push(() => {
      toggle.setAttribute('aria-label', text('Navigation menu', 'قائمة التنقل'));
      nav.setAttribute('aria-label', text('Main navigation', 'التنقل الرئيسي'));
    });
  }

  // Quick links use the same anchor handling as the rest of the page.
  const projects = [...document.querySelectorAll('.proj[id]')];
  const workWrap = document.querySelector('#work .wrap');
  if (workWrap && projects.length) {
    const index = document.createElement('div');
    index.id = 'project-index';
    index.className = 'project-index';
    index.setAttribute('role', 'navigation');
    const projectLinks = projects.map((project, position) => {
      const link = document.createElement('a');
      link.href = `#${project.id}`;
      const number = document.createElement('span');
      number.className = 'project-num';
      number.setAttribute('aria-hidden', 'true');
      number.textContent = String(position + 1).padStart(2, '0');
      link.append(number, bilingual(project.dataset.name || project.id,
        project.dataset.nameAr || project.dataset.name || project.id));
      index.append(link);
      return link;
    });
    workWrap.append(index);
    languageUpdates.push(() => {
      index.setAttribute('aria-label', text('Jump to a project', 'انتقل إلى مشروع'));
      projectLinks.forEach((link, position) => link.setAttribute('aria-label',
        text(`Project ${position + 1}: ${projects[position].dataset.name}`,
          `المشروع ${position + 1}: ${projects[position].dataset.nameAr || projects[position].dataset.name}`)));
    });
    if ('IntersectionObserver' in window) {
      const visible = new Set();
      const setActive = project => {
        projectLinks.forEach((link, position) => {
          const active = projects[position] === project;
          link.classList.toggle('is-active', active);
          if (active) link.setAttribute('aria-current', 'location');
          else link.removeAttribute('aria-current');
        });
      };
      const observer = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (entry.isIntersecting) visible.add(entry.target);
          else visible.delete(entry.target);
        });
        const nearest = [...visible].sort((a, b) =>
          Math.abs(a.getBoundingClientRect().top - innerHeight * .35) -
          Math.abs(b.getBoundingClientRect().top - innerHeight * .35))[0];
        setActive(nearest);
      }, { rootMargin: '-20% 0px -35% 0px', threshold: 0 });
      projects.forEach(project => observer.observe(project));
    }
  }

  // Touch and reduced-motion visitors get a conventional, keyboard-ready gallery.
  const track = document.getElementById('track');
  const galleryHead = document.querySelector('.hs-head');
  if (track && galleryHead) {
    const cards = [...track.querySelectorAll('.card')];
    const controls = document.createElement('div');
    controls.className = 'gallery-controls';
    const makeButton = (className, en, ar, arrow) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = className;
      button.setAttribute('aria-controls', track.id);
      const symbol = document.createElement('span');
      symbol.className = 'gallery-arrow';
      symbol.setAttribute('aria-hidden', 'true');
      symbol.textContent = arrow;
      button.append(symbol, bilingual(en, ar));
      return button;
    };
    const previous = makeButton('gallery-prev', 'Previous', 'السابق', '←');
    const next = makeButton('gallery-next', 'Next', 'التالي', '→');
    const position = document.createElement('span');
    position.className = 'gallery-position';
    position.setAttribute('aria-live', 'polite');
    position.setAttribute('aria-atomic', 'true');
    controls.append(previous, position, next);
    galleryHead.append(controls);
    track.setAttribute('role', 'region');

    const nativeGallery = () => smallGallery.matches || reducedMotion.matches;
    const maximum = () => Math.max(0, track.scrollWidth - track.clientWidth);
    const offset = () => Math.max(0, Math.min(maximum(), Math.abs(track.scrollLeft)));
    const behavior = () => reducedMotion.matches ? 'auto' : 'smooth';
    const pitch = () => {
      if (cards.length > 1) return Math.abs(cards[1].offsetLeft - cards[0].offsetLeft);
      return cards[0] ? cards[0].offsetWidth : track.clientWidth;
    };
    let framePending = false;
    const updatePosition = () => {
      framePending = false;
      const current = offset();
      const max = maximum();
      previous.disabled = current <= 2;
      next.disabled = current >= max - 2;
      const viewport = track.getBoundingClientRect();
      const shown = cards.map((card, index) => {
        const rectangle = card.getBoundingClientRect();
        return Math.min(rectangle.right, viewport.right) - Math.max(rectangle.left, viewport.left) >
          Math.min(40, rectangle.width * .15) ? index + 1 : 0;
      }).filter(Boolean);
      const first = shown[0] || 1;
      const last = shown[shown.length - 1] || first;
      const range = first === last ? String(first) : `${first}–${last}`;
      const label = `${range} / ${cards.length}`;
      if (position.textContent !== label) position.textContent = label;
      position.setAttribute('aria-label', text(`Projects ${range} of ${cards.length}`,
        `المشاريع ${range} من ${cards.length}`));
    };
    const schedulePosition = () => {
      if (!framePending) {
        framePending = true;
        requestAnimationFrame(updatePosition);
      }
    };
    const move = direction => {
      if (!nativeGallery()) return;
      track.scrollBy({ left: pitch() * direction * (arabic() ? -1 : 1), behavior: behavior() });
    };
    previous.addEventListener('click', () => move(-1));
    next.addEventListener('click', () => move(1));
    track.addEventListener('scroll', schedulePosition, { passive: true });
    track.addEventListener('keydown', event => {
      if (!nativeGallery() || event.target !== track) return;
      if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
        event.preventDefault();
        move((event.key === 'ArrowRight' ? 1 : -1) * (arabic() ? -1 : 1));
      } else if (event.key === 'Home' || event.key === 'End') {
        event.preventDefault();
        track.scrollTo({ left: event.key === 'Home' ? 0 : maximum() * (arabic() ? -1 : 1),
          behavior: behavior() });
      }
    });
    const setGalleryMode = () => {
      controls.hidden = !nativeGallery();
      if (nativeGallery()) track.tabIndex = 0;
      else track.removeAttribute('tabindex');
      schedulePosition();
    };
    smallGallery.addEventListener('change', setGalleryMode);
    reducedMotion.addEventListener('change', setGalleryMode);
    window.addEventListener('resize', schedulePosition, { passive: true });
    languageUpdates.push(() => {
      track.setAttribute('aria-label', text('More projects. Use the arrow keys to browse.',
        'مشاريع أخرى. استخدم مفاتيح الأسهم للتصفح.'));
      previous.setAttribute('aria-label', text('Previous projects', 'المشاريع السابقة'));
      next.setAttribute('aria-label', text('Next projects', 'المشاريع التالية'));
      previous.querySelector('.gallery-arrow').textContent = arabic() ? '→' : '←';
      next.querySelector('.gallery-arrow').textContent = arabic() ? '←' : '→';
      if (nativeGallery()) track.scrollTo({ left: 0, behavior: 'instant' });
      schedulePosition();
    });
    setGalleryMode();
  }

  const updateLanguage = () => languageUpdates.forEach(update => update());
  document.addEventListener('langchange', updateLanguage);
  updateLanguage();
})();
