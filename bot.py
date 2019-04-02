#!/usr/bin/env python3

from __future__ import division, print_function

import argparse
from collections import defaultdict
from random import sample


def get_ngrams(seq, n):
    ngrams = set()
    current_ngram = tuple()
    for s in seq:
        if len(current_ngram) < n - 1:
            current_ngram += (s,)
        else:
            current_ngram = current_ngram[1:] + (s,)
            ngrams.add(current_ngram)
    return ngrams


def dissociate(full_corpus, num_words, chunk_size):
    ngrams = get_ngrams(full_corpus.lower().split(), chunk_size)
    ngram_mapping = defaultdict(set)
    for ngram in ngrams:
        n_minus_one_gram = ngram[:-1]
        ngram_mapping[n_minus_one_gram].add(ngram)

    current_ngram = sample(ngrams, 1)[0]

    def get_next_word():
        nonlocal current_ngram
        tail = current_ngram[1:]
        if tail in ngram_mapping:
            current_ngram = sample(ngram_mapping[tail], 1)[0]
        else:
            current_ngram = sample(ngrams, 1)[0]
        return current_ngram[-1]

    return " ".join(get_next_word() for _ in range(num_words))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("NUM_WORDS", type=int)
    parser.add_argument("FILENAMES", nargs="+")
    parser.add_argument("--chunk-size", type=int, default=5)
    args = parser.parse_args()

    full_corpus = []
    for fname in args.FILENAMES:
        with open(fname, "r") as f:
            full_corpus.append(f.read())
    full_corpus = " ".join(full_corpus)

    print(dissociate(full_corpus, args.NUM_WORDS, args.chunk_size))


if __name__ == "__main__":
    main()
