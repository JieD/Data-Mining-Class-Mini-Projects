#######################################################################################################################
#
# This script extract sentences that contain a word association.
# For each word association:
# 1. find all the containing sentences
# 2. count its appearances in different reports, remove it if appears in less than MIN_SUP reports
# 3. write word association and its containing sentences to output file
#
# Command line arguments:
# [input1]  - a txt file containing all of the word associations
# [input2]  - a txt file containing all of family history sentences
# [output1] - a text file containing word associations
# [output2] - a text file containing word associations and containing family history sentences
# input1: primitive_closed_word_associations.txt
# input2: family_history_sentences.txt
# output1: closed_word_associations.txt
# output2: closed_word_association_with_sentences.txt
#
# usage: #python extract_sentences_for_each_word_association.py [input1] [input2] [output1] [output2]
#
#######################################################################################################################

import sys
import re
import lib

def main():

    # load command line arguments
    if len(sys.argv) is not 5:
        print 'incorrect arguments\nneed: input_file1.txt input_file2.txt output_file1.txt output_file2.txt'
        sys.exit(2)
    else:
        input_file1 = sys.argv[1]
        input_file2 = sys.argv[2]
        output_file1 = sys.argv[3]
        output_file2 = sys.argv[4]

    primitive_word_association_file = open(input_file1, 'r')
    word_association_file = open(output_file1, 'w')
    word_association_sentences_file = open(output_file2, 'w')
    MIN_SUP = 5;

    while 1:
        file_count = 0;
        containing_sentences = [];

        # read a word association
        line = primitive_word_association_file.readline()
        if line == '': # EOF, close file
            word_association_file.close()
            word_association_sentences_file.close()
            break

        association = line.split()
        association.pop() # remove support value

        # open file to find containing sentences
        family_history_file = open(input_file2, 'r')

        # for each word association, find the sentences that contain it.
        # remove word associations that appear in less than 5 reports
        while 1:
            appear = False
            sent = family_history_file.readline()
            if sent == '': # EOF
                break

            # check all sentences belonging to the same report
            while 1:
                sent = sent.replace('\n', ' ').replace('\r', '') # remove newline
                if len(sent.split()) > 1:
                    if lib.contain_association(sent, association):
                        appear = True
                        containing_sentences.append(sent)
                else: # This line is the report information. It marks reading a new report.
                    if appear:
                        file_count += 1
                    break
                sent = family_history_file.readline()

        if file_count >= MIN_SUP:
            word_association_file.write(line)
            word_association_sentences_file.write('\n' + line)
            for sent in containing_sentences:
                word_association_sentences_file.write(sent + '\n')


if __name__ == "__main__":
    main()
