"""vault_page.py — the Vault (خزنة الضمانات) app page (/apps/vault/).

Why a module of its own: same reason as docmatic_page.py — a long,
hand-tuned page kept out of build.py. It reuses the DocMatic page's layout
styles and lightbox (one design for every app page) but has its own content
and its own pictures in /assets/img/apps/vault/<name>_<lang>.webp.

Every claim follows Vault's marketing rules (Suhaarah/advertising/marketing/
marketing.yaml) and its code (2026-11-01): warranty-centric, the invoice QR
fills only the store name and purchase date, backup never names a cloud
provider, no AI claims, free tier = 3 invoices with one product each, paid =
one-time Lifetime Access (never a subscription), no prices or totals.
Screens are the owner's real-device captures (copied, never edited).
"""

import docmatic_page

IMG = "/assets/img/apps/vault"

FEATURES = [
    ("🧾", "Every invoice in one place", "كل فواتيرك في مكان واحد", [
        ("Paper and digital invoices together", "الفواتير الورقية والرقمية معًا"),
        ("Photograph a paper invoice inside a guide frame", "صوّر الفاتورة الورقية داخل إطار يرشدك"),
        ("Share an invoice in from WhatsApp, Files, Drive or email", "شارك الفاتورة إلى التطبيق من واتساب أو الملفات أو Drive أو البريد"),
        ("No invoice? Enter it by hand", "لا توجد فاتورة؟ أدخلها يدويًا"),
        ("A picture of the store, if you like", "صورة للمتجر إن أردت"),
    ]),
    ("🔳", "Invoice QR", "رمز QR في الفاتورة", [
        ("Scan the QR code on a Saudi invoice", "امسح رمز QR في الفاتورة السعودية"),
        ("Fills the store name and purchase date for you", "يعبّئ اسم المتجر وتاريخ الشراء لك"),
        ("Torch for dark receipts", "كشاف للإيصالات في الإضاءة الضعيفة"),
        ("No QR? Continue by hand", "لا يوجد رمز؟ تابع يدويًا"),
    ]),
    ("📦", "Products under each invoice", "المنتجات داخل كل فاتورة", [
        ("Several products on one invoice", "عدة منتجات في فاتورة واحدة"),
        ("Each product with its own warranty", "لكل منتج ضمانه الخاص"),
        ("A photo for each product", "صورة لكل منتج"),
        ("A category for each product", "فئة لكل منتج"),
    ]),
    ("🛡️", "Warranty tracking", "متابعة الضمان", [
        ("Duration in years, months and days", "المدة بالسنوات والأشهر والأيام"),
        ("Lifetime warranty", "ضمان مدى الحياة"),
        ("Or mark it plainly: no warranty", "أو حدّد بوضوح: بلا ضمان"),
        ("Live countdown of the time left", "عدّاد حي للمدة المتبقية"),
        ("Time elapsed since the purchase", "المدة المنقضية منذ الشراء"),
        ("Status at a glance: active, expiring, expired, lifetime", "الحالة بنظرة: ساري، قريب الانتهاء، منتهٍ، مدى الحياة"),
    ]),
    ("🔔", "Reminders", "التذكيرات", [
        ("A reminder before a warranty ends", "تذكير قبل انتهاء الضمان"),
        ("On the expiry day, or days before", "في يوم الانتهاء، أو قبله بأيام"),
        ("The nearest expiry right on the home page", "أقرب ضمان ينتهي على الصفحة الرئيسية"),
    ]),
    ("🏠", "Home at a glance", "الرئيسية بنظرة واحدة", [
        ("Total, expiring soon and expired", "الإجمالي، والقريب من الانتهاء، والمنتهي"),
        ("The 10 warranties nearest to expiry", "أقرب 10 ضمانات إلى الانتهاء"),
        ("Add a new invoice with one button", "أضف فاتورة جديدة بزر واحد"),
    ]),
    ("🔎", "Search and filters", "البحث والتصفية", [
        ("Search by store, invoice or product", "ابحث بالمتجر أو الفاتورة أو المنتج"),
        ("Filter by status", "صفِّ حسب الحالة"),
        ("Filter by year and month", "صفِّ حسب السنة والشهر"),
    ]),
    ("🗂️", "Categories", "الفئات", [
        ("Ready categories: electronics, home, personal care…", "فئات جاهزة: إلكترونيات، المنزل، العناية الشخصية…"),
        ("Your own categories", "فئاتك الخاصة"),
        ("An icon and a colour for each", "أيقونة ولون لكل فئة"),
    ]),
    ("📍", "Store details", "بيانات المتجر", [
        ("Store location from GPS or your maps app", "موقع المتجر من GPS أو من تطبيق الخرائط"),
        ("Open it later in Maps", "افتحه لاحقًا في الخرائط"),
        ("Store phone, call in one tap", "هاتف المتجر، اتصل بلمسة"),
        ("Branch name", "اسم الفرع"),
    ]),
    ("📤", "Share and print", "المشاركة والطباعة", [
        ("Share the invoice when you need it", "شارك الفاتورة عند الحاجة"),
        ("Print it", "اطبعها"),
        ("Open and view the invoice pages", "افتح صفحات الفاتورة واعرضها"),
    ]),
    ("📄", "Warranty report as PDF", "تقرير الضمانات PDF", [
        ("Export the warranties you filtered", "صدّر الضمانات التي اخترتها بالتصفية"),
        ("A cover page and every invoice page", "صفحة غلاف وكل صفحات الفواتير"),
        ("Large reports split into volumes", "التقارير الكبيرة تُقسَّم إلى أجزاء"),
    ]),
    ("📊", "Insights", "الإحصائيات", [
        ("Coverage: how many warranties are still active", "التغطية: كم ضمانًا ما زال ساريًا"),
        ("Rhythm of your purchases", "إيقاع مشترياتك"),
        ("Forecasts: what expires next", "التوقعات: ما الذي ينتهي قريبًا"),
        ("Active versus expired at a glance", "الساري مقابل المنتهي بنظرة"),
    ]),
    ("🎨", "12 card styles", "12 نمطًا للبطاقة", [
        ("Classic", "كلاسيك"), ("One line", "سطر واحد"), ("Large counters", "عدّادات كبيرة"),
        ("Days only", "الأيام فقط"), ("Circular", "دائري"), ("Progress bar", "شريط تقدّم"),
        ("Big photo", "صورة كبيرة"), ("Minimal", "مينيمال"), ("Timeline", "خطّ زمني"),
        ("Dashboard", "داشبورد"), ("Modern premium", "بريميوم حديث"), ("Large number", "رقم ضخم"),
    ]),
    ("🔐", "Encrypted backup", "نسخ احتياطي مشفّر", [
        ("AES-256 encryption with your own password", "تشفير AES-256 بكلمة مرورك أنت"),
        ("You choose where each backup is kept", "أنت تختار أين تحفظ كل نسخة"),
        ("Restore on a new phone", "استعادة على جوال جديد"),
        ("A reminder when your backup gets old", "تذكير حين تقدم نسختك الاحتياطية"),
    ]),
    ("🔒", "App lock", "قفل التطبيق", [
        ("Face ID, fingerprint or device PIN", "بصمة الوجه أو الإصبع أو رمز الجهاز"),
        ("Your invoices stay on your phone", "فواتيرك تبقى على جوالك"),
    ]),
    ("🌍", "18 languages and two calendars", "18 لغة وتقويمان", [
        ("18 languages, Arabic and Urdu right to left", "18 لغة، والعربية والأردية من اليمين إلى اليسار"),
        ("Hijri or Gregorian dates", "تاريخ هجري أو ميلادي"),
        ("Light and dark", "فاتح وداكن"),
    ]),
]

