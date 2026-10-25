# Dr Vasileva – Website Project Notes

## 1. The plan in one sentence

One website, two domains: **drvasileva.bg** shows the site in Bulgarian, **drvasileva.co.uk** shows it in English. Same design, same photos, same code.

---

## 2. Domains – the easy version

### How it works

```
drvasileva.bg     ─┐
                   ├──►  one website  ──►  .bg     = Bulgarian, prices in EUR
drvasileva.co.uk  ─┘                       .co.uk  = English,   prices in GBP
```

- We build the site **once**. Every text exists in two languages.
- Both domains point to the **same hosting**.
- The site looks at which domain the visitor typed and picks the language.
- A **BG / EN** button in the menu takes you to the same page on the other domain.
- Change a photo or her bio once → both sites update.

### Steps

1. **Buy the domains**
   - `drvasileva.co.uk` from any registrar (Cloudflare, Namecheap, GoDaddy…).
   - `drvasileva.bg` from Register.bg or a Bulgarian registrar.
2. **Pick a host.** Vercel, Netlify or Cloudflare Pages are free for a site like this, and HTTPS (the padlock) is included.
3. **Connect both domains** to the same project on the host (the host shows you the DNS records to copy into the registrar).
4. **Build the site** with two languages (e.g. Astro or Next.js, which both support "language by domain").
5. **Tell Google** (see below).

### What differs between the two sites

| | drvasileva.bg | drvasileva.co.uk |
|---|---|---|
| Language | Bulgarian | English |
| Currency | EUR (€) – Bulgaria uses the euro since 1 Jan 2026 | GBP (£) |
| Time zone for sessions | Bulgaria (EET) | UK (GMT/BST) – 2 hours behind |
| Appointments offered | **Online only** | **Online and in person** |
| Phone number | +44 7999 334778 | 07999 334778 |
| Email | contact@drvasileva.bg | contact@drvasileva.co.uk |
| Chat button | **Viber** | **WhatsApp** |
| Socials | Facebook | Facebook |
| Payment | Bank transfer, Revolut | Bank transfer, Revolut |
| Address | Not shown | Not shown |
| Opening hours | Not shown (she's flexible) | Not shown (she's flexible) |
| Legal pages | Privacy policy under EU GDPR | Privacy policy under UK GDPR |

### Contact buttons

She has one phone number (UK), so both sites use it. Only the chat app changes:

- **drvasileva.bg → Viber** (what most people in Bulgaria use). Link: `viber://chat?number=%2B447999334778`
- **drvasileva.co.uk → WhatsApp** (what most people in the UK use). Link: `https://wa.me/447999334778`
- **Phone:** shown as `+44 7999 334778` on .bg (so it works when dialled from Bulgaria) and `07999 334778` on .co.uk. Both link to `tel:+447999334778`.
- **Email:** `contact@drvasileva.bg` on .bg, `contact@drvasileva.co.uk` on .co.uk. Both can forward into one inbox she already uses.
- **Facebook** is her only social account, so it's linked in the footer of both sites: <https://www.facebook.com/share/1Bh2hqG1Ac/>. This is a share link. Before launch, open it and copy the page's real address (`facebook.com/<her-page>`), which is more reliable.
- **No address on either site.** For in-person sessions in the UK, she gives the details when people message or call her.

> The Viber link only opens if the visitor has Viber installed (normal in Bulgaria). Show the number as text next to the button as a fallback.

### Google search – do's and don'ts

- **Do** add both domains to **Google Search Console**.
- **Do** add `hreflang` tags (one line in the page code). They tell Google "these two pages are the same page in two languages", so it shows the right one in each country and doesn't see them as duplicates.
- **Do** let the domains do the targeting: Google automatically treats `.bg` as Bulgaria and `.co.uk` as the UK.
- **Don't** auto-redirect people by their location. It confuses Google and annoys people (e.g. a Bulgarian living in London). Use the BG / EN button instead.

---

## 3. About Dr Vasileva

Source: her CV, plus her list of BG BEN columns.

### Name

- **EN:** Dr Mirena Vasileva, PhD (full: Dr Mirena Koleva Vasileva)
- **BG:** д-р Мирена Василева (full: д-р Мирена Колева Василева)

### Photo

`images/dr-vasileva.jpg` (1242 × 1242, square). It's a warm, friendly selfie, which suits About and Home. For the big Home banner, a crop that keeps the focus on her face (with less of the wall behind) will look cleaner. A professional portrait can replace it later.

### Experience

