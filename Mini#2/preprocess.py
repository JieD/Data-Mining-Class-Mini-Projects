import sys

Missing_Value = '?'
Replace_dic = {1: 'Private', 6: 'Prof-specialty', 13: 'United-States'}
files = ['in_data/adult.all.csv', 'in_data/adult.all1.csv']


def main():
    remove_missing_value()


def remove_missing_value():
    global File_Size
    in_f = open(files[0], 'r')
    out_f = open(files[1], 'w')

    target_indexes = Replace_dic.keys()

    while (1):
        line = in_f.readline()
        if line == '':  #EOF
            in_f.close()
            out_f.close()
            break
        if line == '\r' or line == '\n':  #skip empty line
            continue

        # separate words
        ll = [x.strip() for x in line.split(',')]

        # remove missing values
        for i in range(0, len(ll) - 1):
            if i in target_indexes and ll[i] == Missing_Value:
                ll[i] = Replace_dic[i]

        out_f.write(','.join(ll))
        out_f.write('\n')

if __name__ == '__main__':
    main()
