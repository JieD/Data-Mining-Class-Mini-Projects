import re

# remove parenthesis around frequency
def clean_word_association_sent(word_association_sent):
    words = word_association_sent.split()
    frequency = words.pop()
    frequency = frequency.replace('(', '').replace(')', '')
    return [words, frequency]

# check the sent contain the word association
def contain_association(sent, association):
    for word in association:
        if not isContainWord(sent, word):
            return False
    return True

# check whether the sentence contain the word
def isContainWord(sent, word):
    regex = r'\b' + word + r'\b'
    pattern = re.compile(regex, re.I)
    return pattern.search(sent) is not None
