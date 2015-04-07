import sys
import helper
import operator
import math
from collections import Counter, OrderedDict


# declare global variables
file_size = 0
dics = {}
categorical_keys = [1, 3, 5, 6, 7, 8, 9, 13]
continuous_keys = [0, 2, 4, 10, 11, 12]
num_categorical = 8
num_coutinuous = 6
categorical_dics = []
continuous_dics = []

histogram_dics = []
bin_dics = []
Selected_Bin_Nums = [20, 30, 4, 20, 20, 10]
Selected_Bin_Nums1 = [10, 5, 4, 5, 5, 10]
Selected_Bin_Nums2 = [20, 30, 4, 80, 60, 10]
Label_Count = Counter()
CLASSES = ['>50K', '<=50K']
files = ['out_data/categorical.txt', 'out_data/continuous.txt', 'out_data/histogram.txt', 'out_data/histogram_visual.txt']
gaussian_infos = {}
labeled_dict = {}


def main():
    if len(sys.argv) is not 3:
        print 'incorrect arguments\nneed: file1.txt file2.txt'
        sys.exit(2)
    else:
        training_file = sys.argv[1]
        test_file = sys.argv[2]

    init()
    categorical_file, continuous_file, histogram_file, histogram_file_visual = files
    parse_file(training_file, bin)
    print "file_size: {0}".format(file_size)
    for label in CLASSES:
        print "{0}: {1}".format(label, Label_Count[label])
    write_categorical_count(categorical_file)
    write_continuous_data(continuous_file)
    write_histogram_data(histogram_file, histogram_file_visual, Selected_Bin_Nums2)
    train_gaussian()
    test(test_file, bin)


def run_classifier(file, bin):
    train(file, bin)
    accuracy = test(file, bin)
    clear()
    return accuracy


def train(file, bin):
    init()
    categorical_file, continuous_file, histogram_file, histogram_file_visual = files
    parse_file(file, bin)
    #print "file_size: {0}".format(file_size)
    for label in CLASSES:
        print "{0}: {1}".format(label, Label_Count[label])
    write_categorical_count(categorical_file)
    write_continuous_data(continuous_file)
    write_histogram_data(histogram_file, histogram_file_visual, Selected_Bin_Nums2)
    train_gaussian()


def test(test_file, bin):
    global file_size, labeled_dict
    file_size = 1
    bin_width = bin[1] - bin[0] + 1
    data_file = open(test_file, 'r')
    accuracies = [0, 0]

    while 1:
        line = data_file.readline()

        if line == '': #EOF
            data_file.close()
            break
        if line == '\r' or line == '\n':  #skip empty line
            continue
        file_size += 1

        # separate words and find class label
        if in_range(file_size, bin):
            ll = [x.strip() for x in line.split(',')]
            true_label = ll.pop().rstrip('.')

            for label in CLASSES:
                labeled_dict[label] = {}
                init_dict(labeled_dict[label])

            get_categorical_counts(ll)
            get_bin_counts(ll)
            get_gaussian_counts(ll)
            #print_dict()
            if classify_bin() == true_label:
                accuracies[0] += 1
            if classify_gaussian() == true_label:
                accuracies[1] += 1

    for i in range(0, len(accuracies)):
        accuracies[i] = (accuracies[i] * 100.0) / bin_width
    print "test_size: {0} with accuracy of {1}".format(bin_width, accuracies)
    return accuracies


def print_dict():
    for label in CLASSES:
        print "{0} ps:".format(label)
        for key in labeled_dict[label].keys():
            print "{0}: {1}".format(key, labeled_dict[label][key])

def init_dict(dict):
    dict[1] = []
    dict[2] = []
    dict[3] = []


def classify_bin():
    label_p = {}
    for label in CLASSES:
        dict = labeled_dict[label]
        l1 = dict[1]
        l2 = dict[2]
        label_p[label] = multiply(l1) * multiply(l2)
    c = CLASSES[0] if label_p[CLASSES[0]] > label_p[CLASSES[1]] else CLASSES[1]
    #print label_p
    return c


