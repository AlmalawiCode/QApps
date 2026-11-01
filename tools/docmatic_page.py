"""docmatic_page.py — the DocMatic app page (/apps/docmatic/).

Why a module of its own: this page is long and hand-tuned (story, journey,
spotlights, full feature catalogue, lightbox), and it is kept out of
build.py so edits to the rest of the site never collide with it. build.py
calls build_page(...) with its own helpers, so the header, footer, SEO tags
and language switch stay identical to every other page.

Every claim here matches what the app really does (checked against the
DocMatic code, 2026-11-01). Feature counts are computed from FEATURES, never
typed by hand. Screens are real app renders in both languages
(/assets/img/apps/docmatic/<name>_<lang>.webp); the hidden language's
images are display:none, so a browser loads only one set.
The owner's rule for order: the strong PDF features come first, the small
everyday tools last.
"""

IMG = "/assets/img/apps/docmatic"

# (icon, title_en, title_ar, [(sub_en, sub_ar), ...]) — the full catalogue.
FEATURES = [
    ("📸", "Photos to PDF", "الصور إلى PDF", [
        ("Turn any number of photos into one PDF", "حوّل أي عدد من الصور إلى ملف PDF واحد"),
        ("Drag to reorder pages", "رتّب الصفحات بالسحب"),
        ("Finds the paper's edges and straightens it", "يجد حواف الورقة ويعدّل ميلانها"),
        ("Smart crop, margins or your own hand crop", "قصّ ذكي، أو حسب الهوامش، أو بيدك"),
        ("Fix the tilt by a degree", "تصحيح الميلان بالدرجة"),
        ("Filters: original, document, photocopy, vivid", "مرشّحات: الأصل، مستند، نسخة ضوئية، ألوان زاهية"),
        ("Clean the edges and punch holes", "تنظيف الحواف وثقوب التخريم"),
        ("Pick photos from the gallery or the Inbox", "اختر الصور من المعرض أو من الوارد"),
    ]),
    ("📑", "Editor — pages", "المحرر — الصفحات", [
        ("All pages at a glance", "كل الصفحات في نظرة واحدة"),
        ("Select all, odd, even or a range", "حدّد الكل أو الفردية أو الزوجية أو نطاقًا"),
        ("Rotate, duplicate, delete", "تدوير، تكرار، حذف"),
        ("Move pages after any page", "انقل الصفحات بعد أي صفحة"),
        ("Reverse the order", "اعكس الترتيب"),
        ("Insert pages from other files or the camera", "أدرج صفحات من ملفات أخرى أو من الكاميرا"),
        ("Merge other files into it", "ادمج ملفات أخرى فيه"),
        ("Replace a page with one from another file", "استبدل صفحة بصفحة من ملف آخر"),
        ("Add a blank page before or after", "أضف صفحة فارغة قبل أو بعد"),
        ("Find and remove blank pages", "اكتشف الصفحات الفارغة واحذفها"),
        ("Extract pages as a new file", "استخرج صفحات كملف جديد"),
        ("Split the file", "قسّم الملف"),
        ("Pages to images", "الصفحات إلى صور"),
        ("Undo and redo every step", "تراجع وإعادة لكل خطوة"),
    ]),
    ("✍️", "Editor — add", "المحرر — الإضافة", [
        ("Fill in the form's fields", "املأ حقول النموذج"),
        ("Your signature, drawn once and kept", "توقيعك: ترسمه مرة ويبقى محفوظًا"),
        ("Initials", "الأحرف الأولى"),
        ("Text and date", "نص وتاريخ"),
        ("Tick and cross", "علامة صح وخطأ"),
        ("Stamps: Approved, Paid, Received, Copy…", "أختام: معتمد، مدفوع، مستلم، نسخة…"),
        ("Your own logo or stamp", "شعارك أو ختمك الخاص"),
        ("Pictures", "صور"),
        ("Page numbers in six positions", "ترقيم الصفحات في ست مواضع"),
        ("Header and footer on every page", "ترويسة وتذييل في كل صفحة"),
        ("Watermark", "علامة مائية"),
        ("Notes and bookmarks", "ملاحظات وعلامات مرجعية"),
    ]),
    ("🖊️", "Editor — draw", "المحرر — الرسم", [
        ("Pen and highlighter", "قلم وقلم تظليل"),
        ("Line, arrow, rectangle, circle", "خط، سهم، مستطيل، دائرة"),
        ("Highlight, underline or strike out text", "ظلّل النص أو ضع تحته خطًا أو اشطبه"),
        ("Eraser", "ممحاة"),
        ("Marks stay sharp on PDF pages", "العلامات تبقى حادة على صفحات PDF"),
    ]),
    ("🛡️", "Editor — protect", "المحرر — الحماية", [
        ("Hide with a black box that really erases", "أخفِ بمربع أسود يمحو ما تحته فعلًا"),
        ("Blur a face or a number", "موّه وجهًا أو رقمًا"),
        ("Find a word and hide it on every page", "ابحث عن كلمة وأخفِها في كل الصفحات"),
        ("Hidden data removed on every save", "البيانات المخفية تُزال مع كل حفظ"),
    ]),
    ("📐", "Editor — paper", "المحرر — الورق", [
        ("Crop and fit", "قص وملاءمة"),
        ("Enlarge the content to fill the paper", "كبّر المحتوى ليملأ الورقة"),
        ("Whole image or fill the page", "الصورة كاملة أو تملأ الصفحة"),
    ]),
    ("🗜️", "File size", "حجم الملف", [
        ("Original, standard or small", "الأصلي، أو متوسط، أو صغير"),
        ("See the size before you choose", "ترى الحجم قبل أن تختار"),
        ("Always reversible: the original is kept", "يمكن التراجع دائمًا: الأصل محفوظ"),
        ("Paper size: A4, A5, Letter or as is", "مقاس الورق: A4 أو A5 أو Letter أو كما هو"),
    ]),
    ("🔎", "Searchable text", "نص قابل للبحث", [
        ("Reads photographed pages on the phone", "يقرأ الصفحات المصوّرة على الجوال"),
        ("Arabic and English", "العربية والإنجليزية"),
        ("Search, highlight and copy the text", "ابحث وظلّل وانسخ النص"),
    ]),
    ("📂", "Open any PDF", "افتح أي PDF", [
        ("From the Inbox: what you shared to DocMatic", "من الوارد: ما شاركته إلى DocMatic"),
        ("From My files: what you saved before", "من ملفاتي: ما حفظته من قبل"),
        ("From outside the app: Files, iCloud, Google Drive", "من خارج التطبيق: الملفات وiCloud وGoogle Drive"),
        ("Opens password-protected PDFs", "يفتح ملفات PDF المحمية بكلمة مرور"),
    ]),
    ("📷", "Scan with the camera", "المسح بالكاميرا", [
        ("A scan door right on the home page", "باب المسح على الصفحة الرئيسية مباشرة"),
        ("Several pages in one go", "عدة صفحات في مرة واحدة"),
        ("Edges found and the page straightened for you", "يجد الحواف ويعدّل الصفحة تلقائيًا"),
        ("Camera asked only at the first scan", "لا يطلب الكاميرا إلا عند أول مسح"),
    ]),
    ("💬", "Share in from WhatsApp", "شارك من واتساب", [
        ("Share photos or a PDF from any chat", "شارك الصور أو ملف PDF من أي محادثة"),
        ("Everything lands in one Inbox", "كل شيء يصل إلى وارد واحد"),
        ("Works from any app that can share", "يعمل من أي تطبيق فيه «مشاركة»"),
        ("Nothing in the Inbox is deleted by itself", "لا يُحذف شيء من الوارد من تلقاء نفسه"),
    ]),
    ("🗂️", "Save like on a computer", "احفظ كما في الكمبيوتر", [
        ("Choose the folder before you save", "اختر المجلد قبل الحفظ"),
        ("Folders and folders inside folders", "مجلدات ومجلدات داخلها"),
        ("Move files between folders", "انقل الملفات بين المجلدات"),
        ("Recent files and search", "آخر الملفات والبحث"),
        ("Trash that keeps files for 30 days", "سلة تحفظ الملفات 30 يومًا"),
        ("A reminder when you leave without saving", "تنبيه إذا خرجت دون حفظ"),
    ]),
    ("📤", "Share and print", "المشاركة والطباعة", [
        ("Send by WhatsApp, email or Drive in one tap", "أرسل بواتساب أو البريد أو Drive بلمسة"),
        ("Print straight from the file", "اطبع من الملف مباشرة"),
        ("Share several files at once", "شارك عدة ملفات مرة واحدة"),
        ("What you see is exactly what you send", "ما تراه هو بالضبط ما ترسله"),
    ]),
    ("🔐", "Locked folders and app lock", "المجلدات المقفلة وقفل التطبيق", [
        ("Locked folders with real AES-256 encryption", "مجلدات مقفلة بتشفير حقيقي AES-256"),
        ("Not just a password: the files themselves are encrypted", "ليست مجرد كلمة مرور: الملفات نفسها مشفّرة"),
        ("Fingerprint or device PIN to open the app", "البصمة أو رمز الجهاز لفتح التطبيق"),
    ]),
    ("🔳", "QR codes and barcodes — read", "رموز QR والباركود — القراءة", [
        ("Scan with the camera", "امسح بالكاميرا"),
        ("Read from a picture or a file", "اقرأ من صورة أو ملف"),
        ("Read every code inside a PDF", "اقرأ كل الرموز داخل ملف PDF"),
        ("Understands links, Wi-Fi, contacts, products, tax invoices", "يفهم الروابط والواي فاي وجهات الاتصال والمنتجات والفواتير الضريبية"),
        ("History of every code you read", "سجل لكل رمز قرأته"),
    ]),
    ("✨", "QR codes and barcodes — create", "رموز QR والباركود — الإنشاء", [
        ("Link, text, Wi-Fi, contact, email", "رابط، نص، واي فاي، جهة اتصال، بريد"),
        ("Phone, message, location", "هاتف، رسالة، موقع"),
        ("13 barcode types: EAN, UPC, Code 128, Data Matrix, PDF417…", "13 نوع باركود: EAN وUPC وCode 128 وData Matrix وPDF417…"),
        ("Your own colours", "ألوانك الخاصة"),
        ("Checks the new code really scans", "يتحقق أن الرمز الجديد يُقرأ فعلًا"),
        ("Print at an exact size in millimetres", "اطبعه بمقاس دقيق بالمليمتر"),
        ("Label sheets from a list (CSV)", "ورقة ملصقات من قائمة (CSV)"),
        ("Put the code on a page in the editor", "ضع الرمز على صفحة في المحرر"),
    ]),
    ("🟢", "WhatsApp without saving the number", "واتساب دون حفظ الرقم", [
        ("Message any number in one tap", "راسل أي رقم بلمسة"),
        ("Country code chosen for you", "رمز الدولة مختار لك"),
        ("Ready messages you reuse", "رسائل جاهزة تعيد استخدامها"),
        ("A location inside the ready message", "موقع داخل الرسالة الجاهزة"),
    ]),
    ("🪪", "ID card", "بطاقة الهوية", [
        ("Both sides on one page", "الوجهان في صفحة واحدة"),
        ("ID, passport or licence", "هوية أو جواز أو رخصة"),
        ("Real size, ready to print", "بالمقاس الحقيقي جاهزة للطباعة"),
        ("Two copies per page", "نسختان في الصفحة"),
        ("Blur the photo before you send", "موّه الصورة الشخصية قبل الإرسال"),
    ]),
    ("🧑‍💼", "ID and passport photos", "صور الهوية والجواز", [
        ("Take it with the camera or choose a photo", "التقطها بالكاميرا أو اختر صورة"),
        ("Standard sizes or your own", "مقاسات معتمدة أو مقاسك"),
        ("Light, contrast and warmth", "الإضاءة والتباين والدفء"),
        ("White background on a plain wall", "خلفية بيضاء على جدار سادة"),
        ("As many as fit on your paper, with cut lines", "أكبر عدد يتسع في ورقتك، مع خطوط القص"),
        ("Print quality up to 600 dpi", "جودة طباعة حتى 600 نقطة"),
    ]),
    ("🖼️", "Compress and convert images", "ضغط الصور وتحويلها", [
        ("Make photos smaller", "صغّر حجم الصور"),
        ("HEIC to JPG", "من HEIC إلى JPG"),
        ("Resize", "غيّر المقاس"),
        ("From the gallery or from My files", "من المعرض أو من ملفاتي"),
    ]),
    ("📅", "Date converter", "محوّل التاريخ", [
        ("Hijri ⇄ Gregorian", "هجري ⇄ ميلادي"),
    ]),
    ("🏠", "Your home page", "صفحتك الرئيسية", [
        ("Three doors: Open PDF, Photos to PDF, Scan", "ثلاثة أبواب: افتح PDF، صور إلى PDF، امسح"),
        ("Pin up to nine shortcuts", "ثبّت حتى تسعة اختصارات"),
        ("Drag to reorder your shortcuts", "رتّب اختصاراتك بالسحب"),
        ("Arabic and English, light and dark", "عربي وإنجليزي، فاتح وداكن"),
    ]),
]

