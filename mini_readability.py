# from readability import Document
import re

from bs4 import BeautifulSoup, Comment, NavigableString
from urllib import request

# url = 'https://lenta.ru/news/2018/11/14/sankcii/'
# request.urlretrieve(url, 'lenta.txt')

whitelist = [
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
    'aside'
]

blacklisted_classes = [
    'sidebar',
    'footer',
    'tabloid',
    'addition'
]

text_headers = [
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
]

with open('resources/lenta.txt', 'r') as file:
    webpage = file.read()
    # doc = Document(webpage)
    # print(doc.summary())
    soup = BeautifulSoup(webpage, 'html.parser')
    body = soup.find('body')

    for tag in body.find_all():
        is_empty_tag = not tag.get_text(strip=True)
        is_blacklisted_tag = tag.name.lower() in blacklisted_tags
        if_blacklisted_class = any(map(
            lambda class_mask: any(class_mask in attr_class for attr_class in tag.attrs.get('class', [])),
            blacklisted_classes
        ))
        is_header = any('header' in attr_class for attr_class in tag.attrs.get('class', []))

        if is_empty_tag \
                or is_blacklisted_tag \
                or if_blacklisted_class:
            tag.extract()
        elif is_header:
            headers = list(map(lambda header: str(header), list(tag.find_all(text_headers))))
            tag.replace_with(BeautifulSoup(''.join(headers), "html.parser"))

    # Extract comments
    comments = body.findAll(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    for tag in body.find_all():
        child_tags = [child_tag for child_tag in tag.contents if
                      not isinstance(child_tag, NavigableString) and child_tag.name not in whitelist]
        if len(child_tags) == 1:
            tag.unwrap()

    print(body.prettify())
    # print(body.get_text())


