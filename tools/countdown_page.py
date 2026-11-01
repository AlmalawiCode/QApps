"""countdown_page.py — the Countdown Keeper (كم مضى وكم بقي) page (/apps/countdown-keeper/).

Why a module of its own: same reason as docmatic_page.py and vault_page.py —
a long, hand-tuned page kept out of build.py. It reuses the DocMatic page's
layout styles and lightbox but has its own content and pictures in
/assets/img/apps/countdown/<name>_<lang>.webp (raw app renders + status bar).

Every claim follows Countdown's marketing rules (Countdown/marketing/
marketing.yaml) and its code (2026-11-01): never mention birthdays or
celebrations (examples are graduation, first job, marriage, home, travel,
last installment, retirement); free tier = 5 events (FreeTierLimits.maxEvents);
the full version is a one-time Lifetime Access. 9 card styles (three were
removed from EventCardLayout), 8 sort orders, 6 counter units, 5 date tools.
Live on the App Store; Google Play not yet.
"""

import docmatic_page

IMG = "/assets/img/apps/countdown"

FEATURES = [
    ("⏳", "Live counters", "عدّادات حيّة", [
        ("How long since a date, or how long until it", "كم مضى على تاريخ، أو كم بقي حتى موعده"),
        ("Updated every second", "تتحدّث كل ثانية"),
        ("Turns from “remaining” to “elapsed” by itself when the day comes", "تتحوّل من «كم بقي» إلى «كم مضى» وحدها عند حلول الموعد"),
        ("Shows “Today” on the day itself", "تُظهر «اليوم» في يوم الحدث نفسه"),
        ("Choose the units: years, months, days, hours, minutes, seconds", "اختر الوحدات: سنوات، أشهر، أيام، ساعات، دقائق، ثوانٍ"),
        ("A time of day, if you want one", "وقت من اليوم إن أردت"),
    ]),
    ("🌙", "Hijri and Gregorian", "هجري وميلادي", [
        ("Gregorian or Hijri (Umm al-Qura)", "ميلادي أو هجري (أم القرى)"),
        ("A calendar for each date on its own", "تقويم لكل تاريخ على حدة"),
        ("Have a date in the other calendar? Convert it and save it", "عندك تاريخ بالتقويم الآخر؟ حوّله واحفظه مباشرة"),
    ]),
    ("📖", "Event story", "قصة الحدث", [
        ("Write the story of any date", "اكتب قصة أي تاريخ"),
        ("Show it under its card with one tap", "اعرضها أسفل بطاقته بلمسة"),
    ]),
    ("🔁", "Monthly dates", "تواريخ شهرية", [
        ("Salary, rent, installments", "الراتب، والإيجار، والأقساط"),
        ("Moves to the next date by itself", "ينتقل إلى الموعد التالي وحده"),
    ]),
    ("🔔", "Reminders", "التذكيرات", [
        ("At the time, a day before or a week before", "في وقته، أو قبله بيوم، أو قبله بأسبوع"),
        ("Repeat after 5 or 10 minutes", "تكرار بعد 5 أو 10 دقائق"),
        ("“Remind me again” from the reminder log", "«ذكّرني مجددًا» من سجلّ التذكيرات"),
    ]),
    ("🎨", "Make it yours", "على ذوقك", [
        ("An emoji or your own photo for each date", "أيقونة تعبيرية أو صورتك الخاصة لكل تاريخ"),
        ("A colour for each card", "لون لكل بطاقة"),
        ("Pin your most important dates", "ثبّت أهم تواريخك"),
    ]),
    ("🃏", "9 card styles", "9 أشكال للبطاقة", [
        ("Classic", "كلاسيك"), ("One line", "سطر واحد"), ("Large counters", "عدّادات كبيرة"),
        ("Days only", "الأيام فقط"), ("Big emoji", "إيموجي كبير"), ("Minimal", "مينيمال"),
        ("Dashboard", "داشبورد"), ("Modern premium", "بريميوم حديث"), ("Large number", "رقم ضخم"),
    ]),
    ("🔎", "Search and 8 ways to sort", "البحث و8 طرق للترتيب", [
        ("Search your dates", "ابحث في تواريخك"),
        ("My order: drag to arrange", "ترتيبي: اسحب لترتّب"),
        ("Upcoming first, or past first", "القادمة أولًا، أو المنقضية أولًا"),
        ("Pinned first", "المثبّتة أولًا"),
        ("By date or by name", "حسب التاريخ أو حسب الاسم"),
        ("Recently added, or oldest added", "المضافة حديثًا، أو الأقدم إضافة"),
    ]),
    ("🏠", "Home at a glance", "الرئيسية بنظرة واحدة", [
        ("Total, upcoming and past", "الإجمالي، والقادمة، والمنقضية"),
        ("Your nearest dates first", "أقرب أحداثك أولًا"),
        ("Open the app and see your counters at once", "افتح التطبيق فترى عدّاداتك مباشرة"),
    ]),
    ("🧮", "5 date tools", "5 أدوات للتاريخ", [
        ("Hijri ⇄ Gregorian converter", "محوّل هجري ⇄ ميلادي"),
        ("Age calculator", "حاسبة العمر"),
        ("Difference between two dates", "الفرق بين تاريخين"),
        ("Add or subtract days", "جمع الأيام وطرحها"),
        ("Retirement estimator", "مقدّر التقاعد"),
    ]),
    ("♻️", "Trash", "المحذوفات", [
        ("Deleted dates kept for 30 days", "التواريخ المحذوفة تبقى 30 يومًا"),
        ("Restore with a tap", "استعدها بلمسة"),
        ("Select several at once", "حدّد عدة تواريخ مرة واحدة"),
    ]),
    ("🔐", "Backup and your data", "النسخ الاحتياطي وبياناتك", [
        ("Encrypted backup of all your data", "نسخة احتياطية مشفّرة لكل بياناتك"),
        ("Restore when you need it", "استعدها عند الحاجة"),
        ("Export and import your dates as a JSON file", "صدّر تواريخك واستوردها كملف JSON"),
    ]),
    ("🔒", "Private and locked", "خاص ومقفل", [
        ("No account, no sign-in", "بلا حساب وبلا تسجيل دخول"),
        ("Works offline; your data stays on your phone", "يعمل دون إنترنت، وبياناتك على جوالك"),
        ("Optional fingerprint or face lock", "قفل اختياري بالبصمة أو الوجه"),
    ]),
    ("🌍", "18 languages", "18 لغة", [
        ("Arabic and Urdu right to left", "العربية والأردية من اليمين إلى اليسار"),
        ("Light and dark", "فاتح وداكن"),
    ]),
]

