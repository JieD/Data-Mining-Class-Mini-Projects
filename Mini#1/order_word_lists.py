########################################################################################################################
# This script create ordered word lists file by the frequency.
# usage: #python order_word_lists.py
#
#######################################################################################################################

def main():

    ins, outs = [], []
    in_file_names = ['results/word_lists_3.txt', 'results/word_lists_5.txt', 'results/word_lists_10.txt']
    out_file_names = ['results/ordered_word_lists_3.txt', 'results/ordered_word_lists_5.txt', 'results/ordered_word_lists_10.txt']
    for i in range(0, 3):
        ins.append(open(in_file_names[i], 'r'))
        outs.append(open(out_file_names[i], 'w'))

    for i in range(0, 3):
        word_list_file = ins[i]
        ordered_list_file = outs[i]
        dictionary = {}

        while 1:
            line = word_list_file.readline()
            if line == '': # EOF
                break

            # read the word list line
            words = line.split()
            frequency = int(words.pop()) # remove support value
            word_list = ' '.join(words)

            if dictionary.has_key(frequency):
                value = dictionary[frequency]
                value.append(word_list)
                dictionary[frequency] = value
            else:
                dictionary[frequency] = [word_list]

        frequencies = dictionary.keys()
        frequencies.sort(reverse=True)
        for frequency in frequencies:
            word_lists = dictionary[frequency]
            for word in word_lists:
                ordered_list_file.write(word + ' ' + str(frequency) + '\n')
        ordered_list_file.close()


if __name__ == "__main__":
    main()
