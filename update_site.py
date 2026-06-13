import html
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CONTENT_PATH = ROOT / "content.json"
INDEX_PATH = ROOT / "index.html"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def safe_url(value: object) -> str:
    url = str(value).strip()
    scheme_match = re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", url)
    allowed = (
        url.startswith("#")
        or url.startswith("/")
        or url.startswith("./")
        or url.startswith("../")
        or url.startswith("http://")
        or url.startswith("https://")
        or url.startswith("mailto:")
        or scheme_match is None
    )
    return esc(url if allowed else "#")


def inline_md(value: object) -> str:
    text = str(value)
    parts = text.split("`")
    rendered = []

    for index, part in enumerate(parts):
        if index % 2:
            rendered.append(f"<code>{esc(part)}</code>")
            continue

        segment = esc(part)
        segment = re.sub(
            r"\[([^\]]+)\]\(([^)\s]+)\)",
            lambda match: f'<a href="{safe_url(html.unescape(match.group(2)))}">{match.group(1)}</a>',
            segment,
        )
        segment = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", segment)
        segment = re.sub(r"__(.+?)__", r"<strong>\1</strong>", segment)
        segment = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", segment)
        segment = re.sub(r"(?<!_)_(?!_)(.+?)(?<!_)_(?!_)", r"<em>\1</em>", segment)
        rendered.append(segment.replace("\n", "<br>"))

    return "".join(rendered)


def markdown_blocks(value: object, indent: str = "          ") -> str:
    blocks = []
    paragraphs = re.split(r"\n\s*\n", str(value).strip())

    for paragraph in paragraphs:
        lines = [line.rstrip() for line in paragraph.splitlines() if line.strip()]
        if not lines:
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", lines[0])
        if heading and len(lines) == 1:
            level = min(len(heading.group(1)) + 2, 6)
            blocks.append(f"{indent}<h{level}>{inline_md(heading.group(2))}</h{level}>")
            continue

        if all(re.match(r"^\s*[-*]\s+", line) for line in lines):
            item_lines = []
            for line in lines:
                text = re.sub(r"^\s*[-*]\s+", "", line)
                item_lines.append(f"{indent}  <li>{inline_md(text)}</li>")
            items = "\n".join(item_lines)
            blocks.append(f"{indent}<ul>\n{items}\n{indent}</ul>")
            continue

        if all(re.match(r"^\s*\d+[.)]\s+", line) for line in lines):
            item_lines = []
            for line in lines:
                text = re.sub(r"^\s*\d+[.)]\s+", "", line)
                item_lines.append(f"{indent}  <li>{inline_md(text)}</li>")
            items = "\n".join(item_lines)
            blocks.append(f"{indent}<ol>\n{items}\n{indent}</ol>")
            continue

        text = "\n".join(lines)
        blocks.append(f"{indent}<p>{inline_md(text)}</p>")

    return "\n".join(blocks)


def list_items(items: list[str]) -> str:
    return "\n".join(f"              <li>{inline_md(item)}</li>" for item in items)


def paragraphs(items: list[str]) -> str:
    return "\n".join(markdown_blocks(item) for item in items)


def link_group(links: list[dict[str, str]]) -> str:
    if not links:
        return ""
    rendered = "\n".join(
        f'              <a href="{esc(link.get("url", "#"))}">{esc(link.get("label", "Link"))}</a>'
        for link in links
    )
    return f'            <div class="links">\n{rendered}\n            </div>'


def contact_buttons(items: list[dict[str, str]]) -> str:
    if not items:
        return ""
    rendered = "\n".join(
        f'                <a class="contact-button" href="{safe_url(item.get("url", "#"))}">{esc(item.get("label", "contact"))}</a>'
        for item in items
    )
    return f'''              <div class="hero-contacts" aria-label="Contact links">
{rendered}
              </div>'''


def researcher_stars(count: object) -> str:
    try:
        total = max(0, int(count))
    except (TypeError, ValueError):
        total = 0

    if total == 0:
        return ""

    stars = "\n".join(
        '                <img src="assets/researcher-star.svg" alt="">'
        for _ in range(total)
    )
    return f'''              <span class="hero-stars">
{stars}
              </span>'''


def news_items(items: list[dict[str, str]]) -> str:
    return "\n".join(
        f'''          <article class="news-item">
            <span class="news-date">{esc(item.get("date", ""))}</span>
            <span>{inline_md(item.get("text", ""))}</span>
          </article>'''
        for item in items
    )


def publication_items(items: list[dict[str, object]]) -> str:
    blocks = []
    for item in items:
        blocks.append(
            f'''          <article class="publication">
            <h3>{inline_md(item.get("title", ""))}</h3>
            <p class="authors">{inline_md(item.get("authors", ""))}</p>
            <p class="venue">{inline_md(item.get("venue", ""))}</p>
{link_group(item.get("links", []))}
          </article>'''
        )
    return "\n".join(blocks)


