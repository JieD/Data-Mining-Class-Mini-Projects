#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# above declares encoding

########################################################################################################################
#
# This script will go through a list of files and extract all sentences that contain a family member.
#
# Command line arguments:
# [input]  - a txt file with a list of Absolute file paths
# [output] - a text file containing all of the sentences that include family member
# input:  report_file_names.txt
# output: family_history_sentences.txt
#
# usage: $python extract_sentences_containing_family_member.py [input] [output]
#
# use this grep command to find all files that contian family members and outputs them to ffiles.txt
# egrep -i -w -l -f fnames ~/Documents/csc898/dataset/dataA/* > ffiles.txt
# where fnames is a file that only contains the line:
# (mother|brother|grandfather|sister|grandmother|father|mom|dad|son|daughter|uncle|aunt|niece|nephew|cousin)('s|s)*
#  ! @ # $ % ^ & * ( ) _ +  // remember the position of the metachars
#
# This file is modified based on Neal Lewis's Family Member Sentence Splitter.
########################################################################################################################

import sys
import re
import nltk
import string
from nltk.tokenize import word_tokenize
import lib

def main():

    # define encoding
    reload(sys)
    sys.setdefaultencoding("ISO-8859-1")

    # load command line arguments
    if len(sys.argv) is not 3:
        print 'incorrect arguments\nneed: input.txt output.txt'
        sys.exit(2)
    else:
        file_names = sys.argv[1]
        out_file_name = sys.argv[2]

    # load all file names
    # all file names have been saved in a text file - argv[1]
    files = []
    for filename in open(file_names, 'r'): files.append(filename.strip())

    #initialize arrays
    family_sentences =[]

    #initialize sentence detector
    #Load a given resource from the NLTK data package.
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

    #initialize regular expression pattern for family members
    #
    # compile a pattern into a RegexObject.
    # r - use Python’s raw string notation for regular expression patterns;
    #    backslashes are not handled in any special way in a string literal prefixed with 'r'.
    # \b - Matches the empty string, but only at the beginning or end of a word.
    # \s - matches any whitespace character
    # re.I - ignore case
    family_names = re.compile(r'\b(mother|brother|grandfather|sister|grandmother|father|mom|dad|son|daughter|uncle|aunt|niece|nephew|cousin)(\'s|s)*\b', re.I)

    counter = 0
    #search through all files
    for f in files:

        contain_family_member = False
        if counter % 40 == 0: print '.',
        counter += 1 # no counter++ in python, 'for i in range (0, 10)'
        text = open(f, 'r').read() # file.read() - read all data

        # split into sentences
        sentences = sent_detector.tokenize(text.strip(), realign_boundaries=True)

        # if sentence contains a family member, save it. Make sure sentence is only one line
        # Sentences are followed by the containing filename.
        for sent in sentences:
            if family_names.search(sent) is not None:
                contain_family_member = True
                # clean sentence - lowercase, strip punctuation and 's (e.g. mother's -> mother), non-ASCII characters
                sent = sent.lower()
                words = word_tokenize(sent)
                splitted_sent = ' '.join(words)
                no_punctuation_sent = splitted_sent.translate(string.maketrans("",""), string.punctuation)
                clean_sent = re.sub(re.compile(r'\bs\b'), '', no_punctuation_sent)
                #remove non-ASCII characters
                clean_sent = re.sub(r'[^\x00-\x7F]+','', clean_sent)
                family_sentences.append(clean_sent.replace('\n',''))
        if contain_family_member: family_sentences.append(f) # save file name

    # write output to file
    outfile = open(out_file_name, 'w')
    for sent in family_sentences:
        outfile.write(sent + '\n')
    
    outfile.close()

if __name__ == "__main__":
    main()

