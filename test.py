import os

from mini_readability import MiniRedability

test_urls = [
    'https://lenta.ru/news/2018/11/14/sankcii/',
    'https://lenta.ru/news/2018/11/15/itsaprotest/',
    'https://www.gazeta.ru/culture/photo/yubilei_svetlany_surganovoi.shtml',
    'https://www.gazeta.ru/science/photo/buran-2018.shtml',
    'https://www.gazeta.ru/business/2018/11/15/12059587.shtml',
    'https://journal.tinkoff.ru/no-diploma-cash/',
    'https://journal.tinkoff.ru/ask/bolnichniy-bez-raboty/',
    'https://medium.com/@KKruglov/127915b78ce2',
    'https://medium.com/@KKruglov/%D0%B1%D1%83%D0%BC-%D0%BF%D0%BE%D0%B4%D0%BA%D0%B0%D1%81%D1%82%D0%BE%D0%B2-766495006408',
]


test_output_folder = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'test'
)
if not os.path.exists(test_output_folder):
    os.makedirs(test_output_folder)

mr = MiniRedability(path_to_save=test_output_folder)

for url in test_urls:
    print('Processing url: ' + url)
    mr.save_article(url)
