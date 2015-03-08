########################################################################################################################
#
# This script prepare the sentences to be applied with association mining algorithm.
# 1. Transform each sentence as a bag of words, discard report information
#    Note: no need to remove duplicate words
# 2. Write each bag of words as one line to the output
#
# Command line arguments:
# [input]  - a txt file containing all of the sentences with stopwords removed
# [output] - a text file with all stopwords removed
# input:  stopwords_removed_sentences.txt
# output: bag_of_words_sentences.txt
#
# usage: #python prepare_bags_of_words.py [input] [output]
#
# Call Apriori:
# frequent item sets
# apriori\ 2/apriori/src/apriori -ts -s-5 -m2 results/bag_of_words_sentences.txt results/primitive_word_associations.txt
# closed item sets
# apriori\ 2/apriori/src/apriori -tc -s-5 -m2 results/bag_of_words_sentences.txt results/closed_word_associations.txt
########################################################################################################################

import sys

def main():

    # load command line arguments
    if len(sys.argv) is not 3:
        print 'incorrect arguments\nneed: input_file.txt output_file.txt'
        sys.exit(2)
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    in_file = open(input_file, 'r')
    out_file = open(output_file, 'w')

    # transform the sentences
    while 1:
        sentence = in_file.readline()
        if sentence == '':
            break
        if len(sentence.split()) > 1:
            out_file.write(sentence)
    out_file.close()

if __name__ == "__main__":
    main()
