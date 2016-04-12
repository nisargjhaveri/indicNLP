#!/usr/bin/env python
# coding=utf-8

import os.path

tagset = set(['N', 'N_NN', 'N_NNP', 'N_NNV', 'N_NST', 'PR', 'PR_PRP',
              'PR_PRF', 'PR_PRL', 'PR_PRC', 'PR_PRQ', 'PR_PRI', 'DM',
              'DM_DMD', 'DM_DMR', 'DM_DMQ', 'DM_DMI', 'V', 'V_VM',
              'V_VM_VF', 'V_VM_VNF', 'V_VM_VINF', 'V_VM_VNG', 'V_VN',
              'V_VAUX', 'V_VAUX_VF', 'V_VAUX_VNF', 'V_VAUX_VINF',
              'V_VAUX_VNG', 'V_VAUX_VNP', 'JJ', 'RB', 'PSP', 'CC', 'CC_CCD',
              'CC_CCS', 'CC_CCS_UT', 'RP', 'RP_RPD', 'RP_CL', 'RP_INJ',
              'RP_INTF', 'RP_NEG', 'QT', 'QT_QTF', 'QT_QTC', 'QT_QTO', 'RD',
              'RD_RDF', 'RD_SYM', 'RD_PUNC', 'RD_UNK', 'RD_ECH'])


class ILCI_MonoCorpus:
    def __init__(self, lang, domain):
        self.lang = lang
        self.domain = domain
        self.load_file()

    def load_file(self):
        datapath = os.path.join(os.path.dirname(__file__), 'data', 'ilci')
        filename = '_'.join([self.lang, self.domain, 'all_ilci.mono'])
        self.datafile = open(os.path.join(datapath, filename))

    def tokens(self):
        for sentence in self.sentences():
            for token in sentence:
                yield token

    def sentences(self):
        for rawline in self.datafile:
            line = rawline.decode('utf-8')
            token_tags = line.split()
            tokens_in_line = []
            for token_tag in token_tags:
                try:
                    token, tag = token_tag.split('\\')
                    if tag not in tagset:
                        raise ValueError("Invalid POS tag")
                    tokens_in_line.append((token, tag))
                except ValueError:
                    continue
            yield tokens_in_line


def load(lang, domain):
    return ILCI_MonoCorpus(lang, domain)
