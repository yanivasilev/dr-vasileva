# Dr Vasileva – Website Project Notes

## 1. The plan in one sentence

One website, two domains: **drvasileva.bg** shows the site in Bulgarian, **drvasileva.co.uk** shows it in English. Same content, same design, same photos, same code. Only the language changes.

---

## 2. Domains – the easy version

### How it works

```
drvasileva.bg     ─┐
                   ├──►  one website  ──►  .bg     = Bulgarian
drvasileva.co.uk  ─┘                       .co.uk  = English
```

- We build the site **once**. Every text exists in two languages.
- Both domains point to the **same hosting**.
- The site looks at which domain the visitor typed and picks the language.
- **The content is identical on both.** Only the language changes.
- A **BG / EN** button in the menu takes you to the same page on the other domain (see "Switching language" below).
- Change a photo or her bio once → both sites update.

### Steps

1. **Buy the domains**
   - `drvasileva.co.uk` from any registrar (Cloudflare, Namecheap, GoDaddy…).
   - `drvasileva.bg` from Register.bg or a Bulgarian registrar.
2. **Host:** your own OVH VPS with nginx. Both domains point to it, and free Let's Encrypt certificates provide HTTPS (the padlock). See section 13 and `deploy/README.md`.
3. **Point both domains** (and their `www`) at the VPS with DNS A records.
4. **The site** is built with two languages by `build/build.py` into `dist/en` and `dist/bg`.
5. **Tell Google** (see below).

### Same on both sites ✅

Everything is the same on both sites, just in a different language:

