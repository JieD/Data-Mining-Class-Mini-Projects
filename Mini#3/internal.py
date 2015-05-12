
def import_data(file_name, data):
    in_f = open(file_name, 'r')

    while 1:
        line = in_f.readline()
        if line == '':  # EOF
            in_f.close()
            break
        if line == '\r' or line == '\n':  #skip empty line
            continue

        value = []
        words = line.strip().split(',')[1:]  # skip the first attribute (index)
        cluster = words.pop()  # the last attribute is the cluster
        #print words, cluster
        length = len(words)
        for i in range(0, length - 1):  # skip the last attribute (class label)
            value.append(float(words[i]))
        #print value
        data[cluster].append(value)



def main():
    data = {'cluster0': [], 'cluster1': [], 'cluster2': []}
    import_data('Statistics/iris/kmean_result.arff', data)
    print data['cluster1']


if __name__ == "__main__":
    main()

