import re
import requests
from bs4 import BeautifulSoup, Comment, NavigableString

# url = 'https://lenta.ru/news/2018/11/14/sankcii/'
# request.urlretrieve(url, 'lenta.txt')

whitelisted_tags = [
    'blockquote',
    'em',
    'i',
    'strong',
    'u',
    'a',
    'b',
    'p',
    'br',
    'code',
    'pre'
]

blacklisted_tags = [
    'script',
    'noscript',
    'style',
    'iframe',
    'svg',
    'nav',
    'noindex',
    'footer'
]

blacklisted_classes = [
    'sidebar',
    'footer',
    'tabloid',
    'addition',
    'subscribe',
    'preview',
    'recommend'
]

blacklisted_ids = [
    'sidebar',
    'footer',
    'tabloid',
    'addition',
    'subscribe',
]

text_headers = [
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
]

tags_for_newline = [
    'li',
]

tags_for_double_newline = text_headers + [
    'p',
    'div',
    'ul',
    'ol',
]


###

# url = 'https://www.gazeta.ru/culture/photo/yubilei_svetlany_surganovoi.shtml'
# r = requests.get(url)


def tags_as_string(tags):
    return ''.join(list(map(lambda _tag: str(_tag), list(tags))))


def remove_if_blacklisted_tag(_tag):
    if _tag.name.lower() in blacklisted_tags:
        _tag.decompose()
        return True
    else:
        return False


def remove_if_empty(_tag):
    if not _tag.get_text(strip=True) and _tag.name not in whitelisted_tags:
        _tag.decompose()
        return True
    else:
        return False


def remove_if_blacklisted_class(_tag):
    if any(map(
            lambda class_mask: any(
                class_mask in attr_class for attr_class in _tag.attrs.get('class', [])
            ),
            blacklisted_classes
    )):
        _tag.decompose()
        return True
    else:
        return False


def remove_if_blacklisted_id(_tag):
    if any(map(
            lambda id_mask: any(
                id_mask in attr_id for attr_id in _tag.attrs.get('id', [])
            ),
            blacklisted_ids
    )):
        _tag.decompose()
        return True
    else:
        return False


def replace_header_if_contains_h1_h6_tags(_tag):
    if any(
            'header' in attr_class for attr_class in _tag.attrs.get('class', [])
    ) and _tag.name not in text_headers:
        subheaders_as_string = tags_as_string(_tag.find_all(text_headers))
        _tag.replace_with(BeautifulSoup(subheaders_as_string, "html.parser"))


def strip_unnecessary_attributes(_soup):
    for _tag in _soup.find_all():
        if not isinstance(_tag, NavigableString):
            for _subtag in _tag.descendants:
                if _subtag.name == 'a':
                    _href = _subtag.attrs.get('href', None)
                    if _href is not None:
                        _subtag.attrs = {'href': _href}
                else:
                    _subtag.attrs = {}


def unwrap_divs(_tag):
    child_tags = [child_tag for child_tag in _tag.contents if
                  not isinstance(child_tag, NavigableString)
                  and child_tag.name not in whitelisted_tags + blacklisted_tags]
    if len(child_tags) == 1:
        _tag.unwrap()


def remove_tags_with_low_text_length_to_tag_length_ratio(_soup):
    for _tag in _soup.find_all():
        if _tag.name not in whitelisted_tags:
            _text_length = 0
            _tag_length = len(tags_as_string(_tag.contents)) + 1
            for _subtag in _tag.descendants:
                if isinstance(_subtag, NavigableString):
                    _text_length += len(_subtag)
            ratio = _text_length / _tag_length
            if ratio < 0.45:
                _tag.decompose()
                # print('{} ——— {} ——— {} ——— {}'.format(_tag, _text_length, _tag_length, _text_length / _tag_length))
            # print('{} ——— {} ——— {} ——— {}'.format(_tag, _text_length, _tag_length, _text_length / _tag_length))


def add_newlines_before_tags(_soup):
    for _tag in _soup.find_all():
        if _tag.name in tags_for_newline:
            br = BeautifulSoup('<br>', 'html.parser').br
            _tag.insert_before(br)
        elif _tag.name in tags_for_double_newline:
            br = BeautifulSoup('<br>', 'html.parser').br
            _tag.insert_before(br)
            br = BeautifulSoup('<br>', 'html.parser').br
            _tag.insert_before(br)


def unwrap_nested_tags(_body):
    html = ''.join(map(lambda _tag: str(_tag).strip(), _body.prettify().split('\n')))
    # _bs = BeautifulSoup('<html>' + str(_body).replace('\n', '') + '</html>', 'html.parser')
    _bs = BeautifulSoup('<html>' + html + '</html>', 'html.parser')
    while len(_bs.contents) == 1:
        _bs.contents[0].unwrap()
    # new_bs.html.unwrap()
    # print(new_bs.contents[0].name)
    return _bs


def remove_tags(_soup):
    _bs = BeautifulSoup(str(_soup).replace('\n', ''), 'html.parser')
    for _tag in _bs.find_all():
        if _tag.name == 'span':
            _tag.replace_with(
                BeautifulSoup(
                    ' {} '.format(tags_as_string(_tag.contents).strip()),
                    'html.parser'
                )
            )
        elif _tag.name == 'a':
            _tag.replace_with(
                BeautifulSoup(
                    ' [{}]({}) '.format(tags_as_string(_tag.contents).strip(), _tag.attrs['href']),
                    'html.parser'
                )
            )
        elif _tag.name not in ['br']:
            _tag.unwrap()
    return _bs


def remove_extra_br(_soup):
    pass


def replace_tags(_soup):
    for _tag in _soup.find_all():
        if _tag.name == 'br':
            _tag.replace_with('\n')


# file_path = 'resources/lenta.txt'
# file_path = 'resources/lenta2.txt'
# file_path = 'resources/gazeta.txt'
file_path = 'resources/gazeta2.txt'
# file_path = 'resources/gazeta3.txt'
# file_path = 'resources/t-j.txt'
# file_path = 'resources/t-j2.txt'
# file_path = 'resources/some_blog.txt'
# file_path = 'resources/medium.txt'
# file_path = 'resources/medium2.txt'

with open(file_path, 'rb') as file:
    webpage = file.read()
    # doc = Document(webpage)
    # print(doc.summary())
    # soup = BeautifulSoup(r.content, 'html.parser', from_encoding='windows-1251')
    soup = BeautifulSoup(webpage, 'html.parser')
    body = soup.find('body')

    # Extract comments
    comments = body.findAll(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    # bold remove unnecessary tags
    for tag in body.find_all():
        if remove_if_empty(tag) \
                or remove_if_blacklisted_tag(tag) \
                or remove_if_blacklisted_class(tag) \
                or remove_if_blacklisted_id(tag):
            continue
        replace_header_if_contains_h1_h6_tags(tag)

    strip_unnecessary_attributes(body)

    # Iterative process of polishing the document
    while True:
        old_document = body.prettify()

        for tag in body.find_all():
            unwrap_divs(tag)
            remove_if_empty(tag)

        # TODO if site is wikipedia - don't run this
        remove_tags_with_low_text_length_to_tag_length_ratio(body)

        # print('===')
        # print('===')
        # print('===')
        # print(body.prettify())

        if old_document == body.prettify():
            break

    article = unwrap_nested_tags(body)

    #
    # convert html to text
    #

    add_newlines_before_tags(article)
    article = remove_tags(article)
    remove_extra_br(article)
    replace_tags(article)

    # print(str(article).replace('\n\n+', '\n\n'))
    print(re.sub('\n\n+', '\n\n', str(article)).strip())
