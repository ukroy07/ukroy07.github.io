# Portfolio

A single-page portfolio that reconfigures itself for whoever is reading it. A
recruiter picks a track at the top — **AI / GenAI Engineer** or **SDE-I /
SDE-II** — and the headline, the summary, the order of the seven TCS systems,
the order of the engineering decisions, the stack groupings and the résumé
download all re-frame to match. Same facts, different emphasis, exactly like
the two résumé PDFs.

Section 02 carries the human half: a short bio, a three-step timeline, and the
algorithm-practice record. Section 09 ends with the operational facts a
recruiter screens on — notice period, experience, location.

The page opens with a live replay of AgentHub rather than a screenshot of it:
four agents move through the LangGraph state machine, the thought stream fills
in, the Critic scores the draft and sends it back once. Two task presets show
the router taking two different paths.

## Files

| File | What it is |
|---|---|
| `index.template.html` | **The source.** Edit this one. |
| `build.py` | Builds the two outputs below from the template. |
| `index.html` | Generated — a complete standalone document. **This is what you deploy.** |
| `artifact.html` | Generated — the same page as a fragment, for publishing through Claude. |

`index.html` and `artifact.html` are build output. Never edit them by hand;
the next build overwrites them.

## Making a change

```bash
python build.py
```

Edit `index.template.html`, run that, redeploy. The build does two things that
matter:

- **Emits pure ASCII.** Some static hosts serve `.html` with no charset; the
  browser falls back to windows-1252 and every em-dash, arrow and accent comes
  out as mojibake. Markup gets numeric entities, JavaScript gets `\uXXXX`
  escapes.

## The résumés

Both résumé buttons link straight to Google Drive, so there is no file to
upload and nothing to keep in sync. Replacing a résumé means replacing the
file **in Drive**, keeping the same share link - the page then needs no change
at all.

If a link itself ever changes, the two URLs live in `index.template.html`,
once each on the `.btn-primary` anchors (hero and section 09). Both files must
stay shared as *Anyone with the link*, or recruiters hit a permission wall.

## Deploying

Upload `index.html`. That is the whole site - one file, no build step on the
host, no dependencies, no framework. The only external requests the page makes
are to Google Fonts, and to Google Drive when someone opens a résumé.

**GitHub Pages** is the shortest path to `ukroy07.github.io`:

```bash
git init && git add index.html && git commit -m "Portfolio"
```

Push that to a repo named `ukroy07.github.io`, then turn on Pages in the
repository settings. Before deploying elsewhere, update `SITE_URL` at the top
of `build.py` so the Open Graph tags point at the real domain — that is what
LinkedIn reads when the link is shared.

## Things you may want to change

- **Notice period is stated as 60 days** in the at-a-glance grid in section 09.
  Correct it there if that changes.
- **Both phone numbers are public** in the contact grid in section 09. A hosted
  page gets scraped, so expect some spam; remove either `tel:` entry to stop it.
- **Target roles** are stated in the hero eyebrow and in section 08, once per
  track. Change them in both places, or the two tracks will disagree.
- **No photo.** Deliberate — the design is built around instrumentation, not a
  headshot. A portrait would go beside the hero text if you want one.

## Design notes

- Palette is OpenTelemetry's own indigo and amber, over blue-biased neutrals —
  picked because distributed tracing is work that is actually on the page.
- Archivo (condensed to 88%) for display, Newsreader for prose, JetBrains Mono
  for anything telemetry-shaped.
- Light and dark are both designed, driven by tokens; the page follows the
  reader's system theme.
- There is a print stylesheet: the rail, the live demo and every button drop
  away, colours flatten to ink on white, all four decision cards expand, and
  link URLs are printed after their text. It prints as a clean leave-behind.
- Muted text sits at or above a 4.5:1 contrast ratio in both themes.
- Every animation is behind `prefers-reduced-motion`. With motion reduced, the
  agent run renders its finished state immediately instead of playing.
