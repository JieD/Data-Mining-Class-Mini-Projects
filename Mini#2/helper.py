from collections import Counter


class Count(object):
    def __init__(self, labels):
        self.__count = 0
        self.__accu_count = 0
        self.__c = Counter()
        self.labels = labels
        for element in self.labels:
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
        for label in self.labels:
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
        self.bins = []
        #print "min: {0}, max: {1}, bin_nums: {2}, bin_width: {3}".format(self.min, self.max, self.bin_nums, self.bin_width)

    def generate_bins(self):
        for i in range(0, self.bin_nums):
            low = self.bins[i-1][1] + 1 if i > 0 else self.min
            high = low + self.bin_width - 1
            self.bins.append([low, high])
        self.bins[self.bin_nums-1][1] = self.max
        #print self.bins

    def get_bins(self):
        return self.bins


def combine(count_list, labels):
    total_count = Count(labels)
    for count in count_list:
        total = total_count.get_total_count()
        c_total = total + count.get_total_count()
        total_count.set_total_count(c_total)
        for label in labels:
            total_label = total_count.get_label_count(label)
            total_count.set_label_count(label, total_label + count.get_label_count(label))
    return total_count

if __name__ == "__main__":
    count1 = Count(['0', '1'])
    count1.store('0')
    count1.store('0')
    count1.store('1')
    count2 = Count()
    count2.store('1')
    count2.store('0')
    count2.store('1')
    #key_counts = KeyCount(1, count)
    print count1
    print count2
    print combine([count1, count2])
    bin_c = BinCount(1,2,3,4)
    #print key_counts.get_data()