| | Both sites |
|---|---|
| Appointments | **Online and in person** (individual, couples, family, group) |
| Session languages | **Bulgarian and English** (group sessions too) |
| Phone | **+44 7999 334778** |
| Chat buttons | **Viber and WhatsApp**, both shown |
| Email | `contact@drvasileva.bg` on .bg and `contact@drvasileva.co.uk` on .co.uk, both going to one inbox |
| Socials | Facebook |
| Payment | Bank transfer, Revolut |
| Cancellation | 24 hours' notice |
| Prices | Decided after the site is finished. Suggestion: show **both £ and €** on both sites |
| Address | Not shown. Details for in-person sessions are given when people get in touch |
| Opening hours | Not shown (she's flexible) |
| Privacy policy | One policy covering **UK GDPR and EU GDPR** |

The only thing that differs is the **language** (Bulgarian on .bg, English on .co.uk).

### Contact buttons (same on both)

- **Call:** `+44 7999 334778` → `tel:+447999334778`. Written with +44 so it works from Bulgaria too.
- **Viber:** `viber://chat?number=%2B447999334778`
- **WhatsApp:** `https://wa.me/447999334778`
- **Email:** `contact@drvasileva.bg` / `contact@drvasileva.co.uk` → `mailto:` link
- **Facebook:** <https://www.facebook.com/mirena.vasileva.3> ✅

> The Viber link only opens if the visitor has Viber installed. The number is always shown as text next to the buttons as a fallback.

### Switching language (BG ↔ EN)

- Clicking **BG / EN** opens the **same page in the other language** on the other domain. For example, `drvasileva.co.uk/about` ↔ `drvasileva.bg/za-men`.
- It's a normal page load, exactly like clicking any link. The site is static (plain HTML, no heavy app), so the new page appears almost instantly. There's no flash or wait.
- The button sits in the same spot on both sites, so the switch feels seamless.
- Why not switch without loading? Then Google would only see one language, and the .bg / .co.uk split would stop helping in search.

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

`public/images/dr-vasileva.jpg` (1242 × 1242, square). It's a warm, friendly selfie, which suits About and Home. For the big Home banner, a crop that keeps the focus on her face (with less of the wall behind) will look cleaner. A professional portrait can replace it later.

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
- Interview, *"Self murderers are people who want to be noticed"* (EN on the site: *"Suicide is often a cry to be noticed"*), newspaper **"Doctor"**, published by **Здравето / Zdraveto (blitz.bg)**, issue 15 (2015)
- Interview, *"Covid-19 and Panic Attacks"*, **BG Radio** (2019)
- Lectures at Burgas Free University: Experimental Psychology, Pedagogical Psychology, "Art therapy methods in crisis intervention", "Family environment and experience of stress in adolescence"
- 6 scientific and applied contributions from her PhD, recognised at the **Bulgarian Academy of Sciences**

### Title (decided)

**Dr Mirena Vasileva, PhD – Psychologist & CBT Psychotherapist · MBPsS** *(letters to be checked, see section 10)*
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
- [x] About me: EN + BG (section 9), **approved by her** ✅
- [x] **Diploma in CBT** and **Diploma in SEND**: issued by **Burgas Free University** (shown with its logo). ✅ Confirmed.
- [x] **Safeguarding Children Level 3**: removed from the site.
- [ ] Check her current BPS letters (MBPsS → GMBPsS since 2022?), DBS date and Bulgarian society name (section 10)

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
| 1 | **Home** | `/` | `/` | Photo, one-line promise, who I help, online & in person, sessions in BG & EN, "Featured in", call + Viber + WhatsApp buttons |
| 2 | **About me** | `/about` | `/za-men` | Photo, "About me" text (section 9), quick facts box, **badges** (section 10), education, experience timeline, awards, publications link |
| 3 | **Who I help** | `/who-i-help` | `/s-kogo-rabotya` | Overview page, linking to 3a–3f |
| 3a | – Adults | `/who-i-help/adults` | `/s-kogo-rabotya/vazrastni` | Individual CBT therapy: anxiety, depression, panic, stress |
| 3b | – Couples & families | `/who-i-help/couples-families` | `/s-kogo-rabotya/dvoyki-i-semeystva` | CBT couples therapy, family therapy |
| 3c | – Children & teens | `/who-i-help/children-teens` | `/s-kogo-rabotya/deca-i-tiyneydzhari` | Consultations for children and teens, support for parents |
| 3d | – Special educational needs | `/who-i-help/special-educational-needs` | `/s-kogo-rabotya/specialni-obrazovatelni-potrebnosti` | Autism, ADHD, dyslexia, dyspraxia, learning difficulties, assessments and reports |
| 3e | – Organisations & schools | `/who-i-help/organisations` | `/s-kogo-rabotya/organizacii` | Group training: professional stress, teamwork, relationships |
| 3f | – Group sessions | `/who-i-help/group-sessions` | `/s-kogo-rabotya/grupovi-sesii` | What group sessions are, who they're for, how they work, online / in person, **in Bulgarian and English** |
| 4 | **What I help with** | `/issues` | `/problemi` | Grid of issue pages (see list below) |
| 5 | **Fees** | `/fees` | `/ceni` | Online + in person, **£ and €**. Session length, assessments & reports, how online sessions work, time zones UK ↔ BG, **payment by bank transfer or Revolut**, **cancellation: 24 hours' notice**. *Prices added after the site is finished.* |
| 6 | **Articles & publications** | `/articles` | `/statii` | Her "School of Psychology" columns (all of them, see section 6), plus her scientific publications |
| 7 | **Contact** | `/contact` | `/kontakti` | **No form, no booking.** Big buttons: call **+44 7999 334778**, **Viber**, **WhatsApp**, email, Facebook. **No hours, no address or map** |

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
| **FAQ** | `/faq` | `/chesto-zadavani-vaprosi` | Full list of questions and answers in section 7 |
| **Press / Featured in** | `/press` | `/medii` | BG BEN column, "Doctor" newspaper interview (2015), BG Radio interview (2019), university lectures |
| **Crisis help** | `/crisis` | `/spesht-pomosht` | UK: 999, NHS 111, Samaritans 116 123. BG: 112. "I'm not an emergency service." |
| **Privacy policy** | `/privacy` | `/poveritelnost` | One policy covering UK GDPR + EU GDPR – health data |
| **Cookies** | `/cookies` | `/biskvitki` | Cookie banner + policy |
| **Terms** | `/terms` | `/obshti-usloviya` | Payment (bank transfer / Revolut), **24-hour cancellation** |

### On every page

- Header: logo · menu · **BG / EN switch** · "Contact me" button (goes to the contact page)
- Footer: phone number, Viber, WhatsApp, email, Facebook, crisis link, legal links. No address, no hours.
- Bottom of each page: "Ready to talk? Call or message me" block with the phone, Viber and WhatsApp buttons

### Total to build first

**~30 page types**: 7 main pages, 6 "who I help" pages, 11 issue pages and 6 footer pages, each in two languages. Plus one page per column (18 to start), with new columns added over time.

### Not included (decided)

- Google Business Profile
- Listings on other directories
- Address or map
- Opening hours (she's flexible)
- **No booking page or booking calendar.** People call or message her directly (phone, Viber/WhatsApp, email, Facebook) or use the contact form.
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

---

## 7. FAQ (draft – for her to check)

The same questions go on both sites: English on .co.uk, Bulgarian on .bg. Anything in *[brackets]* gets filled in once prices are set.

### English (drvasileva.co.uk/faq)

**1. Is everything I say confidential?**
Yes. What you share stays between us. The only exception is if I believe you or someone else, especially a child, is at serious risk of harm. Then I may have to tell the right services, as the law and my professional code require. I would always try to talk to you about it first.

**2. What languages do you work in?**
Bulgarian and English. This includes individual, couples, family and group sessions.

**3. Do you offer online or in-person sessions?**
Both. Online sessions take place over a secure video call, so you can join from anywhere: the UK, Bulgaria or elsewhere. In-person sessions take place in the UK. I share the location when we arrange your appointment.

**4. How do I make an appointment?**
Simply get in touch by phone, Viber, WhatsApp, email or Facebook. Tell me a little about what you need, and we'll find a time that suits you.

**5. How long is a session?**
*[Session length, e.g. 50 minutes, to be confirmed.]*

**6. How many sessions will I need?**
It depends on you and what you'd like to work on. Some people feel a difference after a few sessions, others prefer longer support. We'll agree a plan together at the start and review your progress along the way.

**7. What approach do you use?**
Mainly cognitive behavioural therapy (CBT), a practical, well-researched approach. It helps you understand the link between your thoughts, feelings and behaviour, and learn tools to change them.

**8. Do you work with children and teenagers?**
Yes. I have many years of experience with children, teenagers and children with special educational needs (autism, ADHD, dyslexia, dyspraxia and other learning difficulties). Parents are involved, and for children under 18 a parent or guardian gives consent.

**9. Do you work with couples and families?**
Yes. I offer couples therapy and family therapy, helping you understand each other, communicate better and get through difficult times together.

**10. What are group sessions?**
Small groups of people working on similar topics, guided by me. They run in Bulgarian and in English, online or in person. Groups are a supportive way to learn from others who understand what you're going through.

**11. Do you offer training for organisations and schools?**
Yes. I run group trainings on topics such as professional stress, effective teamwork and relationships at work and at school.

**12. How much does it cost?**
*[See the Fees page.]*

**13. How do I pay?**
By bank transfer or Revolut.

**14. What if I need to cancel?**
Please give at least **24 hours' notice**. Sessions cancelled with less notice may be charged in full.

**15. I live in Bulgaria and you're in the UK. What about the time difference?**
No problem. Bulgaria is 2 hours ahead of the UK. We always agree the time in your local time zone.

**16. Do I need a referral from my doctor?**
No. You can contact me directly.

**17. What if I'm in crisis?**
I'm not an emergency service. If you or someone else is in immediate danger, call **999** in the UK or **112** in Bulgaria. In the UK you can also call **Samaritans on 116 123** (free, 24/7). See the Crisis help page for more.

### Български (drvasileva.bg/chesto-zadavani-vaprosi)

**1. Поверително ли е всичко, което споделям?**
Да. Това, което споделяте, остава между нас. Единственото изключение е, ако смятам, че Вие или някой друг, особено дете, сте в сериозна опасност. Тогава може да се наложи да уведомя съответните служби, както изискват законът и професионалната ми етика. Винаги ще се опитам първо да говоря с Вас за това.

**2. На какви езици работите?**
На български и английски. Това включва индивидуални, семейни и групови сесии, както и консултации за двойки.

**3. Предлагате ли онлайн или присъствени консултации?**
И двете. Онлайн консултациите се провеждат чрез сигурен видеоразговор, така че можете да се включите отвсякъде: от България, Великобритания или друга държава. Присъствените консултации са във Великобритания. Мястото Ви съобщавам, когато уговорим час.

**4. Как да си запазя час?**
Просто се свържете с мен по телефона, Viber, WhatsApp, имейл или Facebook. Разкажете ми накратко от какво имате нужда и ще намерим удобно за Вас време.

**5. Колко продължава една консултация?**
*[Продължителност, напр. 50 минути, предстои да бъде потвърдена.]*

**6. Колко консултации ще са ми нужни?**
Зависи от Вас и от това, върху което искате да работим. Някои хора усещат промяна след няколко срещи, други предпочитат по-дълга подкрепа. В началото заедно ще изготвим план и ще следим напредъка Ви.

**7. Какъв подход използвате?**
Основно когнитивно-поведенческа терапия (КПТ), практичен и научно доказан подход. Тя помага да разберете връзката между мислите, чувствата и поведението си и да научите начини да ги промените.

**8. Работите ли с деца и тийнейджъри?**
Да. Имам дългогодишен опит с деца, тийнейджъри и деца със специални образователни потребности (аутизъм, ADHD, дислексия, диспраксия и други обучителни затруднения). Родителите участват в процеса, а за деца под 18 години е нужно съгласие от родител или настойник.

**9. Работите ли с двойки и семейства?**
Да. Предлагам терапия за двойки и семейна терапия, за да се разбирате по-добре, да общувате по-лесно и да преминете заедно през трудните моменти.

**10. Какво представляват груповите сесии?**
Малки групи от хора, които работят по сходни теми под мое ръководство. Провеждат се на български и на английски, онлайн или присъствено. Групата е подкрепяща среда, в която се учите от хора, които разбират през какво преминавате.

**11. Предлагате ли обучения за организации и училища?**
Да. Провеждам групови обучения на теми като професионален стрес, ефективна работа в екип и взаимоотношения на работното място и в училище.

**12. Колко струва?**
*[Вижте страница „Цени“.]*

**13. Как мога да платя?**
С банков превод или Revolut.

**14. Какво става, ако трябва да откажа час?**
Моля, уведомете ме поне **24 часа** предварително. При по-късно отказване консултацията може да бъде таксувана изцяло.

**15. Живея в България, а Вие сте във Великобритания. Как стои въпросът с часовата разлика?**
Няма проблем. България е с 2 часа напред спрямо Великобритания. Винаги уговаряме часа по Вашето местно време.

**16. Нужно ли ми е направление от лекар?**
Не. Можете да се свържете директно с мен.

**17. Какво да направя при криза?**
Аз не съм спешна служба. Ако Вие или някой друг сте в непосредствена опасност, обадете се на **112** в България или на **999** във Великобритания. Във Великобритания можете да се обадите и на **Samaritans на 116 123** (безплатно, денонощно). Повече информация има на страница „Спешна помощ“.

---

## 8. Look & feel

Taken from her photo: the **green** of her blouse and the soft **lilac/pink** of her scarf. Calm, warm and personal, not clinical.

### Colours

| Use | Colour | Hex |
|---|---|---|
| Main colour (buttons, headings) | Sage green | `#4F6F52` |
| Darkest green (hero, contact) | Forest green | `#2C4430` |
| Dark green (hover, footer) | Deep green | `#344E38` |
| Accent (highlights, small details) | Soft lilac | `#B9A3C9` |
| Warm accent (awards, quotes) | Muted gold | `#C9A25A` |
| Background | Warm cream | `#FAF7F2` |
| Cards / sections | Light sand | `#F1ECE3` |
| Text | Charcoal | `#2E2E2E` |

### Fonts

Both support **Cyrillic**, so Bulgarian looks just as good as English.

- **Headings:** *Cormorant Garamond*, an elegant, editorial serif
- **Body text:** *Manrope*, clean and very readable on phones

### Logo ✅ (decided: spaced capitals)

**DR VASILEVA** in Manrope, widely letter-spaced, one colour. Saved as a true vector SVG (letters converted to shapes), so it stays sharp at any size and doesn't depend on a font loading.

| File | Use |
|---|---|
| `brand/logo.svg` | Dark green logo for light backgrounds (for use outside the website, e.g. print) |
| `brand/logo-light.svg` | Cream logo for dark backgrounds |

The same logo is used on both .bg and .co.uk (it's her name, so it doesn't need translating).

### Partner logos (`public/images/logos/`)

Supplied by you. Used in the credentials strip, "Featured in", the award cards, the Press page and the About page.

| File | Organisation |
|---|---|
| `bg-ben.png` | BG BEN (her column) |
| `bg-radio.png` | BG Radio (2019 interview) |
| `zdraveto.png` | Здравето / blitz.bg, publisher of the "Doctor" newspaper (2015 interview) |
| `bps-mark.png` | The British Psychological Society emblem |
| `varna-free-university.png`, `varna-free-university-mark.png` | Varna Free University "Chernorizets Hrabar" (full logo / emblem only) |
| `bulgarian-psychological-society.png` | Bulgarian Psychological Society |
| `burgas-free-university.png` | Burgas Free University (CBT & SEND diplomas, lectures) |
| `bulgarian-academy-of-sciences.png` | Bulgarian Academy of Sciences (doctoral contributions) |

> Before launch: the BPS limits how members use its logo. Check her membership grade allows it (her BPS portal or the BPS brand guidelines); if not, we swap back to the "Ψ" badge.

### Icons & share images

| File | Size | Where it shows |
|---|---|---|
| `public/images/favicon.svg` | vector | Browser tab (modern browsers): a simple five-petal **flower** (cream petals, gold centre) on dark green. The same flower is used for all the icons below |
| `public/images/favicon.ico` | 16/32/48 px | Browser tab (older browsers, Windows) |
| `public/images/apple-touch-icon.png` | 180 × 180 | iPhone/iPad "Add to Home Screen" |
| `public/images/icon-192.png`, `icon-512.png` | 192, 512 | Android home screen (`site.webmanifest`) |
| `public/images/og-en.png` | 1200 × 630 | Link preview on **Facebook, WhatsApp, Viber, X/Twitter, LinkedIn** for drvasileva.co.uk |
| `public/images/og-bg.png` | 1200 × 630 | The same, in Bulgarian, for drvasileva.bg |

The share image shows the logo, the headline, her title, "Online & in person · Bulgarian & English", the domain and her photo in the arch.

> Twitter/X uses the same image as Facebook (the `og:image` tag), so one image covers every platform.

### Style

- Lots of white space, rounded corners and soft shadows
- Her photo is large on Home and About
- Big, easy-to-tap buttons for **Call · Viber · WhatsApp** (most visitors will be on a phone), in each app's **own brand colours**: WhatsApp green `#25D366`, Viber purple `#7360F2`, Facebook blue `#1877F2`
- Gentle animations: sections fade up as you scroll, the headline rises in line by line, the photo is unveiled, and the credentials scroll past slowly. All motion switches off for visitors who've set "reduce motion" on their device
- Phone menu opens **full-screen**
- No stock photos of people "looking sad". Instead, calm nature and texture images, or none at all

---

## 9. About me (approved ✅)

Written in her voice, from her CV. Used on the **About me** page, with the short version on **Home**.

### English

**Short version (Home page)**

> I'm Dr Mirena Vasileva, a psychologist and CBT psychotherapist with 21 years of experience. I help adults, couples, families, children and teenagers through anxiety, stress, relationship difficulties and life's big changes, in Bulgarian or in English, online or in person.

**Full version (About me page)**

## Hello, I'm Mirena

For 21 years, since 2005, I have been doing the work I love most: helping people understand themselves, heal and find their way forward. I'm a psychologist and cognitive behavioural therapist (CBT) with a PhD in Pedagogical and Developmental Psychology. I work with adults, couples, families, children and teenagers.

My path began in Bulgaria. For eight years I worked as a psychologist at a home for children with intellectual disabilities near Nessebar, where I learned that every child, whatever their needs, deserves to be truly seen. Alongside that, I built my private practice, worked as a psychotherapist at Viva Clinic in Sunny Beach, and taught Experimental and Pedagogical Psychology at Burgas Free University as a Chief Assistant Professor.

In 2016 I moved to London. Since then I have worked with clients at the Doctors 4 You and Medi-Park clinics, and supported children with special educational needs at the Bulgarian school "Rodna Rech". Many of the people I see know what it's like to build a life between two countries. So do I.

My doctoral research explored how the family environment shapes the way teenagers experience and cope with stress. It still guides my work today: I believe that when we understand the relationships around us, we can change the way we feel.

In our sessions I mainly use CBT, a practical approach backed by research. Together we look at the link between your thoughts, feelings and behaviour, and find tools that work in your everyday life. I listen without judgement, and we go at your pace.

Since 2023 I have written the "School of Psychology" column in BG BEN, the newspaper for Bulgarians in the UK. Outside the therapy room, I organise charity campaigns for children with intellectual disabilities and children without parental care.

Whether you're facing anxiety, a difficult relationship, worries about your child, or you simply feel stuck, you don't have to go through it alone. Call or message me, in Bulgarian or in English.

### Български

**Кратка версия (начална страница)**

> Аз съм д-р Мирена Василева – психолог и когнитивно-поведенчески психотерапевт с 21 години опит. Помагам на възрастни, двойки, семейства, деца и тийнейджъри да се справят с тревожност, стрес, трудности във взаимоотношенията и големите промени в живота – на български или на английски, онлайн или на живо.

**Пълна версия (страница „За мен“)**

## Здравейте, аз съм Мирена

Вече 21 години – от 2005 г. – правя това, което обичам най-много: помагам на хората да разберат себе си, да се излекуват и да намерят своя път напред. Аз съм психолог и когнитивно-поведенчески психотерапевт (КПТ) с докторска степен по педагогическа и възрастова психология. Работя с възрастни, двойки, семейства, деца и тийнейджъри.

Пътят ми започна в България. Осем години работих като психолог в дом за деца с интелектуални затруднения в община Несебър, където научих, че всяко дете, независимо от потребностите си, заслужава да бъде истински видяно. Успоредно с това развивах частната си практика, работих като психотерапевт във Viva Clinic в Слънчев бряг и преподавах експериментална и педагогическа психология в Бургаския свободен университет като главен асистент.

През 2016 г. се преместих в Лондон. Оттогава работя с клиенти в клиниките Doctors 4 You и Medi-Park, а в българското училище „Родна реч“ подкрепях деца със специални образователни потребности. Много от хората, с които работя, знаят какво е да градиш живот между две държави. Знам го и аз.

Докторското ми изследване беше посветено на това как семейната среда влияе на начина, по който тийнейджърите преживяват стреса и се справят с него. То и до днес ръководи работата ми: вярвам, че когато разберем отношенията около нас, можем да променим и начина, по който се чувстваме.

В консултациите използвам основно КПТ – практичен и научно доказан подход. Заедно разглеждаме връзката между мислите, чувствата и поведението Ви и търсим инструменти, които работят в ежедневието Ви. Изслушвам Ви, без да съдя, и вървим с Вашето темпо.

От 2023 г. пиша рубриката „Училище по психология“ във вестник BG BEN – изданието за българите във Великобритания. Извън кабинета организирам благотворителни кампании за деца с интелектуални затруднения и деца, лишени от родителска грижа.

Независимо дали се борите с тревожност, трудна връзка, притеснения за детето си, или просто се чувствате в застой – не е нужно да минавате през това сами. Обадете ми се или ми пишете – на български или на английски.

### Next to the text: quick facts box

| | EN | BG |
|---|---|---|
| 🎓 | PhD in Pedagogical & Developmental Psychology | Доктор по педагогическа и възрастова психология |
| 🧠 | CBT Psychotherapist | Когнитивно-поведенчески психотерапевт |
| 🏆 | Gold Ring of Varna Free University · First Prize, Best Master's Thesis | Златен пръстен на ВСУ · Първа награда за най-добра дипломна работа |
| 🌍 | Sessions in Bulgarian & English | Консултации на български и английски |
| 💻 | Online & in person | Онлайн и на живо |
| 📰 | "School of Psychology" columnist, BG BEN | Автор на рубриката „Училище по психология“, BG BEN |

> **Private details left out on purpose:** date of birth, home address, family, personal email.

---

## 10. Badges (trust signals)

### Rule: our own badges, not official logos

We design **our own simple badges** (icon + short text, in the site colours). We **don't** use the official logos of the BPS, the universities, NSPCC or DBS. Organisations like these usually restrict who may use their logos, and a wrong logo can get a removal request or look misleading. Text badges are always safe, and they look cleaner.

### Badges to show

Shown as a row on **Home** and **About me**:

| Badge | EN text | BG text | Show? |
|---|---|---|---|
| 🎓 | **PhD in Psychology** | **Доктор по психология** | ✅ |
| 🏆 | **Gold Ring award**, Varna Free University | **Златен пръстен**, ВСУ „Черноризец Храбър“ | ✅ |
| 🥇 | **First Prize, Best Master's Thesis** | **Първа награда** за най-добра магистърска теза | ✅ |
| 🧠 | **Diploma in CBT** | **Диплома по КПТ** | ✅ |
| 🧩 | **Diploma in SEND** (special educational needs) | **Диплома по СОП** | ✅ |
| 🏛️ | **Member, British Psychological Society** | **Член на Британското психологическо дружество** | ✅ *(see check 1)* |
| 🇧🇬 | **Member, Bulgarian Psychological Society** | **Член на Дружеството на психолозите в България** | ✅ *(see check 3)* |
| 🛡️ | **Safeguarding Children – Level 3** | **Закрила на детето – ниво 3** | ✅ |
| ⏳ | **21 years' experience** (auto-counted from 2005) | **21 години опит** | ✅ |
| 🗣️ | **Bulgarian & English** | **Български и английски** | ✅ |
| 📰 | **Columnist, BG BEN** | **Автор в BG BEN** | ✅ |
| ✔️ | **Enhanced DBS checked** | **DBS проверка** | ⚠️ *(see check 2)* |

### Checks before launch

1. **BPS letters.** In **September 2022** the BPS changed the letters for graduate members from **MBPsS** to **GMBPsS**. Her CV still says MBPsS. She can see her current grade and letters in her BPS member portal. Until then, the badge just says "Member, British Psychological Society", which is true either way, and the letters after her name should match what the portal shows.
2. **DBS.** Her Enhanced DBS is dated **July 2016**. A DBS check is a snapshot on the day it's issued. Only show the badge if she has a **recent** one or is on the **DBS Update Service**.
3. **Bulgarian Psychological Society.** Confirm the exact name of the society she's a member of, so the badge text is correct.

---

## 11. Contact form ✅ (added)

On the **Contact** page, under the call/message tiles: name, email, phone (optional), "I'm interested in", how to reply (Email / Phone call / WhatsApp / Viber), language (English / Български), message, privacy consent. There's also a note not to share detailed health information, and a crisis reminder.

### How it's protected

- **Cloudflare Turnstile**, a free, privacy-friendly "I'm not a robot" check. Most visitors never see a puzzle.
- **Honeypot**, a hidden field that only bots fill in. Those messages are silently dropped.
- **Server-side checks**: Turnstile is verified on the server, every field has a length limit, and the email and consent are required.

### How a message reaches her

```
Form  →  /api/contact (on the VPS: server/contact_server.py, behind nginx)
      →  checks Turnstile + fields
      →  sends the email through mailcow (SMTP)  →  contact@drvasileva.co.uk  or  contact@drvasileva.bg
```

> Setup steps are in **`deploy/README.md`**.

Replying to the email goes straight to the visitor (the email's reply-to is set to their address).

> The privacy policy mentions the form, her own mail server and Turnstile.

---

## 12. Bulgarian version ✅ (first full draft)

- **Preview files:** `preview/site.html` (English) and `preview/site-bg.html` (Bulgarian). The BG / EN switch moves between them and keeps you on the same page.
- **Live site:** `dist/en` (drvasileva.co.uk) and `dist/bg` (drvasileva.bg) are built with real addresses. The Bulgarian site uses the Bulgarian slugs from section 5 (e.g. `/za-men`). Every page is saved as its own file, so it loads directly and search engines can read it. The switch goes to the same page on the other domain. Each site has its own 404 page, robots.txt and sitemap.xml (with hreflang links between the two languages).
- **Why the preview has `#/` in links:** a single preview file can't have real pages, so it uses `site.html#/about`. The live site doesn't.
- **How it's built:** the English site is built first; `src/bg/` then swaps in the Bulgarian content (`data1.js`, `data2.js`, `blocks.js`, `pages.js`) and translates the remaining interface text with exact pairs (`pairs.py`). The build stops if an English phrase isn't found, so changes to the English text can't silently leave English on the Bulgarian site.
- **Bulgarian specifics:** email `contact@drvasileva.bg`, share image `og-bg.png`, BG listed first in the switch, Bulgarian crisis numbers listed first, prices shown as € / £, dates in Bulgarian.

### For her to check (✅ approved)

- [x] **Letter shapes:** keep the Bulgarian-style Cyrillic letterforms (the page is marked `lang="bg"`, so the fonts use them).

- [x] The whole text reads naturally in her voice (formal **„Вие“** is used throughout).
- [x] **Column titles** of the six older (PDF) columns are my back-translations from English: "Как да бъдем себе си…", "Покана за щастие", "Как да разбираме емоционалната интелигентност…", "Как страховете и емоциите ни разболяват", "Прошката е най-великият учител", "Как родителите могат да помогнат на децата си в юношеството". The other 12 come from the BG BEN web addresses and should be exact.
- [x] **Scientific publications**: the Bulgarian titles are back-translations of the English ones in her CV, so they need checking against the originals.
- [x] The interview title „Самоубийците са хора, които искат да бъдат забелязани“.

---

## 13. Hosting on the VPS ✅

- One nginx on the OVH VPS serves both domains: `.co.uk` from `dist/en`, `.bg` from `dist/bg`. www and http are redirected to `https://` without www.
- The contact form goes to a small Python service (`server/contact_server.py`) that sends through mailcow. Each domain sends to its own `contact@` address.
- If mailcow is on the same VPS, its web server moves to local ports behind the main nginx (`deploy/nginx/mailcow-proxy.conf`).
- Updating = `git pull`. No build is needed on the server.
- Full step-by-step guide: **`deploy/README.md`**.

- **Fonts are self-hosted** (`public/fonts/`, Latin + Cyrillic, SIL Open Font License). Loading them from Google would send every visitor's IP address to Google, which a German court ruled breaks EU GDPR. The Cookies page says so in both languages. The only outside service the site contacts is Cloudflare Turnstile on the contact form.

### Still needed before launch

- [ ] DNS for both domains (and www) → VPS
- [ ] mailcow mailbox for the website (e.g. `website@drvasileva.co.uk`) + its password in `/etc/drvasileva/contact.env`
- [x] Real Turnstile keys: the site key is built into the site; the secret key goes only in `/etc/drvasileva/contact.env` on the server (never in the repo)

---

## 14. Articles / blog ✅ step 1 (pages + the 18 columns)

**What's built:**
- **Articles page** (`/articles` · `/statii`):
  - the newest post large at the top;
  - topic filters;
  - cards with a coloured cover per topic;
  - "Show more" after 12 cards;
  - a link to the new **Scientific publications** page (`/publications` · `/publikacii`), which replaced the old list on the Articles page.
- **Every post has its own page in both languages:**
  - topic, date, cover, the text and the BG BEN box;
  - share buttons (Facebook, WhatsApp, Viber, copy link);
  - the author box, 3 related posts and the "Ready to talk?" band.
  - Each page also has its own address, share data and Google article data, and the EN / BG switch goes to the same post.
- **Elsewhere on the site:**
  - the home page's row shows the latest 12 posts;
  - the "Read my column" links on the topic pages now open the column's page on her site.
- **Where it lives:**
  - posts are in `content/` (see the main README);
  - the pages are made by `build/blog.py`, which needs only Python, so the editor can use it on the server.

**Topics:**
- in use: Anxiety & stress, Relationships, Children & parents, Self-growth (most columns are self-growth);
- also set up, shown once they have a post: Special needs, Living abroad.

### For her to check
- [ ] **The 18 introductions are placeholders.** BG BEN's site couldn't be opened from here, so each introduction was written from the column's title only, without reading the column. Please replace them with her own two or three paragraphs: `content/posts/<id>/en.md` and `bg.md`, or later in the editor.
- [ ] **The six PDF columns:** you're sending the full texts, which will then replace the introduction and the PDF link.
  - How to be ourselves…
  - Invitation to happiness
  - Understanding emotional intelligence…
  - How fears and emotions make us sick
  - Forgiveness is the greatest teacher
  - How parents can help their children in adolescence
- [ ] **Cover photos:** add them later; a post without one shows its topic's coloured cover.

### Next: the editor (steps 2–4)
`admin.drvasileva.co.uk`:
- login with password plus a code from her phone;
- a posts list, and writing in BG | EN tabs with a toolbar;
- Preview, Publish and Unpublish;
- cover photo upload, with the location data removed;
- topics, saved versions, the bin and autosave.

It saves posts in the same format and rebuilds only the blog pages.

## 15. Editor step 2: secure sign-in ✅

Built by `server/admin_server.py`; the setup steps are in `deploy/README.md` step 8.

**Sign-in:**
- a password plus a code from an authenticator app, or a one-time backup code;
- one account, created only with a command on the server;
- no sign-up page and no reset email.

**Limits and alerts:**
- 5 wrong tries pause sign-in for 15 minutes, with a limit per address and an nginx limit as well;
- every sign-in and every lock is emailed;
- the editor shows the previous sign-in.

**Sessions:** a secure cookie; signed out after 1 hour idle, and always after 12 hours.

**Page protection:**
- form posts from other sites are refused;
- strict browser rules: no scripts, no framing, no caching, not indexed;
- the editor runs as a restricted user.

**Tested:**
- 45 attack tests: wrong details, the lock, reused codes, backup codes, forged posts, cookies, timeouts and file access;
- a real browser signing in through nginx over HTTPS.

## 16. Editor step 3: writing and publishing ✅

Setup: `deploy/README.md` step 9.

**The screens:**
- **Posts list:** title, topic, status, date, and which language is missing.
- **Writing a post:**
  - Български | English tabs, with ✓ on a finished language;
  - a toolbar for headings, bold, italic, lists, quotes and links;
  - topic, date, BG BEN link and cover photo.
- **The buttons:**
  - Preview (BG and EN), Save draft and Publish;
  - Save changes and Unpublish for a published post;
  - Versions and Delete.
- **Topics:** add, rename, colour and icon, both languages. A topic with posts can't be deleted.
- **Bin:** 30 days; a restored post comes back as a draft.

**Safety nets:**
- **Versions:** the last 30 saves.
- **Autosave:** in the browser every 30 seconds, with a "restore unsaved changes" banner.
- **Live posts stay complete:** a published post can't be saved incomplete; the live page stays as it was, and her typing is kept in the form.
- **Addresses never change by accident:** emptying the web address field keeps the post's current address.

**Security:**
- **Scripts:** only the editor's own script is allowed.
- **Text in posts:** everything is escaped (tested with a script in a title).
- **Photos:**
  - redrawn on the server: the location data is removed and the photo is resized to at most 2000 px;
  - SVG, GIF, fake files, files over 10 MB and decompression bombs are refused.
- **Preview:** a sandbox with no scripts, which can't read her cookies (checked in a browser).
- **Requests and files:**
  - every change needs her session, the CSRF token and the editor's own origin;
  - path tricks are refused.

**Where things are kept:**
- posts on the server in `/var/lib/drvasileva-admin/content`, seeded once from `content/`;
- published pages in `/var/www/drvasileva-blog`, served by nginx;
- a nightly backup in `/var/backups/drvasileva`.

**Tested:** 52 end-to-end tests, the 45 sign-in attack tests again, and a real browser:
- tabs, toolbar, photo upload, publish, autosave restore and preview;
- nginx serving the published articles.

**Later, if wanted:** a Bulgarian version of the editor's own screens (they're in English now).

### Update: formatting you can see
- **The text box shows real formatting:** bold, italic, headings, lists, quotes, links and colours. There are no `**symbols**` to type.
- **Toolbar buttons:** each has a word next to it: Heading, Subheading, Normal text, Bold, Italic, **Underline** (new), **Colour** (new: green, lilac, gold, rose, all readable on the cream background), Bullet list, Numbered list, Quote, Link, Clear formatting.
  - The buttons light up for the selected text.
  - Ctrl+B, Ctrl+I and Ctrl+U work too.
- **Paste:** pasted text always arrives as plain text, so no hidden formatting or code from Word or websites gets in.
- **Storage:** posts are still stored in the same safe text format.
  - Tested: all 18 columns load and save back unchanged.
  - Without JavaScript the plain text box still works.
- **Numbered lists carry on after a paragraph** (1, explanation, 2, explanation, 3 …), and the numbers are kept when saving and on the site.
  - A heading starts again at 1.
  - **Restart numbering** (shown when the cursor is in a list that carries on) starts a list at 1 on purpose. It's remembered after saving; clicking again carries on.

### Update: posts, sign out and topics
- **Posts:**
  - shows only the time of the previous sign-in (the sign-in emails still include the address);
  - a search box filters the posts by title, Bulgarian or English, as she types.
- **Sign out:** a red button with a "Sign out? No, stay / Yes, sign out" box, so a click by accident doesn't sign her out.
- **Topics:**
  - each topic shows how its cover looks, with its colour and icon, and the preview changes as soon as another one is chosen;
  - **+ New topic** opens its own form, with the same preview.

