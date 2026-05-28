# sairajatg.dev — personal site

Personal website for **Sai Rajat Goparaju** — incoming PhD student in Computer
Science at the University of Wisconsin–Madison (HAL Lab, Prof. Matt Sinclair).

Built as a custom Jekyll 4 site (al-folio-inspired structure) with a dark
indigo "silicon" aesthetic, halo-glow header logos, and a news feed for PhD
updates, preprints, and submissions.

---

## Local development

Prerequisites: Ruby 3.x + Bundler.

```bash
cd /Users/sgoparaju/Desktop/Website
bundle install
bundle exec jekyll serve --livereload
# open http://127.0.0.1:4000
```

## Deploying to GitHub Pages

The repo ships with a GitHub Actions workflow at
[`.github/workflows/jekyll.yml`](.github/workflows/jekyll.yml) that builds
Jekyll 4.x and publishes to GitHub Pages on every push to `main`.

### One-time setup

1. Create a **public** repo on GitHub. For a user site at
   `https://sairajat2303.github.io/`, name it exactly **`SaiRajat2303.github.io`**.
   (For a project site, any name works and the URL becomes
   `https://sairajat2303.github.io/<repo>/`.)
2. From this directory:
   ```bash
   git init
   git add .
   git commit -m "Initial scaffold"
   git branch -M main
   git remote add origin https://github.com/SaiRajat2303/SaiRajat2303.github.io.git
   git push -u origin main
   ```
3. In the repo on GitHub → **Settings → Pages → Build and deployment → Source:
   GitHub Actions**.
4. The next push will deploy. Watch progress in the **Actions** tab.

## Editing content

Everything you'll touch regularly lives in five files:

| What | File |
| --- | --- |
| Hero / bio copy | [`_includes/hero.html`](_includes/hero.html) |
| About summary + skill chips | [`_includes/about.html`](_includes/about.html) |
| The four experience cards | [`_data/experience.yml`](_data/experience.yml) |
| News items (one file per item) | [`_news/`](_news/) |
| Colors / type / spacing tokens | [`_sass/_variables.scss`](_sass/_variables.scss) |

### Add a news item

Create a new file in `_news/` named `YYYY-MM-DD-slug.md`:

```markdown
---
date: 2026-06-01
title: arXiv preprint — "<paper title>"
---

One short paragraph. Markdown links are fine: [arXiv](https://arxiv.org/abs/…).
```

Newest items float to the top automatically.

### Reorder / re-label experience stops

Edit [`_data/experience.yml`](_data/experience.yml). The list order drives both
the halo bar at the top and the section cards below. Set `featured: true` on
exactly one entry — that's the one with the brighter halo + orbiting ring.

### Swap placeholder logos for real ones

See [`assets/img/README.md`](assets/img/README.md).

## File map

```
/
├── _config.yml               # site metadata
├── Gemfile                   # Jekyll 4 + plugins
├── index.html                # composes the home page
├── _layouts/default.html     # base HTML + backdrop layers
├── _includes/                # header logos, hero, about, experience, news, footer
├── _sass/                    # variables, base, backdrops, logos, hero, sections, news
├── assets/
│   ├── css/main.scss         # SCSS entry
│   ├── js/main.js            # smooth-scroll, parallax halos, active-section
│   └── img/logos/            # placeholder SVGs — replace with real logos
├── _data/experience.yml      # four stops (UW, Tenstorrent, Google, BITS)
├── _news/                    # one file per news item
└── .github/workflows/        # GitHub Pages deploy
```

## Iteration ideas (next passes)

- Real official logos + crests.
- A `/publications/` page once arXiv preprints land.
- Optional CV PDF link.
- Custom domain (CNAME) + favicon set.
- View-transitions or scroll-linked die-shot SVG in the backdrop.
