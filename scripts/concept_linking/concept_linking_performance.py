#!/usr/bin/pypy
# Measures YodaQA concept linking performance
# requires the fixed QuestionDump json and the dataset
# exact match means all correct concepts were found
# partial match means -some- (atleast one) correct concept were found
# incorrect means no expected concept was found
# then there is the total number of concepts found vs expected
# usage:
# python concept_linking_performance.py questionDump.json correct_dataset.json
from __future__ import print_function
import sys
import json
import itertools


def compare(dataset, correct):
    partial_match = 0
    exact_match = 0
    concepts_to_be_found = 0
    concepts_found = 0
    total = len(dataset)
    for entry, standard in itertools.izip(dataset, correct):
        if entry['qId'] != standard['qId']:
            print("Incorrect match. Please sort dataset")
            break
        found_one = False
        found_all = True
        for concept in standard['Concept']:
            found_any = False
            concepts_to_be_found += 1
            for concept2 in entry['Concept']:
                if concept['pageID'] == concept2['pageID']:
                    concepts_found += 1
                    found_one = True
                    found_any = True
            if found_any is False:
                found_all = False
        if found_one is False:
            print("no match found for " + str(entry['qId']))
            continue
        if found_all is True:
            print("full match for " + str(entry['qId']))
            exact_match += 1
        else:
            print("partial_match for " + str(entry['qId']))
            partial_match += 1
    print("exact match: {0} questions".format(exact_match))
    print("partial_match: {0} questions".format(partial_match))
    print("not found: {0} questions".format(total - (partial_match + exact_match)))
    print("partial or exact match: {0}% questions".format((exact_match + partial_match) / float(total) * 100))
    print("found {0} out of {1} concepts, {2}% ".format
          (concepts_found, concepts_to_be_found,
           (concepts_found / float(concepts_to_be_found)) * 100))


def main():
    dataset = json.load(open(sys.argv[1], 'r'))
    correct = json.load(open(sys.argv[2], 'r'))
    compare(dataset, correct)


if __name__ == '__main__':
    main()
