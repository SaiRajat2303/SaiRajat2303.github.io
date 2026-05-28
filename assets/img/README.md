# Image assets

## `logos/`

The four files here (`uw.svg`, `tenstorrent.svg`, `google.svg`, `bits.svg`) are
**placeholder monograms** — generated wordmarks in roughly the right brand
colors so the site renders out of the box. Swap them for the real, officially
distributed logos before you publish.

Suggested sources:

- **UW–Madison** — `https://brand.wisc.edu/` (download an SVG; UW crest or
  wordmark works).
- **Tenstorrent** — request from Tenstorrent press kit or strip the SVG from
  `tenstorrent.com` (footer logo).
- **Google** — Google's brand guidelines do not allow third-party use of the
  Google word/logo to imply endorsement. Safest path: a small "Google ·
  Silicon Engineering" text mark (the current placeholder is essentially
  that), or no logo at all and just the org name.
- **BITS Pilani** — `https://www.bits-pilani.ac.in/` (the official institute
  emblem).

### How to swap

1. Drop the new file in this directory (keep the same filename, or update the
   `logo:` path in [`/_data/experience.yml`](../../_data/experience.yml)).
2. Aim for square-ish SVGs that look fine at 56–76 px.
3. If a logo is mostly dark, the `.halo__logo` background already provides a
   light card behind it — but you can also bake a white pad into the SVG.

## `backdrops/`

Reserved for any future high-res die-shot / datacenter photography you want to
layer in. The current backdrop is generated entirely in CSS
([`_sass/_backdrops.scss`](../../_sass/_backdrops.scss)) so the site stays
fast.