N_MAIN = len(FEATURES)
N_SUB = sum(len(f[3]) for f in FEATURES)


def build_page(render, h, p, crumbs, app):
    """Writes /apps/docmatic/ and returns its canonical URL."""

    def img(name, alt_en, alt_ar, cls="", eager=False):
        load = "eager" if eager else "lazy"
        c = f' class="{cls}"' if cls else ""
        return (f'<img{c} data-en src="{IMG}/{name}_en.webp" alt="{alt_en}" loading="{load}" width="620" height="1341">'
                f'<img{c} data-ar src="{IMG}/{name}_ar.webp" alt="{alt_ar}" loading="{load}" width="620" height="1341">')

    def phone(name, alt_en, alt_ar, cls="", eager=False):
        return (f'<button type="button" class="dm-phone {cls}" data-zoom="{name}" '
                f'aria-label="{alt_en}">{img(name, alt_en, alt_ar, eager=eager)}</button>')

    def two(en, ar, tag="span", cls=""):
        c = f' class="{cls}"' if cls else ""
        return f'<{tag}{c} data-en>{en}</{tag}><{tag}{c} data-ar>{ar}</{tag}>'

    # ---------------------------------------------------------------- hero
    hero = f'''<section class="dm-hero"><div class="container dm-hero-grid">
  <div class="dm-hero-copy">
    <div class="dm-brand"><img src="{app['icon']}" alt="DocMatic icon" width="64" height="64">
      <div><strong>DocMatic</strong>{two("PDF &amp; document tools", "أدوات PDF والمستندات", "small")}</div></div>
    <span class="dm-dev">{two("In development · coming soon to App Store &amp; Google Play", "قيد التطوير · قريبًا على App Store وGoogle Play")}</span>
    {h(1, "Every paper task. <em>One app on your phone.</em>", "كل ما تحتاجه لأوراقك، <em>في تطبيق واحد على جوالك.</em>")}
    {p("Photos from WhatsApp become a neat PDF, cropped and straightened for you. Then edit any PDF: arrange, merge, split, fill in and sign, make it smaller — "
       f"{N_MAIN} main features and more than {N_SUB - N_SUB % 10} tools, all on your phone.",
       "صور واتساب تصير ملف PDF مرتّبًا، مقصوصًا ومعدّل الميلان تلقائيًا. ثم حرّر أي ملف PDF: رتّب، وادمج، وقسّم، واملأ النماذج ووقّع، وصغّر الحجم — "
       f"{N_MAIN} خاصية رئيسية وأكثر من {N_SUB - N_SUB % 10} أداة، كلها على جوالك.", "lead")}
    <div class="btn-row">
      <a class="btn btn-accent" href="#features">{two("See all features", "شاهد كل الخصائص")}</a>
      <a class="btn btn-secondary" href="#story">{two("How it started", "كيف بدأت الفكرة")}</a>
    </div>
  </div>
  <div class="dm-hero-stage">
    {phone("home", "DocMatic home page", "الصفحة الرئيسية في DocMatic", "dm-p1", eager=True)}
    {phone("editor_tools", "The editor with a signature and hidden line", "المحرر مع توقيع وسطر مخفي", "dm-p2", eager=True)}
  </div>
</div></section>'''

    stats = f'''<section class="dm-stats-wrap"><div class="container"><div class="dm-stats">
  <div><b>{N_MAIN}</b>{two("main features", "خاصية رئيسية")}</div>
  <div><b>{N_SUB}</b>{two("tools inside them", "أداة داخلها")}</div>
  <div><b dir="ltr">1×</b>{two("small price, yours for life", "سعر زهيد، لك مدى الحياة")}</div>
  <div><b>0</b>{two("subscriptions · ads · accounts", "اشتراكات · إعلانات · حسابات")}</div>
</div></div></section>'''

    # ---------------------------------------------------------------- story
    story = f'''<section id="story" class="dm-story"><div class="container">
  <div class="section-head">
    <span class="kicker" data-en>The story</span><span class="kicker" data-ar>القصة</span>
    {h(2, "It started with school papers on WhatsApp.", "بدأت بأوراق المدرسة على واتساب.")}
  </div>
  <div class="dm-story-grid">
    <div class="dm-story-text">
      {p("My wife follows our son's schooling, and the school sends everything as photos: forms and homework. Every time, she forwarded them to me: <q>Can you make these a PDF?</q> And every time I sat at the computer, collected the photos, straightened them, put them in order and turned them into a file she could print or send back.",
         "زوجتي تتابع دراسة ابننا، والمدرسة ترسل كل شيء على شكل صور: نماذج وواجبات. وفي كل مرة كانت ترسلها لي: <q>ممكن تسويها PDF؟</q> وفي كل مرة أجلس أمام الكمبيوتر، أجمع الصور، وأعدّل ميلانها، وأرتّبها، وأحوّلها إلى ملف تطبعه أو تعيد إرساله.")}
      {p("One day the question came by itself: why not a simple app? You share the photos from WhatsApp, and it puts them in order as a PDF ready to print. No computer, no waiting for me.",
         "وفي أحد الأيام جاء السؤال وحده: لماذا لا يكون هناك تطبيق بسيط؟ تشارك الصور من واتساب، فيرتّبها لك ملف PDF جاهزًا للطباعة. بلا كمبيوتر، وبلا انتظار.")}
      {p("It began as a small idea: photos in, a PDF out. Then the ideas kept coming. The app should find the paper's edges, crop it and straighten it by itself, and let me reorder the pages with a finger. Then it should open any PDF and edit it: merge files and split them, extract, rotate and delete pages, fill in forms and sign them, write and highlight on the page, and make the file small enough for any website. Photographed pages should become searchable text, in Arabic and English.",
         "بدأت فكرة صغيرة: صور تدخل، وملف PDF يخرج. ثم توالت الأفكار. أن يجد التطبيق حواف الورقة ويقصّها ويعدّل ميلانها وحده، وأن أرتّب الصفحات بإصبعي. ثم أن يفتح أي ملف PDF ويحرّره: يدمج الملفات ويقسّمها، ويستخرج الصفحات ويدوّرها ويحذفها، ويملأ النماذج ويوقّعها، ويكتب على الصفحة ويظلّل، ويصغّر حجم الملف حتى يقبله أي موقع. وأن تصير الصفحات المصوّرة نصًا قابلًا للبحث، بالعربية والإنجليزية.")}
      {p(f"Then came the everyday jobs of the house: both sides of the ID on one page, a passport photo printed at home, QR codes and barcodes… One by one they were added, until the small idea became a complete app: {N_MAIN} main features and {N_SUB} tools inside them.",
         f"ثم جاءت حاجات البيت اليومية: وجها الهوية في صفحة واحدة، وصورة الجواز تطبعها في البيت، ورموز QR والباركود… أُضيفت واحدة بعد واحدة، حتى صارت الفكرة الصغيرة تطبيقًا متكاملًا: {N_MAIN} خاصية رئيسية و{N_SUB} أداة داخلها.")}
    </div>
    <ol class="dm-timeline">
      <li><span>🖼️</span><div>{two("Photos from the school", "صور من المدرسة", "b")}{two("Forms and homework arrive as WhatsApp photos.", "النماذج والواجبات تصل صورًا على واتساب.", "small")}</div></li>
      <li><span>💻</span><div>{two("A PDF by hand", "PDF باليد", "b")}{two("Every time: the computer, the order, the file.", "كل مرة: الكمبيوتر والترتيب والملف.", "small")}</div></li>
      <li><span>💡</span><div>{two("A simple app", "تطبيق بسيط", "b")}{two("Share the photos, get a PDF ready to print.", "شارك الصور، يصلك PDF جاهز للطباعة.", "small")}</div></li>
      <li><span>🚀</span><div>{two(f"{N_MAIN} features", f"{N_MAIN} خاصية", "b")}{two("A full PDF editor, and much more.", "محرر PDF كامل، وأكثر بكثير.", "small")}</div></li>
    </ol>
  </div>
</div></section>'''

    # ---------------------------------------------------------------- journey
    steps = [
        ("inbox", "1", "Share from WhatsApp", "شارك من واتساب",
         "Select the photos in the chat, tap Share and choose DocMatic. They land in the Inbox.",
         "حدّد الصور في المحادثة، اضغط «مشاركة» واختر DocMatic، فتصل إلى الوارد."),
        ("board", "2", "Arrange", "رتّب",
         "The pages are straightened and cropped for you. Drag to reorder, add or remove.",
         "تُعدَّل الصفحات وتُقصّ لك تلقائيًا. اسحب لترتيبها، أضف أو احذف."),
        ("save_location", "3", "Choose a folder, save", "اختر المجلد واحفظ",
         "Like on a computer: pick the folder first, then Save.",
         "كما في الكمبيوتر: اختر المجلد أولًا ثم احفظ."),
        ("file", "4", "Share or print", "شارك أو اطبع",
         "The file opens ready: Share, Print, Size, Editor.",
         "يُفتح الملف جاهزًا: مشاركة، طباعة، الحجم، المحرر."),
        ("size", "5", "Make it smaller", "صغّر الحجم",
         "Too big for the website? Choose a smaller size. The original is kept.",
         "أكبر مما يقبله الموقع؟ اختر حجمًا أصغر، والأصل محفوظ."),
    ]
    journey_items = "".join(
        f'''<li class="dm-step">{phone(n, en_t, ar_t)}<div class="dm-step-txt"><span class="dm-num">{k}</span>
        {two(en_t, ar_t, "h3")}{two(en_d, ar_d, "p")}</div></li>'''
        for n, k, en_t, ar_t, en_d, ar_d in steps)
    journey = f'''<section class="section-soft dm-journey"><div class="container">
  <div class="section-head center">
    <span class="kicker" data-en>How it works</span><span class="kicker" data-ar>كيف يعمل</span>
    {h(2, "From WhatsApp photos to a printed file, in five steps.", "من صور واتساب إلى ملف مطبوع، في خمس خطوات.")}
  </div>
  <ol class="dm-steps">{journey_items}</ol>
  {p("Swipe to see every step.", "اسحب لترى كل الخطوات.", "dm-swipe-hint")}
</div></section>'''

    # ---------------------------------------------------------------- spotlights
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

    # Order: the PDF power first (editor, pages, open), small tools last.
    spots = "".join([
        spot(("The editor", "المحرر"),
             ("A full PDF editor in your pocket.", "محرر PDF كامل في جيبك."),
             ("Fill in forms, write, highlight and stamp right on the page, crop and fit it to the paper, hide what is private. Every step can be undone, and nothing changes until you tap Save.",
              "املأ النماذج، واكتب، وظلّل، واختم على الصفحة نفسها، وقصّ الصفحة وناسبها مع الورق، وأخفِ ما هو خاص. كل خطوة يمكن التراجع عنها، ولا يتغيّر شيء حتى تضغط «حفظ»."),
             [("Five sections: Pages, Add, Draw, Protect, Paper", "خمسة أقسام: الصفحات، الإضافة، الرسم، الحماية، الورق"),
              ("Fill in the form's fields, then sign", "املأ حقول النموذج ثم وقّع"),
              ("A black box that really erases what is under it", "مربع أسود يمحو ما تحته فعلًا"),
              ("Marks stay sharp on PDF pages", "العلامات تبقى حادة على صفحات PDF")],
             [("editor_tools", "Editor: Add tools on a signed lease", "المحرر: أدوات الإضافة على عقد موقّع"),
              ("sign_hide", "A signed page with a hidden line", "صفحة موقّعة مع سطر مخفي")]),
        spot(("Pages", "الصفحات"),
             ("Every page, in your hands.", "كل صفحة، بين يديك."),
             ("See all the pages at once, pick odd, even or a range, then rotate, move, duplicate, extract or split.",
              "شاهد كل الصفحات مرة واحدة، حدّد الفردية أو الزوجية أو نطاقًا، ثم دوّر أو انقل أو كرّر أو استخرج أو قسّم."),
             [("Insert pages from other files or the camera", "أدرج صفحات من ملفات أخرى أو من الكاميرا"),
              ("Find and remove blank pages", "اكتشف الصفحات الفارغة واحذفها"),
              ("Pages to images in one tap", "الصفحات إلى صور بلمسة")],
             [("editor_pages", "All pages, two selected", "كل الصفحات، صفحتان محددتان")], flip=True),
        spot(("Open PDF", "افتح PDF"),
             ("Any PDF, from anywhere.", "أي ملف PDF، من أي مكان."),
             ("Three doors and nothing to learn: what was shared to you, what you saved, or a file from Drive, iCloud or the phone.",
              "ثلاثة أبواب ولا شيء تتعلمه: ما وصلك بالمشاركة، أو ما حفظته، أو ملف من Drive أو iCloud أو الجوال."),
             [("From the Inbox, My files or outside the app", "من الوارد أو ملفاتي أو من خارج التطبيق"),
              ("Password-protected PDFs open too", "حتى الملفات المحمية بكلمة مرور تُفتح"),
              ("A tip on every door: how to send a file from WhatsApp", "تلميح في كل باب: كيف ترسل ملفًا من واتساب")],
             [("open_pdf", "The Open PDF sheet", "قائمة افتح PDF")]),
        spot(("QR &amp; barcodes", "QR والباركود"),
             ("Read any code. Create your own.", "اقرأ أي رمز. وأنشئ رمزك."),
             ("Wi-Fi for your guests, your contact card, your shop's link, product labels from a list — and the app checks the new code really scans.",
              "واي فاي لضيوفك، بطاقة التواصل، رابط متجرك، ملصقات منتجات من قائمة — والتطبيق يتحقق أن الرمز الجديد يُقرأ فعلًا."),
             [("Link, text, Wi-Fi, contact, email, phone, message, location", "رابط، نص، واي فاي، جهة اتصال، بريد، هاتف، رسالة، موقع"),
              ("13 barcode types and label sheets", "13 نوع باركود وأوراق ملصقات"),
              ("Put the code on a page in the editor", "ضع الرمز على صفحة في المحرر")],
             [("code_contact", "Creating a QR code for a contact", "إنشاء رمز QR لجهة اتصال"),
              ("codes", "Codes and their history", "الرموز وسجلها")], flip=True),
        spot(("Everyday tools", "أدوات يومية"),
             ("The small jobs, done in seconds.", "المهام الصغيرة، في ثوانٍ."),
             ("Both sides of an ID on one page, a passport photo printed at home, WhatsApp without saving the number, smaller photos, Hijri and Gregorian dates.",
              "وجها الهوية في صفحة واحدة، وصورة جواز تطبعها في البيت، وواتساب دون حفظ الرقم، وصور أصغر، وتاريخ هجري وميلادي."),
             [("ID card at real size, photo blurred if you want", "بطاقة الهوية بمقاسها الحقيقي، مع تمويه الصورة إن شئت"),
              ("ID and passport photos, as many as fit on the paper", "صور الهوية والجواز، بأكبر عدد يتسع في الورقة"),
              ("Pin your favourite tools to the home page", "ثبّت أدواتك المفضلة على الصفحة الرئيسية")],
             [("id_card", "Both sides of an ID on one page", "وجها الهوية في صفحة واحدة"),
              ("studio", "ID and passport photos", "صور الهوية والجواز"),
              ("whatsapp", "WhatsApp without saving the number", "واتساب دون حفظ الرقم")]),
    ])

    # ---------------------------------------------------------------- catalogue
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

    # ---------------------------------------------------------------- price
    price = f'''<section class="dm-price"><div class="container"><div class="dm-price-card">
  <div>
    <span class="kicker" data-en>Price</span><span class="kicker" data-ar>السعر</span>
    {h(2, "One small price. Yours for life.", "سعر زهيد مرة واحدة، ولك مدى الحياة.")}
    {p("No monthly or yearly subscription, no ads, no account. Your files stay on your phone, and they leave it only when you share or print them.",
       "بلا اشتراك شهري أو سنوي، وبلا إعلانات، وبلا حساب. ملفاتك تبقى على جوالك، ولا تخرج منه إلا حين تشاركها أو تطبعها.")}
  </div>
  <ul class="dm-ticks dm-ticks-big">
    <li data-en>Pay once</li><li data-ar>ادفع مرة واحدة</li>
    <li data-en>No subscription, no ads</li><li data-ar>بلا اشتراك وبلا إعلانات</li>
    <li data-en>No account needed</li><li data-ar>لا حاجة لحساب</li>
    <li data-en>Works on the phone, even offline</li><li data-ar>يعمل على الجوال حتى دون إنترنت</li>
    <li data-en>Arabic and English</li><li data-ar>العربية والإنجليزية</li>
  </ul>
</div></div></section>'''

    # ---------------------------------------------------------------- gallery
    gal = [("home", "Home", "الرئيسية"), ("open_pdf", "Open PDF", "افتح PDF"), ("inbox", "Inbox", "الوارد"),
           ("board", "Photos to PDF", "الصور إلى PDF"), ("save_location", "Save location", "مكان الحفظ"),
           ("file", "The file", "الملف"), ("editor_tools", "Editor", "المحرر"), ("editor_pages", "Pages", "الصفحات"),
           ("size", "File size", "حجم الملف"), ("sign_hide", "Sign &amp; hide", "التوقيع والإخفاء"),
           ("code_contact", "Create a code", "إنشاء رمز"), ("codes", "QR &amp; barcodes", "QR والباركود"),
           ("id_card", "ID card", "بطاقة الهوية"), ("studio", "ID photo", "صورة رسمية"),
           ("whatsapp", "WhatsApp", "واتساب"), ("tools", "Tools", "الأدوات")]
    gallery = f'''<section class="section-soft"><div class="container">
  <div class="section-head center">
    <span class="kicker" data-en>Screens</span><span class="kicker" data-ar>الشاشات</span>
    {h(2, "Real screens from the app.", "شاشات حقيقية من التطبيق.")}
    {p("Tap any screen to see it large.", "اضغط أي شاشة لتراها مكبّرة.")}
  </div>
  <div class="dm-gallery">{"".join(f'<figure>{phone(n, en, ar)}<figcaption>{two(en, ar)}</figcaption></figure>' for n, en, ar in gal)}</div>
</div></section>'''

    faqs = [
        ("Is DocMatic available now?", "هل DocMatic متاح الآن؟",
         "It is in its final testing. It will be on the App Store and Google Play soon.",
         "هو في مرحلة الاختبار الأخيرة، وسيكون قريبًا على App Store وGoogle Play."),
        ("Do my files leave my phone?", "هل تخرج ملفاتي من جوالي؟",
         "No. Everything is done on the phone. A file leaves only when you share or print it.",
         "لا. كل شيء يتم على الجوال، ولا يخرج الملف إلا حين تشاركه أو تطبعه."),
        ("Do I need an account?", "هل أحتاج إلى حساب؟",
         "No account, no sign-in. Open the app and start.",
         "لا حساب ولا تسجيل دخول. افتح التطبيق وابدأ."),
        ("Is it a subscription?", "هل هو اشتراك؟",
         "No. One small price, and the app is yours for life.",
         "لا. سعر زهيد مرة واحدة، ويبقى التطبيق لك مدى الحياة."),
        ("Does it read Arabic?", "هل يقرأ العربية؟",
         "Yes. The whole app is in Arabic and English, and it reads Arabic and English text on photographed pages.",
         "نعم. التطبيق كله بالعربية والإنجليزية، ويقرأ النص العربي والإنجليزي في الصفحات المصوّرة."),
    ]
    faq_html = "".join(
        f'<details><summary>{two(qe, qa)}</summary><p data-en>{ae}</p><p data-ar>{aa}</p></details>'
        for qe, qa, ae, aa in faqs)
    faq = f'''<section><div class="container" style="max-width:820px">
  {h(2, "Questions", "أسئلة", "center")}
  <div class="faq" style="margin-top:28px">{faq_html}</div>
</div></section>'''

    cta = f'''<section style="padding-top:0"><div class="container"><div class="cta-band">
  <div>
    {h(2, "Coming soon to your phone.", "قريبًا على جوالك.")}
    {p("Have an idea that would make DocMatic better? Tell us — the best ones are added for everyone.",
       "عندك فكرة تجعل DocMatic أفضل؟ أخبرنا — وأفضل الأفكار تُضاف للجميع.")}
  </div>
  <a class="btn btn-accent" href="/suggest/">{two("Suggest a feature", "اقترح ميزة")}</a>
</div></div></section>'''

    lightbox = '''<div class="dm-lb" hidden><button type="button" class="dm-lb-x" aria-label="Close">✕</button>
  <button type="button" class="dm-lb-nav dm-lb-prev" aria-label="Previous">‹</button>
  <img alt=""><button type="button" class="dm-lb-nav dm-lb-next" aria-label="Next">›</button></div>'''

    body = (crumbs([("Home", "الرئيسية", "/"), ("Apps", "التطبيقات", "/apps/"), ("DocMatic", "DocMatic", None)])
            + hero + stats + story + journey + spots + catalogue + price + gallery + faq + cta
            + lightbox + f"<script>{JS}</script>")

    return render("/apps/docmatic/",
                  "DocMatic — Photos to PDF, PDF editor, QR codes & ID tools | Q Apps",
                  "DocMatic — الصور إلى PDF، محرر PDF، رموز QR وأدوات الهوية | كيو آبز",
                  f"DocMatic turns WhatsApp photos into a neat PDF ready to print, edits and signs PDFs, hides private details, creates QR codes and prints ID photos — {N_MAIN} features, all on your phone.",
                  f"DocMatic يحوّل صور واتساب إلى ملف PDF مرتّب جاهز للطباعة، ويحرر ملفات PDF ويوقّعها، ويخفي البيانات الخاصة، وينشئ رموز QR ويطبع الصور الرسمية — {N_MAIN} خاصية على جوالك.",
                  body, active="apps", og_image=f"{IMG}/og.png", head_extra=f"<style>{CSS}</style>")