- **21 years in psychology (since 2005).** The site should calculate this from 2005 automatically, so it never goes out of date.
- **Living and working in London since 2016.**

| When | Role | Where |
|---|---|---|
| 2007 – now | Psychotherapist in **private practice** | Bulgaria → UK |
| 2016 – now | Psychologist | **Doctors 4 You** clinic, London |
| 2018 – now | Psychologist | **Medi-Park Clinic**, London |
| 2018 – 2019 | Psychologist | BG Medical Clinic, London |
| 2015 – 2017 | Assistant teacher, children with special educational needs | Bulgarian School **"Rodna Rech"**, London |
| 2015 – 2018 | **Chief Assistant Professor** (lecturer), Experimental & Pedagogical Psychology | **Burgas Free University** |
| 2013 – 2016 | PhD Consultant – Psychotherapist | Viva Clinic, Sunny Beach |
| 2007 – 2015 | Psychologist | "St. Stiliyan Paflagoniyski" home for children with intellectual disabilities, Kosharitsa (Nessebar) |

### Education

| Years | Degree | University |
|---|---|---|
| 2009 – 2013 | **PhD – Doctor in Pedagogical and Developmental Psychology**. Thesis: *"Family environment and experiencing stress in adolescence"* | Varna Free University "Chernorizets Hrabar" |
| 2005 – 2006 | **MA Psychology**, specialisation in Psychology and Developmental Psychopathology. Thesis: *"Stress effects on the family environment and the upbringing of children"* | Varna Free University |
| 2000 – 2005 | **BA Psychology**. Thesis: *"Anxiety and aggression in adolescents"* | Varna Free University |

### Qualifications & memberships

- **British Psychological Society**, MBPsS (membership no. 464684)
- **Psychological Society of the Republic of Bulgaria**, member
- **Diploma in Cognitive Behavioural Therapy (CBT)**
- **Diploma in Special Educational Needs & Disability (SEND)**
- Certificate in CBT and Counselling
- CBT courses, Bulgarian Association of Cognitive-Behavioural Psychotherapy (Sofia, 2006–2007)
- "Therapeutic Crisis Intervention" training (Burgas Free University, 2006–2007)
- "Child and its Symptoms" programme (Doctors of the World / CIEN Bordeaux, with the French Cultural Institute)
- Safeguarding Children Level 3, Safeguarding Vulnerable Adults, NSPCC Child Protection, Child Mental Health
- Enhanced DBS check (2016)

> The CV has many more training certificates (fire safety, infection control, CPR…). They're normal for clinic work but not worth showing to clients. We list only the psychology-related ones above.

### Awards 🏆

- **Gold Ring of Varna Free University "Chernorizets Hrabar"** for graduating with honours, Master's in Psychology and Psychopathology of Development (Class of 2006)
- **First Prize, "Best Diploma Thesis" competition** for her Master's thesis (2005–2006 academic year)

### Charity work

- Organised **charity campaigns for children with intellectual disabilities and children without parental care**, and volunteers to help care for them.

### What she works with (from the CV)

- **Adults:** anxiety, depression, panic disorder, stress, crisis support
- **Couples & families:** CBT couples therapy, family therapy, marriage and family programmes, the role of emotions in relationships
- **Children & teens:** psychological consultations, behavioural difficulties, parent–child relationships, adolescence
- **Children with special educational needs:**
  - autism spectrum
  - ADHD / ADD
  - dyslexia, dyspraxia, handwriting difficulties
  - learning disabilities and developmental delays
- **Psychological assessments and written psychological reports**
- **Group sessions** (group therapy)
- **Group training for organisations and schools:** professional stress, effective teamwork, relationships (adult–child, child–child, adult–adult, employer–employee)
- **Method:** mainly **CBT (cognitive behavioural therapy)**, plus art-therapy methods in crisis work

### Languages

Bulgarian (native), English (fluent), Russian (good), German (basic).
**On the site:** sessions in **Bulgarian and English** only (no Russian sessions).

### Media & public work

- **"School of Psychology" ("Училище по психология")**, her regular column in BG BEN, the UK newspaper for Bulgarians (2023 – now). Full list in section 6.
- Interview, *"Self murderers are people who want to be noticed"*, newspaper **"Doctor"**, issue 15 (2015)
- Interview, *"Covid-19 and Panic Attacks"*, **BG Radio** (2019)
- Lectures at Burgas Free University: Experimental Psychology, Pedagogical Psychology, "Art therapy methods in crisis intervention", "Family environment and experience of stress in adolescence"
- 6 scientific and applied contributions from her PhD, recognised at the **Bulgarian Academy of Sciences**

