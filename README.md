# RiskPrism — project page

Jekyll site for GitHub Pages. The page content lives in a single markdown file.

## Local preview

```sh
bundle install
bundle exec jekyll serve --config _config.yml,_config.dev.yml
# http://127.0.0.1:4000/
```

Two things matter here. Use `bundle exec` — a bare `jekyll serve` picks up
whichever Jekyll is first on your `PATH` and can conflict with the versions
pinned in the `Gemfile`. And pass both configs: `_config.dev.yml` blanks out
`baseurl` so the page is served at `/`. Without it the site lives at
`/riskprism/` and `/` returns 404.

## Publishing

`baseurl` in `_config.yml` must match the path the site is published under.
It is set to `/riskprism` for `https://roborisk.github.io/riskprism/`. If you
move to a user/org site or a custom domain, change it to `""` — otherwise
every stylesheet and image 404s and the page renders unstyled.

Either Pages source works:

- **GitHub Actions** (recommended) — set Settings → Pages → Source to
  *GitHub Actions*. `.github/workflows/pages.yml` builds on each push to `main`
  using the `Gemfile`, so the deployed site matches local preview.
- **Deploy from a branch** — GitHub builds it with its own Jekyll 3.10 and
  ignores the `Gemfile` and the workflow. Works for this site, since it uses no
  plugins, but you lose version parity.

## What to edit

| File | Contains |
| --- | --- |
| `_config.yml` | Title, venue, and the header button links. Set a link to `""` to hide its button. |
| `_layouts/default.html` | Author list and affiliations. |
| `index.md` | All page content. |
| `assets/css/style.css` | Colours and typography, all via the variables in `:root`. |
| `assets/videos/` | The four video slots — see the README in that folder. |

## Still to fill in

- Author names and affiliations in `_layouts/default.html`.
- Paper, arXiv, and dataset links in `_config.yml`.
- The `TBD` cells in Table 1 in `index.md`.

## Figures

`assets/images/` holds web-sized renders and `assets/pdf/` the vector originals,
generated from the LaTeX figure sources. Each figure on the page links to its
PDF. To regenerate after changing a figure:

```sh
python -m pip install pymupdf pillow numpy
python tools/build_figures.py /path/to/figure/pdf/directory
```

## Logo and favicons

The header logo and the browser-tab icons are all derived from
`assets/images/riskprism-logo.jpg`. Replace that file and rerun:

```sh
python tools/build_logo.py
```

## Colours

The accent is `#ff6937`, applied to the title, section rules, links, headline
numbers, and the copy button. Change `--accent`, `--accent-soft`,
`--accent-tint`, and `--accent-wash` in `assets/css/style.css` to restyle the
whole page.
