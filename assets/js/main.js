// Light interactions only — keep the site snappy.

// ── Helpers ───────────────────────────────────────────────────────────────
const tabs   = document.querySelectorAll('.journey-tab');
const stops  = document.querySelectorAll('.stop[id]');
const halos  = document.querySelectorAll('.halo[href^="#"]');
const navLinks = document.querySelectorAll('.site-nav__links a[href^="#"]');

const stopIds = new Set(Array.from(tabs).map((t) => t.dataset.stopId));

// Activate a stop in the Journey section (tab + panel + matching halo).
function activateStop(id) {
  if (!stopIds.has(id)) return false;
  tabs.forEach((t) => {
    const on = t.dataset.stopId === id;
    t.classList.toggle('journey-tab--active', on);
    t.setAttribute('aria-selected', String(on));
  });
  stops.forEach((s) => {
    const on = s.id === id;
    s.classList.toggle('stop--active', on);
  });
  halos.forEach((h) => {
    const on = h.getAttribute('href').slice(1) === id;
    h.classList.toggle('halo--active', on);
  });
  return true;
}

// Smooth-scroll to an element id (no-op if missing).
function smoothScrollTo(id) {
  const target = document.getElementById(id);
  if (!target) return;
  target.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── 1) Anchor link handling ───────────────────────────────────────────────
// If the href targets a Journey stop (e.g. #tenstorrent), activate that tab
// and scroll to the Journey section rather than the (hidden) panel.
// Otherwise, smooth-scroll to the target normally.
document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener('click', (e) => {
    const id = link.getAttribute('href').slice(1);
    if (!id) return;

    if (stopIds.has(id)) {
      e.preventDefault();
      activateStop(id);
      smoothScrollTo('journey');
      history.replaceState(null, '', `#${id}`);
      return;
    }

    if (document.getElementById(id)) {
      e.preventDefault();
      smoothScrollTo(id);
      history.replaceState(null, '', `#${id}`);
    }
  });
});

// ── 2) Journey tab clicks ─────────────────────────────────────────────────
tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    const id = tab.dataset.stopId;
    activateStop(id);
    history.replaceState(null, '', `#${id}`);
  });
});

// ── 3) Halo parallax inside the About affiliations band ───────────────────
const haloBar = document.querySelector('.halo-bar');
if (haloBar && halos.length && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  haloBar.addEventListener('mousemove', (e) => {
    const rect = haloBar.getBoundingClientRect();
    const cx = (e.clientX - rect.left) / rect.width - 0.5;
    const cy = (e.clientY - rect.top) / rect.height - 0.5;
    halos.forEach((h) => {
      const depth = h.classList.contains('halo--featured') ? 12 : 6;
      h.style.transform = `translate(${cx * depth}px, ${cy * depth - 1}px)`;
    });
  });
  haloBar.addEventListener('mouseleave', () => {
    halos.forEach((h) => (h.style.transform = ''));
  });
}

// ── 4) Initial hash + hashchange → activate matching tab ──────────────────
function applyHash() {
  const id = location.hash.slice(1);
  if (id && stopIds.has(id)) activateStop(id);
}
window.addEventListener('hashchange', applyHash);
applyHash();

// ── 5) Top nav active-section highlight (scroll-driven) ───────────────────
if (navLinks.length && 'IntersectionObserver' in window) {
  const navTargets = new Map();
  navLinks.forEach((a) => {
    const id = a.getAttribute('href').slice(1);
    const el = document.getElementById(id);
    if (el) navTargets.set(id, a);
  });
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const a = navTargets.get(entry.target.id);
        if (!a) return;
        a.classList.toggle('site-nav__link--active', entry.isIntersecting);
      });
    },
    { rootMargin: '-40% 0px -55% 0px' }
  );
  navTargets.forEach((_a, id) => {
    const el = document.getElementById(id);
    if (el) io.observe(el);
  });
}
