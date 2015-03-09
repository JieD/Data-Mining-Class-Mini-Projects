########################################################################################################################
# This script create ordered word lists file by characteristic and frequency.
# Choose top N = 100, 200, 500, 1000
# usage: #python order_word_lists.py
#
#######################################################################################################################
import re
import lib

def main():

    N = [100, 200, 500, 1000]
    ins, outs = [], []
    #in_file_names = ['results/ordered_word_lists_3.txt', 'results/ordered_word_lists_5.txt', 'results/ordered_word_lists_10.txt']

    #for i in range(0, 3):
    #    ins.append(open(in_file_names[i], 'r'))
    #    outs.append(open(out_file_names[i], 'w'))

    #for i in range(0, 3):
    #    word_list_file = ins[i]
    #    ordered_list_file = outs[i]
    #    dictionary = {}

    #input = open('results/ordered_word_lists_3.txt', 'r')
    input = open('test.txt', 'r')
    output = open('out.txt', 'w')
    #output = open('ordered_lists/one_family_member.txt', 'w')

    family_name_string = 'mother brother grandfather sister grandmother father mom dad son daughter uncle aunt niece nephew cousin'

    while 1:
        line = input.readline()
        if line == '': # EOF
            output.close()
            break

        # read the word list line
        words = line.split()
        frequency = int(words.pop()) # remove support value

        # check whether contain at least one family member
        result = False
        for word in words:
            if lib.isContainWord(family_name_string, word):
                result = True
                break

        if result:
            word_list = ' '.join(words)
            output.write(word_list + ' ' + str(frequency) + '\n')


if __name__ == "__main__":
    main()
