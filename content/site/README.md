# Website translations (qeuapps.com in 18 languages)

English and Arabic live together in the root pages (`/apps/vault/` shows either,
by the 🌐 menu). Every other language gets its own copy of each page under
`/<lang>/`, e.g. `/fr/apps/vault/`, `/ur/about/`.

| file | what it is | edit by hand? |
|---|---|---|
| `_source.json` | every English text on the site → the page it first appears on. Written by `extract`. | no |
| `<lang>.json` | the translations: `{"English text": "translation"}`, in the same order as `_source.json` | yes |
| `glossary.json` | names that never change, app names, tone rules for translators | yes |
| `README.md` | this file | yes |

The English and Arabic texts themselves stay in `tools/build.py` and the
`tools/*_page.py` files (the `data-en` / `data-ar` pairs). Per-app privacy
policies are separate: `content/privacy/<app>/<lang>.json`.

Languages: fr de es it pt nl ru tr ur hi bn id ms zh ja ko (+ en, ar).
A language gets pages only when its `<lang>.json` exists. Urdu is right-to-left.

## Commands (run from the repo root)

```bash
python3 tools/build.py                       # build everything (en/ar pages, then /<lang>/ pages)
python3 tools/site_i18n.py extract           # refresh _source.json after changing English texts
python3 tools/site_i18n.py status            # per language: done / missing / unused
python3 tools/site_i18n.py check [fr de …]   # tags kept, brand names kept, nothing left in English
python3 tools/site_i18n.py missing fr /tmp/fr_todo.json   # the English texts French still lacks
python3 tools/site_i18n.py merge fr /tmp/fr_done.json     # put new translations into fr.json
```

## Common jobs

- **Change an English text**: edit it in `tools/`, run `build.py`, `extract`, then `status`.
  The changed text shows as *missing* in every language; get it translated
  (`missing` → translate → `merge`), run `check`, then `build.py` again.
  Until then that sentence shows in English on the other-language pages.
- **Fix one translation**: edit the value in `<lang>.json`, run `check <lang>`, then `build.py`.
- **Add a language**: add its code to `LANGS`, `MENU_ORDER`, `NATIVE`, `OG_LOCALE`
  (and `RTL` if right-to-left) in `tools/site_i18n.py`; create `<lang>.json` with
  `missing` → translate → `merge`; `check`; `build.py`.
- **Remove a language from the site**: delete (or rename) its `<lang>.json`; `build.py` removes its folder.
- **New page**: build it in `tools/build.py` with `render()`; it is translated
  automatically once its texts are in `<lang>.json` (`extract` → `missing` → `merge`).

## How visitors reach a language

- The 🌐 menu in the header lists all 18; the choice is remembered in the browser.
- First visit with no choice yet: the browser's language decides
  (a French phone opening `/apps/vault/` is sent to `/fr/apps/vault/`).
- `?lang=en` or `?lang=ar` on a root page forces that language.
- Search engines see `hreflang` links between all versions and every
  language page is in `sitemap.xml`.

Code: `tools/site_i18n.py` (menu, hreflang, page copies, commands).
