########################################################################################################################
# This script create ordered word lists file by characteristic and frequency.
# Choose top N = 100, 200, 500, 1000
# usage: #python order_word_lists.py
#
#######################################################################################################################

import os

N = [100, 200, 500, 1000]
ROOT_DIR = 'ordered_lists'
SPAN_DIR = ['span_3', 'span_5', 'span_10']
N_DIR = ['n_100', 'n_200', 'n_500', 'n_1000']
CHILD_DIR = []
SOURCE_FILE_NAME = ['results/ordered_word_lists_3.txt', 'results/ordered_word_lists_5.txt', 'results/ordered_word_lists_10.txt']
FAMILY_MEMBER = 'family_member.txt'
DISEASE = 'disease.txt'
ONE_FAMILY_MEMBER = 'one_family_member.txt'
NO_FAMILY_MEMBER = 'no_family_member.txt'
ONE_DISEASE = 'one_disease.txt'
NO_DISEASE = 'no_disease.txt'
ONE_FAMILY_MEMBER_NO_DISEASE = 'one_family_member_no_disease.txt'
ONE_FAMILY_MEMBER_ONE_DISEASE = 'one_family_member_one_disease.txt'
NO_FAMILY_MEMBER_NO_DISEASE = 'no_family_member_no_disease.txt'

def main():
    make_directory()

    print SPAN_DIR
    print CHILD_DIR

    for i in range(0, len(SPAN_DIR)):
        dir = SPAN_DIR[i] + '/'
        ordered_word_list = SOURCE_FILE_NAME[i]
        one_family_member_path = dir + ONE_FAMILY_MEMBER
        no_family_member_path = dir + NO_FAMILY_MEMBER
        one_disease_path = dir + ONE_DISEASE
        no_disease_path = dir + NO_DISEASE
        one_family_member_no_disease_path = dir + ONE_FAMILY_MEMBER_NO_DISEASE
        one_family_member_one_disease_path = dir + ONE_FAMILY_MEMBER_ONE_DISEASE
        no_family_member_no_disease_path = dir + NO_FAMILY_MEMBER_NO_DISEASE
        characteristics_for_each_family_member = dir + 'characteristics_for_each_family_member.txt'

        order_list_by_one_attribute(ordered_word_list, one_family_member_path, no_family_member_path, FAMILY_MEMBER)
        order_list_by_one_attribute(ordered_word_list, one_disease_path, no_disease_path, DISEASE)
        order_list_using_intersection(one_family_member_path, no_disease_path, one_family_member_no_disease_path)
        order_list_using_intersection(one_family_member_path, one_disease_path, one_family_member_one_disease_path)
        order_list_using_intersection(no_family_member_path, no_disease_path, no_family_member_no_disease_path)
        order_list_for_each_family_member(FAMILY_MEMBER, one_family_member_path, characteristics_for_each_family_member)

        files = [ONE_FAMILY_MEMBER, ONE_DISEASE, ONE_FAMILY_MEMBER_NO_DISEASE, ONE_FAMILY_MEMBER_ONE_DISEASE,
                 NO_FAMILY_MEMBER_NO_DISEASE]
        for j in range(0, len(CHILD_DIR[i])):
            out_dir = CHILD_DIR[i][j] + '/'
            for k in range(0, len(files)):
                input_file_path = dir + files[k]
                output_file_path = out_dir + files[k]
                choose_top_n(input_file_path, output_file_path, N[j])
        a = 1


def choose_top_n(input, output, n):
    in_file = open(input, 'r')
    out_file = open(output, 'w')
    line_count = 0;
    while 1:
        line = in_file.readline()
        line_count += 1
        if line == '':
            out_file.close()
            break
        if line_count <= n:
            out_file.write(line)


def make_directory():
    create_directory(ROOT_DIR)
    for i in range(0, len(SPAN_DIR)):
        SPAN_DIR[i] = ROOT_DIR + '/' + SPAN_DIR[i]
        create_directory(SPAN_DIR[i])
        tem_dir = []
        for j in range(0, len(N_DIR)):
            dir = SPAN_DIR[i] + '/' + N_DIR[j]
            tem_dir.append(dir)
            create_directory(dir)
        CHILD_DIR.append(tem_dir)


def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)


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


def order_list_for_each_family_member(source, target, out):
    source = make_list(FAMILY_MEMBER)
    target = make_list(target)
    out_file = open(out, 'w')

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
    if len(l1) > len(l2):
        short_l, long_l = l2, l1
    for item in short_l:
        if item in long_l:
            result.append(item)
    return result


# create a list by combining all lines in the file
def make_list(file_name):
    l = []
    f = open(file_name, 'r')
    while 1:
        line = f.readline()
        if line == '':
            break
        l.append(line.strip().lower())
    f.close()
    return l


if __name__ == "__main__":
    main()
