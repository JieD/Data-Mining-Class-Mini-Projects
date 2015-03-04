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

def main():

  reload(sys) # gives back the setdefaultencoding() function that was deleted from sys
  sys.setdefaultencoding("ISO-8859-1") # AttributeError: 'module' object has no attribute 'setdefaultencoding'

  # load command line arguments
  if len(sys.argv) is not 3: # argv[0] is the python script name
    print 'incorrect arguments\nneed: inputfilelist.txt outputfile.txt'
    sys.exit(2) # Unix programs generally use 2 for command line syntax errors and 1 for all other kind of errors.
  else:
    filenames = sys.argv[1]
    outfilename = sys.argv[2]

  # load all filenames
  # all filenames have been saved in a text file - argv[1]
  files =[]
  for filename in open(filenames, 'r'): files.append(filename.strip())
  #string.strip() - Return a copy of the string with leading and trailing characters removed.

  #initialize arrays 
  familysentences =[]

  #initialize sentence detector
  #Load a given resource from the NLTK data package.
  sentdetector = nltk.data.load('tokenizers/punkt/english.pickle')

  #initialize regular expression pattern for family members
  #
  # compile a pattern into a RegexObject.
  # r - use Python’s raw string notation for regular expression patterns;
  #    backslashes are not handled in any special way in a string literal prefixed with 'r'.
  # \b - Matches the empty string, but only at the beginning or end of a word.
  # \s - matches any whitespace character
  # re.I - ignore case
  familynames = re.compile(r'\b(mother|brother|grandfather|sister|grandmother|father|mom|dad|son|daughter|uncle|aunt|niece|nephew|cousin)(\'s|s)*\b', re.I)

  counter = 0
  #search through all files
  for file in files:

    contain_family_member = False
    if counter % 40 == 0:  print '.',
    counter = counter + 1 # no counter++ in python, 'for i in range (0, 10)'
    text = open(file, 'r').read() # file.read() - read all data

    # split into sentences
    sentences = sentdetector.tokenize(text.strip(), realign_boundaries=True)

    # if sentence contains a family member, save it. Make sure sentence is only one line
    # Sentences are followed by the containing filename.
    for sent in sentences:
      if familynames.search(sent) is not None:
          contain_family_member = True

          # clean sentence - lowercase and strip punctuation
          sent = sent.lower()
          words = word_tokenize(sent)
          splitted_sent = ' '.join(words)
          no_punctuation_sent = splitted_sent.translate(string.maketrans("",""), string.punctuation)
          clean_sent = re.sub(re.compile(r'\bs\b'), '', no_punctuation_sent)

          familysentences.append(clean_sent.replace('\n',''))

    if contain_family_member: familysentences.append(file) # save file name

  # write output to file
  outfile = open(outfilename, 'w')
  for sent in familysentences:
    # print sent
    outfile.write(sent + '\n')

  outfile.close()  

if __name__ == "__main__":
  main()

