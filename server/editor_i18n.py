"""The editor in English or Bulgarian. Screens are written in English and wrapped in _(); in Bulgarian, _() looks
the text up below. Each request runs in its own thread, so the chosen language is kept per thread."""
import re
import threading

LANGS = ('bg', 'en')
_local = threading.local()


def set_request(lang, path='/'):
    _local.lang = lang if lang in LANGS else 'en'
    _local.path = path


def lang():
    return getattr(_local, 'lang', 'en')


def path():
    return getattr(_local, 'path', '/')


def _(text):
    return BG.get(text, text) if lang() == 'bg' else text


MONTHS_BG = ('яну', 'фев', 'мар', 'апр', 'май', 'юни', 'юли', 'авг', 'сеп', 'окт', 'ное', 'дек')

BG = {
    # sign-in
    'Sign in': 'Вход',
    'Password': 'Парола',
    'Code': 'Код',
    'from your authenticator app, or a backup code': 'от приложението за удостоверяване или резервен код',
    'Website editor': 'Редактор на сайта',
    'Sign in to write and publish articles.': 'Влезте, за да пишете и публикувате статии.',
    'Every sign-in is emailed to the owner.': 'За всяко влизане се изпраща имейл до собственика.',
    'The editor has not been set up yet. Run the setup command on the server (see deploy/README.md).':
        'Редакторът още не е настроен. Изпълнете командата за настройка на сървъра (вижте deploy/README.md).',
    'That didn’t work. Check your password and the code, then try again.': 'Не се получи. Проверете паролата и кода и опитайте отново.',
    'Too many attempts. Sign-in is paused for 15 minutes.': 'Твърде много опити. Влизането е спряно за 15 минути.',
    'Not found': 'Не е намерено',
    'Back to the editor': 'Обратно към редактора',
    'Dr Vasileva editor': 'Редактор Д-р Василева',
    'Language of the editor': 'Език на редактора',
    # frame
    'Posts': 'Публикации',
    'Topics': 'Теми',
    'Bin': 'Кошче',
    'Editor': 'Редактор',
    'Sign out': 'Изход',
    'Sign out?': 'Да излезете ли?',
    'Anything not saved on this page will be lost.': 'Всичко незапазено на тази страница ще се загуби.',
    'No, stay': 'Не, оставам',
    'Yes, sign out': 'Да, изход',
    'Delete this post?': 'Да изтрия ли тази публикация?',
    'Delete this topic?': 'Да изтрия ли тази тема?',
    'Delete post': 'Изтриване на публикация',
    'Delete topic': 'Изтриване на тема',
    'To confirm, type': 'За потвърждение напишете',
    'Cancel': 'Отказ',
    'Delete': 'Изтрий',
    'Close this message': 'Затвори съобщението',
    # posts list
    'Published': 'Публикувана',
    'Draft': 'Чернова',
    '(no title)': '(без заглавие)',
    'Edit': 'Редактирай',
    'Preview': 'Преглед',
    'It disappears from the site and stays in the bin for 30 days.': 'Изчезва от сайта и остава в кошчето 30 дни.',
    'It stays in the bin for 30 days.': 'Остава в кошчето 30 дни.',
    'Title': 'Заглавие',
    'Topic': 'Тема',
    'Status': 'Статус',
    'Date': 'Дата',
    'No posts yet.': 'Още няма публикации.',
    'this is the first sign-in': 'това е първото влизане',
    '+ New post': '+ Нова публикация',
    'New post': 'Нова публикация',
    'Previous sign-in:': 'Предишно влизане:',
    'You are signed out after 1 hour without activity.': 'Излизате автоматично след 1 час без активност.',
    'Search posts by title': 'Търсене на публикации по заглавие',
    'Search by title, in Bulgarian or English…': 'Търсете по заглавие, на български или английски…',
    'Search': 'Търси',
    'Order': 'Подредба',
    'Newest first': 'Първо най-новите',
    'Oldest first': 'Първо най-старите',
    'All topics': 'Всички теми',
    'All': 'Всички',
    'Drafts': 'Чернови',
    'Clear filters': 'Изчисти филтрите',
    'No posts match.': 'Няма публикации, които да отговарят.',
    # post screen
    'Complete': 'Готово',
    'Not finished': 'Недовършено',
    'Short description': 'Кратко описание',
    'One or two sentences that tell readers what the article is about. They appear under the title on the Articles page, and in Google’s search results.':
        'Едно-две изречения, които казват на читателите за какво е статията. Показват се под заглавието на страницата „Статии“ и в резултатите от търсенето в Google.',
    'Text': 'Текст',
    'Formatting': 'Форматиране',
    'Heading': 'Подзаглавие',
    'A big heading for a new section': 'Голямо подзаглавие за нов раздел',
    'Subheading': 'Малко подзаглавие',
    'A smaller heading': 'По-малко подзаглавие',
    'Normal text': 'Обикновен текст',
    'Back to normal text': 'Обратно към обикновен текст',
    'Bold': 'Удебелен',
    'Bold (Ctrl+B)': 'Удебелен (Ctrl+B)',
    'Italic': 'Курсив',
    'Italic (Ctrl+I)': 'Курсив (Ctrl+I)',
    'Underline': 'Подчертан',
    'Underline (Ctrl+U)': 'Подчертан (Ctrl+U)',
    'Colour': 'Цвят',
    'Colour the selected words': 'Оцвети избраните думи',
    'Green': 'Зелен',
    'Lilac': 'Лилав',
    'Gold': 'Златист',
    'Rose': 'Розов',
    'No colour': 'Без цвят',
    'Bullet list': 'Списък с точки',
    'A list with dots': 'Списък с точки',
    'Numbered list': 'Номериран списък',
    'A numbered list': 'Номериран списък',
    'Restart numbering': 'Започни номерата от 1',
    'Continue numbering': 'Продължи номерата',
    'Numbered lists carry on after a paragraph. Use this to start this list again at 1, or to carry on again.':
        'Номерираните списъци продължават след абзац. С този бутон списъкът започва отново от 1 или пак продължава.',
    'Quote': 'Цитат',
    'A quote, shown larger': 'Цитат, показан по-едро',
    'Link': 'Връзка',
    'Turn the selected words into a link': 'Направи избраните думи връзка',
    'Clear formatting': 'Изчисти форматирането',
    'Remove bold, italic, underline, colour and links from the selected words':
        'Премахва удебеляване, курсив, подчертаване, цвят и връзки от избраните думи',
    'A blank line starts a new paragraph.': 'Празен ред започва нов абзац.',
    'Save changes': 'Запази промените',
    'Unpublish': 'Свали от сайта',
    'Save draft': 'Запази черновата',
    'Publish': 'Публикувай',
    'Preview in Bulgarian': 'Преглед на български',
    'Preview in English': 'Преглед на английски',
    'Opens in a new tab': 'Отваря се в нов раздел',
    'Versions': 'Версии',
    'Earlier saved copies': 'По-рано запазени варианти',
    'Preview and versions': 'Преглед и версии',
    'Published – changes go live when you save': 'Публикувана – промените излизат на сайта, когато запазите',
    'Draft – not on the site': 'Чернова – не е на сайта',
    'Edit post': 'Редактиране на публикация',
    '← All posts': '← Всички публикации',
    'Post': 'Публикация',
    'Unsaved changes from this browser were found': 'В този браузър има незапазени промени',
    'Restore them': 'Върни ги',
    'Discard': 'Откажи се от тях',
    'Add or change topics': 'Добави или промени теми',
    'Year-month-day. Empty = the day it is published.': 'Година-месец-ден. Празно = денят на публикуване.',
    'BG BEN link': 'Връзка към BG BEN',
    'only for columns': 'само за рубриките',
    'Cover photo': 'Снимка за корицата',
    'Click to choose a photo': 'Щракнете, за да изберете снимка',
    'No photo yet': 'Още няма снимка',
    'Click here to add one': 'Щракнете тук, за да добавите',
    'JPG, PNG or WebP, up to 10 MB. Click the photo to change it, or × to remove it. The location phones save in photos is removed.':
        'JPG, PNG или WebP, до 10 MB. Щракнете върху снимката, за да я смените, или върху ×, за да я премахнете. Местоположението, което телефоните записват в снимките, се премахва.',
    'JPG, PNG or WebP, up to 10 MB. The location phones save in photos is removed.':
        'JPG, PNG или WebP, до 10 MB. Местоположението, което телефоните записват в снимките, се премахва.',
    'Remove the photo': 'Премахни снимката',
    'The photo will be removed when you save.': 'Снимката ще бъде премахната, когато запазите.',
    'Photo description in Bulgarian': 'Описание на снимката на български',
    'Photo description in English': 'Описание на снимката на английски',
    'Say in a few words what the photo shows, for example “A mother and daughter talking”. It is read out to blind visitors and helps Google.':
        'Опишете с няколко думи какво показва снимката, например „Майка и дъщеря разговарят“. Прочита се на незрящи посетители и помага на Google.',
    'Language': 'Език',
    # versions
    'Saved': 'Запазена',
    'Status then': 'Статус тогава',
    'Restore': 'Възстанови',
    'No earlier versions yet. One is kept each time you save.': 'Още няма по-ранни версии. При всяко запазване се пази по една.',
    'The last 30 saved versions are kept. Restoring brings back the text and photo of that version; whether the post is published stays as it is now.':
        'Пазят се последните 30 запазени версии. Възстановяването връща текста и снимката от тази версия; дали публикацията е на сайта, остава както е сега.',
    # topics
    'Sage green': 'Сиво-зелен',
    'Forest green': 'Тъмнозелен',
    'Plum': 'Сливов',
    'Sand': 'Пясъчен',
    'Sun': 'Слънце',
    'Heart': 'Сърце',
    'Smile': 'Усмивка',
    'Leaf': 'Листо',
    'Puzzle': 'Пъзел',
    'Globe': 'Глобус',
    'Feather': 'Перо',
    'Icon': 'Икона',
    'Looks like': 'Изглежда така',
    'English': 'Английски',
    'It disappears from the editor. This can’t be undone.': 'Изчезва от редактора. Това не може да се отмени.',
    'Can’t be deleted': 'Не може да се изтрие',
    '+ New topic': '+ Нова тема',
    'Topics appear as filters on the Articles page once they have a published post.':
        'Темите се показват като филтри на страницата „Статии“, щом имат публикувана статия.',
    'New topic': 'Нова тема',
    'Edit topic': 'Редактиране на тема',
    '← All topics': '← Всички теми',
    'English name': 'Име на английски',
    'Bulgarian name': 'Име на български',
    'How it looks on the Articles page': 'Как изглежда на страницата „Статии“',
    'The topic appears on the site once it has a published post.': 'Темата се появява на сайта, щом има публикувана статия.',
    'Changes go live on the site when you save.': 'Промените излизат на сайта, когато запазите.',
    'Add topic': 'Добави темата',
    '← Back': '← Назад',
    # bin
    'Deleted': 'Изтрита',
    'Removed for good': 'Изтрива се завинаги',
    'The bin is empty.': 'Кошчето е празно.',
    'Deleted posts stay here for 30 days. A restored post comes back as a draft, so you can check it before publishing.':
        'Изтритите публикации остават тук 30 дни. Възстановената публикация се връща като чернова, за да я прегледате, преди да я публикувате.',
    # messages after a change
    'Saved.': 'Запазено.',
    'Published. The post is now on both sites.': 'Публикувано. Статията вече е и на двата сайта.',
    'Unpublished. The post is no longer on the site.': 'Свалено. Статията вече не е на сайта.',
    'Saved as a draft.': 'Запазено като чернова.',
    'Restored.': 'Възстановено.',
    'The post was moved to the bin.': 'Публикацията е преместена в кошчето.',
    'Topic saved.': 'Темата е запазена.',
    'New topic added.': 'Новата тема е добавена.',
    'The topic was deleted.': 'Темата е изтрита.',
    # problems
    'No such post.': 'Няма такава публикация.',
    'Please choose a topic.': 'Моля, изберете тема.',
    'The date must look like 2026-09-19 (or 2026-09, or 2026).': 'Датата трябва да изглежда така: 2026-09-19 (или 2026-09, или 2026).',
    'The BG BEN link must start with https://bgben.co.uk/': 'Връзката към BG BEN трябва да започва с https://bgben.co.uk/',
    'Please give the post a title first.': 'Първо дайте заглавие на публикацията.',
    'No such version.': 'Няма такава версия.',
    'No such post in the bin.': 'Няма такава публикация в кошчето.',
    'A post with the same name exists again. Rename or delete that one first.': 'Отново има публикация със същото име. Първо преименувайте или изтрийте нея.',
    'This topic still has posts. Move them to another topic first.': 'В тази тема още има публикации. Първо ги преместете в друга тема.',
    'A new topic needs both an English and a Bulgarian name.': 'Новата тема трябва да има име и на английски, и на български.',
    'There is already a topic with this name.': 'Вече има тема с това име.',
    'The photo is too large (more than 10 MB).': 'Снимката е твърде голяма (над 10 MB).',
    'Photos need the Pillow library on the server: apt install python3-pil': 'Снимките изискват библиотеката Pillow на сървъра: apt install python3-pil',
    'Please upload a JPG, PNG or WebP photo.': 'Моля, качете снимка във формат JPG, PNG или WebP.',
    'The photo has too many pixels. Please use a photo of at most 40 megapixels.': 'Снимката има твърде много пиксели. Моля, използвайте снимка до 40 мегапиксела.',
    'That file could not be read as a photo.': 'Този файл не може да се прочете като снимка.',
    'There is nothing to delete here.': 'Тук няма какво да се изтрие.',
    'Please give the topic a name in both English and Bulgarian.': 'Моля, дайте име на темата и на английски, и на български.',
    'No such topic.': 'Няма такава тема.',
    'choose a topic': 'изберете тема',
    'the date must look like 2026-09-19 (or 2026-09, or 2026)': 'датата трябва да изглежда така: 2026-09-19 (или 2026-09, или 2026)',
    'the BG BEN link must be an https://bgben.co.uk/… address': 'връзката към BG BEN трябва да е адрес https://bgben.co.uk/…',
    # in the browser (editor.js)
    'Nothing has changed yet': 'Още няма промени',
    'Fill in both names': 'Попълнете и двете имена',
    'Start writing here…': 'Започнете да пишете тук…',
    'Select words, then click a button above. Press Enter for a new paragraph.': 'Изберете думи и натиснете бутон отгоре. Enter започва нов абзац.',
    'First select the words you want to colour.': 'Първо изберете думите, които искате да оцветите.',
    'First select the words that should become a link.': 'Първо изберете думите, които да станат връзка.',
    'Web address for the link (starting with https://):': 'Уеб адрес на връзката (започва с https://):',
    'Please enter a full address, starting with https://': 'Моля, въведете пълен адрес, който започва с https://',
    ' · unsaved changes kept in this browser at {time}': ' · незапазените промени са съхранени в този браузър в {time}',
}