def project_items(items: list[dict[str, str]]) -> str:
    blocks = []
    for item in items:
        links = [{"label": "Repository", "url": item.get("url", "#")}]
        blocks.append(
            f'''          <article class="project">
            <h3>{inline_md(item.get("name", ""))}</h3>
            <p>{inline_md(item.get("description", ""))}</p>
{link_group(links)}
          </article>'''
        )
    return "\n".join(blocks)


def misc_items(items: list[dict[str, object]]) -> str:
    blocks = []
    for item in items:
        images = item.get("images", [])
        rendered_images = ""
        if images:
            image_blocks = []
            for image in images:
                caption = str(image.get("caption", "")).strip()
                caption_html = f"\n              <figcaption>{inline_md(caption)}</figcaption>" if caption else ""
                image_blocks.append(
                    f'''            <figure class="misc-photo">
              <div class="misc-photo-frame">
                <img src="{safe_url(image.get("src", "#"))}" alt="{esc(image.get("alt", ""))}">
              </div>{caption_html}
            </figure>'''
                )
            rendered_images = f'''          <div class="misc-gallery">
{chr(10).join(image_blocks)}
          </div>'''

        blocks.append(
            f'''          <article class="misc-card">
            <h3>{inline_md(item.get("title", ""))}</h3>
            <div class="misc-copy">
{markdown_blocks(item.get("text", ""), "              ")}
            </div>
{rendered_images}
          </article>'''
        )
    return "\n".join(blocks)


def section(section_id: str, title: str, body: str) -> str:
    return f'''      <section class="section-panel" id="{section_id}">
        <div class="section-title">
          <span class="title-dot" aria-hidden="true"></span>
          <h2>{esc(title)}</h2>
          <span class="title-bar" aria-hidden="true"></span>
        </div>
{body}
      </section>'''


def render(data: dict[str, object]) -> str:
    site = data["site"]
    profile = data["profile"]
    year = date.today().year

    intro = section(
        "intro",
        "Intro",
        f'''        <div class="intro-copy">
{paragraphs(data.get("intro", []))}
        </div>''',
    )
    news = section(
        "news",
        "News",
        f'''        <div class="timeline">
{news_items(data.get("news", []))}
        </div>''',
    )
    publications = section(
        "publications",
        "Selected Publication",
        f'''        <div class="item-list">
{publication_items(data.get("publications", []))}
        </div>''',
    )
    projects = section(
        "projects",
        "Opensource Project",
        f'''        <div class="item-list">
{project_items(data.get("projects", []))}
        </div>''',
    )
    misc = section(
        "misc",
        "Misc",
        f'''        <div class="misc-list">
{misc_items(data.get("misc", []))}
        </div>''',
    )

    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{esc(site.get("page_title", "Personal Webpage"))}</title>
    <link rel="icon" type="image/svg+xml" href="assets/nlp-researcher.svg">
    <link rel="stylesheet" href="styles.css">
  </head>
  <body>
    <div class="page-background" aria-hidden="true"></div>
    <header class="site-dock">
      <div class="dock-inner">
        <div class="brand">{esc(site.get("nav_name", ""))}</div>
        <nav class="dock-nav" aria-label="Primary navigation">
          <a href="#intro">Intro</a>
          <a href="#news">News</a>
          <a href="#publications">Selected Publication</a>
          <a href="#projects">Opensource Project</a>
          <a href="#misc">Misc</a>
        </nav>
      </div>
    </header>

    <main>
      <section class="hero" aria-label="Profile">
        <div class="hero-bar">
          <div class="portrait-shell">
            <img src="{esc(profile.get("portrait", "assets/portrait-placeholder.svg"))}" alt="Portrait placeholder">
          </div>
          <div class="hero-copy">
            <div class="name-clip" data-name="{esc(site.get("hero_name", ""))}">
              <h1 class="hero-name">{esc(site.get("hero_name", ""))}</h1>
              <span class="solid-name" aria-hidden="true">{esc(site.get("hero_name", ""))}</span>
            </div>
            <div class="hero-icons" aria-hidden="true">
              <img src="assets/researcher.svg" alt="">
              <img src="assets/nlp-researcher-gray.svg" alt="">
{researcher_stars(profile.get("researcher_star_count", 0))}
            </div>
{contact_buttons(data.get("contacts", []))}
            <div class="hero-meta">
              <div>
                <span class="meta-label">Research Interests</span>
                <ul>
{list_items(profile.get("interests", []))}
                </ul>
              </div>
              <div>
                <span class="meta-label">Education</span>
                <ul>
{list_items(profile.get("education", []))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div class="content">
{intro}
{news}
{publications}
{projects}
{misc}
      </div>
    </main>

    <footer class="site-footer">
      <span>&copy; 2026 Xiaocheng Yang. Style inspired by the Arknights: Endfield.</span>
    </footer>
    <script src="main.js"></script>
  </body>
</html>
'''


def main() -> None:
    data = json.loads(CONTENT_PATH.read_text(encoding="utf-8"))
    INDEX_PATH.write_text(render(data), encoding="utf-8")
    print(f"Updated {INDEX_PATH.name} from {CONTENT_PATH.name}")


if __name__ == "__main__":
    main()
