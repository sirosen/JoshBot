#!/usr/bin/env python

from __future__ import print_function, division


def get_ngrams(seq, n):
    ngrams = set()
    current_ngram = ()
    for s in seq:
        if len(current_ngram) < n - 1:
            current_ngram += (s,)
        else:
            current_ngram = current_ngram[1:] + (s,)
            ngrams.add(current_ngram)
    return ngrams


def dissociate(s, num_words, chunk_size):
    from random import sample
    seq = s.lower().split()
    ngrams = get_ngrams(seq, chunk_size)
    ngram_mapping = {}
    for ngram in ngrams:
        n_minus_one_gram = ngram[:-1]
        if n_minus_one_gram not in ngram_mapping:
            ngram_mapping[n_minus_one_gram] = set()
        ngram_mapping[n_minus_one_gram].add(ngram)
    cur_num_words = chunk_size - 1
    current_ngram = sample(ngrams, 1)[0]
    out_s = []
    while cur_num_words < num_words:
        out_s.append(current_ngram[-1])
        tail = current_ngram[1:]
        if tail not in ngram_mapping:
            current_ngram = sample(ngrams, 1)[0]
        else:
            current_ngram = sample(ngram_mapping[current_ngram[1:]], 1)[0]
        cur_num_words += 1
    out_s = ' '.join(out_s)
    return out_s

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print(
            "USAGE ERROR. bot.py filename num-words [chunk-size]",
            file=sys.stderr)
        sys.exit(1)
    fname = sys.argv[1]
    num_words = int(sys.argv[2])
    chunk_size = 5
    if len(sys.argv) > 3:
        chunk_size = int(sys.argv[3])

    f = open(fname, 'r')
    s = f.read()
    f.close()

    print(dissociate(s, num_words, chunk_size))
