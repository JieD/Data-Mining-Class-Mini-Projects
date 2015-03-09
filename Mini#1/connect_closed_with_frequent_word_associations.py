#######################################################################################################################
# This script create a dictionary to map closed word associations to its frequent word association.
# This algorithm is based on the observation that each closed item set precedes its corresponding
# frequent item sets.

# Step:
# 1. read one word association
# 2. if contain the next word association,
#
#    Note: no need to remove duplicate words
# 2. Write each bag of words as one line to the output
#
# Command line arguments:
# [input1]  - a txt file containing all of the word associations
# [output1]  - a txt file containing all closed word associations
# [output2] - a filename to store dictionary which maps closed word associations to frequent word associations
# input1: primitive_word_associations.txt
# output1: closed_word_associations.txt
# output2: dictionary.txt
#
# usage: #python extract_sentences_for_each_word_association.py [input1] [input2] [output1] [output2]
#######################################################################################################################

import sys
import pickle
import lib

def main():
    if len(sys.argv) is not 4:
        print 'incorrect arguments\nneed: input_file.txt output_file1.txt output_file2.txt'
        sys.exit(2)
    else:
        argv1 = sys.argv[1]
        argv2 = sys.argv[2]
        argv3 = sys.argv[3]

    primitive_word_associaiton_file = open(argv1, 'r')
    closed_word_associaiton_file = open(argv2, 'w')
    dictionary = {}

    line = primitive_word_associaiton_file.readline()
    frequent_word_associations = []

    while 1:
        if line == '': # EOF
            closed_word_associaiton_file.close()
            pickle.dump(dictionary, open(argv3, "wb"))
            break

        results = lib.clean_word_association_sent(line)
        closed_word_association, closed_frequency = results[0], results[1]
        frequent_word_associations.append(closed_word_association)

        while 1:
            next_line = primitive_word_associaiton_file.readline()
            if next_line == '': # EOF
                break
            results = lib.clean_word_association_sent(next_line)
            frequent_word_association, frequency = results[0], results[1]

            # check whether corresponding frequent word association
            if frequency == closed_frequency: # possible corresponding frequent word association
                if set(frequent_word_association) < set(closed_word_association): # check subset relationship
                    frequent_word_associations.append(frequent_word_association)
                    continue
            break

        # this is another closed word association, save found frequent word associations
        key = ' '.join(closed_word_association)
        dictionary[key] = frequent_word_associations
        closed_word_associaiton_file.write(key + ' ' + str(closed_frequency) + '\n')

        # house keeping
        frequent_word_associations = []
        line = next_line


if __name__ == "__main__":
    main()