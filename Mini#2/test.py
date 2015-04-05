#age, fnlwgt, education-num, capital-gain, capital-loss, hours-per-week,
#workclass, education, marital-status, occupation, relationship, race, sex, native-country,

# create a list of data for each attribute,
#
import sys
import helper
import operator
import math

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
K = 10
Ratios = [0.4, 0.7, 1.0]

# init variables
def init_dics():
    workclass_dic, education_dic, marital_status_dic, occupation_dic, relationship_dic, race_dic, \
    sex_dic, native_country_dic = {}, {}, {}, {}, {}, {}, {}, {}
    age_dic, fnlwgt_dic, education_num_dic, capital_gain_dic, capital_loss_dic, hours_per_week_dic \
        = {}, {}, {}, {}, {}, {}
    global dics, categorical_dics, continuous_dics
    dics = { 0: age_dic,            1: workclass_dic,    2: fnlwgt_dic,       3: education_dic, 4: education_num_dic,
             5: marital_status_dic, 6: occupation_dic,   7: relationship_dic, 8: race_dic,      9: sex_dic,
            10: capital_gain_dic,  11: capital_loss_dic, 12: hours_per_week_dic, 13: native_country_dic}
    categorical_dics = [workclass_dic, education_dic, marital_status_dic, occupation_dic, relationship_dic, race_dic,
                        sex_dic, native_country_dic]
    continuous_dics = [age_dic, fnlwgt_dic, education_num_dic, capital_gain_dic, capital_loss_dic, hours_per_week_dic]


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
# calculate statistical value: min, max, mean, median, Q1, Q3
def reconstruct_continuous_data(file_name):
    out = open(file_name, 'w')
    for element in continuous_dics:
        items = element.items()
        sorted_list = sorted(items, key=lambda item: int(item[0]))  # sort by key value
        sorted_key = [x[0] for x in sorted_list]
        #print sorted_list
        #print sorted_key
        #collect_statistical_data(sorted_list, sorted_key)
        separator_list = histogram(sorted_list, sorted_key)
        #print separator_list
        #print get_separator_range(separator_list)
        #for i in range(0, K1):
        #    for value in sorted_key:



        # write to file
        for key in sorted_key:
            count = element[str(key)]
            out.write(str(key) + str(count))
            out.write('\n')
        out.write('\n\n')
    out.close()


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
    if len(sys.argv) is not 4:
        print 'incorrect arguments\nneed: input_file.txt out_file1.txt out_file2.txt'
        sys.exit(2)
    else:
        argv1 = sys.argv[1]
        argv2 = sys.argv[2]
        argv3 = sys.argv[3]

    init_dics()
    parse_file(argv1)
    print file_size

    #print_dics()
    #reconstruct_data()
    write_categorical_count(argv2)
    reconstruct_continuous_data(argv3)



if __name__ == "__main__":
    main()

