########################################################################################################################
# This script create word lists for each frequent word patterns.
#
# For each frequent word association, make word lists by applying order and save its frequency.
#
# Command line arguments:
# [input]  - a txt file containing all the word associations and their containing original sentences
# input: closed_word_association_with_sentences.txt
#
# usage: #python make_word_lists.py [input]
#
#######################################################################################################################
import sys
import re
import pickle

def main():
    if len(sys.argv) is not 2:
        print 'incorrect arguments\nneed: input_file.txt'
        sys.exit(2)
    else:
        input_file1 = sys.argv[1]

    association_file = open(input_file1, 'r')
    dictionary_with_span3 = pickle.load(open('results/dictionary_with_span_3.p', "rb"))
    dictionary_with_span5 = pickle.load(open('results/dictionary_with_span_5.p', "rb"))
    dictionary_with_span10 = pickle.load(open('results/dictionary_with_span_10.p', "rb"))
    dictionaries = [dictionary_with_span3, dictionary_with_span5, dictionary_with_span10]

    # prepare output files
    out = []
    out_file_names = ['results/word_lists_3.txt', 'results/word_lists_5.txt', 'results/word_lists_10.txt']
    loop_count = len(out_file_names)
    for i in range(0, loop_count):
        out.append(open(out_file_names[i], 'w'))

    # for each closed word association, load its frequent word associations from dictionaries.
    # mine each frequent word association for its word lists and frequency
    while 1:
        line = association_file.readline()
        if line == '': # EOF
            for i in range(0, loop_count):
                out[i].close()
            break
        if line == '\n':
            continue

        # read the closed word association line
        closed_word_association = line.split()
        frequency = int(closed_word_association.pop()) # remove support value
        key = ' '.join(closed_word_association)
        word_associations_with_spans = [[], [], []]

        # load frequent word associations from all dictionaries
        for i in range(0, loop_count):
            if dictionaries[i].has_key(key):
                word_associations_with_spans[i] = dictionaries[i][key]

        # utilize superset and subset properties
        # e.g. the set of word associations with span 5 should be superset of the set of word associations with span 3
        for i in range(loop_count - 1, 0, -1):
            for word_association in word_associations_with_spans[i-1]:
                word_associations_with_spans[i].remove(word_association)

        all_word_lists = [[], [], []]
        # read all containing sentences
        sents = []
        for i in range(0, frequency):
            sents.append(association_file.readline())

        # find all word lists and their frequencies for all word associations with all spans
        for i in range (0, loop_count):
            word_associations = word_associations_with_spans[i]

            # find all word lists and frequencies for all word associations with a specific span
            for association in word_associations:
                frequency_dic = {}

                # for each word association, find its word lists and frequencies in all containing sentences
                for sent in sents:
                    word_list = find_word_list(association, sent)
                    if frequency_dic.has_key(word_list):
                        frequency_dic[word_list] += 1
                    else:
                        frequency_dic[word_list] = 1

                all_word_lists[i].append(save_word_list_dic(frequency_dic))

        for i in range(1, loop_count):
            all_word_lists[i].extend(all_word_lists[i - 1])

        for i in range(0, loop_count):
            for word_lists in all_word_lists[i]:
                for word_list in word_lists:
                    out[i].write(word_list + '\n')

# find the word list in sent
def find_word_list(association, sent):
    word_list = ''
    sent_words = sent.split()
    dictionary = create_index_dict(association, sent_words)
    indexes = dictionary.keys()
    indexes.sort()
    for index in indexes:
        word_list += dictionary[index] + ' '
    return word_list.strip()

# create a dictionary of word index and its corresponding word
def create_index_dict(source, target):
    dictionary = {}
    for source_word in source:
        dictionary[target.index(source_word)] = source_word
    return dictionary

def save_word_list_dic(dictionary):
    list = []
    keys = dictionary.keys()
    for key in keys:
        list.append(key + ' ' + str(dictionary[key]))
    return list;

if __name__ == "__main__":
    main()
