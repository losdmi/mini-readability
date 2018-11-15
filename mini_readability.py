import requests
from bs4 import BeautifulSoup, Comment, NavigableString

# url = 'https://lenta.ru/news/2018/11/14/sankcii/'
# request.urlretrieve(url, 'lenta.txt')

whitelisted_tags = [
    'blockquote',
    'em',
    'i',
    'img',
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
    'aside',
    'noindex',
    'footer'
]

blacklisted_classes = [
    'sidebar',
    'footer',
    'tabloid',
    'addition',
    'subscribe',
    'preview'
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


###

# url = 'https://www.gazeta.ru/culture/photo/yubilei_svetlany_surganovoi.shtml'
# r = requests.get(url)


def tags_as_string(tags):
    return ''.join(list(map(lambda _tag: str(_tag), list(tags))))


def remove_if_blacklisted_tag(_tag):
    if _tag.name.lower() in blacklisted_tags:
        _tag.extract()
        return True
    else:
        return False


def remove_if_empty(_tag):
    if not _tag.get_text(strip=True) and _tag.name not in whitelisted_tags:
        _tag.extract()
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
        _tag.extract()
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
        _tag.extract()
        return True
    else:
        return False


def replace_header_if_contains_h1_h6_tags(_tag):
    if any(
            'header' in attr_class for attr_class in _tag.attrs.get('class', [])
    ) and _tag.name not in text_headers:
        subheaders_as_string = tags_as_string(_tag.find_all(text_headers))
        _tag.replace_with(BeautifulSoup(subheaders_as_string, "html.parser"))


def unwrap_divs(_tag):
    child_tags = [child_tag for child_tag in _tag.contents if
                  not isinstance(child_tag, NavigableString)
                  and child_tag.name not in whitelisted_tags + blacklisted_tags]
    if len(child_tags) == 1:
        _tag.unwrap()


def remove_if_div_with_short_content(_soup):
    for _tag in _soup.find_all():
        if not isinstance(_tag, NavigableString):
            for _subtag in _tag.descendants:
                _subtag.attrs = {}

            string_ = ''.join(tags_as_string(_tag.contents).split())

            # print('{} ——— {} ——— {}'.format(tag_, string_, len(string_)))

            is_div_with_short_content = _tag.name == 'div' and len(string_) < 60
            _is_empty_tag = not _tag.get_text(strip=True) and _tag.name not in whitelisted_tags
            if is_div_with_short_content or _is_empty_tag:
                _tag.extract()
            #     print('extracted')
            #
            # print()
            # print()
            # print()


def remove_if_tag_only_contain_links(_soup):
    for _tag in _soup.find_all():
        _children = set([_child.name for _child in _tag.contents if _child.name is not None])
        if _children == {'a'}:
            _tag.extract()
            # print('{} ——— {}'.format(_tag, _children))
            # print()


# with open('resources/gazeta.txt', 'rb') as file:
with open('resources/lenta.txt', 'rb') as file:
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

    while True:
        current_document = body.prettify()

        for tag in body.find_all():
            unwrap_divs(tag)

        remove_if_div_with_short_content(body)
        remove_if_tag_only_contain_links(body)

        if current_document == body.prettify():
            break

    # for tag in body.find_all():
    #     for subtag in tag.descendants:
    #         subtag.attrs = {}
    #
    #     string = ''.join(tags_as_string(tag.contents).split())
    #     print('{} - {} - {}'.format(tag, string, len(string)))

    print()
    print()
    print()

    print(body.prettify())
    # print(body.get_text())