### Title (decided)

**Dr Mirena Vasileva, PhD – Psychologist & CBT Psychotherapist · MBPsS**
(BG: **д-р Мирена Василева – психолог и когнитивно-поведенчески психотерапевт**)

Use this title everywhere: header, About page, page titles, Facebook.

- ✅ Show: **Dr**, **PhD**, **Psychologist**, **CBT Psychotherapist**, **MBPsS** (BPS membership no. 464684)
- ❌ Never show: "Counselling Psychologist", "CPsychol", "EuroPsy". She doesn't hold these, and "Counselling Psychologist" is a protected title in the UK.
- Write "Dr … PhD" together so it's clear it's a doctorate, not a medical degree.

### Info we still need from her

- [x] Full name
- [x] Photo
- [x] Qualifications, university, PhD
- [x] Awards
- [x] Specialisms
- [x] Phone, email, Facebook
- [x] Payment methods
- [x] Languages
- [ ] **Prices and session length**: decided **after the website is finished**. The Fees page is built with placeholders until then.
- [x] Cancellation policy: **24 hours' notice**
- [x] Titles: use the decided title above
- [x] Russian-language sessions: **no**
- [x] "Organisations & schools" page: **yes**
- [x] Group sessions: **yes**, gets its own page
- [x] Columns: **translated into English** for .co.uk
- [ ] **Full list of scientific papers** (she has more than the CV shows; coming soon)
- [x] BG BEN: she can republish her columns in full ✅
- [ ] A short "about me" paragraph in her own words (we can draft one from the CV for her to approve)

---

## 4. Reference site: The Chelsea Psychology Clinic

Analysed: <https://www.thechelseapsychologyclinic.com/> (October 2026)

### What it is

A big private clinic in London: 5 locations (Chelsea, Harley Street, Knightsbridge, Mayfair, Kensington), 100+ clinicians, therapy plus psychiatry. Her site will be **one person, not a clinic**, so we copy the *structure and the good ideas*, not the size.

### Their menu

| Menu | What's inside |
|---|---|
| **Adults** | Private therapy, couples, family, group, psychiatry, ADHD/autism assessments, nutrition, sleep, retreats |
| **Child & Adolescent** | Child therapy, child psychiatry, assessments, **educational psychology assessments**, **schools & education** |
| **Therapies** | One page per method: CBT, ACT, CFT, DBT, EMDR, schema therapy, online therapy… (15 pages) |
| **Issues** | One page per problem: anxiety, depression, ADHD, autism, dyslexia, bereavement, stress, self-harm… (30 pages) |
| **Psychiatry / Online / Corporate** | Separate sections |
| **Team** | One profile page per clinician, **with the languages they speak** |
| **Membership** | Paid membership plan |

**Footer:** Locations, Our Fees, Careers, **Crisis Information**, Sitemap, Privacy Policy, Terms & Conditions, Instagram.

### Homepage, top to bottom

1. Headline: "Private Psychiatry & Therapy Clinic in London"
2. Three promises: *leading specialists, tailored therapy, best outcomes*
3. Service tiles (Adults / Children)
4. Online therapy block
5. Membership plan
6. Team carousel
7. Featured resources: blog posts and short videos ("Is therapy confidential?", "How many sessions will I need?")
8. **Press**: articles they were quoted in
9. "Featured in…" media logos, plus health-insurance logos
10. "Start your journey today" button
11. Locations with "Get directions"
12. Phone number and opening hours

### How their pages are built

- **Issue page** (e.g. Anxiety): what it is → types → how it's treated → **FAQ** → related videos → "Start your journey" button.
- **Team profile**: photo, name, title, bio, languages, contact form.
- **Fees page**: a clear table. Each line has the service, the price (£200–£300 for a 50-min session, £250–£350 for an assessment) and the length in minutes. It also mentions health insurance.
- **Contact page**: a short form (name, email, phone, message, **best time to call** with Pre-9am / 9–12 / 12–5 / 5–8, privacy consent). It promises a callback within 24 hours and shows the phone number, opening hours and addresses.

### What we copy ✅

- Clear menus split into **who I help** and **what I help with**
- One page per issue, each ending in an FAQ and a contact button. These pages are what bring people in from Google.
- An **open fees table**. People trust prices they can see.
- **Short FAQ videos** (1–2 min) – easy to film on a phone
- **Press / "As featured in"**. Her BG BEN column fits here.
- A **crisis information** page
- A "get in touch" button on every page (for us: call / Viber / WhatsApp, not a booking form)

