#age, fnlwgt, education-num, capital-gain, capital-loss, hours-per-week,
#workclass, education, marital-status, occupation, relationship, race, sex, native-country,

# create a list of data for each attribute,
#
import sys
import helper
import operator
import math
from collections import Counter, OrderedDict

CLASSES = ['>50K', '<=50K']
WORKCLASSES = ['Private', 'Self-emp-not-inc', 'Self-emp-inc', 'Federal-gov', 'Local-gov', 'State-gov',
               'Without-pay', 'Never-worked']
EDUCATION = ['Bachelors', 'Some-college', '11th', 'HS-grad', 'Prof-school', 'Assoc-acdm', 'Assoc-voc',
             '9th', '7th-8th', '12th', 'Masters', '1st-4th', '10th', 'Doctorate', '5th-6th', 'Preschool']
MARITAL_STATUS = ['Married-civ-spouse', 'Divorced', 'Never-married', 'Separated', 'Widowed',
                  'Married-spouse-absent', 'Married-AF-spouse']
OCCUPATIONS = ['Tech-support', 'Craft-repair', 'Other-service', 'Sales', 'Exec-managerial', 'Prof-specialty',
               'Handlers-cleaners', 'Machine-op-inspct', 'Adm-clerical', 'Farming-fishing', 'Transport-moving',
               'Priv-house-serv', 'Protective-serv', 'Armed-Forces']
RELATIONSHIPS =['Wife', 'Own-child', 'Husband', 'Not-in-family', 'Other-relative', 'Unmarried']
RACES = ['White', 'Asian-Pac-Islander', 'Amer-Indian-Eskimo', 'Other', 'Black']
SEXES = ['Female', 'Male']
NATIVE_COUNTRIES = ['United-States', 'Cambodia', 'England', 'Puerto-Rico', 'Canada', 'Germany',
                    'Outlying-US(Guam-USVI-etc)', 'India', 'Japan', 'Greece', 'South', 'China', 'Cuba',
                    'Iran', 'Honduras', 'Philippines', 'Italy', 'Poland', 'Jamaica', 'Vietnam', 'Mexico',
                    'Portugal', 'Ireland', 'France', 'Dominican-Republic', 'Laos', 'Ecuador', 'Taiwan',
                    'Haiti', 'Columbia', 'Hungary', 'Guatemala', 'Nicaragua', 'Scotland', 'Thailand',
                    'Yugoslavia', 'El-Salvador', 'Trinadad&Tobago', 'Peru', 'Hong', 'Holand-Netherlands']


# declare global variables
file_size = 0
dics = {}
categorical_keys = [1, 3, 5, 6, 7, 8, 9, 13]
categorical_dics = []
continuous_keys = [0, 2, 4, 10, 11, 12]
continuous_dics = []
num_categorical = 8
num_coutinuous = 6
histogram_dics = []
Max_k = 20
Ks = [8, 14, 20]
bin_dics = []
Selected_Bin_Widths = [3, 105579, 1, 5000, 311, 5]
Label_Count = Counter()


def main():
    #if len(sys.argv) is not 5:
    #    print 'incorrect arguments\nneed: input_file.txt out_file1.txt out_file2.txt out_file3.txt'
    #    sys.exit(2)
    #else:
    #    argv1 = sys.argv[1]
    #    argv2 = sys.argv[2]
    #    argv3 = sys.argv[3]
    #    argv4 = sys.argv[4]

    visualize_files = ['in_data/adult.all.csv', 'out_data/categorical_all.txt', 'out_data/continuous_all.txt',
                   'out_data/histogram_all.txt']
    train_files = ['in_data/adult.data.csv', 'out_data/categorical_train.txt', 'out_data/continuous_train.txt',
               'out_data/histogram_train.txt']
    init()
    collect_statistics(visualize_files)
    clear()
    collect_statistics(train_files)
    train_classifier()


# init variables
def init():
    global dics, categorical_dics, continuous_dics, histogram_dics, Label_Count
    for i in range(0, 14):
        dics[i] = {}
    categorical_dics = [{}, {}, {}, {}, {}, {}, {}, {}]
    continuous_dics = [{}, {}, {}, {}, {}, {}]
    init_cc()
    histogram_dics = [{}, {}, {}, {}, {}, {}]
    for label in CLASSES:
        Label_Count[label] = 0


def init_cc():
    global categorical_dics, continuous_dics
    init_by_keys(categorical_dics, categorical_keys)
    init_by_keys(continuous_dics, continuous_keys)


def init_by_keys(c_dics, key_list):
    for i in range(0, len(key_list)):
        key = key_list[i]
        dic = dics[key]
        c_dics[i] = dic


# visualize data, write statistics to output files
def collect_statistics(files):
    data_file, categorical_file, continuous_file, histogram_file = files
    parse_file(data_file)
    print "file_size: {0}".format(file_size)
    for label in CLASSES:
        print "{0}: {1}".format(label, Label_Count[label])
    write_categorical_count(categorical_file)
    write_continuous_data(continuous_file)
    write_histogram_data(histogram_file)


# clear dics & histogram_dics
def clear():
    global file_size, dics, categorical_dics, continuous_dics, histogram_dics
    file_size = 0
    for key in dics.keys():
        dics[key].clear()
    clear_dic_list(histogram_dics)
    init_cc()


def clear_dic_list(dic_list):
    for dic in dic_list:
        dic.clear()


def train_classifier():
    print


# read the data file and count frequencies for each unique value
# return the total entries in the file
def parse_file(file_name):
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


