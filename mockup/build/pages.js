
  /* =====================================================================
     Content
     ===================================================================== */
  const PHONE = '+44 7999 334778', TEL = 'tel:+447999334778';
  const WA = 'https://wa.me/447999334778', VIBER = 'viber://chat?number=%2B447999334778';
  const EMAIL = 'contact@drvasileva.co.uk', FB = 'https://www.facebook.com/share/1Bh2hqG1Ac/';

  const WHO = [
    { slug: 'adults', icon: 'i-user', title: 'Adults',
      lead: 'Individual sessions for adults who feel weighed down by anxiety, low mood, stress or a difficult period in life.',
      for: ['Worry, anxiety or panic attacks', 'Low mood or depression', 'Stress and burnout', 'Big life changes, including moving to a new country', 'Feeling stuck or not like yourself'],
      how: 'We use cognitive behavioural therapy (CBT) to understand the link between your thoughts, feelings and behaviour, and to build practical tools for everyday life. We set goals together and review them along the way.',
      issues: ['anxiety-panic', 'depression', 'stress', 'living-abroad'] },
    { slug: 'couples-families', icon: 'i-heart', title: 'Couples & families',
      lead: 'Support for couples and families who want to understand each other better and get through difficult times together.',
      for: ['Frequent arguments or growing distance', 'Communication difficulties', 'Changes such as a new baby, a move or a separation', 'Tension between parents and children', 'Rebuilding trust'],
      how: 'Sessions draw on CBT for couples and family therapy, with a focus on the role of emotions in how we relate to each other. Everyone gets a voice, and we work on practical steps you can take at home.',
      issues: ['relationships', 'parenting-teens'] },
    { slug: 'children-teens', icon: 'i-smile', title: 'Children & teenagers',
      lead: 'Consultations for children and teenagers, with parents involved every step of the way.',
      for: ['Worries, fears and anxiety', 'Anger, behaviour and emotional outbursts', 'Difficulties at school and bullying, including online', 'The ups and downs of the teenage years', 'Changes in the family'],
      how: 'I adapt every session to the child’s age, using conversation, play and creative methods. Parents are part of the process: I help you understand what is happening and how to support your child at home. For children under 18, a parent or guardian gives consent.',
      issues: ['child-behaviour', 'parenting-teens', 'bullying'] },
    { slug: 'special-educational-needs', icon: 'i-puzzle', title: 'Special educational needs',
      lead: 'Assessments, reports and practical support for children with special educational needs, and guidance for their families.',
      for: ['Autism spectrum', 'ADHD / ADD', 'Dyslexia and dyspraxia', 'Handwriting difficulties', 'Learning disabilities and developmental delays'],
      how: 'With a Diploma in Special Educational Needs & Disability and many years of work with children with additional needs, I offer psychological assessments and written reports, together with practical strategies for home and school.',
      issues: ['autism', 'adhd', 'learning-difficulties'] },
    { slug: 'group-sessions', icon: 'i-users', title: 'Group sessions',
      lead: 'Small, supportive groups where people working on similar themes can learn from each other.',
      for: ['People who would like support alongside others', 'Those who find it helpful to share and listen', 'Anyone looking for a gentle first step into therapy'],
      how: 'Groups run in Bulgarian and in English, online or in person. I guide every session and keep the group a safe, confidential space. Topics vary, so get in touch to hear about current and upcoming groups.',
      issues: ['stress', 'anxiety-panic', 'living-abroad'] },
    { slug: 'organisations', icon: 'i-building', title: 'Organisations & schools',
      lead: 'Dynamic, flexible group training for workplaces and schools.',
      for: ['Professional stress and burnout', 'Effective teamwork', 'Relationships: adult–child, child–child, adult–adult and employer–employee', 'Staff who work with children with special needs'],
      how: 'Training is tailored to your organisation and can be delivered online or in person, in Bulgarian or in English. Get in touch to talk about what your team or school needs.',
      issues: ['stress'] },
  ];

  const COL = {
    panic: ['Self-help for panic attacks and anxiety (part one)', 'https://bgben.co.uk/samopomosht-pri-panicheski-atakitrevozhnost-chast-purva'],
    holiday: ['Holiday stress and the invisible loneliness of the holidays', 'https://bgben.co.uk/praznichen-stres-i-nevidimata-samota-po-vreme-na-praznitsite-'],
    marriage: ['Several successful steps to preserve love in marriage', 'https://bgben.co.uk/nyakolko-uspeshni-stupki-za-suhranenie-na-lyubovta-v-braka'],
    teens: ['How parents can help their children in adolescence', 'https://bgben.co.uk/files/pdf_1739663167_482.pdf'],
    violence: ['Practical guidelines for preventing violence in children', 'https://bgben.co.uk/prakticheski-nasoki-za-predotvratyavane-na-nasilieto-pri-detsata'],
    digital: ['The silence of digital violence', 'https://bgben.co.uk/v-uchilishte-po-psihologiya-tishinata-na-digitalnoto-nasilie'],
    fears: ['How fears and emotions make us sick', 'https://bgben.co.uk/files/pdf_1739663445_490.pdf'],
    peace: ['Why it is important to make peace with ourselves', 'https://bgben.co.uk/zashto-e-vazhno-da-se-pomirim-sus-sebe-si'],
  };

  const ASSESS_NOTE = 'I provide psychological assessments and written reports. A formal diagnosis can also involve other specialists, such as a paediatrician or psychiatrist. I will explain the next steps clearly.';
  const ISSUES = [
    { slug: 'anxiety-panic', icon: 'i-sun', title: 'Anxiety & panic attacks', short: 'Constant worry, racing thoughts or sudden waves of fear.',
      about: 'Anxiety is the body’s natural alarm system. It becomes a problem when the alarm is too loud or goes off when there is no real danger. Panic attacks can feel frightening and come out of nowhere.',
      signs: ['Constant worry that is hard to control', 'A racing heart, shortness of breath or dizziness', 'Avoiding places or situations', 'Trouble sleeping or concentrating', 'Sudden waves of intense fear'],
      help: 'CBT is one of the most researched approaches for anxiety and panic. Together we look at what keeps the anxiety going and practise tools to calm the body and to question anxious thoughts.',
      faq: [['Can anxiety be treated?', 'Yes. With the right support and practical tools, many people learn to manage anxiety well and feel more in control.'], ['Are panic attacks dangerous?', 'They feel very frightening but are not dangerous in themselves. It is still a good idea to check any physical symptoms with your doctor.']],
      col: 'panic' },
    { slug: 'depression', icon: 'i-cloud', title: 'Depression', short: 'Low mood, no energy, and losing interest in things.',
      about: 'Depression is more than feeling sad. It can drain your energy, change the way you see yourself and make everyday tasks feel heavy.',
      signs: ['Low mood on most days', 'Losing interest in things you used to enjoy', 'Tiredness and low energy', 'Changes in sleep or appetite', 'Feelings of guilt or worthlessness'],
      help: 'CBT helps you notice the patterns that keep low mood going and take small, manageable steps back towards the things that matter to you.',
      faq: [['Should I see my doctor as well?', 'It is a good idea to talk to your GP or doctor too, especially if your symptoms are severe or you are thinking about medication.'], ['What if I have thoughts of harming myself?', 'Please get help straight away. Call 999 in the UK or 112 in Bulgaria, or see the Crisis help page for 24/7 support lines.']],
      col: 'peace' },
    { slug: 'stress', icon: 'i-flame', title: 'Stress & burnout', short: 'Feeling overwhelmed, exhausted and unable to switch off.',
      about: 'Some stress is part of life. When pressure builds up for too long, it starts to affect your body, your mood and your relationships.',
      signs: ['Feeling overwhelmed', 'Irritability or a short temper', 'Headaches or muscle tension', 'Poor sleep', 'Finding it hard to switch off'],
      help: 'We identify where your stress comes from, build coping strategies that fit your life and work on healthier boundaries, at work and at home.',
      faq: [['Is it stress or burnout?', 'Burnout is long-term exhaustion, often linked to work, where you feel empty and detached. If stress has gone on for months, it is worth talking about.'], ['Can you help my team at work?', 'Yes. I run group training on professional stress and teamwork for organisations and schools.']],
      col: 'holiday' },
    { slug: 'relationships', icon: 'i-heart', title: 'Couple & relationship problems', short: 'Repeated arguments, distance or a loss of trust.',
      about: 'Every relationship goes through difficult times. When the same arguments keep repeating or you feel far apart, talking with someone neutral can help.',
      signs: ['The same arguments again and again', 'Feeling unheard or misunderstood', 'Losing closeness', 'Problems with trust', 'Difficulty adjusting to big changes'],
      help: 'In couples sessions we look at how emotions shape the way you interact, and practise new ways of listening and communicating.',
      faq: [['Do we both need to come?', 'Ideally yes, but you are also welcome to start on your own.'], ['Do couples sessions work online?', 'Yes. Many couples find online sessions just as helpful, and easier to fit into busy lives.']],
      col: 'marriage' },
    { slug: 'parenting-teens', icon: 'i-users', title: 'Parents & the teenage years', short: 'Conflict, withdrawal and finding a way to reconnect.',
      about: 'Adolescence is a time of big change for the whole family. My doctoral research looked at how the family environment shapes the way teenagers experience and cope with stress.',
      signs: ['Constant conflict at home', 'Your teenager withdrawing or shutting you out', 'Mood swings', 'Not wanting to go to school', 'Not knowing how to reach your child any more'],
      help: 'I work with teenagers and parents, separately and together, to rebuild communication and find parenting strategies that really work.',
      faq: [['Will you tell me what my teenager says?', 'Sessions are confidential, which helps teenagers open up. If there is a risk to their safety, I will always act. We agree together what parents need to know.'], ['Can parents come without their child?', 'Yes. Parent-only sessions can be a very good place to start.']],
      col: 'teens' },
    { slug: 'child-behaviour', icon: 'i-smile', title: 'Behavioural difficulties in children', short: 'Tantrums, aggression or trouble following rules.',
      about: 'Tantrums, aggression or defiance are often a child’s way of communicating something they cannot yet put into words.',
      signs: ['Frequent emotional outbursts', 'Aggression towards others', 'Difficulty following rules', 'Problems at school', 'Worries that show up as behaviour'],
      help: 'I help you understand what is behind the behaviour, and give you practical, consistent strategies to use at home and at school.',
      faq: [['Is it just a phase?', 'Sometimes it is. If the behaviour lasts for months or affects family life or school, it is worth getting support.'], ['Do parents take part?', 'Yes. Parents are an important part of the work.']],
      col: 'violence' },
    { slug: 'autism', icon: 'i-puzzle', title: 'Autism spectrum', short: 'Understanding and supporting autistic children.',
      about: 'Autistic children experience and process the world differently. With the right understanding and support, they can thrive.',
      signs: ['Differences in communication and social interaction', 'A strong need for routine', 'Sensitivity to sounds, light or touch', 'Intense, focused interests'],
      help: 'I offer psychological assessment and reports, and support families with strategies for communication, routines and managing emotions.',
      faq: [['Do you diagnose autism?', ASSESS_NOTE], ['Can you work with my child’s school?', 'Yes. I can suggest practical strategies to support your child at school.']] },
    { slug: 'adhd', icon: 'i-zap', title: 'ADHD / ADD', short: 'Difficulties with attention, focus and restlessness.',
      about: 'Difficulties with attention, focus or restlessness can make school and family life very hard, for children and for parents.',
      signs: ['Trouble concentrating', 'Being easily distracted', 'Restlessness or fidgeting', 'Acting before thinking', 'Often forgetting or losing things'],
      help: 'Assessment and a written report, plus practical strategies for attention, organisation and behaviour at home and at school.',
      faq: [['Do you diagnose ADHD?', ASSESS_NOTE], ['Can adults have ADHD too?', 'Yes. If you recognise these signs in yourself, get in touch and we can talk about the next steps.']] },
    { slug: 'learning-difficulties', icon: 'i-pen', title: 'Dyslexia, dyspraxia & learning difficulties', short: 'Reading, writing, handwriting or coordination.',
      about: 'Some children find reading, writing, handwriting or coordination much harder than their classmates, even when they are trying their very best.',
      signs: ['Difficulty with reading or spelling', 'Slow or untidy handwriting', 'Clumsiness or coordination difficulties', 'Falling behind at school', 'Low confidence about learning'],
      help: 'Assessment and a written report, practical strategies (including "Handwriting: cracking the code and mastering the skills") and support with confidence.',
      faq: [['What happens in an assessment?', 'We meet, I use structured tasks suited to your child’s age, and you receive a written report with clear recommendations.'], ['Can the report be shared with school?', 'Yes. Reports are written so that parents and teachers can use them.']] },
    { slug: 'bullying', icon: 'i-shield', title: 'Bullying & digital violence', short: 'At school or online, often in silence.',
      about: 'Bullying, in person or online, can leave a child feeling ashamed, alone and afraid to speak. Digital violence often happens silently, behind a screen.',
      signs: ['Not wanting to go to school', 'Being upset after using their phone or computer', 'Withdrawing from friends and family', 'Sleep problems', 'Unexplained injuries or lost belongings'],
      help: 'I help children talk about what is happening and rebuild their confidence, and I guide parents on how to respond and help keep their child safe online.',
      faq: [['My child won’t tell me anything. What can I do?', 'Stay calm, listen without judging and let them know they are not in trouble. Talking to someone outside the family can make it easier to open up.'], ['Should I contact the school?', 'Usually yes. I can help you plan what to say.']],
      col: 'digital' },
    { slug: 'living-abroad', icon: 'i-globe', title: 'Life abroad', short: 'Homesickness, loneliness and life between two cultures.',
      about: 'Moving to a new country brings new opportunities, but also loneliness, homesickness and pressure. I know this from my own life between Bulgaria and the UK.',
      signs: ['Loneliness or isolation', 'Homesickness', 'Feeling caught between two cultures', 'Stress of adapting to a new system', 'Tension in the family after a move'],
      help: 'Sessions in Bulgarian give you a space to talk in your own language, with someone who understands both worlds.',
      faq: [['Can we talk in Bulgarian?', 'Yes, of course. All sessions are available in Bulgarian or in English.'], ['I live in Bulgaria. Can I still book?', 'Yes. Online sessions work wherever you are.']],
      col: 'holiday' },
  ];

  const FAQ = [
    ['Is everything I say confidential?', 'Yes. What you share stays between us. The only exception is if I believe you or someone else, especially a child, is at serious risk of harm. Then I may have to inform the right services, as the law and my professional code require. I would always try to talk to you about it first.'],
    ['What languages do you work in?', 'Bulgarian and English. This includes individual, couples, family and group sessions.'],
    ['Do you offer online or in-person sessions?', 'Both. Online sessions take place over a secure video call, so you can join from anywhere: the UK, Bulgaria or elsewhere. In-person sessions take place in the UK. I share the location when we arrange your appointment.'],
    ['How do I make an appointment?', 'Simply get in touch by phone, Viber, WhatsApp, email or Facebook. Tell me a little about what you need, and we’ll find a time that suits you.'],
    ['How long is a session?', 'Session length will be confirmed soon.'],
    ['How many sessions will I need?', 'It depends on you and what you’d like to work on. Some people feel a difference after a few sessions, others prefer longer support. We’ll agree a plan together at the start and review your progress along the way.'],
    ['What approach do you use?', 'Mainly cognitive behavioural therapy (CBT), a practical, well-researched approach. It helps you understand the link between your thoughts, feelings and behaviour, and learn tools to change them.'],
    ['Do you work with children and teenagers?', 'Yes. I have many years of experience with children, teenagers and children with special educational needs (autism, ADHD, dyslexia, dyspraxia and other learning difficulties). Parents are involved, and for children under 18 a parent or guardian gives consent.'],
    ['Do you work with couples and families?', 'Yes. I offer couples therapy and family therapy, helping you understand each other, communicate better and get through difficult times together.'],
    ['What are group sessions?', 'Small groups of people working on similar topics, guided by me. They run in Bulgarian and in English, online or in person. Groups are a supportive way to learn from others who understand what you’re going through.'],
    ['Do you offer training for organisations and schools?', 'Yes. I run group trainings on topics such as professional stress, effective teamwork and relationships at work and at school.'],
    ['How much does it cost?', 'Prices will be published on the Fees page soon.'],
    ['How do I pay?', 'By bank transfer or Revolut.'],
    ['What if I need to cancel?', 'Please give at least 24 hours’ notice. Sessions cancelled with less notice may be charged in full.'],
    ['I live in Bulgaria and you’re in the UK. What about the time difference?', 'No problem. Bulgaria is 2 hours ahead of the UK. We always agree the time in your local time zone.'],
    ['Do I need a referral from my doctor?', 'No. You can contact me directly.'],
    ['What if I’m in crisis?', 'I’m not an emergency service. If you or someone else is in immediate danger, call 999 in the UK or 112 in Bulgaria. In the UK you can also call Samaritans on 116 123 (free, 24/7). See the Crisis help page for more.'],
  ];

  const PUBS = [
    'Gertcheva-Nesterova, G., <b>Vasileva, M.</b> (2014). Specificity of interference of stress "parent–child". <i>Applied Psychology and Social Practice</i>, conference proceedings. Varna Free University.',
    '<b>Vasileva, M.</b> (2011). Conflict interactions between parents and adolescents as a manifestation of conflict interaction parent–child and coping strategies. <i>Applied Psychology and Social Practice</i>. Varna Free University.',
    '<b>Vasileva, M.</b> (2011). Relationships between parents and adolescents. <i>e-Journal VFU</i>, issue 3, Varna.',
    '<b>Vasileva, M.</b> (2011). Effects of stress on the family climate. <i>Applied Psychology and Social Practice</i>. Varna Free University.',
    'Gertcheva-Nesterova, G., <b>Vasileva, M.</b> (2010). Parental behaviour styles. <i>Applied Psychology and Social Practice</i>. Varna Free University.',
    '<b>Vasileva, M.</b> (2010). Effects of stress on the family climate and upbringing of children. <i>Proceedings of the Union of Scientists – Varna</i>.',
    '<b>Vasileva, M.</b> (2007). Effects of stress on the family climate and upbringing of children. <i>Applied Psychology and Social Practice</i>. Varna Free University.',
    '<b>Vasileva, M.</b> (2007). The art of being a parent. <i>Psychology Journal</i>, issue 38, Varna.',
    '<b>Vasileva, M.</b> (2007). The problem of anxiety and aggression in adolescence. <i>Psychology Journal</i>, issue 39, Varna.',
    '<b>Vasileva, M.</b> (2007). Aggressiveness as a phenomenon and problem. Factors of aggression in adolescence. <i>Psychology Journal</i>, issue 41, Varna.',
  ];

  /* =====================================================================
     Building blocks
     ===================================================================== */
  const logo = (file, alt, w, h) => `<span class="ico logo-tile"><img src="../images/logos/${file}" alt="${alt}" width="${w}" height="${h}" loading="lazy"></span>`;
  const ic = (id, cls = 'icon') => `<svg class="${cls}"><use href="#${id}"/></svg>`;
  const ctaButtons = `
    <a class="btn btn-whatsapp" href="${WA}">${ic('b-whatsapp', 'bi')}WhatsApp</a>
    <a class="btn btn-viber" href="${VIBER}">${ic('b-viber', 'bi')}Viber</a>
    <a class="btn btn-cream" href="${TEL}">${ic('i-phone')}Call</a>`;
  const hero = ({ crumbs = [], eyebrow, title, lead, icon }) => `
    <section class="page-hero grain on-dark">
      <span class="blob b1"></span><span class="blob b2"></span>
      ${icon ? `<svg class="icon hero-icon"><use href="#${icon}"/></svg>` : ''}
      <div class="wrap">
        <nav class="crumbs" aria-label="Breadcrumb"><a href="#/">Home</a>${crumbs.map(([t, h]) => h ? `<span><a href="${h}">${t}</a></span>` : `<span>${t}</span>`).join('')}</nav>
        ${eyebrow ? `<span class="eyebrow" data-reveal>${eyebrow}</span>` : ''}
        <h1 data-reveal style="--d:.05s">${title}</h1>
        ${lead ? `<p class="lead" data-reveal style="--d:.12s">${lead}</p>` : ''}
      </div>
    </section>`;
  const ctaBand = (title = 'Ready to <em>talk</em>?', text = 'Call or message me in Bulgarian or English. We’ll find a time that suits you.') => `
    <section class="cta-band"><div class="wrap"><div class="cta-box grain on-dark" data-reveal>
      <div><h2>${title}</h2><p>${text}</p></div>
      <div class="btn-row">${ctaButtons}</div>
    </div></div></section>`;
  const contactBox = `
    <div class="box dark grain on-dark"><h3>Talk to me</h3><p>Online or in person, in Bulgarian or English.</p>
      <div class="btn-row">
        <a class="btn btn-whatsapp" href="${WA}">${ic('b-whatsapp', 'bi')}WhatsApp</a>
        <a class="btn btn-viber" href="${VIBER}">${ic('b-viber', 'bi')}Viber</a>
        <a class="btn btn-cream" href="${TEL}">${ic('i-phone')}${PHONE}</a>
      </div></div>`;
  const faqList = items => `<div class="faq">${items.map(([q, a]) => `<details data-reveal><summary>${q}<span class="plus"></span></summary><div class="answer"><p>${a}</p></div></details>`).join('')}</div>`;
  const issueBy = s => ISSUES.find(i => i.slug === s);

  /* =====================================================================
     Pages
     ===================================================================== */
  const PAGES = {};

  PAGES['/about'] = () => `
    ${hero({ crumbs: [['About me']], eyebrow: 'About me', title: 'Hello, I’m <em>Mirena</em>', lead: 'Dr Mirena Vasileva, PhD · Psychologist &amp; CBT Psychotherapist', icon: 'i-leaf' })}
    <section class="page-body"><div class="wrap split">
      <div class="prose">
        <div class="about-photo" data-reveal="left" style="max-width:520px;margin-bottom:56px"><span class="frame"></span><div class="img"><img src="../images/dr-vasileva.jpg" alt="Dr Mirena Vasileva" width="1242" height="1242" loading="lazy"></div><div class="years"><strong><span class="js-count" data-to="${YEARS}">0</span><sup>+</sup></strong><span>years of experience</span></div></div>
        <p data-reveal>For ${YEARS} years, since 2005, I have been doing the work I love most: helping people understand themselves, heal and find their way forward. I’m a psychologist and cognitive behavioural therapist (CBT) with a PhD in Pedagogical and Developmental Psychology. I work with adults, couples, families, children and teenagers.</p>
        <p data-reveal>My path began in Bulgaria. For eight years I worked as a psychologist at a home for children with intellectual disabilities near Nessebar, where I learned that every child, whatever their needs, deserves to be truly seen. Alongside that, I built my private practice, worked as a psychotherapist at Viva Clinic in Sunny Beach, and taught Experimental and Pedagogical Psychology at Burgas Free University as a Chief Assistant Professor.</p>
        <p data-reveal>In 2016 I moved to London. Since then I have worked with clients at the Doctors 4 You and Medi-Park clinics, and supported children with special educational needs at the Bulgarian school "Rodna Rech". Many of the people I see know what it’s like to build a life between two countries. So do I.</p>
        <p data-reveal>My doctoral research explored how the family environment shapes the way teenagers experience and cope with stress. It still guides my work today: I believe that when we understand the relationships around us, we can change the way we feel.</p>
        <p data-reveal>In our sessions I mainly use CBT, a practical approach backed by research. Together we look at the link between your thoughts, feelings and behaviour, and find tools that work in your everyday life. I listen without judgement, and we go at your pace.</p>
        <p data-reveal>Since 2023 I have written the "School of Psychology" column in BG BEN, the newspaper for Bulgarians in the UK. Outside the therapy room, I organise charity campaigns for children with intellectual disabilities and children without parental care.</p>
        <p data-reveal>Whether you’re facing anxiety, a difficult relationship, worries about your child, or you simply feel stuck, you don’t have to go through it alone. Call or message me, in Bulgarian or in English.</p>

        <h2 data-reveal>Experience</h2>
        <ol class="timeline" data-reveal>
          <li><span class="when">2018 – now</span><b>Psychologist, Medi-Park Clinic</b><span>London</span></li>
          <li><span class="when">2016 – now</span><b>Psychologist, Doctors 4 You</b><span>London</span></li>
          <li><span class="when">2018 – 2019</span><b>Psychologist, BG Medical Clinic</b><span>London</span></li>
          <li><span class="when">2015 – 2017</span><b>Assistant teacher, special educational needs</b><span>Bulgarian School "Rodna Rech", London</span></li>
          <li><span class="when">2015 – 2018</span><b>Chief Assistant Professor</b><span>Experimental &amp; Pedagogical Psychology, Burgas Free University</span></li>
          <li><span class="when">2013 – 2016</span><b>Psychotherapist, Viva Clinic</b><span>Sunny Beach, Bulgaria</span></li>
          <li><span class="when">2007 – 2015</span><b>Psychologist, "St. Stiliyan Paflagoniyski" children’s home</b><span>Nessebar municipality, Bulgaria</span></li>
          <li><span class="when">2007 – now</span><b>Private practice</b><span>Bulgaria → United Kingdom</span></li>
        </ol>

        <h2 data-reveal>Education</h2>
        <ol class="timeline" data-reveal>
          <li><span class="when">2009 – 2013</span><b>PhD in Pedagogical &amp; Developmental Psychology</b><span>"Family environment and experiencing stress in adolescence" · Varna Free University "Chernorizets Hrabar"</span></li>
          <li><span class="when">2005 – 2006</span><b>MA Psychology, Psychology &amp; Developmental Psychopathology</b><span>"Stress effects on the family environment and the upbringing of children" · Varna Free University</span></li>
          <li><span class="when">2000 – 2005</span><b>BA Psychology</b><span>"Anxiety and aggression in adolescents" · Varna Free University</span></li>
        </ol>

        <h2 data-reveal>Qualifications &amp; memberships</h2>
        <ul class="ticks" data-reveal>
          <li>Member, British Psychological Society</li>
          <li>Member, Bulgarian Psychological Society</li>
          <li>Diploma in Cognitive Behavioural Therapy (CBT)</li>
          <li>Diploma in Special Educational Needs &amp; Disability (SEND)</li>
          <li>Certificate in CBT and Counselling</li>
          <li>CBT training, Bulgarian Association of Cognitive-Behavioural Psychotherapy</li>
          <li>Therapeutic Crisis Intervention training</li>
          <li>Safeguarding Children Level 3 · Safeguarding Vulnerable Adults · NSPCC Child Protection</li>
        </ul>

        <h2 data-reveal>Awards</h2>
        <div class="recog-grid" style="margin-top:20px">
          <div class="award" data-reveal><span class="year">2006</span><span class="wreath"><svg aria-hidden="true"><use href="#laurel"/></svg><span class="inner">${ic('i-ring')}</span></span><h3>Gold Ring of Varna Free University</h3><p>For graduating with honours.</p><span class="by"><img src="../images/logos/varna-free-university.png" alt="" width="500" height="225">Varna Free University</span></div>
          <div class="award" data-reveal style="--d:.1s"><span class="year">2006</span><span class="wreath"><svg aria-hidden="true"><use href="#laurel"/></svg><span class="inner">1st</span></span><h3>First Prize, Best Master’s Thesis</h3><p>"Best diploma thesis" competition.</p><span class="by"><img src="../images/logos/varna-free-university.png" alt="" width="500" height="225">Varna Free University</span></div>
        </div>
      </div>
      <aside class="aside">
        <div class="box" data-reveal><h3>Quick facts</h3><ul class="facts">
          <li>${ic('i-cap')}PhD in Pedagogical &amp; Developmental Psychology</li>
          <li>${ic('i-bulb')}CBT Psychotherapist</li>
          <li>${ic('i-award')}Gold Ring · First Prize, Best Master’s Thesis</li>
          <li>${ic('i-globe')}Sessions in Bulgarian &amp; English</li>
          <li>${ic('i-video')}Online &amp; in person</li>
          <li>${ic('i-feather')}"School of Psychology" columnist, BG BEN</li>
        </ul></div>
        <div class="box" data-reveal><h3>Studied at &amp; member of</h3><div class="affil">
          <img src="../images/logos/varna-free-university.png" alt="Varna Free University Chernorizets Hrabar" width="500" height="225" loading="lazy">
          <img src="../images/logos/bps.png" alt="The British Psychological Society" width="400" height="200" loading="lazy">
          <div class="affil-row"><img src="../images/logos/bulgarian-psychological-society.png" alt="" width="208" height="208" loading="lazy"><span>Bulgarian Psychological Society</span></div>
        </div></div>
        <div data-reveal>${contactBox}</div>
      </aside>
    </div></section>
    ${ctaBand()}`;

  PAGES['/who-i-help'] = () => `
    ${hero({ crumbs: [['Who I help']], eyebrow: 'Who I help', title: 'Support for every <em>stage</em> of life', lead: 'Whatever you’re going through, on your own or with the people close to you, we’ll find a way forward at your pace.', icon: 'i-users' })}
    <section class="page-body"><div class="wrap"><div class="cards">${WHO.map((w, i) => `
      <a class="card" href="#/who-i-help/${w.slug}" data-reveal style="--d:${(i % 3) * .08}s"><span class="num">0${i + 1}</span><span class="ico">${ic(w.icon)}</span><h3>${w.title.replace('&', '&amp;')}</h3><p>${w.lead}</p><span class="go">${ic('i-arrow')}</span></a>`).join('')}
    </div></div></section>
    ${ctaBand()}`;

  WHO.forEach(w => {
    PAGES['/who-i-help/' + w.slug] = () => `
      ${hero({ crumbs: [['Who I help', '#/who-i-help'], [w.title]], eyebrow: 'Who I help', title: w.title, lead: w.lead, icon: w.icon })}
      <section class="page-body"><div class="wrap split">
        <div class="prose">
          <h2 data-reveal>Who it’s for</h2>
          <ul class="ticks" data-reveal>${w.for.map(f => `<li>${f}</li>`).join('')}</ul>
          <h2 data-reveal>How I can help</h2>
          <p data-reveal>${w.how}</p>
          <div class="note" data-reveal>${ic('i-globe')}<span>Available in <b>Bulgarian and English</b>, <b>online or in person</b>.</span></div>
        </div>
        <aside class="aside">
          <div class="box" data-reveal><h3>Related topics</h3><div class="links-list">${w.issues.map(s => `<a href="#/issues/${s}">${issueBy(s).title}${ic('i-arrow')}</a>`).join('')}</div></div>
          <div data-reveal>${contactBox}</div>
        </aside>
      </div></section>
      ${ctaBand()}`;
  });

  PAGES['/issues'] = () => `
    ${hero({ crumbs: [['What I help with']], eyebrow: 'What I help with', title: 'You don’t have to <em>name</em> it to get help', lead: 'Here are some of the things I work with most often. If you don’t see yours, just get in touch.', icon: 'i-sun' })}
    <section class="page-body"><div class="wrap"><div class="issue-grid">${ISSUES.map((x, i) => `
      <a class="issue" href="#/issues/${x.slug}" data-reveal style="--d:${(i % 3) * .07}s"><span class="ico">${ic(x.icon)}</span><span><h3>${x.title.replace('&', '&amp;')}</h3><p>${x.short}</p></span></a>`).join('')}
    </div></div></section>
    ${ctaBand()}`;

  ISSUES.forEach(x => {
    PAGES['/issues/' + x.slug] = () => `
      ${hero({ crumbs: [['What I help with', '#/issues'], [x.title]], eyebrow: 'What I help with', title: x.title, lead: x.short, icon: x.icon })}
      <section class="page-body"><div class="wrap split">
        <div class="prose">
          <h2 data-reveal>What it is</h2>
          <p data-reveal>${x.about}</p>
          <h2 data-reveal>Common signs</h2>
          <ul class="ticks" data-reveal>${x.signs.map(s => `<li>${s}</li>`).join('')}</ul>
          <h2 data-reveal>How I can help</h2>
          <p data-reveal>${x.help}</p>
          ${x.col ? `<a class="read-more" href="${COL[x.col][1]}" target="_blank" rel="noopener" data-reveal><span class="ri">${ic('i-news')}</span><span><small>Read my column</small><b>${COL[x.col][0]}</b></span></a>` : ''}
          <h2 data-reveal>Questions</h2>
          ${faqList(x.faq)}
        </div>
        <aside class="aside">
          <div data-reveal>${contactBox}</div>
          <div class="box" data-reveal><h3>Other topics</h3><div class="links-list">${ISSUES.filter(o => o.slug !== x.slug).slice(0, 5).map(o => `<a href="#/issues/${o.slug}">${o.title}${ic('i-arrow')}</a>`).join('')}<a href="#/issues">See all${ic('i-arrow')}</a></div></div>
        </aside>
      </div></section>
      ${ctaBand()}`;
  });

  PAGES['/articles'] = () => `
    ${hero({ crumbs: [['Articles']], eyebrow: 'Articles &amp; publications', title: 'School of <em>Psychology</em>', lead: 'My column in BG BEN, the newspaper for Bulgarians in the UK, together with my scientific publications.', icon: 'i-feather' })}
    <section class="page-body"><div class="wrap">
      <div class="tabs" role="group" aria-label="Filter by topic" data-reveal>
        <button class="tab" aria-pressed="true" data-filter="all">All</button>
        <button class="tab" aria-pressed="false" data-filter="anxiety">Anxiety &amp; stress</button>
        <button class="tab" aria-pressed="false" data-filter="parents">Parents &amp; children</button>
        <button class="tab" aria-pressed="false" data-filter="relationships">Relationships</button>
        <button class="tab" aria-pressed="false" data-filter="growth">Self-growth</button>
      </div>
      <div class="articles-grid">${articleCards()}</div>
      <div class="note" style="margin-top:40px">${ic('i-feather')}<span>On the finished site each column will have its own page with the full text in Bulgarian and English. For now the links open the original on BG BEN.</span></div>
    </div></section>
    <section class="page-body" style="background:var(--white)"><div class="wrap split">
      <div class="prose">
        <h2 data-reveal>Scientific publications</h2>
        <p data-reveal>Selected publications on the family environment, parent–child relationships and stress in adolescence. <b>PhD thesis:</b> <i>Family environment and experiencing stress in adolescence</i> (2013).</p>
        <ol class="pubs" data-reveal>${PUBS.map(p => `<li><span>${p}</span></li>`).join('')}</ol>
      </div>
      <aside class="aside"><div class="box" data-reveal><h3>Interviews</h3><div class="links-list">
        <a href="#/press">"Suicide is often a cry to be noticed" · <i>Doctor</i> (Zdraveto), 2015${ic('i-arrow')}</a>
        <a href="#/press">"Covid-19 and panic attacks" · BG Radio, 2019${ic('i-arrow')}</a>
      </div></div></aside>
    </div></section>
    ${ctaBand()}`;

  PAGES['/fees'] = () => `
    ${hero({ crumbs: [['Fees']], eyebrow: 'Fees', title: 'Fees &amp; <em>payment</em>', lead: 'Clear prices, no surprises. Prices will be confirmed soon.', icon: 'i-calendar' })}
    <section class="page-body"><div class="wrap">
      <div data-reveal style="overflow-x:auto"><table class="fees-table">
        <thead><tr><th>Session</th><th>Online</th><th>In person (UK)</th></tr></thead>
        <tbody>
          <tr><td>Individual session<small>Adults</small></td><td><span class="tbc">£ / € to be confirmed</span></td><td><span class="tbc">£ to be confirmed</span></td></tr>
          <tr><td>Couples session</td><td><span class="tbc">£ / € to be confirmed</span></td><td><span class="tbc">£ to be confirmed</span></td></tr>
          <tr><td>Family session</td><td><span class="tbc">£ / € to be confirmed</span></td><td><span class="tbc">£ to be confirmed</span></td></tr>
          <tr><td>Child or teenager session</td><td><span class="tbc">£ / € to be confirmed</span></td><td><span class="tbc">£ to be confirmed</span></td></tr>
          <tr><td>Group session<small>Per person</small></td><td><span class="tbc">£ / € to be confirmed</span></td><td><span class="tbc">£ to be confirmed</span></td></tr>
          <tr><td>Psychological assessment &amp; report</td><td><span class="tbc">£ / € to be confirmed</span></td><td><span class="tbc">£ to be confirmed</span></td></tr>
          <tr><td>Training for organisations &amp; schools</td><td colspan="2">Price on request</td></tr>
        </tbody>
      </table></div>
      <div class="info-grid">
        <div class="box" data-reveal><span class="ico">${ic('i-card')}</span><h3>Payment</h3><p>By <b>bank transfer</b> or <b>Revolut</b>.</p></div>
        <div class="box" data-reveal style="--d:.08s"><span class="ico">${ic('i-calendar')}</span><h3>Cancellation</h3><p>Please give at least <b>24 hours’ notice</b>. Sessions cancelled later may be charged in full.</p></div>
        <div class="box" data-reveal style="--d:.16s"><span class="ico">${ic('i-clock')}</span><h3>Time zones</h3><p>Bulgaria is 2 hours ahead of the UK. Times are always agreed in <b>your</b> local time.</p></div>
      </div>
    </div></section>
    ${ctaBand()}`;

  PAGES['/faq'] = () => `
    ${hero({ crumbs: [['FAQ']], eyebrow: 'FAQ', title: 'Questions &amp; <em>answers</em>', lead: 'If your question isn’t here, just get in touch.', icon: 'i-chat' })}
    <section class="page-body"><div class="wrap split"><div>${faqList(FAQ)}</div><aside class="aside"><div data-reveal>${contactBox}</div></aside></div></section>
    ${ctaBand()}`;

  PAGES['/press'] = () => `
    ${hero({ crumbs: [['Press']], eyebrow: 'Press', title: 'Featured <em>in</em>', lead: 'Columns, interviews and lectures.', icon: 'i-mic' })}
    <section class="page-body"><div class="wrap"><div class="issue-grid">
      <a class="issue" href="#/articles" data-reveal>${logo('bg-ben.png', 'BG BEN', 400, 400)}<span><h3>BG BEN</h3><p>"School of Psychology", my regular column, 2023 – now.</p></span></a>
      <div class="issue" data-reveal style="--d:.07s">${logo('zdraveto.png', 'Zdraveto (blitz.bg)', 326, 100).replace('logo-tile', 'logo-tile wide')}<span><h3>"Doctor" newspaper</h3><p>Published by Zdraveto (blitz.bg). Interview: "Suicide is often a cry to be noticed", issue 15, 2015.</p></span></div>
      <div class="issue" data-reveal style="--d:.14s">${logo('bg-radio.png', 'BG Radio', 203, 203)}<span><h3>BG Radio</h3><p>Interview: "Covid-19 and panic attacks", 2019.</p></span></div>
      <div class="issue" data-reveal><span class="ico">${ic('i-cap')}</span><span><h3>Burgas Free University</h3><p>Lectures in Experimental and Pedagogical Psychology, art therapy in crisis intervention, and family stress in adolescence.</p></span></div>
      <div class="issue" data-reveal style="--d:.07s"><span class="ico">${ic('i-award')}</span><span><h3>Bulgarian Academy of Sciences</h3><p>Six scientific and applied contributions from my doctoral research.</p></span></div>
    </div></div></section>
    ${ctaBand()}`;

  PAGES['/contact'] = () => `
    <section class="contact grain on-dark" style="padding-top:170px">
      <span class="blob b2"></span>
      <div class="wrap contact-grid">
        <div>
          <nav class="crumbs" aria-label="Breadcrumb"><a href="#/">Home</a><span>Contact</span></nav>
          <span class="eyebrow" data-reveal>Get in touch</span>
          <h1 data-reveal style="--d:.05s">You don't have to go through it <em>alone</em></h1>
          <p class="lead" data-reveal style="--d:.1s">Call or message me in Bulgarian or English. Tell me a little about what you need, and we'll find a time that suits you.</p>
          <div class="contact-note">${ic('i-lock')}Everything you share is confidential.</div>
          <div class="contact-note">${ic('i-video')}Online sessions anywhere · in person in the UK.</div>
        </div>
        ${document.querySelector('#home-tiles').outerHTML.replace('id="home-tiles"', '')}
      </div>
    </section>`;

  PAGES['/crisis'] = () => `
    ${hero({ crumbs: [['Crisis help']], eyebrow: 'Crisis help', title: 'If you need help <em>now</em>', lead: 'I’m not an emergency service and can’t always reply straight away. If you are in crisis, please contact one of these services.', icon: 'i-alert' })}
    <section class="page-body"><div class="wrap">
      <div class="crisis-grid">
        <div class="crisis-card" data-reveal><h3>United Kingdom</h3><div class="emergency">Immediate danger: call 999</div><ul>
          <li><span>Emergency services</span><a class="num" href="tel:999">999</a></li>
          <li><span>NHS 111 (urgent mental health: option 2)</span><a class="num" href="tel:111">111</a></li>
          <li><span>Samaritans, free, 24/7</span><a class="num" href="tel:116123">116 123</a></li>
          <li><span>Shout, text support, 24/7</span><a class="num" href="sms:85258">85258</a></li>
          <li><span>Childline, for under-19s</span><a class="num" href="tel:08001111">0800 1111</a></li>
        </ul></div>
        <div class="crisis-card" data-reveal style="--d:.1s"><h3>Bulgaria</h3><div class="emergency">Immediate danger: call 112</div><ul>
          <li><span>Emergency services</span><a class="num" href="tel:112">112</a></li>
          <li><span>National Child Helpline</span><a class="num" href="tel:116111">116 111</a></li>
        </ul></div>
      </div>
      <div class="note warn" data-reveal>${ic('i-alert')}<span>Numbers to be double-checked before launch.</span></div>
    </div></section>`;

  const legal = (key, title, body) => {
    PAGES[key] = () => `
      ${hero({ crumbs: [[title]], eyebrow: 'Legal', title, icon: 'i-shield' })}
      <section class="page-body"><div class="wrap"><div class="prose">
        <div class="note warn">${ic('i-alert')}<span><b>Draft.</b> This text will be finalised and checked before the website goes live.</span></div>
        ${body}
      </div></div></section>`;
  };
  legal('/privacy', 'Privacy policy', `
    <h2>Who I am</h2><p>Dr Mirena Vasileva is the data controller for the personal information you share through this website and in sessions. Contact: ${EMAIL}. ICO registration number: <span class="tbc">to be added</span>.</p>
    <h2>What I collect</h2><p>Your name and contact details when you get in touch, and, if you become a client, information about your health and wellbeing that you share in sessions.</p>
    <h2>Why</h2><p>To reply to you, arrange and provide sessions, and keep the records my professional code requires. Health information is processed to provide health care, under UK GDPR and EU GDPR.</p>
    <h2>How long</h2><p>Records are kept securely only for as long as needed and as professional guidance requires.</p>
    <h2>Your rights</h2><p>You can ask to see, correct or delete your information, and you can complain to the ICO (UK) or the Commission for Personal Data Protection (Bulgaria).</p>`);
  legal('/cookies', 'Cookies', `
    <h2>In short</h2><p>This website does not use advertising or tracking cookies. If visitor statistics are added, they will use a privacy-friendly service that does not need cookies.</p>
    <h2>Links to other services</h2><p>WhatsApp, Viber and Facebook have their own privacy policies, which apply when you use their apps.</p>`);
  legal('/terms', 'Terms', `
    <h2>Appointments</h2><p>Appointments are arranged by phone, WhatsApp, Viber, email or Facebook.</p>
    <h2>Payment</h2><p>By bank transfer or Revolut.</p>
    <h2>Cancellations</h2><p>Please give at least 24 hours’ notice. Sessions cancelled with less notice may be charged in full.</p>
    <h2>Confidentiality</h2><p>Sessions are confidential, except where there is a serious risk of harm to you or others.</p>
    <h2>Emergencies</h2><p>I’m not an emergency service. See the <a href="#/crisis">Crisis help</a> page.</p>`);

  function articleCards() {
    return columns.map(([date, title, tag, url]) => `
      <a class="article t-${tag}" data-tag="${tag}" href="${url}" target="_blank" rel="noopener" data-reveal>
        <div class="top"><span class="bg"></span><svg class="icon motif"><use href="#${tagInfo[tag][1]}"/></svg><span class="label">${tagInfo[tag][0]}</span></div>
        <div class="body"><h3>${title}</h3><div class="meta"><time datetime="${date}">${fmt(date)}</time>${ic('i-arrow')}</div></div>
      </a>`).join('');
  }

  /* =====================================================================
     Router
     ===================================================================== */
  const pagesEl = document.getElementById('pages');
  const homeEl = document.querySelector('.page[data-route="/"]');
  const titles = { '/': 'Dr Vasileva – Psychologist & CBT Psychotherapist' };
  const render = () => {
    let path = location.hash.replace(/^#/, '') || '/';
    if (!path.startsWith('/')) return;           // ordinary in-page anchor
    path = path.replace(/\/$/, '') || '/';
    setMenu(false);
    pagesEl.innerHTML = '';
    if (path === '/' || !PAGES[path]) {
      homeEl.classList.add('active');
    } else {
      homeEl.classList.remove('active');
      const el = document.createElement('div');
      el.className = 'page active';
      el.innerHTML = PAGES[path]();
      pagesEl.appendChild(el);
      wirePage(el);
    }
    const h1 = document.querySelector('.page.active h1');
    document.title = path === '/' ? titles['/'] : `${h1 ? h1.textContent : ''} – Dr Vasileva`;
    navLinks.forEach(a => a.toggleAttribute('aria-current', a.getAttribute('href') !== '#/' && path.startsWith(a.getAttribute('href').slice(1))));
    scrollTo({ top: 0, behavior: 'instant' });
    observeReveals();
    onScroll();
  };
  function wirePage(el) {
    el.querySelectorAll('.js-count').forEach(c => c.dataset.to = YEARS);
    const tabs = el.querySelectorAll('.tab');
    tabs.forEach(tab => tab.addEventListener('click', () => {
      tabs.forEach(t => t.setAttribute('aria-pressed', t === tab));
      el.querySelectorAll('.article').forEach(a => a.hidden = tab.dataset.filter !== 'all' && a.dataset.tag !== tab.dataset.filter);
    }));
  }
  addEventListener('hashchange', render);
  render();