# Texts with a changing part: (English pattern, Bulgarian). {x} in the Bulgarian is the changing part, translated too.
_TEMPLATES = [
    (r'Not saved, because the published post would be incomplete: (?P<x>.+)\. Fix this and save again, or unpublish the post first\.',
     'Не е запазено, защото публикуваната статия би била непълна: {x}. Поправете това и запазете отново или първо я свалете от сайта.'),
    (r'Saved as a draft, but it can’t be published yet: (?P<x>.+)\.', 'Запазено като чернова, но още не може да се публикува: {x}.'),
    (r'That version can’t be published as it is: (?P<x>.+)\. Unpublish the post first to restore it\.',
     'Тази версия не може да се публикува както е: {x}. За да я възстановите, първо свалете статията от сайта.'),
    (r'Something in the posts needs fixing: (?P<x>.+)', 'Нещо в публикациите трябва да се поправи: {x}'),
    (r'Before it can be published: (?P<x>.+)\.', 'Преди да може да се публикува: {x}.'),
]
_KEEP = [   # the changing part is a name or a number: kept as it is
    (r'The name you typed doesn’t match\. Type (?P<x>\S+) to delete\.', 'Написаното име не съвпада. Напишете {x}, за да изтриете.'),
    (r'(?P<x>.+) missing', 'Липсва: {x}'),
    (r'(?P<x>„.+“) can’t be deleted because 1 post uses it\. Move it to another topic first\.',
     '{x} не може да се изтрие, защото 1 публикация е в тази тема. Първо я преместете в друга тема.'),
    (r'(?P<x>„.+“) can’t be deleted because (?P<n>\d+) posts use it\. Move them to another topic first\.',
     '{x} не може да се изтрие, защото {n} публикации са в тази тема. Първо ги преместете в друга тема.'),
    (r'← Back to (?P<x>„.+“)', '← Обратно към {x}'),
]
_LANG_NAMES = {'English': 'Английски', 'Bulgarian': 'Български'}
_FIELDS = {'title': 'липсва заглавието', 'short description': 'липсва краткото описание', 'web address': 'липсва уеб адресът'}


