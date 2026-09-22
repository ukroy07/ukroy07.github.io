r"""Build the portfolio from index.template.html.

Outputs:

  index.html      A complete, standalone HTML document. This is the one you
                  deploy - GitHub Pages, Netlify, Vercel, any static host.
                  It is the only file you need to upload.

  artifact.html   The same page as a fragment, with no doctype/head, for
                  publishing through Claude's Artifact tool (which supplies
                  its own document shell).

The resumes are not bundled: both buttons link straight to Google Drive, so
the page has no local file dependencies at all.

Both outputs are pure ASCII. Some hosts serve .html with no charset, the
browser falls back to windows-1252, and every dash, arrow and accent comes out
mangled. HTML gets numeric entities; JavaScript gets \uXXXX escapes, valid in
strings and comments alike.
"""
import pathlib
import re

HERE = pathlib.Path(__file__).parent

# Edit these two if you move the site to your own domain.
SITE_URL = "https://ukroy07.github.io/"
SITE_DESC = (
    "Senior GenAI Engineer at TCS, looking for AI / GenAI Engineer or "
    "SDE-I / SDE-II roles anywhere in India. Nearly three years of agentic "
    "workflows, multimodal retrieval and LLM evaluation - plus the backend "
    "systems underneath them."
)

FAVICON = (
    "data:image/svg+xml,"
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' rx='7' fill='%234A5AE0'/%3E"
    "%3Cg fill='none' stroke='white' stroke-width='2' stroke-linecap='round'%3E"
    "%3Cpath d='M9 11v7a7 7 0 0 0 14 0v-7'/%3E%3C/g%3E"
    "%3C/svg%3E"
)


def to_ascii(html):
    r"""Escape non-ASCII per parser: entities in markup, \uXXXX in script."""

    def entities(chunk):
        return "".join(c if ord(c) < 128 else "&#%d;" % ord(c) for c in chunk)

    def js_escapes(chunk):
        return "".join(c if ord(c) < 128 else "\\u%04x" % ord(c) for c in chunk)

    parts = re.split(r"(<script\b[^>]*>.*?</script>)", html, flags=re.S)
    out = "".join(
        js_escapes(p) if p.startswith("<script") else entities(p) for p in parts
    )
    assert out.isascii(), "output is still not ASCII"
    return out


def wrap_document(fragment):
    """Split the fragment's leading head tags out and build a real document."""
    marker = "&display=swap\">"
    cut = fragment.index(marker) + len(marker)
    head_bits, body = fragment[:cut], fragment[cut:]

    meta = "\n".join(
        [
            '<meta charset="utf-8">',
            '<meta name="description" content="%s">' % SITE_DESC,
            '<meta name="author" content="Ujjawal Kumar">',
            '<meta name="theme-color" content="#090B11">',
            '<link rel="icon" href="%s">' % FAVICON,
            '<meta property="og:type" content="profile">',
            '<meta property="og:title" content="Ujjawal Kumar">',
            '<meta property="og:description" content="%s">' % SITE_DESC,
            '<meta property="og:url" content="%s">' % SITE_URL,
            '<meta name="twitter:card" content="summary_large_image">',
        ]
    )
    return (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n"
        + meta
        + "\n"
        + head_bits.strip()
        + "\n</head>\n<body>"
        + body.rstrip()
        + "\n</body>\n</html>\n"
    )


def main():
    template = (HERE / "index.template.html").read_text(encoding="utf-8")
    fragment = to_ascii(template)

    for name, text in (
        ("artifact.html", fragment),
        ("index.html", wrap_document(fragment)),
    ):
        path = HERE / name
        path.write_text(text, encoding="ascii")
        print("wrote %-14s %6.0f KB" % (path.name, path.stat().st_size / 1024))


if __name__ == "__main__":
    main()