### What we skip ❌

- Psychiatry, nutrition, sleep, retreats, membership, careers, corporate, multiple locations. These need a whole clinic.
- 30 issue pages and 15 therapy pages. **6–8 issue pages that match her real specialisms** is plenty to start.
- Health-insurance logos, unless she's registered with insurers.

### Where we can beat them

- **Two languages, two countries.** Chelsea only shows a "Languages: English, Greek" tag on profiles. Her whole site is native Bulgarian *and* English, which is a real selling point for Bulgarians in the UK.
- **Personal.** One face, her own voice, her own story. A solo practitioner can feel warmer than a big clinic.
- **Her niche.** Her background is educational and developmental psychology, with long hands-on work with children with special needs, couples and families. Parents, teens, SEN and Bulgarian families abroad are exactly where Chelsea's offer is thinnest.

---

## 5. Our pages (sitemap)

Every page exists in both languages. URLs are in English on `.co.uk` and in Bulgarian (Latin letters) on `.bg`.

### Main menu

| # | Page | drvasileva.co.uk | drvasileva.bg | What's on it |
|---|---|---|---|---|
| 1 | **Home** | `/` | `/` | Photo, one-line promise, who I help, online & in person (.co.uk) / online only (.bg), "Featured in", call + chat buttons |
| 2 | **About me** | `/about` | `/za-men` | Photo, her story, 21 years since 2005, PhD, education, experience timeline, **awards**, BPS membership, CBT, languages, charity work |
| 3 | **Who I help** | `/who-i-help` | `/s-kogo-rabotya` | Overview page, linking to 3a–3f |
| 3a | – Adults | `/who-i-help/adults` | `/s-kogo-rabotya/vazrastni` | Individual CBT therapy: anxiety, depression, panic, stress |
| 3b | – Couples & families | `/who-i-help/couples-families` | `/s-kogo-rabotya/dvoyki-i-semeystva` | CBT couples therapy, family therapy |
| 3c | – Children & teens | `/who-i-help/children-teens` | `/s-kogo-rabotya/deca-i-tiyneydzhari` | Consultations for children and teens, support for parents |
| 3d | – Special educational needs | `/who-i-help/special-educational-needs` | `/s-kogo-rabotya/specialni-obrazovatelni-potrebnosti` | Autism, ADHD, dyslexia, dyspraxia, learning difficulties, assessments and reports |
| 3e | – Organisations & schools | `/who-i-help/organisations` | `/s-kogo-rabotya/organizacii` | Group training: professional stress, teamwork, relationships |
| 3f | – Group sessions | `/who-i-help/group-sessions` | `/s-kogo-rabotya/grupovi-sesii` | What group sessions are, who they're for, how they work, online / in person |
| 4 | **What I help with** | `/issues` | `/problemi` | Grid of issue pages (see list below) |
| 5 | **Fees** | `/fees` | `/ceni` | **.co.uk:** GBP, online + in person. **.bg:** EUR, online only. Session length, assessments & reports, how online sessions work, time zones UK ↔ BG, **payment by bank transfer or Revolut**, **cancellation: 24 hours' notice**. *Prices added after the site is finished.* |
| 6 | **Articles & publications** | `/articles` | `/statii` | Her "School of Psychology" columns (all of them, see section 6), plus her scientific publications |
| 7 | **Contact** | `/contact` | `/kontakti` | **No form, no booking.** Big buttons: call **07999 334778**, chat (**Viber** on .bg, **WhatsApp** on .co.uk), email (**contact@drvasileva.bg / .co.uk**), Facebook. **No hours, no address or map** |

### Issue pages (from her CV)

| Issue | .co.uk | .bg |
|---|---|---|
| Anxiety & panic attacks | `/issues/anxiety-panic` | `/problemi/trevozhnost-i-panicheski-ataki` |
| Depression | `/issues/depression` | `/problemi/depresiya` |
| Stress | `/issues/stress` | `/problemi/stres` |
| Couple & relationship problems | `/issues/relationships` | `/problemi/problemi-v-dvoykata` |
| Parent–child relationships & the teenage years | `/issues/parenting-teens` | `/problemi/roditeli-i-tiyneydzhari` |
| Behavioural difficulties in children | `/issues/child-behaviour` | `/problemi/povedenie-pri-detsata` |
| Autism spectrum | `/issues/autism` | `/problemi/autizam` |
| ADHD / ADD | `/issues/adhd` | `/problemi/adhd` |
| Dyslexia, dyspraxia & learning difficulties | `/issues/learning-difficulties` | `/problemi/obuchitelni-zatrudneniya` |
| Bullying & digital violence | `/issues/bullying` | `/problemi/tormoz-i-digitalno-nasilie` |
| Life abroad / adapting to a new country | `/issues/living-abroad` | `/problemi/zhivot-v-chuzhbina` |

