def main():
    in_file_name = 'in_data/adult.test.csv'
    out_file_name = 'in_data/adult.test1.csv'
    in_file = open(in_file_name, 'r')
    out_file = open(out_file_name, 'w')

    while 1:
        line = in_file.readline()
        if line == '':  #EOF
            in_file.close()
            out_file.close()
            break
        if line == '\r' or line == '\n':  #skip empty line
            continue

        line = line.rstrip('\n').rstrip('.')
        out_file.write(line + '\n')


if __name__ == '__main__':
    main()
