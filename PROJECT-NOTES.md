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
| Phone number | Her UK number | Her UK number |
| Chat button | **Viber** | **WhatsApp** |
| Socials | Facebook | Facebook |
| Address | Not shown | Not shown |
| Legal pages | Privacy policy under EU GDPR | Privacy policy under UK GDPR |

### Contact buttons

She has one phone number (UK), so both sites use it. Only the chat app changes:

- **drvasileva.bg → Viber** (what most people in Bulgaria use). Link: `viber://chat?number=%2B44XXXXXXXXXX`
- **drvasileva.co.uk → WhatsApp** (what most people in the UK use). Link: `https://wa.me/44XXXXXXXXXX`
- **Facebook** is her only social account, so it's linked in the footer of both sites.
- **No address on either site.** For in-person sessions in the UK, she gives the details when people message or call her.

> The Viber link only opens if the visitor has Viber installed (normal in Bulgaria). Show the number as text next to the button as a fallback.

### Google search – do's and don'ts

- **Do** add both domains to **Google Search Console**.
- **Do** add `hreflang` tags (one line in the page code). They tell Google "these two pages are the same page in two languages", so it shows the right one in each country and doesn't see them as duplicates.
- **Do** let the domains do the targeting: Google automatically treats `.bg` as Bulgaria and `.co.uk` as the UK.
- **Don't** auto-redirect people by their location. It confuses Google and annoys people (e.g. a Bulgarian living in London). Use the BG / EN button instead.

---

## 3. About Dr Vasileva (research)

### Dr Mirena Koleva Vasileva (д-р Мирена Колева Василева)

✅ Confirmed as our Dr Vasileva. **No awards were found online**, so we need those from her.

What the public sources say:

- **Doctorate (PhD)** in **educational and developmental psychology** (доктор по педагогическа и възрастова психология).
- About **20 years** of professional experience in psychology.
- Formerly **Chief Assistant Professor** at **Burgas Free University**, working in experimental and educational psychology.
- **Living in London since 2016.**
- Writes a column called **"School of Psychology" ("Училище по психология")** for the UK-based Bulgarian outlet **BG BEN** (bgben.co.uk). A June 2026 piece covered **digital violence / cyberbullying** ("Тишината на дигиталното насилие").

Source: bgben.co.uk – "В „Училище по психология“: Тишината на дигиталното насилие" (10 June 2026).

### Info we still need from her

- [ ] Full name as it should appear (BG + EN spelling)
- [ ] Photo(s)
- [ ] Qualifications, university, year of PhD
- [ ] Registrations (HCPC / BPS in the UK, Bulgarian society membership)
- [ ] **Awards** – names, years, who gave them (nothing found online)
- [ ] Specialisms (e.g. children, teens, parents, anxiety, cyberbullying…)
- [ ] Session length and prices: online in EUR (.bg); online and in person in GBP (.co.uk)
- [ ] UK phone number (used for Viber and WhatsApp)
- [ ] Facebook page link
- [ ] Email address
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
- **Her niche.** Her background is educational and developmental psychology, and children, teens, parents, schools and cyberbullying are exactly where Chelsea's offer is thinnest.

---

## 5. Our pages (sitemap)

Every page exists in both languages. URLs are in English on `.co.uk` and in Bulgarian (Latin letters) on `.bg`.

### Main menu

| # | Page | drvasileva.co.uk | drvasileva.bg | What's on it |
|---|---|---|---|---|
| 1 | **Home** | `/` | `/` | Photo, one-line promise, who I help, online & in person (.co.uk) / online only (.bg), "Featured in", call + chat buttons |
| 2 | **About me** | `/about` | `/za-men` | Story, education, PhD, experience, **awards**, registrations, languages, approach |
| 3 | **Who I help** | `/who-i-help` | `/s-kogo-rabotya` | Overview page, linking to 3a–3d |
| 3a | – Adults | `/who-i-help/adults` | `/s-kogo-rabotya/vazrastni` | Individual therapy |
| 3b | – Children & teens | `/who-i-help/children-teens` | `/s-kogo-rabotya/deca-i-tiyneydzhari` | Child and teen work |
| 3c | – Parents & families | `/who-i-help/parents` | `/s-kogo-rabotya/roditeli` | Parenting support, family sessions |
| 3d | – Schools | `/who-i-help/schools` | `/s-kogo-rabotya/uchilishta` | Talks, training, consultations *(if she does this)* |
| 4 | **What I help with** | `/issues` | `/problemi` | Grid of issue pages (see list below) |
| 5 | **Fees** | `/fees` | `/ceni` | **.co.uk:** GBP, online + in person. **.bg:** EUR, online only. Session length, how online sessions work, time zones UK ↔ BG, cancellation policy |
| 6 | **Articles** | `/articles` | `/statii` | Her writing, incl. the "School of Psychology" columns |
| 7 | **Contact** | `/contact` | `/kontakti` | **No form, no booking.** Big buttons: call her UK number, chat (**Viber** on .bg, **WhatsApp** on .co.uk), email, Facebook. Hours she answers. **No address or map** |

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

**Every issue page follows the same layout** (copied from Chelsea): what it is → signs → how I help → FAQ (3–5 questions) → "Call or message me" buttons.

> "Life abroad" is our own idea, not from Chelsea. It suits her UK-based Bulgarian clients and very few competitors cover it.

### Footer pages

| Page | .co.uk | .bg | Notes |
|---|---|---|---|
| **FAQ** | `/faq` | `/chesto-zadavani-vaprosi` | Is it confidential? How many sessions? How do online sessions work? Cancellations? (.co.uk also: online vs in person) |
| **Press / Featured in** | `/press` | `/medii` | BG BEN column, interviews, talks |
| **Crisis help** | `/crisis` | `/spesht-pomosht` | UK: 999, NHS 111, Samaritans 116 123. BG: 112. "I'm not an emergency service." |
| **Privacy policy** | `/privacy` | `/poveritelnost` | UK GDPR / EU GDPR – health data |
| **Cookies** | `/cookies` | `/biskvitki` | Cookie banner + policy |
| **Terms** | `/terms` | `/obshti-usloviya` | Payment and cancellation terms |

### On every page

- Header: logo · menu · **BG / EN switch** · "Contact me" button (goes to the contact page)
- Footer: UK phone number, chat button (Viber on .bg / WhatsApp on .co.uk), email, Facebook, hours, crisis link, legal links. No address.
- Bottom of each page: "Ready to talk? Call or message me" block with the phone and chat buttons

### Total to build first

**~21 page types**: 7 main pages, 4 "who I help" pages, 6–8 issue pages and 6 footer pages, each in two languages. Articles get added over time.

### Not included (decided)

- Google Business Profile
- Listings on other directories
- Address or map
- **No booking page, booking calendar or contact form.** People call or message her directly (phone, Viber/WhatsApp, email, Facebook).
- Newsletter

### Nice-to-have later

- Short FAQ videos (1–2 min, filmed on a phone)
- Testimonials. Check her professional body's rules first (HCPC / BPS in the UK, her Bulgarian society); many therapists avoid them for confidentiality reasons.