> Several of her columns match these pages (panic attacks, teens, marriage, digital violence, preventing violence in children). Each issue page can link to the matching column under "Read more".

**Every issue page follows the same layout** (copied from Chelsea): what it is → signs → how I help → FAQ (3–5 questions) → "Call or message me" buttons.

> "Life abroad" is our own idea, not from Chelsea. It suits her UK-based Bulgarian clients and very few competitors cover it.

### Footer pages

| Page | .co.uk | .bg | Notes |
|---|---|---|---|
| **FAQ** | `/faq` | `/chesto-zadavani-vaprosi` | Is it confidential? How many sessions? How do online sessions work? Cancellations? (.co.uk also: online vs in person) |
| **Press / Featured in** | `/press` | `/medii` | BG BEN column, "Doctor" newspaper interview (2015), BG Radio interview (2019), university lectures |
| **Crisis help** | `/crisis` | `/spesht-pomosht` | UK: 999, NHS 111, Samaritans 116 123. BG: 112. "I'm not an emergency service." |
| **Privacy policy** | `/privacy` | `/poveritelnost` | UK GDPR / EU GDPR – health data |
| **Cookies** | `/cookies` | `/biskvitki` | Cookie banner + policy |
| **Terms** | `/terms` | `/obshti-usloviya` | Payment (bank transfer / Revolut), **24-hour cancellation** |

### On every page

- Header: logo · menu · **BG / EN switch** · "Contact me" button (goes to the contact page)
- Footer: phone number, chat button (Viber on .bg / WhatsApp on .co.uk), email, Facebook, crisis link, legal links. No address, no hours.
- Bottom of each page: "Ready to talk? Call or message me" block with the phone and chat buttons

### Total to build first

**~30 page types**: 7 main pages, 6 "who I help" pages, 11 issue pages and 6 footer pages, each in two languages. Plus one page per column (18 to start), with new columns added over time.

### Not included (decided)

