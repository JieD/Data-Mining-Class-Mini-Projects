import sys
import train
import math


Length1 = 48842
Length2 = 45222

def k_fold_test(k, file_name, file_length):
    accuracies = []
    bin_width = file_length / k
    bins = []
    for i in range(0, k - 1):
        bins.append([i * bin_width, (i + 1) * bin_width])
        accuracies.append([])
    accuracies.append([])
    bins.append([(k - 1) * bin_width, file_length])

    for i in range(0, k):
        bin = bins[i]
        print bin
        accuracies[i] = train.run_classifier(file_name, bin)
        print
    evaluate(accuracies)

def evaluate(accuracies):
    list1 = [x[0] for x in accuracies]
    list2 = [x[1] for x in accuracies]
    evaluate1(list1)
    evaluate1(list2)

def evaluate1(list):
    #list = [150.5, 170, 160, 161, 170.5]
    size = len(list)
    #print "size: {0}".format(size)
    temp = list[0]
    for i in range(1, size):
        temp += list[i]
    mean = temp / size
    #print "mean: {0}".format(mean)

    temp = 0
    for i in range(0, size):
        deviation = abs(list[i] - mean)
        sd = deviation * deviation
        temp += sd
    #print "squared deviation: {0}".format(temp)

    temp = math.sqrt(temp * 1.0 / (size - 1))
    temp = temp / math.sqrt(size)
    print "mean: {0}, se: {1}".format(mean, temp)
    #print "se: {0}".format(temp)



def main():
    k_fold_test(10, 'in_data/adult.all.csv', Length1)
    k_fold_test(10, 'in_data/adult.all1.csv', Length1)
    k_fold_test(10, 'in_data/adult.all2.csv', Length2)


if __name__ == "__main__":
    main()
