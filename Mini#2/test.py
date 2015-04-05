#age, fnlwgt, education-num, capital-gain, capital-loss, hours-per-week,
#workclass, education, marital-status, occupation, relationship, race, sex, native-country,

# create a list of data for each attribute,
#
import sys
import helper
import operator
import math
from collections import OrderedDict

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
categorical_dics = []
continuous_dics = []
histogram_dics = []
Max_k = 20
Ks = [8, 14, 20]
num_coutinuous = 0

# init variables
def init_dics():
    workclass_dic, education_dic, marital_status_dic, occupation_dic, relationship_dic, race_dic, \
    sex_dic, native_country_dic = {}, {}, {}, {}, {}, {}, {}, {}
    age_dic, fnlwgt_dic, education_num_dic, capital_gain_dic, capital_loss_dic, hours_per_week_dic \
        = {}, {}, {}, {}, {}, {}
    global dics, categorical_dics, continuous_dics, num_coutinuous
    dics = { 0: age_dic,            1: workclass_dic,    2: fnlwgt_dic,       3: education_dic, 4: education_num_dic,
             5: marital_status_dic, 6: occupation_dic,   7: relationship_dic, 8: race_dic,      9: sex_dic,
            10: capital_gain_dic,  11: capital_loss_dic, 12: hours_per_week_dic, 13: native_country_dic}
    categorical_dics = [workclass_dic, education_dic, marital_status_dic, occupation_dic, relationship_dic, race_dic,
                        sex_dic, native_country_dic]
    continuous_dics = [age_dic, fnlwgt_dic, education_num_dic, capital_gain_dic, capital_loss_dic, hours_per_week_dic]
    num_coutinuous = len(continuous_dics)


# clear values for all dictionaries
def clear_values():
    for key in dics.keys():
        dics[key].clear()


# read the data file and count frequencies for each unique value
# return the total entries in the file
def parse_file(file_name):
    data_file = open(file_name, 'r')
    global file_size

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

        # store each word to its corresponding dictionary and increase its counter
        for i in range(0, len(ll)):
            element = ll[i]
            dic = dics[i]
            if element in dic:  # existing key
                counter = dic[element]
                counter.store(label)
            else:  # new key
                counter = helper.Count()
                counter.store(label)
                dic[element] = counter


# print dics with parsed count info
def print_dics():
    readable_dics = {}
    for key in dics.keys():
        dic = dics[key]
        r_dic = {}
        for dict_key in dic.keys():
            count = dic[dict_key]
            r_dic[dict_key] = count.get_count()
        readable_dics[key] = r_dic
        print r_dic


def reconstruct_data():
    for key in dics.keys():
        dic = dics[key]
        for dict_key in dic.keys():
            count = dic[dict_key]
            dic[dict_key] = count.get_count()


# sort data in each categorical dictionary by its count in descending order
# write all categorical dictionaries to a file
def write_categorical_count(file_name):
    out = open(file_name, 'w')
    for element in categorical_dics:
        items = element.items()
        sorted_list = sorted(items, key=lambda item: item[1].get_total_count(), reverse=True)  # sort by count
        sorted_key = [x[0] for x in sorted_list]
        #print sorted_list
        #print sorted_key
        # write to file
        for key in sorted_key:
            count = element[key]
            out.write(key + str(count))
            out.write('\n')
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
    length = len(continuous_dics)
    for i in range(0, length):
        element = continuous_dics[i]
        ordered_dict = OrderedDict()
        items = element.items()
        sorted_list = sorted(items, key=lambda item: int(item[0]))  # sort by key value
        sorted_key = [x[0] for x in sorted_list]
        for key in sorted_key:
            ordered_dict[int(key)] = element[key]
        continuous_dics[i] = ordered_dict


