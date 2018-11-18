import re
import requests
from bs4 import BeautifulSoup, Comment, NavigableString

url = 'https://lenta.ru/news/2018/11/14/sankcii/pep'
# print(bool(re.match(r'^.*(\.\w+)$', url)))
print(re.sub(
    '\.\w*$',
    '',
    url
))
exit()

url = 'https://medium.com/@KKruglov/%D0%B1%D1%83%D0%BC-%D0%BF%D0%BE%D0%B4%D0%BA%D0%B0%D1%81%D1%82%D0%BE%D0%B2-766495006408'
r = requests.get(url)
with open('resources/medium2.txt', 'wb') as file:
    file.write(r.content)
exit()

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


def tags_as_string(tags):
    return ''.join(list(map(lambda _tag: str(_tag), list(tags))))


html = """<div><a><img/></a>Культура/<time>13.11.2018,19:15</time><a><img/></a>Культура/<time>13.11.2018,09:14</time><a><img/></a>Культура/<time>12.11.2018,22:35</time><a><img/></a>Культура/<time>12.11.2018,10:37</time><a><img/></a>Культура/<time>11.11.2018,10:56</time><a><img/></a>Культура/<time>10.11.2018,23:58</time><a><img/></a>Культура/<time>10.11.2018,22:09</time><a><img/></a>Культура/<time>10.11.2018,21:33</time><a><img/></a></div>"""
soup = BeautifulSoup(html, 'html.parser')
for tag in soup.find_all():
    # if isinstance(tag, NavigableString):
    #     print('{} ——— {}'.format(str(tag), str(tag.contents)))
    _text_length = 0
    _tag_length = len(tags_as_string(tag.contents)) + 1
    for _subtag in tag.descendants:
        if isinstance(_subtag, NavigableString):
            _text_length += len(_subtag)
    ratio = _text_length / _tag_length
    # if ratio:
    #     tag.extract()
    print('{} ——— {} ——— {} ——— {}'.format(tag, _text_length, _tag_length, ratio))

print()
print(soup.prettify())
