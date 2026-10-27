
  /* =====================================================================
     Content
     ===================================================================== */
  const PHONE = '+44 7999 334778', TEL = 'tel:+447999334778';
  const WA = 'https://wa.me/447999334778', VIBER = 'viber://chat?number=%2B447999334778';
  const EMAIL = 'contact@drvasileva.co.uk', FB = 'https://www.facebook.com/mirena.vasileva.3';

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
    ['How do I make an appointment?', 'Simply get in touch by phone, Viber, WhatsApp, email, Facebook or the contact form. Tell me a little about what you need, and we’ll find a time that suits you.'],
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
  const logo = (file, alt, w, h) => `<span class="ico logo-tile"><img src="../public/images/logos/${file}" alt="${alt}" width="${w}" height="${h}" loading="lazy"></span>`;
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


  /* Extra content for the "Who I help" pages */
  const WHO_MORE = {
    'adults': {
      intro: 'Life can feel heavy for many reasons: pressure at work, a loss, a relationship ending, a move abroad, or simply a feeling that something isn’t right. You don’t need a diagnosis or a "big enough" reason to start talking.',
      approach: ['Understanding what keeps difficult feelings going', 'Practical CBT tools for anxious or self-critical thoughts', 'Small, realistic steps back to the things that matter', 'Strategies you can keep using after therapy ends'],
      faq: [['Do I need a diagnosis to start?', 'No. Many people come simply because they feel stuck or overwhelmed.'], ['Can I have sessions in Bulgarian?', 'Yes. Every session is available in Bulgarian or in English.'], ['Will I get homework?', 'Often there are small exercises between sessions, agreed together and always at a pace that suits you.']] },
    'couples-families': {
      intro: 'Relationships change over time. A new baby, a move, work pressure or children growing up can all shift the balance. Sessions give each person a safe space to be heard, and help you find your way back to each other.',
      approach: ['Understanding the patterns behind repeated arguments', 'Learning to talk about feelings without blame', 'Rebuilding closeness and trust', 'Agreeing practical changes at home'],
      faq: [['What if my partner doesn’t want to come?', 'You can start on your own. A change in one person often changes the whole relationship.'], ['Do you take sides?', 'No. My role is to help each of you be heard and understood.'], ['Can children join family sessions?', 'Yes, when it helps. We decide together who comes to which session.']] },
    'children-teens': {
      intro: 'Children often show what they feel through behaviour rather than words. Teenagers may withdraw, argue or seem not to care. My doctoral research and many years of work with young people help me understand what is going on beneath the surface.',
      approach: ['Sessions adapted to your child’s age and interests', 'Creative methods, play and conversation', 'Regular feedback and guidance for parents', 'Working with the school when it helps'],
      faq: [['How do I explain therapy to my child?', 'Keep it simple: it’s a place to talk about feelings with someone whose job is to help. I’m happy to suggest words that fit their age.'], ['Do parents stay in the session?', 'With younger children, parents often join part of the session. Teenagers usually have time on their own.'], ['What ages do you work with?', 'Children and teenagers of all ages, from early childhood up to 18.']] },
    'special-educational-needs': {
      intro: 'For eight years I worked with children with intellectual disabilities, and I later supported children with special educational needs at a Bulgarian school in London. I know how much difference the right understanding and support can make, for the child and for the whole family.',
      approach: ['Psychological assessment adapted to your child', 'A clear written report with recommendations', 'Practical strategies for home and school', 'Support for parents and siblings'],
      faq: [['Do you provide a formal diagnosis?', ASSESS_NOTE], ['Can the report be used at school?', 'Yes. Reports are written so that parents and teachers can use them.'], ['Do you work with children with intellectual disabilities?', 'Yes. This has been a central part of my work for many years.']] },
    'group-sessions': {
      intro: 'Hearing that others feel the same way can be a relief in itself. Groups offer support, new perspectives and practical skills, and they are often more affordable than individual sessions.',
      approach: ['Small groups, so everyone has space to speak', 'Clear group agreements about confidentiality and respect', 'Practical exercises you can use in daily life', 'Groups in Bulgarian and in English'],
      faq: [['Do I have to speak in the group?', 'No. You can share as much or as little as you like.'], ['Is a group confidential?', 'Yes. Every member agrees to keep what is shared within the group.'], ['Can I join online?', 'Yes. Groups can run online, so you can join from anywhere.']] },
    'organisations': {
      intro: 'Healthy teams look after each other. Training helps staff recognise stress early, communicate better and support each other, whether in an office, a clinic or a school.',
      approach: ['Interactive, practical sessions rather than lectures', 'Content tailored to your sector and team', 'Delivered in Bulgarian or in English', 'Online or on site'],
      faq: [['How long is a training session?', 'It depends on your needs, from a single workshop to a series of sessions.'], ['Do you work with schools?', 'Yes. I have trained teachers and staff on relationships with children and on working with children with special needs.'], ['How do we arrange training?', 'Get in touch by phone, WhatsApp, Viber or email and we’ll talk about what you need.']] },
  };

  /* Extra content for the issue pages */
  const ISSUE_MORE = {
    'anxiety-panic': { more: 'Anxiety often grows when we avoid what we fear. Avoiding brings short-term relief, but it teaches the brain that the danger was real.',
      tips: ['Slow your breathing: breathe out for longer than you breathe in', 'Notice anxious thoughts and ask: what is the evidence?', 'Gently face small situations you’ve been avoiding', 'Limit caffeine and keep a regular sleep routine'],
      when: 'If anxiety stops you doing everyday things, or panic attacks keep coming back, it’s a good time to get support.' },
    'depression': { more: 'Depression often comes with a harsh inner voice and a pull to withdraw from people, which can deepen the low mood even further.',
      tips: ['Plan one small, pleasant activity each day', 'Stay in contact with at least one person you trust', 'Keep a regular rhythm of sleep and meals', 'Be as kind to yourself as you would be to a friend'],
      when: 'If low mood lasts more than two weeks or affects your daily life, please reach out.' },
    'stress': { more: 'Long-term stress keeps the body on high alert. Over time it can lead to exhaustion, irritability and health problems.',
      tips: ['Write down what is in your control and what isn’t', 'Take short breaks during the day', 'Protect time for rest and the things you enjoy', 'Practise saying no to extra demands'],
      when: 'If you feel constantly drained, or can’t switch off even on holiday, it’s worth talking to someone.' },
    'relationships': { more: 'Behind most arguments are unmet needs and strong emotions. When we understand them, conflict becomes much easier to resolve.',
      tips: ['Choose a calm moment for difficult conversations', 'Talk about your feelings rather than blaming', 'Listen to understand, not to reply', 'Make regular time for each other'],
      when: 'If you keep having the same arguments, or feel more like flatmates than partners, support can help.' },
    'parenting-teens': { more: 'Teenagers need independence and connection at the same time, which can feel like a contradiction for parents.',
      tips: ['Listen more than you advise', 'Choose your battles and agree a few clear rules', 'Spend low-pressure time together, like a walk or a meal', 'Look after your own stress too'],
      when: 'If conflict is constant, or your teenager seems withdrawn, low or anxious for a long time, get support early.' },
    'child-behaviour': { more: 'Children learn to manage their emotions with the help of the adults around them. Calm, consistent responses help them feel safe.',
      tips: ['Stay calm and name the feeling: "You’re very angry right now"', 'Praise the behaviour you want to see more of', 'Keep routines predictable', 'Agree the same rules between all the adults who care for your child'],
      when: 'If behaviour is affecting school, friendships or family life, or you feel you’ve tried everything, it’s time to get help.' },
    'autism': { more: 'Every autistic child is different. Understanding your child’s strengths and needs is the first step to supporting them well.',
      tips: ['Use clear, simple language and visual supports', 'Prepare your child for changes in routine', 'Notice and reduce sensory triggers', 'Build on your child’s interests'],
      when: 'If you notice differences in communication, play or social interaction, an assessment can help you understand your child’s needs.' },
    'adhd': { more: 'ADHD is not about laziness or bad parenting. With understanding and the right strategies, children can learn to manage their attention and energy.',
      tips: ['Break tasks into small steps', 'Use timers, checklists and visual reminders', 'Build in movement breaks', 'Praise effort, not only results'],
      when: 'If difficulties with attention or restlessness are affecting learning, friendships or family life, an assessment can help.' },
    'learning-difficulties': { more: 'Learning difficulties have nothing to do with intelligence. Many children with dyslexia or dyspraxia are bright and creative, but need a different way in.',
      tips: ['Read together for short, regular periods', 'Use multi-sensory learning: seeing, hearing and doing', 'Focus on strengths as well as difficulties', 'Talk to your child’s teacher early'],
      when: 'If your child is falling behind despite their effort, or losing confidence about school, an assessment can explain why and what helps.' },
    'bullying': { more: 'Children who are bullied often stay silent out of shame or fear of making things worse. Digital violence can follow them home, day and night.',
      tips: ['Talk regularly and calmly about their day, online and offline', 'Keep evidence of online bullying, such as screenshots', 'Agree family rules for phones and social media', 'Tell your child it is never their fault'],
      when: 'If your child seems afraid, withdrawn or reluctant to go to school, don’t wait to get support.' },
    'living-abroad': { more: 'Building a life in a new country takes energy: a new language, new systems, and distance from family and friends. It’s normal to feel unsettled, even years later.',
      tips: ['Keep regular contact with people back home', 'Build small routines and connections where you live now', 'Allow yourself to miss home without guilt', 'Look for a Bulgarian community or group near you'],
      when: 'If loneliness or homesickness are affecting your mood, sleep or relationships, talking in your own language can help.' },
  };

  /* Shared blocks for the detail pages */
  const nextSteps = `
    <ol class="steps-list" data-reveal>
      <li><b>Get in touch</b><span>Call or message me on WhatsApp or Viber, in Bulgarian or English.</span></li>
      <li><b>A first conversation</b><span>We talk about what’s going on and what you’d like to change.</span></li>
      <li><b>A plan that fits you</b><span>We agree goals together, online or in person.</span></li>
      <li><b>Regular reviews</b><span>We check progress along the way and adjust as needed.</span></li>
    </ol>`;
  const practicalBox = `
    <div class="box" data-reveal><h3>Practical details</h3><ul class="facts">
      <li>${ic('i-video')}Online, or in person in the UK</li>
      <li>${ic('i-globe')}In Bulgarian or English</li>
      <li>${ic('i-lock')}Confidential</li>
      <li>${ic('i-clock')}Session length to be confirmed</li>
      <li>${ic('i-card')}<a href="#/fees">See fees</a></li>
    </ul></div>`;

  /* =====================================================================
     Pages
     ===================================================================== */
  const PAGES = {};

  PAGES['/about'] = () => `
    ${hero({ crumbs: [['About me']], eyebrow: 'About me', title: 'Hello, I’m <em>Mirena</em>', lead: 'Dr Mirena Vasileva, PhD · Psychologist &amp; CBT Psychotherapist', icon: 'i-leaf' })}
    <section class="page-body"><div class="wrap split">
      <div class="prose">
        <div class="about-photo" data-reveal="left" style="max-width:520px;margin-bottom:56px"><span class="frame"></span><div class="img"><img src="../public/images/dr-vasileva.jpg" alt="Dr Mirena Vasileva" width="1242" height="1242" loading="lazy"></div><div class="years"><strong><span class="js-count" data-to="${YEARS}">0</span><sup>+</sup></strong><span>years of experience</span></div></div>
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
          <li>Diploma in Cognitive Behavioural Therapy (CBT), Burgas Free University</li>
          <li>Diploma in Special Educational Needs &amp; Disability (SEND), Burgas Free University</li>
          <li>Certificate in CBT and Counselling</li>
          <li>CBT training, Bulgarian Association of Cognitive-Behavioural Psychotherapy</li>
          <li>Therapeutic Crisis Intervention training</li>
          <li>Safeguarding Vulnerable Adults · NSPCC Child Protection</li>
        </ul>

        <h2 data-reveal>Awards</h2>
        <div class="recog-grid" style="margin-top:20px">
          <div class="award" data-reveal><span class="year">2006</span><span class="wreath"><svg aria-hidden="true"><use href="#laurel"/></svg><span class="inner">${ic('i-ring')}</span></span><h3>Gold Ring of Varna Free University</h3><p>For graduating with honours.</p><span class="by"><img src="../public/images/logos/varna-free-university.png" alt="" width="500" height="225">Varna Free University</span></div>
          <div class="award" data-reveal style="--d:.1s"><span class="year">2006</span><span class="wreath"><svg aria-hidden="true"><use href="#laurel"/></svg><span class="inner">1st</span></span><h3>First Prize, Best Master’s Thesis</h3><p>"Best diploma thesis" competition.</p><span class="by"><img src="../public/images/logos/varna-free-university.png" alt="" width="500" height="225">Varna Free University</span></div>
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
          <figure><span><img src="../public/images/logos/varna-free-university-mark.png" alt="" width="224" height="225" loading="lazy"></span><figcaption>Varna Free University</figcaption></figure>
          <figure><span><img src="../public/images/logos/bps-mark.png" alt="" width="153" height="200" loading="lazy"></span><figcaption>British Psychological Society</figcaption></figure>
          <figure><span><img src="../public/images/logos/bulgarian-psychological-society.png" alt="" width="208" height="208" loading="lazy"></span><figcaption>Bulgarian Psychological Society</figcaption></figure>
        </div></div>
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
    const m = WHO_MORE[w.slug];
    PAGES['/who-i-help/' + w.slug] = () => `
      ${hero({ crumbs: [['Who I help', '#/who-i-help'], [w.title]], eyebrow: 'Who I help', title: w.title, lead: w.lead, icon: w.icon })}
      <section class="page-body"><div class="wrap split">
        <div class="prose">
          <p class="intro" data-reveal>${m.intro}</p>
          <h2 data-reveal>Who it’s for</h2>
          <ul class="ticks" data-reveal>${w.for.map(f => `<li>${f}</li>`).join('')}</ul>
          <h2 data-reveal>How I can help</h2>
          <p data-reveal>${w.how}</p>
          <div class="approach" data-reveal>${m.approach.map((a, i) => `<div><span>0${i + 1}</span>${a}</div>`).join('')}</div>
          <h2 data-reveal>What happens next</h2>
          ${nextSteps}
          <h2 data-reveal>Questions</h2>
          ${faqList(m.faq)}
        </div>
        <aside class="aside">
          <div class="box" data-reveal><h3>Related topics</h3><div class="links-list">${w.issues.map(s => `<a href="#/issues/${s}">${issueBy(s).title}${ic('i-arrow')}</a>`).join('')}</div></div>
          ${practicalBox}
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
    const m = ISSUE_MORE[x.slug];
    PAGES['/issues/' + x.slug] = () => `
      ${hero({ crumbs: [['What I help with', '#/issues'], [x.title]], eyebrow: 'What I help with', title: x.title, lead: x.short, icon: x.icon })}
      <section class="page-body"><div class="wrap split">
        <div class="prose">
          <h2 data-reveal>What it is</h2>
          <p data-reveal>${x.about}</p>
          <p data-reveal>${m.more}</p>
          <h2 data-reveal>Common signs</h2>
          <ul class="ticks" data-reveal>${x.signs.map(s => `<li>${s}</li>`).join('')}</ul>
          <div class="note" data-reveal>${ic('i-sun')}<span><b>When to get help:</b> ${m.when}</span></div>
          <h2 data-reveal>How I can help</h2>
          <p data-reveal>${x.help}</p>
          <h2 data-reveal>Things you can try today</h2>
          <div class="tips" data-reveal>${m.tips.map(t => `<div>${ic('i-leaf')}<span>${t}</span></div>`).join('')}</div>
          ${x.col ? `<a class="read-more" href="${COL[x.col][1]}" target="_blank" rel="noopener" data-reveal><span class="ri">${ic('i-news')}</span><span><small>Read my column</small><b>${COL[x.col][0]}</b></span></a>` : ''}
          <h2 data-reveal>What happens next</h2>
          ${nextSteps}
          <h2 data-reveal>Questions</h2>
          ${faqList(x.faq)}
        </div>
        <aside class="aside">
          <div class="box" data-reveal><h3>Other topics</h3><div class="links-list">${ISSUES.filter(o => o.slug !== x.slug).slice(0, 6).map(o => `<a href="#/issues/${o.slug}">${o.title}${ic('i-arrow')}</a>`).join('')}<a href="#/issues">See all${ic('i-arrow')}</a></div></div>
          ${practicalBox}
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
    <section class="page-body"><div class="wrap"><div class="faq-wide">${faqList(FAQ)}</div></div></section>
    ${ctaBand()}`;

  PAGES['/press'] = () => `
    ${hero({ crumbs: [['Press']], eyebrow: 'Press', title: 'Featured <em>in</em>', lead: 'Columns, interviews and lectures.', icon: 'i-mic' })}
    <section class="page-body"><div class="wrap"><div class="issue-grid">
      <a class="issue" href="#/articles" data-reveal>${logo('bg-ben.png', 'BG BEN', 400, 400)}<span><h3>BG BEN</h3><p>"School of Psychology", my regular column, 2023 – now.</p></span></a>
      <div class="issue" data-reveal style="--d:.07s">${logo('zdraveto.png', 'Zdraveto (blitz.bg)', 326, 100).replace('logo-tile', 'logo-tile wide')}<span><h3>"Doctor" newspaper</h3><p>Published by Zdraveto (blitz.bg). Interview: "Suicide is often a cry to be noticed", issue 15, 2015.</p></span></div>
      <div class="issue" data-reveal style="--d:.14s">${logo('bg-radio.png', 'BG Radio', 203, 203)}<span><h3>BG Radio</h3><p>Interview: "Covid-19 and panic attacks", 2019.</p></span></div>
      <div class="issue" data-reveal>${logo('burgas-free-university.png', 'Burgas Free University', 240, 250)}<span><h3>Burgas Free University</h3><p>Lectures in Experimental and Pedagogical Psychology, art therapy in crisis intervention, and family stress in adolescence.</p></span></div>
      <div class="issue" data-reveal style="--d:.07s">${logo('bulgarian-academy-of-sciences.png', 'Bulgarian Academy of Sciences', 440, 240).replace('logo-tile', 'logo-tile wide')}<span><h3>Bulgarian Academy of Sciences</h3><p>Six scientific and applied contributions from my doctoral research.</p></span></div>
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
    </section>
    <section class="page-body" id="message"><div class="wrap split">
      <div>
        <span class="eyebrow" data-reveal>Send a message</span>
        <h2 data-reveal style="--d:.05s">Prefer to <em>write</em>?</h2>
        <p class="lead" data-reveal style="--d:.1s;margin-bottom:34px">Fill in the form and I’ll get back to you, in Bulgarian or in English.</p>
        <form class="cform" id="contact-form" novalidate data-reveal>
          <div class="row2">
            <label class="field"><span>Your name <i>*</i></span><input name="name" autocomplete="name" required maxlength="100"></label>
            <label class="field"><span>Email <i>*</i></span><input name="email" type="email" autocomplete="email" required maxlength="150"></label>
          </div>
          <div class="row2">
            <label class="field"><span>Phone <small>(optional)</small></span><input name="phone" type="tel" autocomplete="tel" maxlength="30"></label>
            <label class="field"><span>I’m interested in</span><select name="topic">
              <option value="">Please choose…</option>
              ${WHO.map(w => `<option>${w.title}</option>`).join('')}
              <option>Something else</option>
            </select></label>
          </div>
          <fieldset class="field"><legend>How should I reply?</legend><div class="chips-choice">
            ${['Email', 'Phone call', 'WhatsApp', 'Viber'].map((o, i) => `<label><input type="radio" name="reply" value="${o}"${i ? '' : ' checked'}><span>${o}</span></label>`).join('')}
          </div></fieldset>
          <fieldset class="field"><legend>Language</legend><div class="chips-choice">
            <label><input type="radio" name="language" value="English" checked><span>English</span></label>
            <label><input type="radio" name="language" value="Bulgarian"><span lang="bg">Български</span></label>
          </div></fieldset>
          <label class="field"><span>Your message <i>*</i></span><textarea name="message" rows="6" required maxlength="3000" placeholder="A few words about what you’d like help with is enough."></textarea></label>
          <p class="hint">${ic('i-lock')}Please keep it brief. There’s no need to share detailed health information here; we can talk about that in person.</p>
          <label class="hp" aria-hidden="true">Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label>
          <label class="check"><input type="checkbox" name="consent" required><span>I agree that my details are used to reply to my message, as described in the <a href="#/privacy">privacy policy</a>. <i>*</i></span></label>
          <div class="ts" id="ts-box"></div>
          <div class="form-error" role="alert" hidden></div>
          <button class="btn btn-green send" type="submit"><span class="send-label">Send message</span>${ic('i-send')}</button>
        </form>
        <div class="form-done" hidden role="status">
          <span class="ico">${ic('i-check')}</span>
          <h3>Thank you, your message has been sent</h3>
          <p>I’ll get back to you as soon as I can. If it’s urgent, please call or message me on WhatsApp or Viber.</p>
        </div>
      </div>
      <aside class="aside">
        <div class="box" data-reveal><h3>What happens next</h3>${nextSteps}</div>
        <div class="note warn" data-reveal>${ic('i-alert')}<span><b>In an emergency</b> please don’t use this form. Call 999 (UK) or 112 (Bulgaria), or see <a href="#/crisis">Crisis help</a>.</span></div>
      </aside>
    </div></section>`;

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
    <h2>What I collect</h2><p>Your name and contact details when you get in touch (by phone, message, email or the contact form), and, if you become a client, information about your health and wellbeing that you share in sessions.</p><h2>The contact form</h2><p>Messages sent through the form are emailed to me through my own secure mail server, not a third-party email service. To protect the form from spam and bots it uses Cloudflare Turnstile, which checks your browser without tracking you across websites.</p>
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

  PAGES['/404'] = () => `
    <section class="page-hero grain on-dark notfound">
      <span class="blob b1"></span><span class="blob b2"></span>
      <div class="wrap">
        <span class="eyebrow">Error 404</span>
        <h1>This page <em>doesn’t</em> exist</h1>
        <p class="lead">The link may be old or mistyped. Here are some places to start instead.</p>
        <div class="btn-row" style="margin-top:32px">
          <a class="btn btn-cream" href="#/">Back to the homepage</a>
          <a class="btn btn-whatsapp" href="${WA}">${ic('b-whatsapp', 'bi')}WhatsApp</a>
          <a class="btn btn-viber" href="${VIBER}">${ic('b-viber', 'bi')}Viber</a>
        </div>
        <div class="nf-links">
          <a href="#/about">About me${ic('i-arrow')}</a><a href="#/who-i-help">Who I help${ic('i-arrow')}</a>
          <a href="#/issues">What I help with${ic('i-arrow')}</a><a href="#/contact">Contact${ic('i-arrow')}</a>
        </div>
      </div>
    </section>`;

  function articleCards() {
    return columns.map(([date, title, tag, url]) => `
      <a class="article t-${tag}" data-tag="${tag}" href="${url}" target="_blank" rel="noopener" data-reveal>
        <div class="top"><span class="bg"></span><svg class="icon motif"><use href="#${tagInfo[tag][1]}"/></svg><span class="label">${tagInfo[tag][0]}</span></div>
        <div class="body"><h3>${title}</h3><div class="meta"><time datetime="${date}">${fmt(date)}</time>${ic('i-arrow')}</div></div>
      </a>`).join('');
  }

  /* =====================================================================
     Dropdown menus: "Who I help" and "What I help with"
     ===================================================================== */
  const ddItems = {
    '#/who-i-help': { all: 'All: who I help', cols: 1, items: WHO.map(w => [`#/who-i-help/${w.slug}`, w.title, w.icon]) },
    '#/issues': { all: 'All: what I help with', cols: 2, items: ISSUES.map(x => [`#/issues/${x.slug}`, x.title, x.icon]) },
  };
  Object.entries(ddItems).forEach(([href, d]) => {
    // Desktop
    const top = document.querySelector(`.nav-links a[href="${href}"]`);
    const li = top.parentElement;
    li.classList.add('has-dd');
    top.insertAdjacentHTML('beforeend', `<svg class="icon chev"><use href="#i-down"/></svg>`);
    top.setAttribute('aria-haspopup', 'true');
    li.insertAdjacentHTML('beforeend', `<div class="dd" role="menu"><div class="dd-panel cols-${d.cols}">
      ${d.items.map(([h, t, i]) => `<a class="dd-link" role="menuitem" href="${h}"><span class="dd-ico">${ic(i)}</span>${t}</a>`).join('')}
      <a class="dd-all" href="${href}">${d.all}${ic('i-arrow')}</a></div></div>`);
    // Phone menu
    const mtop = document.querySelector(`#menu ol a[href="${href}"]`);
    const mli = mtop.parentElement;
    mli.classList.add('m-has-sub');
    mtop.insertAdjacentHTML('afterend', `<button class="m-toggle" aria-expanded="false" aria-label="Show ${mtop.textContent} pages"><span></span></button>`);
    mli.insertAdjacentHTML('beforeend', `<ul class="m-sub">${d.items.map(([h, t]) => `<li><a href="${h}" data-close>${t}</a></li>`).join('')}<li><a href="${href}" data-close>${d.all}</a></li></ul>`);
    const tog = mli.querySelector('.m-toggle');
    tog.addEventListener('click', () => {
      const open = mli.classList.toggle('open');
      tog.setAttribute('aria-expanded', open);
    });
    mli.querySelectorAll('.m-sub a').forEach(a => a.addEventListener('click', () => setMenu(false)));
  });
  // Close desktop dropdowns after choosing a page
  document.querySelectorAll('.dd a').forEach(a => a.addEventListener('click', () => {
    const li = a.closest('.has-dd'); li.classList.add('dd-hide');
    setTimeout(() => li.classList.remove('dd-hide'), 400);
  }));

  /* =====================================================================
     Router
     ===================================================================== */
  const pagesEl = document.getElementById('pages');
  const homeEl = document.querySelector('.page[data-route="/"]');
  const titles = { '/': 'Dr Vasileva – Psychologist & CBT Psychotherapist' };
  // Addresses: the preview files (opened from disk) use #/ links; the live site uses real paths
  // (/about, and Bulgarian slugs on drvasileva.bg). SLUGS maps a page to its address on this site,
  // OTHER_SLUGS to its address on the other language's site. Only the live build sets SLUGS, so the
  // preview files keep #/ links even when they're put on a web server.
  const HASH_MODE = location.protocol === 'file:' || !window.SLUGS;
  const SLUGS = window.SLUGS || {}, OTHER_SLUGS = window.OTHER_SLUGS || {};
  const KEYS = Object.fromEntries(Object.entries(SLUGS).map(([k, v]) => [v, k]));
  const toUrl = (key, map = SLUGS) => map[key] || key;
  const currentKey = () => {
    if (HASH_MODE) return (location.hash.replace(/^#/, '') || '/').replace(/\/$/, '') || '/';
    const p = decodeURI(location.pathname).replace(/\/(index\.html)?$/, '') || '/';
    return KEYS[p] || p;
  };
  const rewriteLinks = root => root.querySelectorAll('a[href^="#/"]').forEach(a => {
    const key = a.getAttribute('href').slice(1);
    a.dataset.key = key;
    if (!HASH_MODE) a.setAttribute('href', toUrl(key));
  });
  const metaLinks = [...document.querySelectorAll('link[rel="canonical"], link[rel="alternate"][hreflang], meta[property="og:url"]')];
  metaLinks.forEach(m => m.dataset.base ||= (m.getAttribute('href') || m.getAttribute('content')).replace(/\/$/, ''));
  const isBG = document.documentElement.lang === 'bg';
  const syncMeta = key => {
    if (HASH_MODE) return;
    metaLinks.forEach(m => {
      const lang = m.getAttribute('hreflang');
      const map = !lang ? SLUGS : (lang === 'bg') === isBG ? SLUGS : OTHER_SLUGS;
      m.setAttribute(m.tagName === 'META' ? 'content' : 'href', m.dataset.base + toUrl(key, map));
    });
  };
  // Language switch: go to the same page in the other language. On a test domain the other language
  // is the same address with or without "-bg" on the first part (test.example.com ↔ test-bg.example.com).
  const LIVE_HOST = /(^|\.)drvasileva\.(co\.uk|bg)$/.test(location.hostname);
  const otherSite = base => HASH_MODE || LIVE_HOST ? base.replace(/\/$/, '')
    : `${location.protocol}//${isBG ? location.host.replace(/^([^.]+)-bg\./, '$1.') : location.host.replace(/^([^.]+)\./, '$1-bg.')}`;
  const syncLang = key => document.querySelectorAll('.lang a[data-base]').forEach(a =>
    a.href = HASH_MODE ? a.dataset.base + location.hash : otherSite(a.dataset.base) + toUrl(key, OTHER_SLUGS));

  const render = () => {
    if (HASH_MODE && location.hash && !location.hash.startsWith('#/')) return;   // ordinary in-page anchor
    let path = currentKey();
    setMenu(false);
    pagesEl.innerHTML = '';
    // Unknown address: the server's 404 page sets NOT_FOUND; unknown routes also land here
    if (window.NOT_FOUND && HASH_MODE && !location.hash) path = '/404';
    else if (path !== '/' && !PAGES[path]) path = '/404';
    if (path === '/') {
      homeEl.classList.add('active');
    } else {
      homeEl.classList.remove('active');
      const el = document.createElement('div');
      el.className = 'page active';
      el.innerHTML = PAGES[path]();
      pagesEl.appendChild(el);
      rewriteLinks(el);
      wirePage(el);
    }
    const h1 = document.querySelector('.page.active h1');
    document.title = path === '/' ? titles['/'] : `${h1 ? h1.textContent : ''} – Dr Vasileva`;
    navLinks.forEach(a => a.toggleAttribute('aria-current', !!a.dataset.key && a.dataset.key !== '/' && path.startsWith(a.dataset.key)));
    syncMeta(path);
    syncLang(path);
    scrollTo({ top: 0, behavior: 'instant' });
    observeReveals();
    onScroll();
  };
  // Contact form. TURNSTILE_SITE_KEY is Cloudflare's public test key (always passes); replace it with the real site key at launch.
  const TURNSTILE_SITE_KEY = '0x4AAAAAAFn0BHwXhddLG2qs';
  const FORM_ENDPOINT = '/api/contact';
  function wireForm(el) {
    const form = el.querySelector('#contact-form');
    if (!form) return;
    const err = form.querySelector('.form-error'), btn = form.querySelector('.send'), label = btn.querySelector('.send-label');
    let widget = null;
    const mountTurnstile = () => {
      if (typeof window.turnstile?.render !== 'function' || !document.body.contains(form)) return false;
      widget = turnstile.render('#ts-box', { sitekey: TURNSTILE_SITE_KEY, theme: 'light', appearance: 'interaction-only' });
      return true;
    };
    if (!mountTurnstile()) {
      const t = setInterval(() => { if (mountTurnstile() || !document.body.contains(form)) clearInterval(t); }, 300);
    }
    const showError = msg => { err.textContent = msg; err.hidden = false; };
    form.addEventListener('submit', async e => {
      e.preventDefault();
      err.hidden = true;
      form.querySelectorAll('.invalid').forEach(f => f.classList.remove('invalid'));
      const bad = [...form.querySelectorAll('[required]')].filter(f => !f.checkValidity());
      if (bad.length) {
        bad.forEach(f => (f.closest('.field') || f.closest('.check')).classList.add('invalid'));
        bad[0].focus();
        return showError('Please fill in the fields marked with *.');
      }
      btn.disabled = true; label.textContent = 'Sending…';
      const done = () => { form.hidden = true; el.querySelector('.form-done').hidden = false; };
      try {
        if (location.protocol === 'file:') { await new Promise(r => setTimeout(r, 900)); return done(); }   // preview only
        const res = await fetch(FORM_ENDPOINT, { method: 'POST', body: new FormData(form) });
        const data = await res.json().catch(() => ({}));
        if (!res.ok || !data.ok) throw new Error(data.error || 'send');
        done();
      } catch (ex) {
        showError(ex.message === 'verification'
          ? 'We couldn’t confirm you’re not a robot. Please try again.'
          : 'Sorry, something went wrong. Please try again, or call or message me instead.');
        if (typeof window.turnstile?.reset === 'function' && widget !== null) turnstile.reset(widget);
      } finally {
        btn.disabled = false; label.textContent = 'Send message';
      }
    });
  }

  function wirePage(el) {
    wireForm(el);
    el.querySelectorAll('.js-count').forEach(c => c.dataset.to = YEARS);
    const tabs = el.querySelectorAll('.tab');
    tabs.forEach(tab => tab.addEventListener('click', () => {
      tabs.forEach(t => t.setAttribute('aria-pressed', t === tab));
      el.querySelectorAll('.article').forEach(a => a.hidden = tab.dataset.filter !== 'all' && a.dataset.tag !== tab.dataset.filter);
    }));
  }
  rewriteLinks(document);
  if (HASH_MODE) {
    addEventListener('hashchange', render);
  } else {
    // Real addresses: follow internal links without reloading, and support the back button
    addEventListener('popstate', render);
    document.addEventListener('click', e => {
      const a = e.target.closest('a[data-key]');
      if (!a || e.defaultPrevented || e.button || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || a.target) return;
      e.preventDefault();
      if (a.getAttribute('href') !== location.pathname) history.pushState(null, '', a.getAttribute('href'));
      render();
    });
  }
  render();
