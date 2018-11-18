from bs4 import BeautifulSoup, Comment, NavigableString
from urllib.parse import urlparse
import os
import requests
import re


class MiniRedability:
    def __init__(self):
        self._whitelisted_tags = [
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
        self._blacklisted_tags = [
            'script',
            'noscript',
            'style',
            'iframe',
            'svg',
            'nav',
            'noindex',
            'footer'
        ]
        self._blacklisted_classes = [
            'sidebar',
            'footer',
            'tabloid',
            'addition',
            'subscribe',
            'preview',
            'recommend'
        ]
        self._blacklisted_ids = [
            'sidebar',
            'footer',
            'tabloid',
            'addition',
            'subscribe',
        ]
        self._text_headers = [
            'h1',
            'h2',
            'h3',
            'h4',
            'h5',
            'h6',
        ]
        self._tags_for_newline = [
            'li',
        ]
        self._tags_for_double_newline = self._text_headers + [
            'p',
            'div',
            'ul',
            'ol',
        ]

    @staticmethod
    def _validate_url(_url):
        try:
            _result = urlparse(_url)
            return all([_result.scheme, _result.netloc, _result.path])
        except:
            return False

    def _extract_info_from_url(self, _url):
        _uri = urlparse(_url)

        self._url_domain = '{uri.scheme}://{uri.netloc}'.format(uri=_uri)

        _path = _uri.path[1:]
        if _path[-1] == '/':
            _path += 'index'
        else:
            _path = re.sub('\.\w*$', '', _path)
        _path += '.txt'

        self._file_path = os.path.abspath(os.path.expanduser(
            os.path.join(os.getcwd(), _uri.netloc, _path)
        ))

    @staticmethod
    def _tags_as_string(tags):
        return ''.join(list(map(lambda _tag: str(_tag), list(tags))))

    def _remove_if_blacklisted_tag(self, _tag):
        if _tag.name.lower() in self._blacklisted_tags:
            _tag.decompose()
            return True
        else:
            return False

    def _remove_if_empty(self, _tag):
        if not _tag.get_text(strip=True) and _tag.name not in self._whitelisted_tags:
            _tag.decompose()
            return True
        else:
            return False

    def _remove_if_blacklisted_class(self, _tag):
        if any(map(
                lambda class_mask: any(
                    class_mask in attr_class for attr_class in _tag.attrs.get('class', [])
                ),
                self._blacklisted_classes
        )):
            _tag.decompose()
            return True
        else:
            return False

    def _remove_if_blacklisted_id(self, _tag):
        if any(map(
                lambda id_mask: any(
                    id_mask in attr_id for attr_id in _tag.attrs.get('id', [])
                ),
                self._blacklisted_ids
        )):
            _tag.decompose()
            return True
        else:
            return False

    def _replace_header_if_contains_h1_h6_tags(self, _tag):
        if any(
                'header' in attr_class for attr_class in _tag.attrs.get('class', [])
        ) and _tag.name not in self._text_headers:
            subheaders_as_string = self._tags_as_string(_tag.find_all(self._text_headers))
            _tag.replace_with(BeautifulSoup(subheaders_as_string, "html.parser"))

    @staticmethod
    def _strip_unnecessary_attributes(_soup):
        for _tag in _soup.find_all():
            if not isinstance(_tag, NavigableString):
                for _subtag in _tag.descendants:
                    if _subtag.name == 'a':
                        _href = _subtag.attrs.get('href', None)
                        if _href is not None:
                            _subtag.attrs = {'href': _href}
                    else:
                        _subtag.attrs = {}

    def _unwrap_divs(self, _tag):
        child_tags = [child_tag for child_tag in _tag.contents if
                      not isinstance(child_tag, NavigableString)
                      and child_tag.name not in self._whitelisted_tags + self._blacklisted_tags]
        if len(child_tags) == 1:
            _tag.unwrap()

    def _remove_tags_with_low_text_length_to_tag_length_ratio(self, _soup):
        for _tag in _soup.find_all():
            if _tag.name not in self._whitelisted_tags:
                _text_length = 0
                _tag_length = len(self._tags_as_string(_tag.contents)) + 1
                for _subtag in _tag.descendants:
                    if isinstance(_subtag, NavigableString):
                        _text_length += len(_subtag)
                ratio = _text_length / _tag_length
                if ratio < 0.45:
                    _tag.decompose()

    def _add_newlines_before_tags(self, _soup):
        for _tag in _soup.find_all():
            if _tag.name in self._tags_for_newline:
                br = BeautifulSoup('<br>', 'html.parser').br
                _tag.insert_before(br)
            elif _tag.name in self._tags_for_double_newline:
                br = BeautifulSoup('<br>', 'html.parser').br
                _tag.insert_before(br)
                br = BeautifulSoup('<br>', 'html.parser').br
                _tag.insert_before(br)

    @staticmethod
    def _unwrap_nested_tags(_body):
        html = ''.join(map(lambda _tag: str(_tag).strip(), _body.prettify().split('\n')))
        _bs = BeautifulSoup('<html>' + html + '</html>', 'html.parser')
        while len(_bs.contents) == 1:
            _bs.contents[0].unwrap()
        return _bs

    def _remove_tags(self, _soup):
        _bs = BeautifulSoup(str(_soup).replace('\n', ''), 'html.parser')
        for _tag in _bs.find_all():
            if _tag.name == 'span':
                _tag.replace_with(
                    BeautifulSoup(
                        ' {} '.format(self._tags_as_string(_tag.contents).strip()),
                        'html.parser'
                    )
                )
            elif _tag.name == 'a':
                _href = _tag.attrs['href']
                if _href[0] == '/':
                    _href = self._url_domain + _href
                _tag.replace_with(
                    BeautifulSoup(
                        ' ({})[{}] '.format(self._tags_as_string(_tag.contents).strip(), _href),
                        'html.parser'
                    )
                )
            elif _tag.name not in ['br']:
                _tag.unwrap()
        return _bs

    @staticmethod
    def _replace_br_tags_with_newline(_soup):
        for _tag in _soup.find_all():
            if _tag.name == 'br':
                _tag.replace_with('\n')

    @staticmethod
    def _limit_number_of_symbols_per_line(_article):
        from textwrap import wrap

        _lines = []
        for _line in _article.split('\n'):
            _lines.append('\n'.join(wrap(_line, 80, break_long_words=False, break_on_hyphens=False)))
        return '\n'.join(_lines)

    def get_article(self, _url):
        if not self._validate_url(_url):
            print('Invalid url: ' + _url)
            return

        self._extract_info_from_url(_url)
        # print(self._file_path)
        # exit()

        soup = BeautifulSoup(requests.get(_url).content, 'html.parser')
        body = soup.find('body')

        # Extract comments
        comments = body.findAll(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        # bold remove unnecessary tags
        for tag in body.find_all():
            if self._remove_if_empty(tag) \
                    or self._remove_if_blacklisted_tag(tag) \
                    or self._remove_if_blacklisted_class(tag) \
                    or self._remove_if_blacklisted_id(tag):
                continue
            self._replace_header_if_contains_h1_h6_tags(tag)

        self._strip_unnecessary_attributes(body)

        # Iterative process of polishing the document
        while True:
            old_document = body.prettify()

            for tag in body.find_all():
                self._unwrap_divs(tag)
                self._remove_if_empty(tag)

            self._remove_tags_with_low_text_length_to_tag_length_ratio(body)

            if old_document == body.prettify():
                break

        article = self._unwrap_nested_tags(body)

        self._add_newlines_before_tags(article)
        article = self._remove_tags(article)
        self._replace_br_tags_with_newline(article)

        article = re.sub('\n\n+', '\n\n', str(article)).strip()

        article = self._limit_number_of_symbols_per_line(article)

        self._save_article(article, self._file_path)

    @staticmethod
    def _save_article(article, _file_path):
        _dirname = os.path.dirname(_file_path)
        if not os.path.exists(_dirname):
            os.makedirs(_dirname)
        with open(_file_path, 'w+') as file:
            file.write(article)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Enter article's URL as a first argument.")
        exit(1)

    url = sys.argv[1]
    MiniRedability().get_article(url)
