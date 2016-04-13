#!/usr/bin/env python
# coding=utf-8


def token(tokens, i):
    return [tokens[i]]


def pos(tokens, i):
    return ['pos_' + str(i)]


def relpos(tokens, i):
    return ['relpos_' + str(int(i * 10 / len(tokens)))]


def lenght(tokens, i):
    return ['len_' + str(len(tokens[i]))]


def prefix(tokens, i, l):
    l = int(l)
    return ['pre_' + tokens[i][:l]]


def suffix(tokens, i, l):
    l = -1 * int(l)
    return ['suf_' + tokens[i][l:]]


def context(tokens, i, offset):
    offset = int(offset)

    if 0 <= i + offset < len(tokens):
        return [str(offset) + '_' + tokens[i + offset]]

    return []
