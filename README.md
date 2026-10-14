# Telegram channel archive

`scripts/tg_scrape.py` saves a public Telegram channel's posts (text, photos,
videos) from its `t.me/s/<channel>` web preview into `archive/<channel>/`:

- `media/` — files named `<post id>_<n>.<ext>`
- `index.json` — every post's id, link, date, text and media paths

The **Archive Telegram channel** workflow runs the script on GitHub Actions and
commits the result. Run it again any time (Actions tab → Run workflow) to pick up
new posts; files already saved are skipped.

Locally: `python scripts/tg_scrape.py Meme_Template_bd`

Limitations: documents/files posted as attachments aren't exposed by the web
preview (they're listed under `documents_not_downloadable`), and files over 95 MB
are skipped because of GitHub's file size limit.

## Template catalog

Every file in `media/` has a descriptive name, and `catalog.json` has one entry per file:
`key` (`<post id>_<n>`), `file`, `link` to the Telegram post, `caption`, `title`, `who` (only when
the caption names someone), `what_happens`, `key_line` (short spoken line, dialogue clips only),
`audio`, `emotion`, `use_when` (meme scenarios it fits), `tags` and `note`.

To find a template, search `catalog.json` for a scenario, emotion or tag, or ask Claude with the
catalog. `transcripts.json` holds machine transcripts for dialogue clips (music and song clips
are left empty). `001906_0.mp4` is a corrupt file and is not catalogued.
