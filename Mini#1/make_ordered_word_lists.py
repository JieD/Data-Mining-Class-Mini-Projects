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

    #order_list_by_one_attribute('results/ordered_word_lists_3.txt', 'ordered_lists/one_family_member.txt',
    #                                'ordered_lists/no_family_member.txt', 'family_member.txt')
    #order_list_by_one_attribute('results/ordered_word_lists_3.txt', 'ordered_lists/one_disease.txt',
    #                          'ordered_lists/no_disease.txt', 'disease.txt')
    #order_list_using_intersection('ordered_lists/one_family_member.txt', 'ordered_lists/no_disease.txt',
    #                                       'ordered_lists/one_family_member_no_disease.txt')
    #order_list_using_intersection('ordered_lists/one_family_member.txt', 'ordered_lists/one_disease.txt',
    #                                       'ordered_lists/one_family_member_one_disease.txt')
    #order_list_using_intersection('ordered_lists/no_family_member.txt', 'ordered_lists/no_disease.txt',
    #                                       'ordered_lists/no_family_member_no_disease.txt')
    order_list_for_each_family_member()

def order_list_by_one_attribute(ins, outs1, outs2, attribute_file_name):
    input = open(ins, 'r')
    output1 = open(outs1, 'w')
    output2 = open(outs2, 'w')
    attribute_file = make_list(attribute_file_name)

    while 1:
        line = input.readline()
        if line == '': # EOF
            output1.close()
            output2.close()
            break

        # read the word list line
        words = line.split()
        frequency = int(words.pop()) # remove support value

        # check whether contain at least one disease
        result = False
        for word in words:
            if word in attribute_file:
                result = True
                break

        word_list = ' '.join(words)
        if result:
            output1.write(word_list + ' ' + str(frequency) + '\n')
        else:
            output2.write(word_list + ' ' + str(frequency) + '\n')

def order_list_using_intersection(ins1, ins2, outs):
    output = open(outs, 'w')

    list1 = make_list(ins1)
    list2 = make_list(ins2)
    intersection_l = intersect(list1, list2)

    # not use set intersection since losing descending order of frequency
    #l = list(set(list1) & set(list2))

    for item in intersection_l:
        output.write(item + '\n')
    output.close()

def order_list_for_each_family_member():
    source = make_list('family_member.txt')
    target = make_list('ordered_lists/one_family_member.txt')
    out_file = open('ordered_lists/characteristics_for_each_family_member.txt', 'w')

    for item in source:
        count = 0;
        out_file.write(item + '\n')
        for word_list in target:
            list = word_list.split()
            if item in list:
                out_file.write(word_list + '\n')
                count += 1
                if count >= 20:
                    break
        out_file.write('\n')
    out_file.close()

def intersect(l1, l2):
    result = []
    short_l, long_l = l1, l2
    if (len(l1) > len(l2)):
        short_l, long_l = l2, l1
    for item in short_l:
        if item in long_l:
            result.append(item)
    return result

# create a list by combining all lines in the file
def make_list(file_name):
    l = []
    file = open(file_name, 'r')
    while 1:
        line = file.readline()
        if line == '':
            break
        l.append(line.strip().lower())
    file.close()
    return l


if __name__ == "__main__":
    main()
