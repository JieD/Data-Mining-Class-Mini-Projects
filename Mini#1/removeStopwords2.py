#######################################################################################
#  This script will remove the stopwords from the sentences in the input file and
#  write the new sentences into the output file.
#
# Command line arguments:
# [input]  - a txt file containing all of the sentences that include family member
# [output] - a text file with all stopwords removed
# input:  family_history_sentences.txt
# output: stopwords_removed_sentences.txt
#
# usage: #python removeStopwords2.py [input] [output]
#######################################################################################

import sys
import re

def main():
    stopwords = re.compile(r'\b(a|an|and|are|as|at|be|by|for|from|has|he|in|is|it|its|of|on|that|the|to|was|were|will|with)\b', re.I)

    if len(sys.argv) is not 3:
        print 'incorrect arguments\nneed: input_file.txt output_file.txt'
        sys.exit(2)
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    in_file = open(input_file, 'r')
    filtered_sents = [];

    while 1:
        line = in_file.readline()
        if line == '': # EOF
            break

        filtered_sent = re.sub(stopwords, '', line)
        filtered_sents.append(filtered_sent)

    out_file = open(output_file, 'w')
    for sent in filtered_sents:
        out_file.write(sent)

    out_file.close()

if __name__ == "__main__":
  main()