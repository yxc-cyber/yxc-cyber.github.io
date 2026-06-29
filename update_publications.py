import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_BIB = ROOT / "cite.bib"
DEFAULT_CONTENT = ROOT / "content.json"

MONTHS = {
    "jan": 1,
    "january": 1,
    "feb": 2,
    "february": 2,
    "mar": 3,
    "march": 3,
    "apr": 4,
    "april": 4,
    "may": 5,
    "jun": 6,
    "june": 6,
    "jul": 7,
    "july": 7,
    "aug": 8,
    "august": 8,
    "sep": 9,
    "sept": 9,
    "september": 9,
    "oct": 10,
    "october": 10,
    "nov": 11,
    "november": 11,
    "dec": 12,
    "december": 12,
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def find_matching_brace(text: str, start: int) -> int:
    depth = 0
    in_quote = False
    escape = False

    for index in range(start, len(text)):
        char = text[index]
        if escape:
            escape = False
            continue
        if char == "\\":
            escape = True
            continue
        if char == '"':
            in_quote = not in_quote
        if in_quote:
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index

    raise ValueError("Unmatched brace in BibTeX input")


def parse_bibtex(text: str) -> list[dict[str, object]]:
    entries = []
    position = 0

    while True:
        match = re.search(r"@([A-Za-z]+)\s*[{(]", text[position:])
        if not match:
            break

        entry_type = match.group(1).lower()
        open_index = position + match.end() - 1
        close_index = find_matching_brace(text, open_index)
        body = text[open_index + 1 : close_index].strip()
        key, fields_text = split_key_and_fields(body)
        entries.append(
            {
                "type": entry_type,
                "key": key.strip(),
                "fields": parse_fields(fields_text),
            }
        )
        position = close_index + 1

    return entries


def split_key_and_fields(body: str) -> tuple[str, str]:
    depth = 0
    in_quote = False
    escape = False

    for index, char in enumerate(body):
        if escape:
            escape = False
            continue
        if char == "\\":
            escape = True
            continue
        if char == '"':
            in_quote = not in_quote
        if in_quote:
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
        elif char == "," and depth == 0:
            return body[:index], body[index + 1 :]

    return body, ""


def parse_fields(text: str) -> dict[str, str]:
    fields = {}
    index = 0

    while index < len(text):
        while index < len(text) and text[index] in " \t\r\n,":
            index += 1
        name_match = re.match(r"([A-Za-z][A-Za-z0-9_-]*)\s*=", text[index:])
        if not name_match:
            break

        name = name_match.group(1).lower()
        index += name_match.end()
        value, index = parse_value(text, index)
        fields[name] = clean_bibtex(value)

    return fields


def parse_value(text: str, index: int) -> tuple[str, int]:
    while index < len(text) and text[index].isspace():
        index += 1

    if index >= len(text):
        return "", index

    if text[index] == "{":
        close_index = find_matching_brace(text, index)
        return text[index + 1 : close_index], close_index + 1

    if text[index] == '"':
        index += 1
        start = index
        escape = False
        while index < len(text):
            char = text[index]
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                return text[start:index], index + 1
            index += 1
        return text[start:index], index

    start = index
    while index < len(text) and text[index] not in ",\r\n":
        index += 1
    return text[start:index].strip(), index


def clean_bibtex(value: str) -> str:
    replacements = {
        r"\"{u}": "ü",
        r"\"u": "ü",
        r"{\&}": "&",
        r"\&": "&",
        r"{\%}": "%",
        r"\%": "%",
        r"{---}": "-",
        r"---": "-",
        r"``": '"',
        r"''": '"',
        r"\'": "'",
        r"\textbf": "",
        r"\url": "",
    }
    cleaned = value.strip()
    for source, target in replacements.items():
        cleaned = cleaned.replace(source, target)
    cleaned = cleaned.replace("眉", "ü")
    cleaned = re.sub(r"\\[A-Za-z]+\s*", "", cleaned)
    cleaned = cleaned.replace("\\", "")
    cleaned = cleaned.replace("{", "").replace("}", "")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.strip()


def split_authors(author_text: str) -> list[str]:
    return [part.strip() for part in re.split(r"\s+and\s+", author_text) if part.strip()]


def format_author(author: str) -> str:
    author = clean_bibtex(author)
    if "," not in author:
        return author

    pieces = [piece.strip() for piece in author.split(",")]
    if len(pieces) >= 2:
        last = pieces[0]
        first = " ".join(piece for piece in pieces[1:] if piece)
        return f"{first} {last}".strip()
    return author


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z]", "", value.lower())