N_MAIN = len(FEATURES)
N_SUB = sum(len(f[3]) for f in FEATURES)


def build_page(render, h, p, crumbs, app, store_button):
    """Writes /apps/vault/ and returns its canonical URL."""

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

    stores = "".join(store_button(k, app[u]) for k, u in (("apple", "appstore"), ("play", "playstore")) if app.get(u))

    hero = f'''<section class="dm-hero"><div class="container dm-hero-grid">
  <div class="dm-hero-copy">
    <div class="dm-brand"><img src="{app['icon']}" alt="Vault icon" width="64" height="64">
      <div><strong data-en>Vault</strong><strong data-ar>خزنة الضمانات</strong>{two("Warranty &amp; invoice manager", "متتبع الضمانات والفواتير", "small")}</div></div>
    <span class="dm-dev">{two("Available now on the App Store &amp; Google Play", "متاح الآن على App Store وGoogle Play")}</span>
    {h(1, "Never lose a warranty <em>again.</em>", "لا تخسر ضمانًا <em>مرة ثانية.</em>")}
    {p("Keep every invoice, every product and every warranty in one place, see exactly how many days are left, and get a reminder before it ends — "
       f"{N_MAIN} main features and {N_SUB} tools inside them.",
       "احفظ كل فاتورة وكل منتج وكل ضمان في مكان واحد، واعرف بالضبط كم يومًا بقي، واحصل على تذكير قبل أن ينتهي — "
       f"{N_MAIN} خاصية رئيسية و{N_SUB} أداة داخلها.", "lead")}
    <div class="stores">{stores}</div>
  </div>
  <div class="dm-hero-stage">
    {phone("home", "Vault home page", "الصفحة الرئيسية في خزنة الضمانات", "dm-p1", eager=True)}
    {phone("status", "Warranty status with its countdown", "حالة الضمان مع العدّاد", "dm-p2", eager=True)}
  </div>
</div></section>'''

    stats = f'''<section class="dm-stats-wrap"><div class="container"><div class="dm-stats">
  <div><b>{N_MAIN}</b>{two("main features", "خاصية رئيسية")}</div>
  <div><b>{N_SUB}</b>{two("tools inside them", "أداة داخلها")}</div>
  <div><b>18</b>{two("languages", "لغة")}</div>
  <div><b dir="ltr">1×</b>{two("one payment, yours for life", "دفعة واحدة، لك مدى الحياة")}</div>
</div></div></section>'''

    story = f'''<section id="story" class="dm-story"><div class="container">
  <div class="section-head">
    <span class="kicker" data-en>Why Vault</span><span class="kicker" data-ar>لماذا خزنة الضمانات</span>
    {h(2, "Where did the invoice go?", "وين راحت الفاتورة؟")}
  </div>
  <div class="dm-story-grid">
    <div class="dm-story-text">
      {p("You buy a washing machine, a phone, an air conditioner. The invoice arrives on paper or in a WhatsApp message — and then it disappears: in a drawer, under older chats, in an email you will never find again. The day the device breaks, the same question comes back: <q>Where is the warranty?</q>",
         "تشتري غسالة، أو جوالًا، أو مكيفًا. تصلك الفاتورة ورقًا أو في رسالة واتساب — ثم تختفي: في درج، أو تحت محادثات أقدم، أو في بريد لن تجده مرة أخرى. ويوم يتعطل الجهاز يعود السؤال نفسه: <q>وين الضمان؟</q>")}
      {p("Vault was built for that day. Photograph the invoice or share it in from WhatsApp, add the products on it, and give each one its warranty. From then on the app counts the days for you, shows what is about to expire, and reminds you before it ends.",
         "صُنعت خزنة الضمانات لذلك اليوم. صوّر الفاتورة أو شاركها من واتساب، وأضف المنتجات التي فيها، وحدّد لكل منتج ضمانه. ومن بعدها يعدّ التطبيق الأيام عنك، ويُريك ما يقترب من الانتهاء، ويذكّرك قبل أن ينتهي.")}
      {p(f"Then the details that make the difference: the store's location and phone, the invoice QR that fills the store and date for you, a PDF report of all your warranties, insights, an encrypted backup — {N_MAIN} main features and {N_SUB} tools inside them.",
         f"ثم التفاصيل التي تصنع الفرق: موقع المتجر وهاتفه، ورمز QR الذي يعبّئ المتجر والتاريخ لك، وتقرير PDF لكل ضماناتك، والإحصائيات، ونسخة احتياطية مشفّرة — {N_MAIN} خاصية رئيسية و{N_SUB} أداة داخلها.")}
    </div>
    <ol class="dm-timeline">
      <li><span>🧾</span><div>{two("The invoice", "الفاتورة", "b")}{two("Paper, or a message on WhatsApp.", "ورقة، أو رسالة على واتساب.", "small")}</div></li>
      <li><span>😟</span><div>{two("Lost", "ضاعت", "b")}{two("A drawer, old chats, an email.", "درج، أو محادثات قديمة، أو بريد.", "small")}</div></li>
      <li><span>🛡️</span><div>{two("Saved in Vault", "محفوظة في الخزنة", "b")}{two("Invoice, products and warranty together.", "الفاتورة والمنتجات والضمان معًا.", "small")}</div></li>
      <li><span>🔔</span><div>{two("Reminded in time", "تذكير في الوقت", "b")}{two("Before the warranty ends.", "قبل أن ينتهي الضمان.", "small")}</div></li>
    </ol>
  </div>
</div></section>'''

    steps = [
        ("home", "1", "Add the invoice", "أضف الفاتورة",
         "Photograph it, share it in from WhatsApp, or scan its QR code.",
         "صوّرها، أو شاركها من واتساب، أو امسح رمز QR فيها."),
        ("detail", "2", "Products and warranty", "المنتجات والضمان",
         "Each product on the invoice gets its own warranty, store and location.",
         "لكل منتج في الفاتورة ضمانه، ومعه المتجر وموقعه."),
        ("status", "3", "Watch the countdown", "تابع العدّاد",
         "Years, months and days left — and the time already passed.",
         "السنوات والأشهر والأيام المتبقية — والمدة التي مضت."),
        ("warranties", "4", "Find it in seconds", "اعثر عليه في ثوانٍ",
         "Search and filter all your warranties.",
         "ابحث وصفِّ كل ضماناتك."),
        ("insights", "5", "See the whole picture", "شاهد الصورة كاملة",
         "What is active, what expires next, what already ended.",
         "ما الساري، وما الذي ينتهي قريبًا، وما انتهى."),
    ]
    journey_items = "".join(
        f'''<li class="dm-step">{phone(n, en_t, ar_t)}<div class="dm-step-txt"><span class="dm-num">{k}</span>
        {two(en_t, ar_t, "h3")}{two(en_d, ar_d, "p")}</div></li>'''
        for n, k, en_t, ar_t, en_d, ar_d in steps)
    journey = f'''<section class="section-soft dm-journey"><div class="container">
  <div class="section-head center">
    <span class="kicker" data-en>How it works</span><span class="kicker" data-ar>كيف يعمل</span>
    {h(2, "From a lost invoice to a warranty you never miss.", "من فاتورة ضائعة إلى ضمان لا يفوتك.")}
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
        spot(("Warranty tracking", "متابعة الضمان"),
             ("Every warranty, counted to the day.", "كل ضمان، محسوب باليوم."),
             ("Each product keeps its own warranty: years, months and days, lifetime, or no warranty at all. Vault shows the time left and the time passed, live.",
              "لكل منتج ضمانه الخاص: سنوات وأشهر وأيام، أو مدى الحياة، أو بلا ضمان. وتعرض الخزنة المدة المتبقية والمدة المنقضية، مباشرة."),
             [("Active, expiring, expired or lifetime at a glance", "ساري، قريب الانتهاء، منتهٍ، أو مدى الحياة بنظرة"),
              ("A reminder before it ends", "تذكير قبل أن ينتهي"),
              ("The nearest expiry on the home page", "أقرب ضمان ينتهي على الصفحة الرئيسية")],
             [("status", "Warranty status and countdown", "حالة الضمان والعدّاد"),
              ("home", "Home: the warranties nearest to expiry", "الرئيسية: أقرب الضمانات إلى الانتهاء")]),
        spot(("Invoice details", "تفاصيل الفاتورة"),
             ("The invoice, the store, the products.", "الفاتورة، والمتجر، والمنتجات."),
             ("Open a warranty and everything is there: the invoice pages, the store with its location and phone, and every product bought with it.",
              "افتح أي ضمان تجد كل شيء: صفحات الفاتورة، والمتجر بموقعه وهاتفه، وكل منتج اشتريته معها."),
             [("Invoice QR fills the store name and purchase date", "رمز QR يعبّئ اسم المتجر وتاريخ الشراء"),
              ("Open the store in Maps or call it", "افتح المتجر في الخرائط أو اتصل به"),
              ("Share or print the invoice", "شارك الفاتورة أو اطبعها")],
             [("detail", "Warranty details with the invoice", "تفاصيل الضمان مع الفاتورة")], flip=True),
        spot(("Search &amp; filters", "البحث والتصفية"),
             ("Find any warranty in seconds.", "اعثر على أي ضمان في ثوانٍ."),
             ("Search by store, invoice or product, and filter by status, year or month.",
              "ابحث بالمتجر أو الفاتورة أو المنتج، وصفِّ حسب الحالة أو السنة أو الشهر."),
             [("Categories with your own icons and colours", "فئات بأيقوناتك وألوانك"),
              ("Export what you filtered as a PDF report", "صدّر ما اخترته تقريرًا بصيغة PDF")],
             [("warranties", "My warranties", "ضماناتي"),
              ("filter", "Filter warranties", "تصفية الضمانات")]),
        spot(("Insights", "الإحصائيات"),
             ("Your warranties, in numbers.", "ضماناتك بالأرقام."),
             ("Coverage, the rhythm of your purchases and forecasts of what expires next.",
              "التغطية، وإيقاع مشترياتك، وتوقعات ما ينتهي قريبًا."),
             [("How many warranties are still active", "كم ضمانًا ما زال ساريًا"),
              ("What expires in the coming months", "ما الذي ينتهي في الأشهر القادمة")],
             [("insights", "Insights: coverage", "الإحصائيات: التغطية")], flip=True),
        spot(("Your way", "على طريقتك"),
             ("Private, locked, and the way you like it.", "خاصة، ومقفلة، وكما تحب."),
             ("Choose how the warranty cards look, lock the app with your face or fingerprint, and keep an encrypted backup wherever you choose.",
              "اختر شكل بطاقات الضمان، واقفل التطبيق ببصمة الوجه أو الإصبع، واحتفظ بنسخة احتياطية مشفّرة حيث تختار."),
             [("12 card styles to choose from", "12 نمطًا للبطاقة تختار منها"),
              ("AES-256 encrypted backup with your own password", "نسخ احتياطي مشفّر AES-256 بكلمة مرورك"),
              ("18 languages, Hijri or Gregorian dates", "18 لغة، وتاريخ هجري أو ميلادي")],
             [("cardstyle", "Choose a card style", "اختر نمط البطاقة"),
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
    {p("Start free with up to 3 invoices, one product each. Lifetime Access unlocks unlimited invoices and products with a single payment — no subscription, ever.",
       "ابدأ مجانًا بما يصل إلى 3 فواتير، بمنتج واحد لكل فاتورة. و«الوصول مدى الحياة» يفتح فواتير ومنتجات غير محدودة بدفعة واحدة — بلا اشتراك أبدًا.")}
    <div class="stores" style="margin-top:18px">{stores}</div>
  </div>
  <ul class="dm-ticks dm-ticks-big">
    <li data-en>Free: 3 invoices to start</li><li data-ar>مجانًا: 3 فواتير للبداية</li>
    <li data-en>Lifetime Access: pay once</li><li data-ar>الوصول مدى الحياة: ادفع مرة واحدة</li>
    <li data-en>No subscription, no ads</li><li data-ar>بلا اشتراك وبلا إعلانات</li>
    <li data-en>Your invoices stay on your phone</li><li data-ar>فواتيرك تبقى على جوالك</li>
    <li data-en>18 languages</li><li data-ar>18 لغة</li>
  </ul>
</div></div></section>'''

    embed = app.get("youtube_embed")
    video = f'''<section><div class="container" style="max-width:860px">
  {h(2, "Watch it in action", "شاهده أثناء العمل", "center")}
  <div class="video-wrap" style="margin-top:22px">
    <iframe src="{embed}" title="Vault — Warranty Manager video" loading="lazy"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
  </div>
</div></section>''' if embed else ""

    gal = [("home", "Home", "الرئيسية"), ("warranties", "My warranties", "ضماناتي"), ("filter", "Filter", "التصفية"),
           ("detail", "Warranty details", "تفاصيل الضمان"), ("status", "Warranty status", "حالة الضمان"),
           ("insights", "Insights", "الإحصائيات"), ("settings", "Settings", "الإعدادات"),
           ("cardstyle", "Card style", "نمط البطاقة")]
    gallery = f'''<section class="section-soft"><div class="container">
  <div class="section-head center">
    <span class="kicker" data-en>Screens</span><span class="kicker" data-ar>الشاشات</span>
    {h(2, "Real screens from the app.", "شاشات حقيقية من التطبيق.")}
    {p("Tap any screen to see it large.", "اضغط أي شاشة لتراها مكبّرة.")}
  </div>
  <div class="dm-gallery">{"".join(f'<figure>{phone(n, en, ar)}<figcaption>{two(en, ar)}</figcaption></figure>' for n, en, ar in gal)}</div>
</div></section>'''

    faqs = [
        ("Is Vault free?", "هل خزنة الضمانات مجانية؟",
         "You can start free with up to 3 invoices, one product each. Lifetime Access is a single payment that unlocks everything — no subscription.",
         "تبدأ مجانًا بما يصل إلى 3 فواتير، بمنتج واحد لكل فاتورة. و«الوصول مدى الحياة» دفعة واحدة تفتح كل شيء — بلا اشتراك."),
        ("Where are my invoices kept?", "أين تُحفظ فواتيري؟",
         "On your phone. A backup is encrypted with your own password, and you choose where to keep it.",
         "على جوالك. والنسخة الاحتياطية مشفّرة بكلمة مرورك أنت، وأنت تختار أين تحفظها."),
        ("What does the invoice QR fill in?", "ماذا يعبّئ رمز QR في الفاتورة؟",
         "The store name and the purchase date. You add the products and their warranties.",
         "اسم المتجر وتاريخ الشراء. وأنت تضيف المنتجات وضماناتها."),
        ("What if I forget my backup password?", "ماذا لو نسيت كلمة مرور النسخة الاحتياطية؟",
         "It cannot be recovered — not even by us. That is what real encryption means, so keep it somewhere safe.",
         "لا يمكن استعادتها — ولا حتى من قِبلنا. هذا معنى التشفير الحقيقي، فاحفظها في مكان آمن."),
    ]
    faq_html = "".join(
        f'<details><summary>{two(qe, qa)}</summary><p data-en>{ae}</p><p data-ar>{aa}</p></details>'
        for qe, qa, ae, aa in faqs)
    links = (f'<div class="linkrow" style="margin-top:22px;justify-content:center">'
             f'<a href="/tutorials/vault/">{two("Tutorial", "الشرح")}</a>'
             f'<a href="/support/vault/">{two("Support", "الدعم")}</a>'
             f'<a href="/privacy/vault/">{two("Privacy policy", "سياسة الخصوصية")}</a></div>')
    faq = f'''<section><div class="container" style="max-width:820px">
  {h(2, "Questions", "أسئلة", "center")}
  <div class="faq" style="margin-top:28px">{faq_html}</div>
  {links}
</div></section>'''

    cta = f'''<section style="padding-top:0"><div class="container"><div class="cta-band">
  <div>
    {h(2, "Never lose a warranty again.", "لا تخسر ضمانًا مرة ثانية.")}
    {p("Download Vault and keep every invoice and warranty in one place.",
       "حمّل خزنة الضمانات واحفظ كل فاتورة وكل ضمان في مكان واحد.")}
  </div>
  <div class="stores">{stores}</div>
</div></div></section>'''

    lightbox = '''<div class="dm-lb" hidden><button type="button" class="dm-lb-x" aria-label="Close">✕</button>
  <button type="button" class="dm-lb-nav dm-lb-prev" aria-label="Previous">‹</button>
  <img alt=""><button type="button" class="dm-lb-nav dm-lb-next" aria-label="Next">›</button></div>'''

    js = docmatic_page.JS.replace("/assets/img/apps/docmatic/", f"{IMG}/")
    body = (crumbs([("Home", "الرئيسية", "/"), ("Apps", "التطبيقات", "/apps/"), (app["name_en"], app["name_ar"], None)])
            + hero + stats + story + journey + spots + catalogue + docmatic_page.suggest_card("vault", "Vault", "خزنة الضمانات") + price + video + gallery + faq + cta
            + lightbox + f"<script>{js}</script>")

    return render("/apps/vault/",
                  "Vault — Warranty Manager | Q Apps",
                  "خزنة الضمانات — إدارة الفواتير والضمانات | كيو آبز",
                  f"Vault keeps your invoices, products and warranties in one place, counts the days left and reminds you before a warranty ends — {N_MAIN} features in 18 languages.",
                  f"خزنة الضمانات تحفظ فواتيرك ومنتجاتك وضماناتك في مكان واحد، وتعدّ الأيام المتبقية، وتذكّرك قبل انتهاء الضمان — {N_MAIN} خاصية بـ 18 لغة.",
                  body, active="apps", head_extra=f"<style>{docmatic_page.CSS}</style>")
