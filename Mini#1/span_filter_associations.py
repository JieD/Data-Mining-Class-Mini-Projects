########################################################################################################################
# This script removes word associations if they span over k = 3, 5, 10 words.
#
# Filter each word association by the word span, k = 3, 5, 10.
# Only keep the associations that meet the span requirement with more than 60% support.
# (Out of all the original sentences that contain a word association, 60% of them also
#  meet the span requirement)
# For each closed word association, store its corresponding frequent word associations with span info into dictionaries
#
# Command line arguments:
# [input1]  - a txt file containing all the word associations and their containing original sentences
# [input2] - a dictionary which maps closed word associations to its corresponding frequent word associations
# input1: closed_word_association_with_sentences.txt
# input2: dictionary.p
#
# usage: #python span_filter_associations.py [input1] [input2]
#
#######################################################################################################################
import sys
import re
import pickle

def main():
    if len(sys.argv) is not 3:
        print 'incorrect arguments\nneed: input_file1.txt input_file2.txt'
        sys.exit(2)
    else:
        input_file1 = sys.argv[1]
        input_file2 = sys.argv[2]

    association_file = open(input_file1, 'r')
    dictionary = pickle.load(open(input_file2, "rb"))
    SPAN_LIST = [3, 5, 10]

    # prepare output files
    dictionary_with_span = [{}, {}, {}] # store span filtered dictionaries
    dictionary_names = []
    loop_count = len(SPAN_LIST)
    for i in range(0, loop_count):
        dictionary_names.append('results/dictionary_with_span_' + str(SPAN_LIST[i]) + '.p')

    # write out for easy checking
    out1 = open('results/association_with_span_3.txt', 'w')
    out2 = open('results/association_with_span_5.txt', 'w')
    out3 = open('results/association_with_span_10.txt', 'w')
    out = [out1, out2, out3]

    while 1:
        line = association_file.readline()
        if line == '': # EOF
            for i in range(0, loop_count):
                pickle.dump(dictionary_with_span[i], open(dictionary_names[i], "wb"))
                out[i].close()
            break
        if line == '\n':
            continue

        # read the closed word association line
        closed_word_association = line.split()
        frequency = int(closed_word_association.pop()) # remove support value
        key = ' '.join(closed_word_association)
        frequent_word_associations = dictionary[key]
        filtered_frequent_word_associations = [[], [], []] # to store frequent word associations for each word span

        # read all containing sentences
        sents = []
        for i in range (0, frequency):
            sents.append(association_file.readline())

        # apply word filters to all corresponding frequent word associations
        for word_association in frequent_word_associations:
            span_counts = [0, 0, 0]
            # check span
            for sent in sents:
                results = check_span(word_association, sent, SPAN_LIST)
                # keep word associations that meet word span requirements
                for i in range (0, loop_count):
                    if results[i]: span_counts[i] += 1
            for i in range (0, loop_count):
                if (span_counts[i] * 1.0/frequency) >= 0.6:
                    filtered_frequent_word_associations[i].append(word_association)
                    out[i].write(' '.join(word_association) + '\n')

        # save to dictionaries
        for i in range (0, loop_count):
            if len(filtered_frequent_word_associations[i]) > 0:
                dictionary_with_span[i][key] = filtered_frequent_word_associations[i]


def check_span(association, sent, spans):
    results = [False, False, False]
    sent_words = sent.split()
    indexes = find_indexes(association, sent_words)
    min_index, max_index = min(indexes), max(indexes)
    loop_count = len(spans)
    for i in range(0, loop_count):
        if len(association) <= spans[i]: # association length is not greater than spans
            if max_index - min_index + 1 <= spans[i]:
                results[i] = True
    return results


# find source words indexes in target
def find_indexes(source, target):
    indexes = []
    for source_word in source:
        indexes.append(target.index(source_word))
    return indexes

if __name__ == "__main__":
    main()