# Page-only styles: kept here so the shared stylesheet is untouched.
CSS = """
.dm-hero{padding:56px 0 40px;overflow:hidden}
.dm-hero-grid{display:grid;grid-template-columns:1.05fr .95fr;gap:40px;align-items:center}
.dm-hero-copy{display:grid;gap:18px}
.dm-hero h1{font-size:clamp(36px,5.2vw,64px)}
.dm-hero h1 em{font-style:normal;color:var(--accent)}
.dm-brand{display:flex;gap:14px;align-items:center}
.dm-brand img{border-radius:16px;box-shadow:var(--shadow-md)}
.dm-brand strong{display:block;font-family:var(--f-display);font-size:24px;color:var(--ink)}
.dm-brand small{color:var(--muted);font-size:14px}
.dm-dev{justify-self:start;font-size:13.5px;font-weight:700;color:var(--mint);background:var(--mint-soft);padding:6px 12px;border-radius:999px}
.dm-hero-stage{position:relative;height:620px}
.dm-phone{all:unset;cursor:zoom-in;display:block;border-radius:30px;border:7px solid #0F1B2D;background:#0F1B2D;overflow:hidden;box-shadow:var(--shadow-lg);transition:transform .25s}
.dm-phone:hover{transform:translateY(-4px)}
.dm-phone:focus-visible{outline:3px solid var(--accent);outline-offset:4px}
.dm-phone img{width:100%;height:auto;display:block}
.dm-hero-stage .dm-phone{position:absolute;width:250px}
.dm-p1{inset-inline-start:6%;top:0;transform:rotate(-4deg)}
.dm-p2{inset-inline-end:4%;top:70px;transform:rotate(4deg)}
.dm-p1:hover{transform:rotate(-4deg) translateY(-4px)}.dm-p2:hover{transform:rotate(4deg) translateY(-4px)}
.dm-stats-wrap{padding:0 0 24px}
.dm-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.dm-stats div{background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-sm);padding:18px;display:grid;gap:4px;text-align:center}
.dm-stats b{font-family:var(--f-display);font-size:clamp(30px,4vw,44px);color:var(--accent);line-height:1}
.dm-stats span{color:var(--muted);font-weight:600;font-size:14.5px}
.dm-story-grid{display:grid;grid-template-columns:1.3fr .7fr;gap:44px;align-items:start}
.dm-story-text{display:grid;gap:18px}
.dm-story-text p{font-size:18px;line-height:1.85;color:var(--ink)}
.dm-story-text q{color:var(--accent);font-weight:700}
.dm-timeline{list-style:none;margin:0;padding:0;display:grid;gap:14px;position:relative}
.dm-timeline li{display:flex;gap:14px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius-sm);padding:14px 16px}
.dm-timeline li>span{font-size:26px;line-height:1}
.dm-timeline b{display:block;color:var(--ink)}
.dm-timeline small{color:var(--muted);font-size:14.5px}
.dm-steps{list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(5,1fr);gap:18px}
.dm-step{display:grid;gap:14px;align-content:start}
.dm-step-txt{display:grid;gap:6px}
.dm-step h3{font-size:19px}
.dm-step p{font-size:15px}
.dm-num{width:32px;height:32px;border-radius:50%;background:var(--accent);color:var(--accent-ink);display:grid;place-items:center;font-weight:800}
.dm-swipe-hint{display:none;text-align:center;font-size:14px;margin-top:10px}
.dm-spot{padding:72px 0}
.dm-spot-grid{display:grid;grid-template-columns:1fr 1fr;gap:48px;align-items:center}
.dm-flip .dm-spot-copy{order:2}
.dm-spot-copy{display:grid;gap:14px}
.dm-spot h2{font-size:clamp(28px,3.6vw,44px)}
.dm-ticks{list-style:none;margin:6px 0 0;padding:0;display:grid;gap:10px}
.dm-ticks li{position:relative;padding-inline-start:30px;color:var(--ink);font-weight:600}
.dm-ticks li::before{content:"✓";position:absolute;inset-inline-start:0;top:0;width:22px;height:22px;border-radius:50%;background:var(--mint-soft);color:var(--mint);display:grid;place-items:center;font-size:13px;font-weight:800}
.dm-spot-shots{display:flex;gap:18px;justify-content:center;align-items:flex-start}
.dm-spot-shots .dm-phone{width:min(260px,46%)}
.dm-n3 .dm-phone{width:min(210px,31%)}
.dm-n2 .dm-phone:nth-child(2),.dm-n3 .dm-phone:nth-child(2){margin-top:44px}
.dm-feats{columns:3;column-gap:14px}
.dm-feat{break-inside:avoid;margin:0 0 14px;background:var(--bg);border:1px solid var(--line);border-radius:var(--radius-sm);padding:0;transition:box-shadow .2s}
.dm-feat[open]{box-shadow:var(--shadow-md);background:var(--surface)}
.dm-feat summary{list-style:none;cursor:pointer;display:flex;gap:12px;align-items:center;padding:16px 18px}
.dm-feat summary::-webkit-details-marker{display:none}
.dm-ico{font-size:24px;line-height:1}
.dm-feat-t{flex:1;font-weight:750;color:var(--ink)}
.dm-count{min-width:30px;height:30px;padding:0 8px;border-radius:999px;background:var(--accent-soft);color:var(--accent);display:grid;place-items:center;font-weight:800;font-size:14px}
.dm-feat ul{margin:0;padding:0 20px 16px;padding-inline-start:44px;display:grid;gap:6px;color:var(--muted);font-size:15.5px}
.dm-openall{margin-top:6px}
.dm-price-card{display:grid;grid-template-columns:1.2fr .8fr;gap:36px;align-items:center;background:var(--night);border-radius:var(--radius);padding:44px;color:var(--on-night)}
.dm-price-card h2{color:#fff;font-size:clamp(28px,3.6vw,44px);margin:8px 0 12px}
.dm-price-card p{color:var(--on-night-muted);font-size:17px}
.dm-price-card .dm-ticks li{color:#fff}
.dm-gallery{display:grid;grid-template-columns:repeat(8,1fr);gap:16px}
.dm-gallery figure{margin:0;display:grid;gap:8px}
.dm-gallery .dm-phone{border-width:5px;border-radius:20px;box-shadow:var(--shadow-md)}
.dm-gallery figcaption{text-align:center;font-size:13.5px;font-weight:650;color:var(--muted)}
.dm-lb{position:fixed;inset:0;z-index:100;background:rgba(6,12,22,.92);display:flex;align-items:center;justify-content:center;padding:20px}
.dm-lb[hidden]{display:none}
.dm-lb img{max-height:92vh;max-width:min(94vw,520px);width:auto;border-radius:22px;box-shadow:0 30px 80px rgba(0,0,0,.6)}
.dm-lb-x{position:absolute;top:14px;inset-inline-end:14px;width:46px;height:46px;border-radius:50%;border:0;background:#fff;color:#0F1B2D;font-size:22px;cursor:pointer}
.dm-lb-nav{position:absolute;top:50%;transform:translateY(-50%);width:52px;height:52px;border-radius:50%;border:0;background:rgba(255,255,255,.15);color:#fff;font-size:34px;cursor:pointer}
.dm-lb-prev{left:14px}.dm-lb-next{right:14px}
@media (max-width:1100px){
  .dm-gallery{grid-template-columns:repeat(4,1fr)}
  .dm-feats{columns:2}
}
@media (max-width:900px){
  .dm-hero-grid,.dm-story-grid,.dm-spot-grid,.dm-price-card{grid-template-columns:1fr}
  .dm-hero{padding-top:28px}
  .dm-hero-stage{height:470px;max-width:440px;width:100%;margin-inline:auto}
  .dm-hero-stage .dm-phone{width:200px}
  .dm-flip .dm-spot-copy{order:0}
  .dm-spot{padding:52px 0}
  .dm-stats{grid-template-columns:repeat(2,1fr)}
  .dm-steps{display:flex;overflow-x:auto;scroll-snap-type:x mandatory;gap:16px;padding-bottom:10px;margin-inline:-16px;padding-inline:16px;scrollbar-width:none}
  .dm-steps::-webkit-scrollbar{display:none}
  .dm-step{flex:0 0 68%;scroll-snap-align:center}
  .dm-swipe-hint{display:block}
  .dm-price-card{padding:30px 22px}
}
@media (max-width:620px){
  .dm-feats{columns:1}
  .dm-gallery{grid-template-columns:repeat(2,1fr)}
  .dm-hero-stage{height:400px}
  .dm-hero-stage .dm-phone{width:170px}
  .dm-spot-shots .dm-phone{width:min(220px,47%)}
  .dm-n3{justify-content:flex-start;overflow-x:auto;scroll-snap-type:x mandatory;margin-inline:-16px;padding:4px 16px 12px;scrollbar-width:none}
  .dm-n3::-webkit-scrollbar{display:none}
  .dm-n3 .dm-phone{flex:0 0 58%;width:auto;scroll-snap-align:center}
  .dm-n3 .dm-phone:nth-child(2){margin-top:0}
  .dm-story-text p{font-size:17px}
}
"""

