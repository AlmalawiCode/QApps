"""site_screenshots.py — the app screenshots on the website, in every language.

The app pages show plain phone screens (620×1341 WebP) in
assets/img/apps/<app>/<screen>_<lang>.webp. English and Arabic were made by
hand earlier; this script makes the other 16 languages from the store
screenshots in the app folders (the iPhone 6.5" set, 1284×2778, with the
status bar already added). tools/site_i18n.py then shows <screen>_<lang>.webp
on the /<lang>/ pages whenever that file exists (English otherwise).

    python3 tools/site_screenshots.py            # make the missing ones
    python3 tools/site_screenshots.py --force    # remake all
    python3 tools/site_screenshots.py vault fr   # one app / language

After the apps' store screenshots change, run it with --force and rebuild.
"""
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser("~/MobileApps")
SIZE = (620, 1341)
LANGS = ["fr", "de", "es", "it", "pt", "nl", "ru", "tr", "ur", "hi", "bn", "id", "ms", "zh", "ja", "ko"]

# Vault: the owner's own iPhone captures (camera names) for the first store
# languages, matched to the screens by comparing with the English/Arabic set
# (9 Nov 2026); the later languages were rendered by the app's screenshot test.
_VAULT_DIR = f"{HOME}/Suhaarah/advertising/marketing/{{lang}}/screenshots/ios"
_VAULT_STD = {"home": "1_home", "warranties": "2_my_warranties", "filter": "3_filter", "detail": "4_detail",
              "status": "5_status", "insights": "7_statistics", "settings": "8_settings", "cardstyle": "9_cardstyle"}
_VAULT_DEVICE = {
    "de": dict(home="IMG_1900", warranties="IMG_1901", detail="IMG_1902", filter="IMG_1903",
               status="IMG_1904", insights="IMG_1905", settings="IMG_1906", cardstyle="IMG_1907"),
    "es": dict(home="IMG_1908", warranties="IMG_1909", detail="IMG_1910", status="IMG_1911",
               insights="IMG_1912", settings="IMG_1913", cardstyle="IMG_1914", filter="IMG_1915"),
    "fr": dict(home="IMG_1916", warranties="IMG_1917", filter="IMG_1918", detail="IMG_1919",
               status="IMG_1920", insights="IMG_1921", settings="IMG_1922",
               cardstyle="screenshot_fr_fixed_1284x2778"),   # the owner's corrected capture
    "ja": dict(home="IMG_1924", warranties="IMG_1925", detail="IMG_1926", filter="IMG_1927",
               status="IMG_1928", settings="IMG_1929", cardstyle="IMG_1930", insights="IMG_1931"),
    "ko": dict(home="IMG_1941", warranties="IMG_1942", filter="IMG_1943", detail="IMG_1944",
               status="IMG_1945", insights="IMG_1946", settings="IMG_1947", cardstyle="IMG_1948"),
    "tr": dict(home="IMG_1932", warranties="IMG_1933", filter="IMG_1934", detail="IMG_1935",
               status="IMG_1936", insights="IMG_1937", settings="IMG_1938", cardstyle="IMG_1939"),
}


def vault_source(lang, screen):
    d = _VAULT_DIR.format(lang=lang)
    if lang in _VAULT_DEVICE:
        name = _VAULT_DEVICE[lang][screen]
        for ext in (".PNG", ".png"):
            if os.path.exists(f"{d}/{name}{ext}"):
                return f"{d}/{name}{ext}"
        return None
    return f"{d}/{_VAULT_STD[screen]}_1284x2778.png"


_CD_STD = {"home": "01_home", "story": "02_event_story", "list": "03_events_list", "detail": "04_event_detail",
           "add": "05_add_event", "tools": "06_tools", "settings": "07_settings"}


def countdown_source(lang, screen):
    return f"{HOME}/Countdown/marketing/{lang}/screenshots/ios/{_CD_STD[screen]}_{lang}.png"


APPS = {
    "vault": ("assets/img/apps/vault", list(_VAULT_STD), vault_source),
    "countdown": ("assets/img/apps/countdown", list(_CD_STD), countdown_source),
}


def main(argv):
    force = "--force" in argv
    args = [a for a in argv if not a.startswith("--")]
    apps = [a for a in args if a in APPS] or list(APPS)
    langs = [a for a in args if a in LANGS] or LANGS
    made = skipped = 0
    for app in apps:
        out_dir, screens, source = APPS[app]
        for lang in langs:
            for screen in screens:
                out = os.path.join(ROOT, out_dir, f"{screen}_{lang}.webp")
                if os.path.exists(out) and not force:
                    skipped += 1
                    continue
                src = source(lang, screen)
                if not src or not os.path.exists(src):
                    print(f"MISSING {app} {lang} {screen}: {src}")
                    continue
                im = Image.open(src).convert("RGB")
                if abs(im.width / im.height - SIZE[0] / SIZE[1]) > 0.01:
                    print(f"WRONG SHAPE {app} {lang} {screen}: {im.size}")
                    continue
                im.resize(SIZE, Image.LANCZOS).save(out, "WEBP", quality=82, method=6)
                made += 1
    print(f"made {made}, kept {skipped}")


if __name__ == "__main__":
    main(sys.argv[1:])