# collect data for histograms with different bin choices
def write_histogram_data(file_name):
    global bin_dics
    out = open(file_name, 'w')
    if len(bin_dics) is 0:  # need to select proper bins
        bin_dics = [{}, {}, {}, {}, {}, {}]
        get_proper_bins()
    else:  # bin already selected
        bin_dics = get_bin_by_width(Selected_Bin_Widths)
    for i in range(0, num_coutinuous):
        histogram_three_dics = {}
        bin_dic = bin_dics[i]
        data_dic = continuous_dics[i]
        min_v, max_v = get_min_max(data_dic.keys())
        out.write("min: {0}, max: {1}\n".format(min_v, max_v))
        for bin_num in bin_dic.keys():
            out.write("bin_num: {0}, bin_width: {1}\n".format(bin_num, bin_dic[bin_num]))
            bin_count = helper.BinCount(min_v, max_v, bin_num, bin_dic[bin_num])
            bin_count.generate_bins()
            histogram_dic = get_histogram_dic(data_dic, bin_count)
            write_dic(histogram_dic, out)
            histogram_three_dics[bin_num] = histogram_dic
        out.write("\n")
        histogram_dics[i] = histogram_three_dics
    out.write("\n\n")


# choose bins and save info in bin_dics
def get_proper_bins():
    for i in range(0, num_coutinuous):
        element = continuous_dics[i]
        distance = get_data_distance(element.keys())
        #print "distance: {0}".format(distance)
        if distance <= 100:  # distance too small, try choose bin_width to meet distance % bin_width == 0
            get_bin_info(distance)
            bin_dic = select_bin_info(i)
        else:  # distance big enough to use the standard bin sizes
            bin_dic = get_standard_bin_info(distance)
        bin_dics[i] = bin_dic
        #print bin_dic
    #print '\n'


def get_bin_by_width(wl):
    bin_info = []
    for i in range(0, num_coutinuous):
        bin_info.append({})
        dic = continuous_dics[i]
        distance = get_data_distance(dic.keys())
        width = wl[i]
        quotient, remainder = divmod(distance, width)
        if remainder is not 0 and (remainder * 10.0 / width > 6.5):
            quotient += 1
        bin_info[i][quotient] = width
    return bin_info


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


# select 3 bin_widths to equally divide the distance
# return potential {bin_num: bin_width}
def get_bin_info(distance):
    bin_dic = {1: distance}
    max_d = Max_k if distance >= Max_k else distance
    for divisor in range(2, max_d + 1):
        quotient, remainder = divmod(distance, divisor)
        if remainder == 0:  # equally divide
            bin_dic[divisor] = quotient
        elif (remainder * 10.0) / divisor > 6.5:
            bin_dic[divisor] = quotient + 1
    #print bin_dic
    return bin_dic


# manually select three bin sizes for visualization
def select_bin_info(index):
    if index is 0:
        return {25: 3, 15: 5, 7: 11}
    elif index is 2:
        return {16: 1, 8: 2, 4: 4}
    elif index is 5:
        return {20: 5, 10: 10, 5: 20}


# return {bin_num: bin_width} according to Ks
def get_standard_bin_info(distance):
    bin_dic = {}
    for k in Ks:
        bin_width = distance / k
        bin_dic[k] = bin_width
    return bin_dic


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


def write_dic(dic, out):
    for key in dic.keys():
        out.write("{0} {1}\n".format(key, dic[key]))
    out.write('\n')

def histogram(collection, ol):
    num_values = len(ol)
    k = K if num_values >= K else num_values
    bin_width, adjust = refine_bin_width(get_bin_width(ol, k))
    #print "number of bins: {0}".format(k)
    #print "bin_width: {0}".format(bin_width)
    separator_list = []
    for i in range(0, k):
        low = separator_list[i-1][1] + adjust if i > 0 else ol[i]
        high = low + bin_width
        if adjust == 0.1:
            high = int(high)
        separator_list.append([low, high])
    separator_list[k-1][1] = ol[len(ol) - 1]
    print separator_list
    return separator_list


def get_bin_width(ol, k):
    for i in range(0, len(ol)):
        ol[i] = int(ol[i])
    length = len(ol)
    Min = ol[0]
    Max = ol[length-1]
    #print "Min: {0}, Max: {1}".format(Min, Max)
    return (Max - Min) / (k * 1.0)


def refine_bin_width(bin_width):
    if math.ceil(bin_width) >= 10:
        bin_width = int(bin_width)
        adjust = 1
    else:
        adjust = 0.1
    return [bin_width, adjust]


def get_separator_range(l):
    separator_range = []
    length = len(l)
    for i in range(0, length - 1):
        separator_range.append("{0} - {1}".format(l[i], l[i + 1]))
    return separator_range


def get_bin_count(keys, collection, sl):
    bin_num = len(keys)
    dict = {}
    for i in range(0, bin_num - 1):
        low = sl.index(sl[i])
        high = sl.index(sl[i+1])
        count_list = sl[low:high]


def collect_statistical_data(collection, ol):
    #Q1, Q3, Median = -1, -1, -1
    #Q1_count = file_size * 0.25
    #Q3_count = file_size * 0.75
    #Median_count = file_size * 0.5
    length = len(ol)
    Min = ol[0]
    Max = ol[length-1]
    print "min is {0}, max is {1}".format(min, max)
    for i in range(1, length):
        p_count = collection[i-1][1].get_total_count()
        count = collection[i][1].get_total_count()
        collection[i][1].set_accu_count(count + p_count)  # accumulative count
        print "{0} {1}".format(ol[i], str(p_count+count))


def get_statistical_data(source1, source2, target):
    return source1 if abs(target - source1) >= abs(target - source2) else source2


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


# reconstruct the dictionary with only count value
def reconstruct_data():
    for key in dics.keys():
        dic = dics[key]
        for dict_key in dic.keys():
            count = dic[dict_key]
            dic[dict_key] = count.get_count()


if __name__ == "__main__":
    main()

