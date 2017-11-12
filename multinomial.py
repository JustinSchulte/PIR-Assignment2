#! /usr/bin/python
# -*- coding: utf-8 -*-


"""MLE for the multinomial distribution."""


from argparse import ArgumentParser
from collections import Counter, OrderedDict
import math


def get_words(file_path):
    """Return a list of words from a file, converted to lower case."""
    with open(file_path, encoding='utf-8') as hfile:
        return hfile.read().lower().split()


def get_probabilities(words, stopwords, k):
    """
    Create a multinomial probability distribution from a list of words:
        1. Find the top-k most frequent words.
        2. For every one of the most frequent words, calculate its probability according to MLE.

    Return a dictionary of size k that maps the words to their probabilities.
    """
    # TODO
    counter = Counter(words)
    for sword in stopwords:
        del counter[sword]
    comWords = dict(counter.most_common(k))
    n = sum(comWords.values()) #count only freq words: n = sum of xi's
#    print(n)
#    print(comWords)
    for key, value in comWords.items():
        comWords[key] = comWords[key] / n #pi = xi / n 
    
#    print(comWords)
    return comWords


def multinomial_pmf(sample, probabilities):
    """
    The multinomial probability mass function.
    Inputs:
        * sample: dictionary, maps words (X_i) to observed frequencies (x_i)
        * probabilities: dictionary, maps words to their probabilities (p_i)

    Return the probability of observing the sample, i.e. P(X_1=x_1, ..., X_k=x_k).
    """
    # TODO
    product = 1
    n = 0
    for key, value in sample.items():
        x = sample[key]
        p = probabilities[key]
        var = math.pow(p, x)
        var = var / math.factorial(x)
        product = product * var
        n = n + x
    
#    print(n)
    product = product * math.factorial(n)
    return product


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('INPUT_FILE', help='A file containing whitespace-delimited words')
    arg_parser.add_argument('SW_FILE', help='A file containing whitespace-delimited stopwords')
    arg_parser.add_argument('-k', type=int, default=10,
                            help='How many of the most frequent words to consider')
    args = arg_parser.parse_args()

    words = get_words(args.INPUT_FILE)
    #print(words)
    stopwords = set(get_words(args.SW_FILE))
    probabilities = get_probabilities(words, stopwords, args.k)

    # we should have k probabilities
    assert len(probabilities) == args.k

    # check if all p_i sum to 1 (accounting for some rounding error)
    assert 1 - 1e-12 <= sum(probabilities.values()) <= 1 + 1e-12

    # check if p_i >= 0
    assert not any(p < 0 for p in probabilities.values())

    # print estimated probabilities
    print('estimated probabilities:')
    i = 1
    for word, prob in probabilities.items():
        print('p_{}\t{}\t{:.5f}'.format(i, word, prob))
        i += 1

    # read inputs for x_i
    print('\nenter sample:')
    sample = {}
    i = 1
    for word in probabilities:
        sample[word] = int(input('X_{}='.format(i)))
        i += 1

    # print P(X_1=x_1, ..., X_k=x_k)
    print('\nresult: {}'.format(multinomial_pmf(sample, probabilities)))


if __name__ == '__main__':
    main()
