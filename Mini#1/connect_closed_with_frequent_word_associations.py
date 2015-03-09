#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# 1. extract all file names, and store in a text file.
#    use UNIX command: ls -1 [target directory path] | tr '\n' '\0' | xargs -0 -n 1 basename > [outputfile]
# 2. extract all sentences containing the family keywords, prepend with containing file name, store the result.
# 3. remove stop words

#import os
#import extract_sentences_containing_family_member
#os.system(extract_sentences_containing_family_member.py, file.txt, out.txt)

import sys

def main():
    if len(sys.argv) is not 3:
        print 'incorrect arguments\nneed: input_file.txt output_file.txt'
        sys.exit(2)
    else:
        argv1 = sys.argv[1]
        argv2 = sys.argv[2]

    input_file = open(argv1, 'r')
    output_file = open(argv2, 'w')

    line = input_file.readline()
    association = line.split()
    association.pop()

    while 1:
        indexes = []
        line = input_file.readline()
        words = line.split()
        if line == '':
            output_file.close()
            break

        for word in association:
            indexes.append(words.index(word))

        print indexes



if __name__ == "__main__":
    main()