def write_histogram_data(file_name):
    out = open(file_name, 'w')
    bin_dics = get_proper_bins()

    for i in range(0, num_coutinuous):
        bin_dic = bin_dics[i]
        data_dic = continuous_dics[i]
        min_v, max_v = get_min_max(data_dic.keys())
        out.write("min: {0}, max: {1}\n".format(min_v, max_v))
        histogram_dics = {}
        for bin_num in bin_dic.keys():
            out.write("bin_num: {0}, bin_width: {1}\n".format(bin_num, bin_dic[bin_num]))
            bin_count = helper.BinCount(min_v, max_v, bin_num, bin_dic[bin_num])
            bin_count.generate_bins()
            histogram_dic = get_histogram_dic(data_dic, bin_count)
            write_dic(histogram_dic, out)
            histogram_dics[bin_num] = histogram_dic
        out.write("\n")
    out.write("\n\n")


def get_proper_bins():
    bin_dics = [{}, {}, {}, {}, {}, {}]
    length = len(continuous_dics)
    for i in range(0, length):
        element = continuous_dics[i]
        distance = get_data_distance(element.keys())
        print "distance: {0}".format(distance)
        if distance <= 100:
            get_bin_info(distance)
            bin_dic = select_bin_info(i)
        else:
            bin_dic = get_standard_bin_info(distance)
        bin_dics[i] = bin_dic
        print bin_dic
        print '\n'
    return bin_dics


def get_data_distance(ol):
    min_v, max_v = get_min_max(ol)
    print "Min: {0}, Max: {1}".format(min_v, max_v)
    return max_v - min_v + 1


def get_min_max(ol):
    length = len(ol)
    for i in range(0, length):
        ol[i] = int(ol[i])
    min_v = ol[0]
    max_v = ol[length - 1]
    return [min_v, max_v]


def get_bin_info(distance):
    bin_dic = {1: distance}
    max_d = Max_k if distance >= Max_k else distance
    for divisor in range(2, max_d + 1):
        quotient, remainder = divmod(distance, divisor)
        if remainder == 0:
            bin_dic[divisor] = quotient
        elif (remainder * 10.0) / divisor > 6.5:
            bin_dic[divisor] = quotient + 1
    #print bin_dic
    return bin_dic


def select_bin_info(index):
    if index is 0:
        return {25: 3, 15: 5, 7: 11}
    elif index is 2:
        return {16: 1, 8: 2, 4: 4}
    elif index is 5:
        return {20: 5, 10: 10, 5: 20}


def get_standard_bin_info(distance):
    bin_dict = {}
    for k in Ks:
        bin_width = distance / k
        bin_dict[k] = bin_width
    return bin_dict


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
            high = find_index(high, keys, False)
        high_index = keys.index(high)
        count_list = values[low_index:high_index+1]
        histogram_dic[str(bin)] = helper.combine(count_list)
        print "{0}: {1}\n".format(str(bin), histogram_dic[str(bin)])
    return histogram_dic


def find_index(element, l, low):
    step = -1 if low else 1
    while (1):
        if element not in l:
            element += step
        else:
            break
    return element


def write_dic(dic, out):
    for key in dic.keys():
        out.write("{0}: {1}\n".format(key, dic[key]))


def histogram(collection, ol):
    num_values = len(ol)
    k = K if num_values >= K else num_values
    bin_width, adjust = refine_bin_width(get_bin_width(ol, k))
    print "number of bins: {0}".format(k)
    print "bin_width: {0}".format(bin_width)
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
    print "Min: {0}, Max: {1}".format(Min, Max)
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


def main():
    if len(sys.argv) is not 5:
        print 'incorrect arguments\nneed: input_file.txt out_file1.txt out_file2.txt out_file3.txt'
        sys.exit(2)
    else:
        argv1 = sys.argv[1]
        argv2 = sys.argv[2]
        argv3 = sys.argv[3]
        argv4 = sys.argv[4]

    init_dics()
    parse_file(argv1)
    #print file_size
    write_categorical_count(argv2)
    write_continuous_data(argv3)
    write_histogram_data(argv4)


if __name__ == "__main__":
    main()

