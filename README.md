# Xiaocheng Yang Personal Website

This repository contains the source for my personal academic website, designed as a static GitHub Pages site with an Arknights: Endfield-inspired visual style.

The site is intentionally lightweight: no frontend framework, no package manager, and no build system beyond a few small Python scripts. The rendered page is `index.html`; most editable content lives in `content.json`.

## Features

- Static GitHub Pages deployment
- Responsive desktop and mobile layouts
- JSON-driven profile, news, publications, contacts, and projects
- Markdown support in editable text fields
- BibTeX-to-publication syncing from `cite.bib`
- Automatic author-name highlighting in publications
- Generated contour-map visual assets
- Smooth section navigation and background parallax

## Repository Layout

- `index.html`: generated static page served by GitHub Pages
- `styles.css`: visual system, layout, responsive behavior
- `main.js`: navigation state and background parallax
- `content.json`: editable website content
- `cite.bib`: BibTeX source for publications
- `update_site.py`: regenerates `index.html` from `content.json`
- `update_publications.py`: updates `content.json` publications from `cite.bib`
- `assets/`: images, icons, resume, generated visual assets, and asset-generation script
- `agent.md`: original design and implementation notes

## Editing Content

Most website text can be edited directly in `content.json`.

After editing, rebuild the generated page:

```powershell
python -B update_site.py
```

Supported Markdown in content fields includes:

- `**bold**`
- `*italic*`
- `` `inline code` ``
- `[links](https://example.com)`
- headings
- ordered and unordered lists

## Updating Publications

Add or edit publications in `cite.bib`, then run:

```powershell
python -B update_publications.py
python -B update_site.py
```

The publication updater:

- sorts publications newest first
- highlights my name automatically
- preserves existing `links` in `content.json` for matching papers
- generates links from BibTeX `url`, `doi`, or `eprint` when no existing links are present

By default, the name to highlight is read from `site.hero_name` in `content.json`. To override it:

```powershell
python -B update_publications.py --name "Xiaocheng Yang"
```

## Local Preview

Because the site is static, you can open `index.html` directly in a browser. For a local server preview:

```powershell
python -m http.server 8000
```

Then visit:

```text
http://localhost:8000
```

## Deploying

This repository is ready for GitHub Pages. Commit the generated `index.html` together with the source files, then enable GitHub Pages for the repository in GitHub settings.

If the site is hosted from the repository root, no additional build step is needed.
