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

blacklist = [
    'script',
    'noscript',
    'style',
    'iframe',
    'svg',
]

text_headers = [
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
]

html = """<div class="g-application js-root" id="root"><div><div>foo</div></div></div><div>ofo</div><div><h3>bar</h3><h2></h2><h4 class='title'></h4><p>baz</p></div>"""
soup = BeautifulSoup(html, 'html.parser')
for tag in soup.find_all():
    # tag.
    child_tags = [child_tag for child_tag in tag.contents if not isinstance(child_tag, NavigableString) and child_tag.name not in whitelist]
    print('{} - {} - {}'.format(tag, child_tags, len(tag.contents)))
    # print('{} - {}'.format(tag, type(tag)))

    if len(child_tags) == 1:
        tag.unwrap()



    # print(dir(tag.find_all(text_headers)))
    # headers = list(map(lambda header: str(header), list(tag.find_all(text_headers))))
    # if len(headers) > 0:
    #     tag.replace_with(BeautifulSoup(''.join(headers), "html.parser"))

# with open('lenta.txt', 'r') as file:
#     webpage = file.read()
#     # doc = Document(webpage)
#     # print(doc.summary())
#     soup = BeautifulSoup(webpage)
#     body = soup.find('body')
#
#     for tag in body.findAll():
#         if tag.name.lower() in blacklist or not tag.contents:
#             tag.extract()
#
#     # Extract comments
#     comments = body.findAll(text=lambda text: isinstance(text, Comment))
#     for comment in comments:
#         comment.extract()
#
print()
print(soup.prettify())
