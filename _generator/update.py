import pypandoc
import yaml
import re
import ads
import requests
from string import ascii_letters
import re
import os
from collections import namedtuple


class Parser:
    filters = ['pandoc-citeproc']
    pdoc_args = ['--mathjax']

    def fill(self, pattern, data, format, to):
        if isinstance(data, str):
            return pattern.replace('%%', str(data))

        if isinstance(data, (list, tuple)):
            items = enumerate(data)
        else:
            items = data.items()
        for key, value in items:
            value = self.convert_text(value, format, to)
            pattern = pattern.replace('%{}%'.format(str(key)), str(value))
        return pattern

    def convert_text(self, text, format, to):
        if isinstance(text, (list, tuple)):
            text = '\n'.join(text)
        t = pypandoc.convert_text(str(text), to, format=format, extra_args=self.pdoc_args, filters=self.filters).strip()
        if to == 'latex':
            return t.replace(r'\[', '$').replace(r'\]', '$')
        return t



class List(Parser):
    def fill(self, pattern, data, format, to):
        return '\n'.join(super(List, self).fill(pattern, d, format, to) for d in data)


PARSERS = {'FILL': Parser(), 'LIST': List()}


def parse(template, data, template_format='latex', ignore_unmatched=False):
    regex = "%FORMAT\\[(\\w*)\\]\\[(\\w+)\\](.+)"
    found = re.search(regex, template)
    while found:
        key, p, pattern = found.groups()
        pattern = pattern.replace('\\n', '\n')
        parser = PARSERS[p]
        try:
            if key == '':
                datum = data
            else:
                datum = data[key]
            replace = parser.fill(pattern, datum, 'md', template_format)
        except KeyError as e:
            if ignore_unmatched:
                replace = pattern
            else:
                raise e

        template = template[:found.start()] + replace + template[found.end():]
        found = re.search(regex, template)
    return template


ARXIV = r'arXiv:(\d{4}\.\d{5})'
DOI = r'(.*/.*/.*)'


def arxiv_id(paper):
    for id in paper.identifier:
        if 'arxiv:' in id.lower():
            return '{}'.format(re.search(ARXIV, id).groups()[0])
    else:
        return ''


def clean_title(paper):
    title = paper.title[0]
    return title, paper.pubdate + '-' + ''.join([i if i in ascii_letters else '-' for i in title.split(':')[0]])

def clean_date(paper):
    return paper.pubdate.replace('00', '01')

def clean_authors(paper, start='**', end='**'):
    try:
        authors = paper.author
    except AttributeError:
        authors = paper['authors']
    return '; '.join(['{}{}{}'.format(start, i, end) if 'Read, S' in i else i for i in authors])


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(here, 'cv-shauncread.template.tex'), 'r') as f:
        latex_cv_template = f.read()

    with open(os.path.join(here, 'cv-shauncread.template.md'), 'r') as f:
        markdown_cv_template = f.read()

    with open(os.path.join(here, 'paper-page-template.md'), 'r') as f:
        markdown_paper_page_template = f.read()

    with open(os.path.join(here, 'info.yml'), 'r') as f:
        from yaml import CLoader as Loader
        info = yaml.load(f, Loader=Loader)
    
    print('finding papers...')
    fields = ['title', 'pubdate', 'pub', 'abstract', 'identifier', 'bibcode', 'doi', 'author', 'year']
    published = []
    for entry in info['published']['ADS']:
        for paper in ads.SearchQuery(author='Read, S.C.', sort="year", aff="*Hertfordshire*", 
                                     database='astronomy', fl=fields):
            d = {f: getattr(paper, f) for f in fields}
            d['authors'] = clean_authors(paper)
            d['title'], d['filename'] = clean_title(paper)
            d['date'] = clean_date(paper)
            d['arxiv'] = arxiv_id(paper)
            published.append(d)
    print(len(published), 'published papers found on ADS')
    info['published'] = published
    
    for entry in info['unpublished']:
        entry['authors'] = clean_authors(entry)

    print('parsing cv...')
    new_latex_cv = parse(latex_cv_template, info, 'latex')
    new_markdown_cv = parse(markdown_cv_template, info, 'md')

    print('updating cv...')
    with open('_latex/cv-shauncread.tex', 'w') as f:
        f.write(new_latex_cv)

    with open('_pages/cv.md', 'w') as f:
        f.write(new_markdown_cv)

    print('updating publication list... ')
    for paper in published:
        fname = '_publications/{}.md'.format(paper['filename'])
        if (not os.path.exists(fname)) or args.overwrite:
            print('writing new paper:  {}'.format(paper['title']))
            page = parse(markdown_paper_page_template, paper, 'md')
            with open(fname, 'w') as f:
                f.write(page)
        else:
            print('not overwriting existing paper: {}'.format(paper['title']))