N_MAIN = len(FEATURES)
N_SUB = sum(len(f[3]) for f in FEATURES)


def build_page(render, h, p, crumbs, app, store_button):
    """Writes /apps/countdown-keeper/ and returns its canonical URL."""

    def img(name, alt_en, alt_ar, eager=False):
        load = "eager" if eager else "lazy"
        return (f'<img data-en src="{IMG}/{name}_en.webp" alt="{alt_en}" loading="{load}" width="620" height="1341">'
                f'<img data-ar src="{IMG}/{name}_ar.webp" alt="{alt_ar}" loading="{load}" width="620" height="1341">')

    def phone(name, alt_en, alt_ar, cls="", eager=False):
        return (f'<button type="button" class="dm-phone {cls}" data-zoom="{name}" '
                f'aria-label="{alt_en}">{img(name, alt_en, alt_ar, eager=eager)}</button>')

    def two(en, ar, tag="span", cls=""):
        c = f' class="{cls}"' if cls else ""
        return f'<{tag}{c} data-en>{en}</{tag}><{tag}{c} data-ar>{ar}</{tag}>'

    apple = store_button("apple", app["appstore"]) if app.get("appstore") else ""
    play = (store_button("play", app["playstore"]) if app.get("playstore") else
            '<span class="chip"><span data-en>Google Play — coming soon</span><span data-ar>Google Play — قريبًا</span></span>')
    stores = f'<div class="stores" style="align-items:center">{apple}{play}</div>'

    hero = f'''<section class="dm-hero"><div class="container dm-hero-grid">
  <div class="dm-hero-copy">
    <div class="dm-brand"><img src="{app['icon']}" alt="Countdown Keeper icon" width="64" height="64">
      <div><strong data-en>Countdown Keeper</strong><strong data-ar>كم مضى وكم بقي</strong>{two("How long since, how long until", "العدّاد — لتواريخك المهمة", "small")}</div></div>
    <span class="dm-dev">{two("Now on the App Store · Google Play soon", "متاح الآن على App Store · وقريبًا على Google Play")}</span>
    {h(1, "How long has it been? <em>How long is left?</em>", "كم مضى؟ <em>وكم بقي؟</em>")}
    {p("Your graduation, your marriage, your first day at work, the day you moved into your home — and the retirement or trip still ahead. Live counters for the dates that made your story, in Hijri and Gregorian — "
       f"{N_MAIN} main features and {N_SUB} tools inside them.",
       "تخرجك، وزواجك، وأول يوم في عملك، ويوم انتقلت إلى بيتك — والتقاعد أو الرحلة التي تنتظرك. عدّادات حيّة للتواريخ التي صنعت قصتك، بالهجري والميلادي — "
       f"{N_MAIN} خاصية رئيسية و{N_SUB} أداة داخلها.", "lead")}
    {stores}
  </div>
  <div class="dm-hero-stage">
    {phone("home", "Countdown Keeper home page", "الصفحة الرئيسية في كم مضى وكم بقي", "dm-p1", eager=True)}
    {phone("detail", "A date with its live counter", "تاريخ مع عدّاده الحي", "dm-p2", eager=True)}
  </div>
</div></section>'''

    stats = f'''<section class="dm-stats-wrap"><div class="container"><div class="dm-stats">
  <div><b>{N_MAIN}</b>{two("main features", "خاصية رئيسية")}</div>
  <div><b>{N_SUB}</b>{two("tools inside them", "أداة داخلها")}</div>
  <div><b>2</b>{two("calendars: Hijri &amp; Gregorian", "تقويمان: هجري وميلادي")}</div>
  <div><b>18</b>{two("languages", "لغة")}</div>
</div></div></section>'''

    story = f'''<section id="story" class="dm-story"><div class="container">
  <div class="section-head">
    <span class="kicker" data-en>The story</span><span class="kicker" data-ar>القصة</span>
    {h(2, "Our lives are made of events — and every event has a story.", "حياتنا كلها أحداث، ولكل حدث قصة.")}
  </div>
  <div class="dm-story-grid">
    <div class="dm-story-text">
      {p("One day you wonder: how long has it been since I graduated? You sit and try to remember the year, then count on your fingers… and still you are not sure. Countdown Keeper answers at once: <q>7 years, 4 months and 12 days</q> — and the counter keeps moving, to the second.",
         "في يوم من الأيام تسأل نفسك: كم مضى على تخرجي من الجامعة؟ تجلس تتذكّر السنة، ثم تبدأ تحسب… ويبقى في نفسك شيء من الشك. أما «كم مضى وكم بقي» فيجيبك فورًا: <q>7 سنوات و4 أشهر و12 يومًا</q> — والعدّاد يمضي معك حتى الثانية.")}
      {p("And the most beautiful part: every date can keep its story. You see that five years have passed since your graduation, then you read the story you wrote that day — and it brings back things in your life you had almost forgotten. Numbers alone do not move us; the stories behind them do.",
         "والأجمل من ذلك أن كل تاريخ يحفظ قصته. ترى أنه مضى على تخرجك خمس سنوات، ثم تقرأ القصة التي كتبتها يومها — فتذكّرك بأشياء جميلة في حياتك كدت تنساها. الأرقام وحدها لا تحرّكنا، ولكن القصص التي وراءها تفعل.")}
      {p("How long since you bought your car? Since you moved into your home? Since your first day at work? When you know exactly how long has passed, you value things as they deserve. Buy a product, save its date — and years later the app tells you: <q>5 years and 3 months</q>. You feel at ease with it, and you trust it. Without that, we only guess: three years, maybe four…",
         "كم مضى على شرائك لسيارتك؟ وعلى سكنك في بيتك؟ وعلى أول يوم في عملك؟ حين تعرف بالضبط كم مضى، تقدّر الأشياء قدرها. تشتري منتجًا وتحفظ تاريخه — وبعد سنوات يخبرك التطبيق: <q>مضى عليه 5 سنوات و3 أشهر</q>، فتشعر بالارتياح له والثقة به. وبدون ذلك نرجم بالغيب: ثلاث سنوات، وربما أربع…")}
      {p(f"And because we live with two calendars every day, Hijri and Gregorian, the app counts with both — for each date on its own. A Hijri year is shorter than a Gregorian one, so five years by the Hijri calendar can be less than five by the Gregorian. Small details like these matter in our lives — that is why we built {N_MAIN} main features and {N_SUB} tools inside them, so you always know, at a glance, how long has passed and how long is left.",
         f"ولأننا نعيش مع التقويمين كل يوم، الهجري والميلادي، يحسب التطبيق بالاثنين — لكل تاريخ على حدة. فالسنة الهجرية أقصر من الميلادية، وقد يكون مضى على الحدث خمس سنوات بالهجري وأقل منها بالميلادي. تفاصيل صغيرة، لكنها تهمّنا في حياتنا — ولهذا صنعنا {N_MAIN} خاصية رئيسية و{N_SUB} أداة داخلها، لتعرف دائمًا وبنظرة واحدة: كم مضى، وكم بقي.")}
    </div>
    <ol class="dm-timeline">
      <li><span>🎓</span><div>{two("How long since I graduated?", "كم مضى على تخرجي؟", "b")}{two("No more counting on your fingers.", "بلا حساب على الأصابع.", "small")}</div></li>
      <li><span>📖</span><div>{two("A date with its story", "تاريخ ومعه قصته", "b")}{two("The number, then the memory behind it.", "الرقم، ثم الذكرى التي وراءه.", "small")}</div></li>
      <li><span>🚗</span><div>{two("5 years and 3 months", "5 سنوات و3 أشهر", "b")}{two("Your car, your home, a product — no guessing.", "سيارتك، بيتك، منتج — بلا تخمين.", "small")}</div></li>
      <li><span>🌙</span><div>{two("Hijri and Gregorian", "هجري وميلادي", "b")}{two("Each calendar counts the years its own way.", "لكل تقويم حسابه للسنين.", "small")}</div></li>
    </ol>
  </div>
</div></section>'''

    steps = [
        ("add", "1", "Add a date", "أضف تاريخًا",
         "Name it, pick the date in Hijri or Gregorian, and choose what the counter shows.",
         "سمّه، واختر التاريخ بالهجري أو الميلادي، وحدّد ما يعرضه العدّاد."),
        ("home", "2", "See your counters", "شاهد عدّاداتك",
         "Open the app: total, upcoming and past, nearest first.",
         "افتح التطبيق: الإجمالي والقادمة والمنقضية، والأقرب أولًا."),
        ("story", "3", "Tell its story", "اكتب قصته",
         "Every date can keep the story behind it, under its card.",
         "كل تاريخ يحفظ قصته، أسفل بطاقته."),
        ("list", "4", "Search and sort", "ابحث ورتّب",
         "Eight ways to sort, or drag them into your own order.",
         "ثماني طرق للترتيب، أو اسحبها بترتيبك الخاص."),
        ("tools", "5", "Use the date tools", "استخدم أدوات التاريخ",
         "Converter, age, difference, add or subtract, retirement.",
         "المحوّل، والعمر، والفرق، والجمع والطرح، والتقاعد."),
    ]
    journey_items = "".join(
        f'''<li class="dm-step">{phone(n, en_t, ar_t)}<div class="dm-step-txt"><span class="dm-num">{k}</span>
        {two(en_t, ar_t, "h3")}{two(en_d, ar_d, "p")}</div></li>'''
        for n, k, en_t, ar_t, en_d, ar_d in steps)
    journey = f'''<section class="section-soft dm-journey"><div class="container">
  <div class="section-head center">
    <span class="kicker" data-en>How it works</span><span class="kicker" data-ar>كيف يعمل</span>
    {h(2, "Your important dates, counted for you.", "تواريخك المهمة، محسوبة لك.")}
  </div>
  <ol class="dm-steps">{journey_items}</ol>
  {p("Swipe to see every step.", "اسحب لترى كل الخطوات.", "dm-swipe-hint")}
</div></section>'''

    def spot(kicker, title, body, bullets, shots, flip=False):
        lis = "".join(f'<li data-en>{e}</li><li data-ar>{a}</li>' for e, a in bullets)
        ph = "".join(phone(*s) for s in shots)
        return f'''<section class="dm-spot{' dm-flip' if flip else ''}"><div class="container dm-spot-grid">
  <div class="dm-spot-copy">
    <span class="kicker" data-en>{kicker[0]}</span><span class="kicker" data-ar>{kicker[1]}</span>
    {h(2, title[0], title[1])}
    {p(body[0], body[1], "lead")}
    <ul class="dm-ticks">{lis}</ul>
  </div>
  <div class="dm-spot-shots dm-n{len(shots)}">{ph}</div>
</div></section>'''

    spots = "".join([
        spot(("Live counters", "عدّادات حيّة"),
             ("Every date, counted to the second.", "كل تاريخ، محسوب حتى الثانية."),
             ("Years, months and days since a date — or until it — on a counter that moves every second, and turns from “remaining” to “elapsed” by itself.",
              "سنوات وأشهر وأيام منذ تاريخ — أو حتى موعده — في عدّاد يتحرّك كل ثانية، ويتحوّل من «كم بقي» إلى «كم مضى» وحده."),
             [("Choose the units the counter shows", "اختر الوحدات التي يعرضها العدّاد"),
              ("“Today” on the day itself", "«اليوم» في يوم الحدث نفسه"),
              ("Monthly dates move to the next one by themselves", "التواريخ الشهرية تنتقل إلى الموعد التالي وحدها")],
             [("detail", "A date with its live counter", "تاريخ مع عدّاده الحي"),
              ("home", "Home: your nearest dates", "الرئيسية: أقرب أحداثك")]),
        spot(("Event story", "قصة الحدث"),
             ("Every date has a story.", "لكل تاريخ قصة."),
             ("Write what happened on that day, and show it under its card with one tap.",
              "اكتب ما حدث في ذلك اليوم، واعرضه أسفل بطاقته بلمسة."),
             [("An emoji or your own photo for each date", "أيقونة أو صورتك الخاصة لكل تاريخ"),
              ("A colour and 9 card styles", "لون و9 أشكال للبطاقة")],
             [("story", "A date with its story", "تاريخ مع قصته")], flip=True),
        spot(("Hijri &amp; Gregorian", "هجري وميلادي"),
             ("Both calendars, date by date.", "التقويمان معًا، لكل تاريخ."),
             ("Pick Gregorian or Hijri (Umm al-Qura) for each date on its own — and if you have a date in the other calendar, convert it and save it straight away.",
              "اختر الميلادي أو الهجري (أم القرى) لكل تاريخ على حدة — وإن كان لديك تاريخ بالتقويم الآخر، حوّله واحفظه مباشرة."),
             [("Reminders at the time, a day or a week before", "تذكيرات في وقتها، أو قبلها بيوم أو أسبوع"),
              ("Repeat after 5 or 10 minutes", "تكرار بعد 5 أو 10 دقائق")],
             [("add", "Adding a new date", "إضافة تاريخ جديد")]),
        spot(("Search &amp; sort", "البحث والترتيب"),
             ("Find any date, in any order.", "اعثر على أي تاريخ، بأي ترتيب."),
             ("Search your dates and sort them eight ways — or drag them into your own order. Pin the ones that matter most.",
              "ابحث في تواريخك ورتّبها بثماني طرق — أو اسحبها بترتيبك الخاص. وثبّت أهمّها."),
             [("Upcoming first, past first, pinned first", "القادمة أولًا، المنقضية أولًا، المثبّتة أولًا"),
              ("Deleted dates kept 30 days in the trash", "المحذوفات تبقى 30 يومًا")],
             [("list", "Sorting your dates", "ترتيب تواريخك")], flip=True),
        spot(("Date tools", "أدوات التاريخ"),
             ("Five date tools, built in.", "خمس أدوات للتاريخ، مدمجة."),
             ("Convert Hijri and Gregorian, calculate an exact age, the difference between two dates, add or subtract days, and estimate your retirement date.",
              "حوّل بين الهجري والميلادي، واحسب العمر بدقة، والفرق بين تاريخين، واجمع الأيام أو اطرحها، وقدّر تاريخ تقاعدك."),
             [("Encrypted backup and restore", "نسخ احتياطي مشفّر واستعادة"),
              ("Optional fingerprint or face lock", "قفل اختياري بالبصمة أو الوجه"),
              ("18 languages", "18 لغة")],
             [("tools", "Date tools", "أدوات التاريخ"),
              ("settings", "Settings", "الإعدادات")]),
    ])

    cards = []
    for icon, en, ar, subs in FEATURES:
        lis = "".join(f'<li data-en>{e}</li><li data-ar>{a}</li>' for e, a in subs)
        cards.append(f'''<details class="dm-feat"><summary><span class="dm-ico" aria-hidden="true">{icon}</span>
      <span class="dm-feat-t">{two(en, ar)}</span><span class="dm-count">{len(subs)}</span></summary>
      <ul>{lis}</ul></details>''')
    catalogue = f'''<section id="features" class="section-soft"><div class="container">
  <div class="section-head center">
    <span class="kicker" data-en>Everything inside</span><span class="kicker" data-ar>كل ما في التطبيق</span>
    {h(2, f"{N_MAIN} main features. {N_SUB} tools inside them.", f"{N_MAIN} خاصية رئيسية. {N_SUB} أداة داخلها.")}
    {p("Tap any feature to see what it holds.", "اضغط أي خاصية لترى ما بداخلها.")}
    <button type="button" class="btn btn-secondary dm-openall" aria-pressed="false">{two("Open all", "افتح الكل")}</button>
  </div>
  <div class="dm-feats">{"".join(cards)}</div>
</div></section>'''

    price = f'''<section class="dm-price"><div class="container"><div class="dm-price-card">
  <div>
    <span class="kicker" data-en>Price</span><span class="kicker" data-ar>السعر</span>
    {h(2, "Free to start. One payment for life.", "ابدأ مجانًا. ودفعة واحدة مدى الحياة.")}
    {p("Start free with up to 5 dates. When you need more, Lifetime Access removes the limit with a single payment — no subscription.",
       "ابدأ مجانًا بما يصل إلى 5 أحداث. وحين تحتاج إلى المزيد، يفتح «الوصول مدى الحياة» الحدّ بدفعة واحدة — بلا اشتراك.")}
    <div style="margin-top:18px">{stores}</div>
  </div>
  <ul class="dm-ticks dm-ticks-big">
    <li data-en>Free: up to 5 dates</li><li data-ar>مجانًا: حتى 5 أحداث</li>
    <li data-en>Lifetime Access: pay once</li><li data-ar>الوصول مدى الحياة: ادفع مرة واحدة</li>
    <li data-en>No account, works offline</li><li data-ar>بلا حساب، ويعمل دون إنترنت</li>
    <li data-en>Your data stays on your phone</li><li data-ar>بياناتك تبقى على جوالك</li>
    <li data-en>18 languages</li><li data-ar>18 لغة</li>
  </ul>
</div></div></section>'''

    gal = [("home", "Home", "الرئيسية"), ("story", "Event story", "قصة الحدث"), ("list", "Events", "الأحداث"),
           ("detail", "A date", "تاريخ"), ("add", "New date", "حدث جديد"), ("tools", "Tools", "الأدوات"),
           ("settings", "Settings", "الإعدادات")]
    gallery = f'''<section class="section-soft"><div class="container">
  <div class="section-head center">
    <span class="kicker" data-en>Screens</span><span class="kicker" data-ar>الشاشات</span>
    {h(2, "Real screens from the app.", "شاشات حقيقية من التطبيق.")}
    {p("Tap any screen to see it large.", "اضغط أي شاشة لتراها مكبّرة.")}
  </div>
  <div class="dm-gallery">{"".join(f'<figure>{phone(n, en, ar)}<figcaption>{two(en, ar)}</figcaption></figure>' for n, en, ar in gal)}</div>
</div></section>'''

    faqs = [
        ("Is it free?", "هل التطبيق مجاني؟",
         "You can start free with up to 5 dates. Lifetime Access is a single payment that removes the limit — no subscription.",
         "تبدأ مجانًا بما يصل إلى 5 أحداث. و«الوصول مدى الحياة» دفعة واحدة ترفع الحدّ — بلا اشتراك."),
        ("Does it support the Hijri calendar?", "هل يدعم التقويم الهجري؟",
         "Yes — Hijri (Umm al-Qura) and Gregorian, chosen for each date on its own.",
         "نعم — الهجري (أم القرى) والميلادي، تختار لكل تاريخ على حدة."),
        ("Do I need an account or the internet?", "هل أحتاج إلى حساب أو إنترنت؟",
         "Neither. It works offline and your data stays on your phone.",
         "لا هذا ولا ذاك. يعمل دون إنترنت، وتبقى بياناتك على جوالك."),
        ("Is it on Google Play?", "هل هو على Google Play؟",
         "It is on the App Store now, and coming soon to Google Play.",
         "هو على App Store الآن، وقريبًا على Google Play."),
    ]
    faq_html = "".join(
        f'<details><summary>{two(qe, qa)}</summary><p data-en>{ae}</p><p data-ar>{aa}</p></details>'
        for qe, qa, ae, aa in faqs)
    links = (f'<div class="linkrow" style="margin-top:22px;justify-content:center">'
             f'<a href="/tutorials/countdown-keeper/">{two("Tutorial", "الشرح")}</a>'
             f'<a href="/support/countdown-keeper/">{two("Support", "الدعم")}</a>'
             f'<a href="/privacy/countdown-keeper/">{two("Privacy policy", "سياسة الخصوصية")}</a></div>')
    faq = f'''<section><div class="container" style="max-width:820px">
  {h(2, "Questions", "أسئلة", "center")}
  <div class="faq" style="margin-top:28px">{faq_html}</div>
  {links}
</div></section>'''

    cta = f'''<section style="padding-top:0"><div class="container"><div class="cta-band">
  <div>
    {h(2, "How long has it been? How long is left?", "كم مضى؟ وكم بقي؟")}
    {p("Keep every important date in one place, and always know at a glance.",
       "احفظ كل تاريخ مهمّ في مكان واحد، واعرف دائمًا بنظرة واحدة.")}
  </div>
  {stores}
</div></div></section>'''

    lightbox = '''<div class="dm-lb" hidden><button type="button" class="dm-lb-x" aria-label="Close">✕</button>
  <button type="button" class="dm-lb-nav dm-lb-prev" aria-label="Previous">‹</button>
  <img alt=""><button type="button" class="dm-lb-nav dm-lb-next" aria-label="Next">›</button></div>'''

    js = docmatic_page.JS.replace("/assets/img/apps/docmatic/", f"{IMG}/")
    body = (crumbs([("Home", "الرئيسية", "/"), ("Apps", "التطبيقات", "/apps/"), (app["name_en"], app["name_ar"], None)])
            + hero + stats + story + journey + spots + catalogue + price + gallery + faq + cta
            + lightbox + f"<script>{js}</script>")

    return render("/apps/countdown-keeper/",
                  "Countdown Keeper — How long since, how long until | Q Apps",
                  "كم مضى وكم بقي — عدّاد تواريخك المهمة بالهجري والميلادي | كيو آبز",
                  f"Countdown Keeper shows how long has passed since your important dates and how long is left until the next ones — live counters in Hijri and Gregorian, reminders and date tools. {N_MAIN} features.",
                  f"«كم مضى وكم بقي» يخبرك كم مضى على تواريخك المهمة وكم بقي حتى القادمة — عدّادات حيّة بالهجري والميلادي، وتذكيرات، وأدوات للتاريخ. {N_MAIN} خاصية.",
                  body, active="apps", head_extra=f"<style>{docmatic_page.CSS}</style>")