def classify_gaussian():
    label_p = {}
    for label in CLASSES:
        dict = labeled_dict[label]
        l1 = dict[1]
        l2 = dict[3]
        label_p[label] = multiply(l1) * multiply(l2)
    c = CLASSES[0] if label_p[CLASSES[0]] > label_p[CLASSES[1]] else CLASSES[1]
    return c


def multiply(l):
    product = 1
    for i in l:
        product *= i
    return product


def get_categorical_counts(ll):
    global labeled_dict
    for label in CLASSES:
        for i in range(0, num_categorical):
            index = categorical_keys[i]
            classifier_dict = categorical_dics[i]
            p = get_categorical_p(ll[index], label, classifier_dict)
            labeled_dict[label][1].append(p)


def get_bin_counts(ll):
    global labeled_dict
    for label in CLASSES:
        for i in range(0, num_coutinuous):
            index = continuous_keys[i]
            classifier_dict = histogram_dics[i]
            p = get_bin_p(int(ll[index]), label, classifier_dict)
            labeled_dict[label][2].append(p)


def get_gaussian_counts(ll):
    global labeled_dict
    for label in CLASSES:
        for i in range(0, num_coutinuous):
            index = continuous_keys[i]
            p = get_gaussian_p(int(ll[index]), label, index)
            labeled_dict[label][3].append(p)


def get_gaussian_p(target, label, index):
    mean, variance = gaussian_infos[index][label]
    #if variance == 0:
    #    return 1
    #else:
    return (math.e ** (-1.0 * (((abs(float(target) - mean)) ** 2) / (2 * variance)))) / math.sqrt(2 * math.pi * variance)


def gaussian(target, mean, variance):
    return (math.e ** (-1.0 * (((abs(float(target) - mean)) ** 2) / (2 * variance)))) / math.sqrt(2 * math.pi * variance)


def train_gaussian():
    global gaussian_infos
    for i in range(0, num_coutinuous):
        local_dicts = get_labeled_dict(continuous_dics[i])
        for label in CLASSES:
            dict = local_dicts[label]
            mean = compute_mean(dict, label)
            variance = compute_variance(dict, mean, label)
            gaussian_infos[continuous_keys[i]][label] = [mean, variance]
            #print "{0} - Gaussian: {1} {2}".format(label, mean, variance)
        #print


def get_categorical_p(target, label, dict):
    lc = 0
    if target in dict:
        count = dict[target]
        lc = count.get_label_count(label)
    if lc == 0:
        lc += 1
    p = lc * 1.0 / Label_Count[label]
    return p
    #return lc


def get_bin_p(target, label, dict):
    length = len(dict)
    keys = dict.keys()
    min = get_boundary(keys[0])[0]
    max = get_boundary(keys[length-1])[1]
    #print "target: {0}, min: {1}, max: {2}".format(target, min, max)
    if target < min:
        count = dict[keys[0]]
        #print "lower"
    elif target > max:
        count = dict[keys[length-1]]
        #print "higher"
    else:  # within range
        #print "within range"
        for i in range(0, length):
            boundary = keys[i]
            low, high = get_boundary(boundary)
            if target < low or target > high:
                continue
            else:
                count = dict[keys[i]]
                #print "{0} lies within range no. {1}".format(target, i)
                break
    lc = count.get_label_count(label)
    if lc == 0:
        lc += 1
    p = lc * 1.0 / Label_Count[label]
    return p
    #return lc


def get_boundary(s):
    l = s.split('-')
    for i in range(0, len(l)):
        l[i] = int(l[i])
    return l


def get_labeled_dict(dict):
    local_dicts = {}
    for label in CLASSES:
        local_dicts[label] = transform_dict(dict, label)
    return local_dicts


# get the dictionary for label
def transform_dict(dict, label):
    new_dict = {}
    for key in dict.keys():
        value = dict[key].get_label_count(label)
        if value is not 0:
            new_dict[key] = value
    #print "{0} - {1}".format(label, new_dict)
    return new_dict


def compute_mean(dict, label):
    mean = 0
    for key in dict.keys():
        mean += key * dict[key]
    return (mean * 1.0) / Label_Count[label]


