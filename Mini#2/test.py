#age, fnlwgt, education-num, capital-gain, capital-loss, hours-per-week,
#workclass, education, marital-status, occupation, relationship, race, sex, native-country,

# create a list of data for each attribute,
#
import sys
from collections import Counter

def main():
    if len(sys.argv) is not 2:
        print 'incorrect arguments\nneed: input_file.txt'
        sys.exit(2)
    else:
        argv1 = sys.argv[1]

    data_file = open(argv1, 'r')
    data_list = []

    header_line = data_file.readline();
    while 1:
        line = data_file.readline()
        if line == '': #EOF
            data_file.close()
            break
        if line == '\r' or line == '\n':
            continue

        data_list.append(line)

    print(data_list)


if __name__ == "__main__":
    main()