# Lightbox over every phone (current language's picture, arrows / swipe /
# Esc), and «Open all» for the catalogue (open by default on a computer).
JS = """
(function(){
  var lb=document.querySelector('.dm-lb'),im=lb.querySelector('img'),list=[],i=0;
  function lang(){return document.documentElement.getAttribute('data-lang')==='ar'?'ar':'en';}
  function names(){var s=[];document.querySelectorAll('.dm-gallery [data-zoom]').forEach(function(b){s.push(b.dataset.zoom);});return s;}
  function show(){im.src='/assets/img/apps/docmatic/'+list[i]+'_'+lang()+'.webp';}
  function open(n){list=names();i=Math.max(0,list.indexOf(n));show();lb.hidden=false;document.body.style.overflow='hidden';}
  function close(){lb.hidden=true;document.body.style.overflow='';}
  function step(d){i=(i+d+list.length)%list.length;show();}
  document.querySelectorAll('[data-zoom]').forEach(function(b){b.addEventListener('click',function(){open(b.dataset.zoom);});});
  lb.querySelector('.dm-lb-x').addEventListener('click',close);
  lb.querySelector('.dm-lb-prev').addEventListener('click',function(e){e.stopPropagation();step(-1);});
  lb.querySelector('.dm-lb-next').addEventListener('click',function(e){e.stopPropagation();step(1);});
  lb.addEventListener('click',function(e){if(e.target===lb)close();});
  document.addEventListener('keydown',function(e){if(lb.hidden)return;if(e.key==='Escape')close();if(e.key==='ArrowRight')step(1);if(e.key==='ArrowLeft')step(-1);});
  var x0=null;lb.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;},{passive:true});
  lb.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>40)step(dx<0?1:-1);x0=null;});
  var btn=document.querySelector('.dm-openall');
  if(btn)btn.addEventListener('click',function(){var on=btn.getAttribute('aria-pressed')!=='true';
    document.querySelectorAll('.dm-feat').forEach(function(d){d.open=on;});btn.setAttribute('aria-pressed',on);
    btn.querySelectorAll('span').forEach(function(s){s.textContent=on?(s.hasAttribute('data-ar')?'أغلق الكل':'Close all'):(s.hasAttribute('data-ar')?'افتح الكل':'Open all');});});
  if(window.matchMedia('(min-width:901px)').matches&&btn)btn.click();
})();
"""