def compute_variance(dict, mean, label):
    sum = 0
    for key in dict.keys():
        deviation = abs(key - mean)
        squared_d = deviation * deviation
        sum += squared_d
    sum = (sum * 1.0) / Label_Count[label]
    return sum


# init variables
def init():
    global dics, categorical_dics, continuous_dics, histogram_dics, Label_Count, gaussian_infos
    for i in range(0, 14):
        dics[i] = {}
    categorical_dics = [{}, {}, {}, {}, {}, {}, {}, {}]
    continuous_dics = [{}, {}, {}, {}, {}, {}]
    init_cc()
    histogram_dics = [{}, {}, {}, {}, {}, {}]
    for label in CLASSES:
        Label_Count[label] = 0
    for index in continuous_keys:
        gaussian_infos[index] = {}


def init_cc():
    global categorical_dics, continuous_dics
    init_by_keys(categorical_dics, categorical_keys)
    init_by_keys(continuous_dics, continuous_keys)


def init_by_keys(c_dics, key_list):
    for i in range(0, len(key_list)):
        key = key_list[i]
        dic = dics[key]
        c_dics[i] = dic


# clear data
def clear():
    global file_size, dics, categorical_dics, continuous_dics, histogram_dics, Label_Count, gaussian_infos, labeled_dict
    file_size = 0
    for key in dics.keys():
        dics[key].clear()
    clear_dic_list(histogram_dics)
    init_cc()
    for label in CLASSES:
        Label_Count[label] = 0
    gaussian_infos = {}
    labeled_dict = {}


def clear_dic_list(dic_list):
    for dic in dic_list:
        dic.clear()


def in_range(target, bin):
    return target >= bin[0] and target <= bin[1]

def out_range(target, bin):
    return target < bin[0] or target > bin[1]

# read the data file and count frequencies for each unique value
# return the total entries in the file
def parse_file(file_name, bin):
    data_file = open(file_name, 'r')
    global file_size, dics, Label_Count

    while 1:
        line = data_file.readline()

        if line == '': #EOF
            data_file.close()
            break
        if line == '\r' or line == '\n':  #skip empty line
            continue
        file_size += 1

        # separate words and find class label
        if out_range(file_size, bin):
            ll = [x.strip() for x in line.split(',')]
            label = ll.pop().rstrip('.')
            Label_Count[label] += 1

            # store each word to its corresponding dictionary and increase its counter
            for i in range(0, len(ll)):
                element = ll[i]
                dic = dics[i]
                if element in dic:  # existing key
                    counter = dic[element]
                    counter.store(label)
                else:  # new key
                    counter = helper.Count(CLASSES)
                    counter.store(label)
                    dic[element] = counter


# sort data in each categorical dictionary by its count in descending order
# save the new ordered dictionary
# write all categorical dictionaries to a file
def write_categorical_count(file_name):
    global categorical_dics
    out = open(file_name, 'w')
    for i in range(0, num_categorical):
        element = categorical_dics[i]
        ordered_categorical_dic = OrderedDict()
        items = element.items()
        sorted_list = sorted(items, key=lambda item: item[1].get_total_count(), reverse=True)  # sort by count
        sorted_key = [x[0] for x in sorted_list]

        # save the ordered dictionary and write to file
        for key in sorted_key:
            count = element[key]
            ordered_categorical_dic[key] = count
            out.write(key + str(count))
            out.write('\n')
        categorical_dics[i] = ordered_categorical_dic
        out.write('\n\n')
    out.close()


# sort data in each continuous dictionary by its key in ascending order
def write_continuous_data(file_name):
    out = open(file_name, 'w')
    order_continuous_data()
    for element in continuous_dics:
        # write to file
        for key in element.keys():
            count = element[key]
            out.write(str(key) + str(count))
            out.write('\n')
        out.write('\n\n')
    out.close()


