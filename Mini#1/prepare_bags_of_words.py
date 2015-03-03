#######################################################################################
# This script
# 1. Transform sentences belonging to the same report as a bag of words
# 1.1 tokenize the sentence, remove punctuation and merge sentences belonging to one report
#     no need to remove duplicate words
# 2. Mine frequent pattern
#
# Command line arguments:
# [input]  - a txt file containing all of the sentences with stopwords removed
# [output] - a text file with all stopwords removed
# input:  stopwords_removed_sentences.txt
# output: bag_of_words_sentences.txt
#
# usage: #python prepare_bags_of_words.py [input] [output]
#
# call Apriori: apriori\ 2/apriori/src/apriori -s1.57m2n2 bag_of_words_sentences.txt primitive_word_associations.txt
#######################################################################################

import sys

def main():
    if len(sys.argv) is not 3:
        print 'incorrect arguments\nneed: input_file.txt output_file.txt'
        sys.exit(2)
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    tokenize(input_file, output_file)

def tokenize(file1, file2):
    in_file = open(file1, 'r')
    out_file = open(file2, 'w')
    while 1:
        sentence = in_file.readline()
        if sentence == '':
            break
        # write all sentences belonging to the same report to one line
        sentence = sentence.replace('\n', ' ').replace('\r', '')
        while 1:
            if len(sentence.split()) > 1:
                out_file.write(sentence)
            else:
                out_file.write('\n')
                break
            sentence = in_file.readline()
            sentence = sentence.replace('\n', ' ').replace('\r', '')

    out_file.close()


if __name__ == "__main__":
  main()
