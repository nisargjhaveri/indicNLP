# Dataset helpers

## ILCI corpus
`ilci_corpus` is for ILCI monolingual POS tagged data files.

Data files are stored in `data/ilci/` as `<lang>_<domain>_all_ilci.mono`

The format of file is as followed

- Each line is one sentence
- No header, no sentence id.
- Each space separated token is pair of token and POS tag, written as `<token>\<POS_tag>`.
- Valid POS tags are listed in `ilci_corpus.py`

## News articles with primary catagory

Data files are stored in `data/newscat/` with names `<lang>_news.data`.

The format of data file is as followed

- Each line containing on JSON encoded object.
- The medatory fields in JSON object are `title`, `text`, `url` and `mCategory`.
