import requests
from bs4 import BeautifulSoup, Comment, NavigableString

# url = 'https://www.gazeta.ru/culture/photo/yubilei_svetlany_surganovoi.shtml'
# r = requests.get(url)
# with open('resources/gazeta.txt', 'wb') as file:
#     file.write(r.content)
# exit()

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

html = """<div><a><img/></a>Культура/<time>13.11.2018,19:15</time><a><img/></a>Культура/<time>13.11.2018,09:14</time><a><img/></a>Культура/<time>12.11.2018,22:35</time><a><img/></a>Культура/<time>12.11.2018,10:37</time><a><img/></a>Культура/<time>11.11.2018,10:56</time><a><img/></a>Культура/<time>10.11.2018,23:58</time><a><img/></a>Культура/<time>10.11.2018,22:09</time><a><img/></a>Культура/<time>10.11.2018,21:33</time><a><img/></a></div>"""
soup = BeautifulSoup(html, 'html.parser')
for tag in soup.find_all():
    # if isinstance(tag, NavigableString):
        print(tag)

print()
print(soup.prettify())
