# Site addresses, shared by the site build (build.py) and the blog (blog.py).
# A page is identified by its route key (the English path); the Bulgarian site uses its own slugs.

DOMAINS = {'en': 'https://drvasileva.co.uk/', 'bg': 'https://drvasileva.bg/'}

# Page addresses on the Bulgarian site (route key -> URL); the English site uses the keys as they are
BG_SLUGS = {
    '/': '/', '/about': '/za-men', '/who-i-help': '/s-kogo-rabotya',
    '/who-i-help/adults': '/s-kogo-rabotya/vazrastni', '/who-i-help/couples-families': '/s-kogo-rabotya/dvoyki-i-semeystva',
    '/who-i-help/children-teens': '/s-kogo-rabotya/deca-i-tiyneydzhari', '/who-i-help/special-educational-needs': '/s-kogo-rabotya/specialni-obrazovatelni-potrebnosti',
    '/who-i-help/group-sessions': '/s-kogo-rabotya/grupovi-sesii', '/who-i-help/organisations': '/s-kogo-rabotya/organizacii',
    '/issues': '/problemi', '/issues/anxiety-panic': '/problemi/trevozhnost-i-panicheski-ataki', '/issues/depression': '/problemi/depresiya',
    '/issues/stress': '/problemi/stres', '/issues/relationships': '/problemi/problemi-v-dvoykata', '/issues/parenting-teens': '/problemi/roditeli-i-tiyneydzhari',
    '/issues/child-behaviour': '/problemi/povedenie-pri-detsata', '/issues/autism': '/problemi/autizam', '/issues/adhd': '/problemi/adhd',
    '/issues/learning-difficulties': '/problemi/obuchitelni-zatrudneniya', '/issues/bullying': '/problemi/tormoz-i-digitalno-nasilie',
    '/issues/living-abroad': '/problemi/zhivot-v-chuzhbina', '/articles': '/statii', '/publications': '/publikacii', '/fees': '/ceni',
    '/faq': '/chesto-zadavani-vaprosi', '/press': '/medii', '/contact': '/kontakti', '/crisis': '/spesht-pomosht',
    '/privacy': '/poveritelnost', '/cookies': '/biskvitki', '/terms': '/obshti-usloviya',
}
EN_SLUGS = {k: k for k in BG_SLUGS}
SLUGS = {'en': EN_SLUGS, 'bg': BG_SLUGS}

# The blog's pages are made by blog.py, not by the single-page app
BLOG_KEY = '/articles'