- Google Business Profile
- Listings on other directories
- Address or map
- Opening hours (she's flexible)
- **No booking page, booking calendar or contact form.** People call or message her directly (phone, Viber/WhatsApp, email, Facebook).
- Newsletter

### Nice-to-have later

- Short FAQ videos (1–2 min, filmed on a phone)
- Testimonials. Check her professional body's rules first (HCPC / BPS in the UK, her Bulgarian society); many therapists avoid them for confidentiality reasons.

---

## 6. Publications (for the Articles & publications page)

She'd like **all** of her publications on the site. There are enough that she's thinking of turning them into a book.

### "School of Psychology" column – BG BEN (18 columns)

The titles below are English translations. The originals are in Bulgarian. On .bg we show the Bulgarian title, on .co.uk the English one.

| # | Date | Title (EN) | Link |
|---|---|---|---|
| 1 | 27.01.2023 | How parents can help their children in adolescence | [PDF](https://bgben.co.uk/files/pdf_1739663167_482.pdf) |
| 2 | 14.04.2023 | Forgiveness is the greatest teacher | [PDF](https://bgben.co.uk/files/pdf_1739663300_486.pdf) |
| 3 | 30.06.2023 | How fears and emotions make us sick | [PDF](https://bgben.co.uk/files/pdf_1739663445_490.pdf) |
| 4 | 11.08.2023 | How to understand emotional intelligence and where we are | [PDF](https://bgben.co.uk/files/pdf_1739663529_492.pdf) |
| 5 | 12.01.2024 | Invitation to happiness | [PDF](https://bgben.co.uk/files/pdf_1739663720_498.pdf) |
| 6 | 13.09.2024 | How to be ourselves and acquire the skill of understanding | [PDF](https://bgben.co.uk/files/pdf_1739664087_506.pdf) |
| 7 | 2025 | Several successful steps to preserve love in marriage | [Article](https://bgben.co.uk/nyakolko-uspeshni-stupki-za-suhranenie-na-lyubovta-v-braka) |
| 8 | 10.02.2025 | Self-help for panic attacks / anxiety (part one) | [Article](https://bgben.co.uk/samopomosht-pri-panicheski-atakitrevozhnost-chast-purva) |
| 9 | 03.2025 | Self-help for panic attacks / anxiety (part two) | [Article](https://bgben.co.uk/samopomosht-pri-panicheski-atakitrevozhnost-chast-vtora) |
| 10 | 21.04.2025 | A conversation with gratitude | [Article](https://bgben.co.uk/v-uchilishte-po-psihologiya-dnes-razgovor-s-blagodarnostta) |
| 11 | 25.09.2025 | The child within us and the path to ourselves | [Article](https://www.bgben.co.uk/deteto-v-nas-i-putyat-kum-sebe-si-) |
| 12 | 12.2025 | Holiday stress and the invisible loneliness of the holidays | [Article](https://bgben.co.uk/praznichen-stres-i-nevidimata-samota-po-vreme-na-praznitsite-) |
| 13 | 13.01.2026 | The quiet revolution of the soul | [Article](https://bgben.co.uk/tihata-revolyutsiya-na-dushata) |
| 14 | 13.03.2026 | Practical guidelines for preventing violence in children | [Article](https://bgben.co.uk/prakticheski-nasoki-za-predotvratyavane-na-nasilieto-pri-detsata) |
| 15 | 04.04.2026 | Why it is important to make peace with ourselves | [Article](https://bgben.co.uk/zashto-e-vazhno-da-se-pomirim-sus-sebe-si) |
| 16 | 10.06.2026 | The silence of digital violence | [Article](https://bgben.co.uk/v-uchilishte-po-psihologiya-tishinata-na-digitalnoto-nasilie) |
| 17 | 08.07.2026 | The alphabet of the human soul | [Article](https://www.bgben.co.uk/azbukata-na-choveshkata-dusha) |
| 18 | 19.09.2026 | Expired gratitude | [Article](https://www.bgben.co.uk/blagodarnostta-s-iztekul-srok) |

> **How to show them:** ✅ BG BEN allows full republishing. Each column gets its own page on her site with the **full text** (good for Google), plus a line at the bottom: "First published in BG BEN, <date>" with a link to the original.
>
> **English versions:** ✅ all columns get **translated into English** for .co.uk, and she approves each translation before it goes live.

### Scientific publications

The CV says 21 scientific publications on peer relationships, the family environment and parent–child relationships. These are the ones listed:

1. Gertcheva-Nesterova, G., **Vasileva, M.** (2014). Specificity of interference of stress "parent–child". *Applied Psychology and Social Practice – 2015*, conference proceedings. Varna Free University "Chernorizets Hrabar".
2. **Vasileva, M.** (2011). Conflict interactions between parents and adolescents as a manifestation of conflict interaction parent–child and coping strategies. *Applied Psychology and Social Practice – 2011*, conference proceedings. Varna Free University.
3. **Vasileva, M.** (2011). Relationships between parents and adolescents. *e-Journal VFU*, issue 3, Varna.
4. **Vasileva, M.** (2011). Effects of stress on the family climate. *Applied Psychology and Social Practice – 2011*, conference proceedings. Varna Free University.
5. Gertcheva-Nesterova, G., **Vasileva, M.** (2010). Parental behaviour styles. *Applied Psychology and Social Practice – 2010*, conference proceedings. Varna Free University.
6. **Vasileva, M.** (2010). Effects of stress on the family climate and upbringing of children. *Proceedings of the Union of Scientists – Varna*.
7. **Vasileva, M.** (2007). Effects of stress on the family climate and upbringing of children. *Applied Psychology and Social Practice – 2007*, conference proceedings. Varna Free University.
8. **Vasileva, M.** (2007). The art of being a parent. *Psychology Journal*, issue 38, Varna, "Psido".
9. **Vasileva, M.** (2007). The problem of anxiety and aggression in adolescence. Manifestation of anxiety in adolescence. *Psychology Journal*, issue 39, Varna, "Psido".
10. **Vasileva, M.** (2007). Aggressiveness as a phenomenon and problem. Factors of aggression in adolescence. *Psychology Journal*, issue 41, Varna, "Psido".

**PhD thesis:** *Family environment and experiencing stress in adolescence* (2013), Varna Free University.

> She has **more scientific papers** than the CV lists. Full list coming soon, then we add them here.

### Interviews

- *"Self murderers are people who want to be noticed"*, newspaper **"Doctor"**, issue 15 (2015)
- *"Covid-19 and Panic Attacks"*, **BG Radio** (2019)
