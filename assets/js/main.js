// Light interactions only — keep the site snappy.

// 1) Smooth-scroll for in-page anchor links (with sticky-header offset)
document.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener('click', (e) => {
    const id = link.getAttribute('href').slice(1);
    if (!id) return;
    const target = document.getElementById(id);
    if (!target) return;
    e.preventDefault();
    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    history.replaceState(null, '', `#${id}`);
  });
});

// 2) Subtle parallax on halo logos based on cursor position
const halos = document.querySelectorAll('.halo');
if (halos.length && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
  const bar = document.querySelector('.halo-bar');
  bar?.addEventListener('mousemove', (e) => {
    const rect = bar.getBoundingClientRect();
    const cx = (e.clientX - rect.left) / rect.width - 0.5;
    const cy = (e.clientY - rect.top) / rect.height - 0.5;
    halos.forEach((h, i) => {
      const depth = h.classList.contains('halo--featured') ? 12 : 6;
      h.style.transform = `translate(${cx * depth}px, ${cy * depth - 1}px)`;
    });
  });
  bar?.addEventListener('mouseleave', () => {
    halos.forEach((h) => (h.style.transform = ''));
  });
}

// 3) Highlight nav halo of the section currently in view
const sections = document.querySelectorAll('.stop[id]');
const haloLinks = new Map();
document.querySelectorAll('.halo[href^="#"]').forEach((a) => {
  haloLinks.set(a.getAttribute('href').slice(1), a);
});
if (sections.length && 'IntersectionObserver' in window) {
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const link = haloLinks.get(entry.target.id);
        if (!link) return;
        if (entry.isIntersecting) link.classList.add('halo--active');
        else link.classList.remove('halo--active');
      });
    },
    { rootMargin: '-40% 0px -50% 0px' }
  );
  sections.forEach((s) => io.observe(s));
}
