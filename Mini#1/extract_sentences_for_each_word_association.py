#######################################################################################
#
# This script prepare the sentences to be applied with association mining algorithm.
# 1. Transform each sentence as a bag of words
#    Note: no need to remove duplicate words
# 2. Write each bag of words as one line to the output
#
# Command line arguments:
# [input1]  - a txt file containing all of the word associations
# [input2]  - a txt file containing all of family history sentences
# [output] - a text file containing word associations and the containing family history sentences
# input1: closed_word_associations.txt
# input2: family_history_sentences.txt
# output: bag_of_words_sentences.txt
#
# usage: #python prepare_bags_of_words.py [input] [output]
#
# Call Apriori:
# frequent item sets
# apriori\ 2/apriori/src/apriori -ts -s-5 -m2 results/bag_of_words_sentences.txt results/primitive_word_associations.txt
# closed item sets
# apriori\ 2/apriori/src/apriori -tc -s-5 -m2 results/bag_of_words_sentences.txt results/primitive_word_associations.txt
#######################################################################################

import sys

def main():

    # load command line arguments
    if len(sys.argv) is not 4:
        print 'incorrect arguments\nneed: input_file1.txt input_file2.txt output_file.txt'
        sys.exit(2)
    else:
        input_file1 = sys.argv[1]
        input_file2 = sys.argv[2]
        output_file = sys.argv[3]

    word_association_file = open(input_file1, 'r')
    word_association_with_sentences = open(output_file, 'w')

    family_history_file = open(input_file2, 'r')

    while 1:
        word_association_sent = word_association_file.readline()
        if word_association_sent == '':
            break

        # extract infomation from the sentence
        results = clean_word_association_sent(word_association_sent)
        
        # for each word association, find the sentences that contain it.
        # remove word associations that appear in less than 5 reports
        while 1:




        # write all sentences belonging to the same report to one line
        # while 1:
        #sentence = sentence.replace('\n', ' ').replace('\r', '') # remove newline
        # skip report name line
        if len(word_association_sent.split()) > 1:
            out_file.write(word_association_sent)
        #else: # This line is the report information. It marks reading a new report.
        #    out_file.write('\n')
        #    break
            #sentence = in_file.readline()
    out_file.close()

def clean_word_association_sent(word_association_sent):
    words = word_association_sent.split()
    frequency = words.pop()
    frequency = frequency.replace('(', '').replace(')', '')
    return [words, frequency]

if __name__ == "__main__":
    main()
