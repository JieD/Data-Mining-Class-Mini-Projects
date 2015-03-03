#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# 1. extract all file names, and store in a text file.
#    use UNIX command: ls -1 [target directory path] | tr '\n' '\0' | xargs -0 -n 1 basename > [outputfile]
# 2. extract all sentences containing the family keywords, prepend with containing file name, store the result.
# 3. remove stop words

import os
import extract_sentences_containing_family_member

os.system(extract_sentences_containing_family_member.py, file.txt, out.txt)