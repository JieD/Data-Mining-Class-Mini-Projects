import sys

Missing_Value = '?'
File_Size = 0


def main():
    if len(sys.argv) is not 3:
        print 'incorrect arguments\nneed: input_file.txt out_file.txt'
        sys.exit(2)
    else:
        argv1 = sys.argv[1]
        argv2 = sys.argv[2]

    remove_missing_value(argv1, argv2)
    print "file size is: {0}".format(File_Size)


def remove_missing_value(input, output):
    global File_Size
    in_f = open(input, 'r')
    out_f = open(output, 'w')
    while (1):
        line = in_f.readline()
        if line == '':  #EOF
            in_f.close()
            out_f.close()
            break
        if line == '\r' or line == '\n':  #skip empty line
            continue

        if not is_contain_missing_value(line):
            out_f.write(line)
            File_Size += 1


def is_contain_missing_value(line):
    return Missing_Value in line


if __name__ == '__main__':
    main()