# order continuous data by its key in ascending order
def order_continuous_data():
    for i in range(0, num_coutinuous):
        element = continuous_dics[i]
        ordered_dict = OrderedDict()
        items = element.items()
        sorted_list = sorted(items, key=lambda item: int(item[0]))  # sort by key value
        sorted_key = [x[0] for x in sorted_list]
        for key in sorted_key:
            ordered_dict[int(key)] = element[key]
        continuous_dics[i] = ordered_dict


# collect data for histograms with bins, write to two files for easy reading and visualization
def write_histogram_data(f1, f2, bin_nums):
    global bin_dics, histogram_dics
    out_r = open(f1, 'w')
    out_v = open(f2, 'w')

    # for each continuous attribute, calculate histogram data according to its given bin_num
    for i in range(0, num_coutinuous):
        bin_num = bin_nums[i]
        bin_width, bin_num = get_bin_width_num(bin_num, i)
        data_dic = continuous_dics[i]
        min_v, max_v = get_min_max(data_dic.keys())
        out_r.write("min: {0}, max: {1}\n".format(min_v, max_v))
        out_v.write("min {0} max {1}\n".format(min_v, max_v))
        out_r.write("bin_width: {0}, bin_num: {1}\n".format(bin_width, bin_num))
        out_v.write("bin_width {0} bin_num {1}\n".format(bin_width, bin_num))

        bin_count = helper.BinCount(min_v, max_v, bin_num, bin_width)
        bin_count.generate_bins()
        histogram_dic = get_histogram_dic(data_dic, bin_count)
        write_dic(histogram_dic, out_r, out_v)

        out_r.write("\n")
        histogram_dics[i] = histogram_dic
    out_r.write("\n\n")
    out_v.write("\n\n")


def get_bin_width_num(bin_num, index):
    element = continuous_dics[index]
    distance = get_data_distance(element.keys())
    bin_width = distance / bin_num
    if bin_width is 0: bin_width = 1

    # calculate the real bin_nums
    bin_num = distance / bin_width
    if distance % bin_width is not 0: bin_num += 1
    return [bin_width, bin_num]


# generate count for each bin
def get_histogram_dic(data_dic, bin_count):
    histogram_dic = OrderedDict()
    keys = data_dic.keys()
    values = data_dic.values()
    high_index = 0
    for bin in bin_count.get_bins():
        low, high = bin
        low_index = keys.index(low) if low in keys else high_index + 1
        if high not in keys:
            high = find_index(high, keys, True)
        high_index = keys.index(high)
        count_list = values[low_index:high_index+1]
        key = list_to_str(bin)
        histogram_dic[key] = helper.combine(count_list, CLASSES)
        #print "{0} {1}\n".format(key, histogram_dic[key])
    return histogram_dic


def write_dic(dic, out_r, out_v):
    for key in dic.keys():
        out_r.write("{0} {1}\n".format(key, dic[key]))
        value = dic[key]
        label_counts = []
        for label in CLASSES:
            label_counts.append(str(dic[key].get_label_count(label)))
        out_v.write("{0} {1}\n".format(key, " ".join(label_counts)))
    out_r.write('\n')
    out_v.write('\n')


# get the range of the lowest and highest element in the ordered list
def get_data_distance(ol):
    min_v, max_v = get_min_max(ol)
    #print "Min: {0}, Max: {1}".format(min_v, max_v)
    return max_v - min_v + 1


# change the data type from string to int of list elements
# return the min and max of the ordered list
def get_min_max(ol):
    length = len(ol)
    for i in range(0, length):
        ol[i] = int(ol[i])
    min_v = ol[0]
    max_v = ol[length - 1]
    return [min_v, max_v]


def find_index(element, l, low):
    step = -1 if low else 1
    while (1):
        if element not in l:
            element += step
        else:
            break
    return element


def list_to_str(l):
    for i in range(len(l)):
        l[i] = str(l[i])
    return '-'.join(l)


# print dics with parsed count info
def print_dics():
    global dics
    readable_dics = {}
    for key in dics.keys():
        dic = dics[key]
        r_dic = {}
        for dict_key in dic.keys():
            count = dic[dict_key]
            r_dic[dict_key] = count.get_count()
        readable_dics[key] = r_dic
        print r_dic


if __name__ == "__main__":
    main()