def _problem(p):
    """One problem from blog.read_post, such as 'Bulgarian: the title is missing'."""
    if p in BG:
        return BG[p]
    m = re.fullmatch(r'(English|Bulgarian): (.+)', p)
    if m:
        who, what = _LANG_NAMES[m.group(1)], m.group(2)
        f = re.fullmatch(r'the (.+) is missing', what)
        if f and f.group(1) in _FIELDS:
            return f'{who}: {_FIELDS[f.group(1)]}'
        if what == 'the text is empty':
            return f'{who}: текстът е празен'
        if what.startswith('the web address may only use'):
            return f'{who}: уеб адресът може да съдържа само малки латински букви, цифри и „-“'
    m = re.fullmatch(r'cover photo (.+) not found', p)
    if m:
        return f'снимката за корицата {m.group(1)} не е намерена'
    m = re.fullmatch(r'web address (.+) is already used by (.+)', p)
    if m:
        return f'уеб адресът {m.group(1)} вече се използва от {m.group(2)}'
    return p


def msg(text):
    """A whole message, which may have a changing part."""
    if lang() != 'bg' or not text:
        return text
    if text in BG:
        return BG[text]
    for pattern, bg in _TEMPLATES:
        m = re.fullmatch(pattern, text, re.S)
        if m:
            return bg.format(x='; '.join(_problem(p) for p in m.group('x').split('; ')))
    for pattern, bg in _KEEP:
        m = re.fullmatch(pattern, text, re.S)
        if m:
            return bg.format(**m.groupdict())
    return text


def when(t, fmt_time=True):
    import time
    lt = time.localtime(t)
    if lang() == 'bg':
        return f'{lt.tm_mday:02d} {MONTHS_BG[lt.tm_mon - 1]} {lt.tm_year}' + (time.strftime(', %H:%M', lt) if fmt_time else '')
    return time.strftime('%d %b %Y, %H:%M' if fmt_time else '%d %b %Y', lt)


# What editor.js needs, sent with each page in Bulgarian
JS_KEYS = ('Nothing has changed yet', 'Fill in both names', 'Close this message', 'New topic', 'Start writing here…', 'Text',
           'Select words, then click a button above. Press Enter for a new paragraph.', 'First select the words you want to colour.',
           'First select the words that should become a link.', 'Web address for the link (starting with https://):',
           'Please enter a full address, starting with https://', 'Continue numbering', 'Restart numbering', 'Complete',
           'Not finished', ' · unsaved changes kept in this browser at {time}', 'The photo will be removed when you save.')
