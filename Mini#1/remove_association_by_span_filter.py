#######################################################################################
# This script
#
# For each association, count the number to original sentences containing this association.
# Filter the association by the word span, k = 3, 5, 10. Only keep the association
# that meet the span requirement with more than 60% support (60% of the original
# sentences meet the span requirement)
#
# Command line arguments:
# [input1]  - a txt file containing all of the sentences with stopwords removed
# [input2]
# [output] - a text file with all stopwords removed
# input1:  primitive_word_associations.txt
# input2: family_history_sentences.txt
# output: filter_applied_associations.txt
#
# usage: #python remove_association_by_span_filter.py [input1] [input2] [output]
#
#######################################################################################
import sys

def main():
    if len(sys.argv) is not 4:
        print 'incorrect arguments\nneed: input_file1.txt input_file2.txt output_file.txt'
        sys.exit(2)
    else:
        input_file1 = sys.argv[1]
        input_file2 = sys.argv[2]
        output_file = sys.argv[3]

    association_file = open(input_file1, 'r')
    original_history_file = open(input_file2, 'r')
    filter_applied_associations = open(output_file, 'w')

    file_count = 0
    span_count = 0
    k = 3

    while 1:
        line = association_file.readline()
        if line == '':
            filter_applied_associations.close()
            break
        association = line.split()
        association.pop()

        while 1:
            original_sent = original_history_file.readline()
            if original_sent == '':
                break
            if all(x in original_sent for x in association):
                file_count = file_count + 1
                if check_span(original_sent, association, k):
                    span_count = span_count + 1

        if (span_count * 1.0 / file_count) >= 0.6:
            filter_applied_associations.write(line)



def check_span(sentence, association, span_limit):
    words = sentence.split()
    index1 = words.index(association[0])
    index2 = words.index(association[1])
    if abs(index1 - index2) >= span_limit:
        return True
    else:
        return False


if __name__ == "__main__":
    main()