def name_aliases(content: dict[str, object], explicit_name: str | None) -> set[str]:
    site = content.get("site", {})
    profile_name = explicit_name or site.get("hero_name") or site.get("nav_name") or ""
    aliases = {normalize_name(str(profile_name))}

    parts = str(profile_name).split()
    if len(parts) >= 2:
        aliases.add(normalize_name(f"{parts[-1]}, {' '.join(parts[:-1])}"))
        aliases.add(normalize_name(f"{' '.join(parts[:-1])} {parts[-1]}"))

    return {alias for alias in aliases if alias}


def highlight_author(author: str, aliases: set[str]) -> str:
    formatted = format_author(author)
    if normalize_name(formatted) in aliases or normalize_name(author) in aliases:
        return f"**{formatted}**"
    return formatted


def author_line(author_text: str, aliases: set[str]) -> str:
    authors = [highlight_author(author, aliases) for author in split_authors(author_text)]
    if len(authors) <= 2:
        return " and ".join(authors)
    return ", ".join(authors[:-1]) + f", and {authors[-1]}"


def month_number(value: str) -> int:
    cleaned = clean_bibtex(value).strip().lower()
    return MONTHS.get(cleaned, 0)


def venue(fields: dict[str, str]) -> str:
    base = (
        fields.get("journal")
        or fields.get("booktitle")
        or fields.get("archiveprefix")
        or fields.get("publisher")
        or "Preprint"
    )
    year = fields.get("year", "")
    return f"{base}, {year}" if year else base


def links(fields: dict[str, str]) -> list[dict[str, str]]:
    result = []
    if fields.get("url"):
        result.append({"label": "Link", "url": fields["url"]})
    elif fields.get("doi"):
        result.append({"label": "DOI", "url": f"https://doi.org/{fields['doi']}"})

    arxiv_url = f"https://arxiv.org/abs/{fields['eprint']}" if fields.get("eprint") else ""
    existing_urls = {item["url"] for item in result}
    if arxiv_url and arxiv_url not in existing_urls:
        result.append({"label": "arXiv", "url": f"https://arxiv.org/abs/{fields['eprint']}"})

    return result


def entry_sort_key(entry: dict[str, object]) -> tuple[int, int, str]:
    fields = entry["fields"]
    assert isinstance(fields, dict)
    year_match = re.search(r"\d{4}", fields.get("year", ""))
    year = int(year_match.group(0)) if year_match else 0
    return (year, month_number(fields.get("month", "")), str(entry.get("key", "")))


def publication_from_entry(
    entry: dict[str, object],
    aliases: set[str],
) -> dict[str, object]:
    fields = entry["fields"]
    assert isinstance(fields, dict)
    title = fields.get("title", "Untitled")
    publication = {
        "title": title,
        "authors": author_line(fields.get("author", ""), aliases),
        "venue": venue(fields),
    }
    entry_links = links(fields)
    if entry_links:
        publication["links"] = entry_links
    return publication


def update_publications(
    bib_path: Path = DEFAULT_BIB,
    content_path: Path = DEFAULT_CONTENT,
    name: str | None = None,
) -> None:
    content = json.loads(read_text(content_path))
    aliases = name_aliases(content, name)
    entries = parse_bibtex(read_text(bib_path))
    entries.sort(key=entry_sort_key, reverse=True)
    content["publications"] = [publication_from_entry(entry, aliases) for entry in entries]
    content_path.write_text(json.dumps(content, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {content_path.name} with {len(entries)} publications from {bib_path.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Update content.json publications from cite.bib.")
    parser.add_argument("--bib", type=Path, default=DEFAULT_BIB, help="Path to the BibTeX file.")
    parser.add_argument("--content", type=Path, default=DEFAULT_CONTENT, help="Path to content.json.")
    parser.add_argument("--name", help="Name to highlight in the author list. Defaults to site.hero_name.")
    args = parser.parse_args()
    update_publications(args.bib, args.content, args.name)


if __name__ == "__main__":
    main()
