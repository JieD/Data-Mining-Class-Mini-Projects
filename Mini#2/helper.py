from collections import Counter

LABEL = ['>50K', '<=50K']


class Count(object):
    def __init__(self):
        self.__count = 0
        self.__accu_count = 0
        self.__c = Counter()
        for element in LABEL:
            self.__c[element] = 0

    def store(self, label):
        self.__count += 1
        self.__c[label] += 1

    def get_total_count(self):
        return self.__count

    def set_total_count(self, new_count):
        self.__count = new_count

    def get_accu_count(self):
        return self.__accu_count

    def set_accu_count(self, accu_count):
        self.__accu_count = accu_count

    def get_label_count(self, label):
        return self.__c[label]

    def set_label_count(self, label, l_count):
        self.__c[label] = l_count

    def get_all_label_count(self):
        dictionary = {}
        for label in LABEL:
            dictionary[label] = self.get_label_count(label)
        return dictionary;

    def get_count(self):
        return [self.get_total_count(), self.get_all_label_count()]

    # override str() for Count
    def __str__(self):
        return " {0} {1}".format(str(self.__count), str(self.get_all_label_count()))


class KeyCount(object):
    def __init__(self, key, count):
        self.data = [key, count.__count, count.get_all_label_count()]

    def get_data(self):
        return self.data


class BinCount(object):
    def __init__(self, min, max, bin_nums, bin_width):
        self.min = min
        self.max = max
        self.bin_nums = bin_nums
        self.bin_width = bin_width

    def generate_bins(self):
        bins = []
        for i in range(0, self.bin_nums):
            low = bins[i-1][1] + 1 if i > 0 else self.min
            high = low + self.bin_width - 1
            bins.append([low, high])
        bins[self.bin_nums-1][1] = self.max
        print bins


def combine(count_list):
    total_count = Count()
    for count in count_list:
        total = total_count.get_total_count()
        c_total = total + count.get_total_count()
        total_count.set_total_count(c_total)
        for label in LABEL:
            total_label = total_count.get_label_count(label)
            total_count.set_label_count(label, total_label + count.get_label_count(label))
    return total_count

if __name__ == "__main__":
    count1 = Count()
    count1.store(LABEL[0])
    count1.store(LABEL[0])
    count1.store(LABEL[1])
    count2 = Count()
    count2.store(LABEL[1])
    count2.store(LABEL[0])
    count2.store(LABEL[1])
    #key_counts = KeyCount(1, count)
    print count1
    print count2
    print combine([count1, count2])
    #print key_counts.get_data()