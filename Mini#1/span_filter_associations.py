#######################################################################################
# This script removes word associations by apply word span filter k = 3, 5, 10.
#
# Filter each word association by the word span, k = 3, 5, 10.
# Only keep the associations that meet the span requirement with more than 60% support.
# (Out of all the original sentences that contain a word association, 60% of them also
#  meet the span requirement)
#
# Command line arguments:
# [input1]  - a txt file containing all the primitive word associations
# [input2] - a text file containing all the original sentences
# [output] - a text file to write all filtered word associations
# input1:  primitive_word_associations.txt
# input2: family_history_sentences.txt
# output: filter_applied_associations.txt
#
# usage: #python span_filter_associations.py [input1] [input2] [output]
#
#######################################################################################
import sys
import re

def main():
    SPAN_LIST = [3, 5, 10]
    OUTPUT_FILE = 'results/association_with_span_'

    if len(sys.argv) is not 3:
        print 'incorrect arguments\nneed: input_file1.txt input_file2.txt'
        sys.exit(2)
    else:
        input_file1 = sys.argv[1]
        input_file2 = sys.argv[2]
    association_file = open(input_file1, 'r')

    out = []
    loop_count = len(SPAN_LIST)
    for i in range(0, loop_count):
        out_file_name = OUTPUT_FILE + str(SPAN_LIST[i]) + '.txt'
        out.append(open(out_file_name, 'w'))

    while 1:
        file_count = 0
        span_counts = [0, 0, 0]

        line = association_file.readline()
        if line == '': # EOF
            break
        association = line.split()
        association.pop() # remove support value
        original_history_file = open(input_file2, 'r')

        # apply word span filters
        while 1:
            sent = original_history_file.readline()
            if sent == '': # EOF
                if file_count > 0:
                    for i in range (0, loop_count):
                        if (span_counts[i] * 1.0 / file_count) >= 0.6:
                            out[i].write(line)
                break
            #if all(x in sent for x in association): not good e.g. 'fam' in 'family history ' == True
            if contain_association(sent, association):
                file_count += 1
                results = check_span(sent, association, SPAN_LIST)

                for i in range (0, loop_count):
                    try:
                        if results[i]: span_counts[i] += 1
                    except IndexError:
                        print span_counts
                        print results
                        print i
                        print association
                        print sent

    for i in range(0, loop_count):
        out[i].close()

def contain_association(sent, association):
    regex1 = r'\b' + association[0] + r'\b'
    regex2 = r'\b' + association[1] + r'\b'
    pattern1 = re.compile(regex1, re.I)
    pattern2 = re.compile(regex2, re.I)
    if pattern1.search(sent) is not None:
        if pattern2.search(sent) is not None:
            return True
    return False

def check_span(sent, association, spans):
    results = [False, False, False]
    words = sent.split()
    try:
        index1 = words.index(association[0])
        index2 = words.index(association[1])
        for i in range(0, len(spans)):
            if abs(index1 - index2) >= spans[i]:
                results[i] = True
        return results
    except ValueError: # caused by unrecognizable mark
        #TODO: check span filter
        return results

if __name__ == "__main__":
    main()
