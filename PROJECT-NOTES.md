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
| Time zone for booking | Bulgaria (EET) | UK (GMT/BST) – 2 hours behind |
| Phone shown | Bulgarian number | UK number (if she has one) |
| Legal pages | Privacy policy under EU GDPR | Privacy policy under UK GDPR |

### Google search – do's and don'ts

- **Do** add both domains to **Google Search Console**.
- **Do** add `hreflang` tags (one line in the page code). They tell Google "these two pages are the same page in two languages", so it shows the right one in each country and doesn't see them as duplicates.
- **Do** let the domains do the targeting: Google automatically treats `.bg` as Bulgaria and `.co.uk` as the UK.
- **Don't** auto-redirect people by their location. It confuses Google and annoys people (e.g. a Bulgarian living in London). Use the BG / EN button instead.

### Google Business Profile (Google Maps)

- A profile needs a **real address where she sees clients in person**.
- **Office only in Bulgaria** → one profile in Bulgaria, linked to `drvasileva.bg`. No UK profile is possible (virtual offices break Google's rules and get suspended).
- **Offices in both countries** → two profiles, each linked to its own domain.
- **Online only** → not eligible for a profile. The website and directories do the work instead.

> **To decide:** where does she actually see clients – Bulgaria, UK, both, or online only?

### Other places to list her

- **UK:** HCPC register (needed to use the title "practitioner psychologist" in the UK), BPS / BACP directories, Psychology Today UK.
- **Bulgaria:** superdoc.bg, imatter.bg, the relevant Bulgarian psychology / psychotherapy society registers.
- **Everywhere:** Bing Places, Apple Business Connect.

---

## 3. About Dr Vasileva (research)

> ⚠️ **Not confirmed.** A web search did not find one clear profile for "Dr Vasileva, psychologist, UK + Bulgaria", and **no awards were found** online. The person below is the **closest match**. Please check with her before anything goes on the site.

### Closest match: Dr Mirena Koleva Vasileva (д-р Мирена Колева Василева)

What the public sources say:

- **Doctorate (PhD)** in **educational and developmental psychology** (доктор по педагогическа и възрастова психология).
- About **20 years** of professional experience in psychology.
- Formerly **Chief Assistant Professor** at **Burgas Free University**, working in experimental and educational psychology.
- **Living in London since 2016.**
- Writes a column called **"School of Psychology" ("Училище по психология")** for the UK-based Bulgarian outlet **BG BEN** (bgben.co.uk). A June 2026 piece covered **digital violence / cyberbullying** ("Тишината на дигиталното насилие").

Source: bgben.co.uk – "В „Училище по психология“: Тишината на дигиталното насилие" (10 June 2026).

### Other psychologists named Vasileva (to avoid mixing up)

None of these are connected to both the UK and Bulgaria. They're listed so we don't use their details by mistake:

- Polina Vasileva – psychologist/psychotherapist in Bulgaria. Her imatter.bg profile lists a J.L. Moreno statuette (2019–2020).
- Mira, Nadezhda, Anelia Vasileva – psychologists in Sofia (superdoc.bg).
- Galina Vasileva, Nina Vasileva – psychologists in Varna (both listed on zlatnafirma.eu "Golden Company" award pages).
- Desi Vasileva – clinical psychologist in Oslo, Norway.
- Dr Mira Vasileva – clinical psychologist in Germany (Oldenburg).

### Info we still need from her

- [ ] Full name as it should appear (BG + EN spelling)
- [ ] Photo(s)
- [ ] Qualifications, university, year of PhD
- [ ] Registrations (HCPC / BPS in the UK, Bulgarian society membership)
- [ ] **Awards** – names, years, who gave them (nothing found online)
- [ ] Specialisms (e.g. children, teens, parents, anxiety, cyberbullying…)
- [ ] Services: in person / online, session length, prices in EUR and GBP
- [ ] Office address(es) – decides the Google Business Profile
- [ ] Phone, email, booking method
- [ ] Languages she works in
- [ ] Short bio in her own words

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
- One page per issue, each ending in an FAQ and a booking button. These pages are what bring people in from Google.
- An **open fees table**. People trust prices they can see.
- **Short FAQ videos** (1–2 min) – easy to film on a phone
- **Press / "As featured in"**. Her BG BEN column fits here.
- A **crisis information** page
- The contact form with "best time to call"
- A "Start your journey" button on every page

### What we skip ❌

- Psychiatry, nutrition, sleep, retreats, membership, careers, corporate, multiple locations. These need a whole clinic.
- 30 issue pages and 15 therapy pages. **6–8 issue pages that match her real specialisms** is plenty to start.
- Health-insurance logos, unless she's registered with insurers.

### Where we can beat them

- **Two languages, two countries.** Chelsea only shows a "Languages: English, Greek" tag on profiles. Her whole site is native Bulgarian *and* English, which is a real selling point for Bulgarians in the UK.
- **Personal.** One face, her own voice, her own story. A solo practitioner can feel warmer than a big clinic.
- **Her niche.** If her background is educational and developmental psychology, then children, teens, parents, schools and cyberbullying are exactly where Chelsea's offer is thinnest.

---

## 5. Our pages (sitemap)

Every page exists in both languages. URLs are in English on `.co.uk` and in Bulgarian (Latin letters) on `.bg`.

### Main menu

| # | Page | drvasileva.co.uk | drvasileva.bg | What's on it |
|---|---|---|---|---|
| 1 | **Home** | `/` | `/` | Photo, one-line promise, who I help, how it works (3 steps), "Featured in", book button |
| 2 | **About me** | `/about` | `/za-men` | Story, education, PhD, experience, **awards**, registrations, languages, approach |
| 3 | **Who I help** | `/who-i-help` | `/s-kogo-rabotya` | Overview page, linking to 3a–3d |
| 3a | – Adults | `/who-i-help/adults` | `/s-kogo-rabotya/vazrastni` | Individual therapy |
| 3b | – Children & teens | `/who-i-help/children-teens` | `/s-kogo-rabotya/deca-i-tiyneydzhari` | Child and teen work |
| 3c | – Parents & families | `/who-i-help/parents` | `/s-kogo-rabotya/roditeli` | Parenting support, family sessions |
| 3d | – Schools | `/who-i-help/schools` | `/s-kogo-rabotya/uchilishta` | Talks, training, consultations *(if she does this)* |
| 4 | **What I help with** | `/issues` | `/problemi` | Grid of issue pages (see list below) |
| 5 | **Online therapy** | `/online-therapy` | `/onlayn-terapiya` | How online sessions work, platform, time zones UK ↔ BG |
| 6 | **Fees & booking** | `/fees` | `/ceni` | Price table (GBP on .co.uk, EUR on .bg), session length, cancellation policy, booking |
| 7 | **Articles** | `/articles` | `/statii` | Her writing, incl. the "School of Psychology" columns |
| 8 | **Contact** | `/contact` | `/kontakti` | Form with best time to call, email, phone, address/map, hours |

### Issue pages (start with 6–8, pick from her real specialisms)

| Issue | .co.uk | .bg |
|---|---|---|
| Anxiety | `/issues/anxiety` | `/problemi/trevozhnost` |
| Depression & low mood | `/issues/depression` | `/problemi/depresiya` |
| Stress & burnout | `/issues/stress` | `/problemi/stres` |
| Relationship difficulties | `/issues/relationships` | `/problemi/vzaimootnosheniya` |
| Bullying & cyberbullying | `/issues/bullying` | `/problemi/tormoz` |
| Learning difficulties (dyslexia…) | `/issues/learning-difficulties` | `/problemi/obuchitelni-zatrudneniya` |
| Child behaviour & emotions | `/issues/child-behaviour` | `/problemi/povedenie-pri-detsata` |
| Life abroad / adapting to a new country | `/issues/living-abroad` | `/problemi/zhivot-v-chuzhbina` |

**Every issue page follows the same layout** (copied from Chelsea): what it is → signs → how I help → FAQ (3–5 questions) → "Book a session" button.

> "Life abroad" is our own idea, not from Chelsea. It suits her UK-based Bulgarian clients and very few competitors cover it.

### Footer pages

| Page | .co.uk | .bg | Notes |
|---|---|---|---|
| **FAQ** | `/faq` | `/chesto-zadavani-vaprosi` | Is it confidential? How many sessions? Online vs in person? Cancellations? |
| **Press / Featured in** | `/press` | `/medii` | BG BEN column, interviews, talks |
| **Crisis help** | `/crisis` | `/spesht-pomosht` | UK: 999, NHS 111, Samaritans 116 123. BG: 112. "I'm not an emergency service." |
| **Privacy policy** | `/privacy` | `/poveritelnost` | UK GDPR / EU GDPR – health data |
| **Cookies** | `/cookies` | `/biskvitki` | Cookie banner + policy |
| **Terms** | `/terms` | `/obshti-usloviya` | Booking, payment, cancellation terms |

### On every page

- Header: logo · menu · **BG / EN switch** · "Book a session" button
- Footer: contact details, hours, social links, crisis link, legal links
- Bottom of each page: "Ready to talk? Book a session" block

### Total to build first

**~22 page types**: 8 main pages, 4 "who I help" pages, 6–8 issue pages and 6 footer pages, each in two languages. Articles get added over time.

### Nice-to-have later

- Short FAQ videos (1–2 min, filmed on a phone)
- Testimonials. Check her professional body's rules first (HCPC / BPS in the UK, her Bulgarian society); many therapists avoid them for confidentiality reasons.
- Online booking calendar (Calendly / Cal.com) that shows UK and BG times
- Newsletter sign-up
