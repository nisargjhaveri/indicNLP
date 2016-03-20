# Dataset helpers

## ILCI corpus
`ilci_corpus` is for ILCI monolingual POS tagged data files.

Data files are stored in `data/` as `<lang>_<domain>_all_ilci.mono`

The format of file is as followed

- Each line is one sentence
- No header, no sentence id.
- Each space separated token is pair of token and POS tag, written as `<token>\<POS_tag>`.
- Valid POS tags are listed in `ilci_corpus.py`
