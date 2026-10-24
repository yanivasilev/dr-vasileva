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

## 4. Suggested site pages

1. **Home** – who she is, who she helps, "Book a session"
2. **About** – bio, education, experience, awards
3. **Services** – what she offers, in person / online
4. **Prices & booking**
5. **Articles** – e.g. her "School of Psychology" columns
6. **Contact**
7. **Privacy policy & cookies**
