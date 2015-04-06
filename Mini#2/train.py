import visualize

def find_categorical_p(target, label, dict):
    count = dict[target]
    #return count
    return count.get_label_count(label)


def find_continuous_p(target, label, dict):
    length = len(dict)
    keys = dict.keys()    
    min = keys[0][0]
    max = keys[length-1][1]
    if target < min: 
        count = dict[keys[0]]
    elif target > max:
        count = dict[keys[length-1]]
    else:  # within range
        for i in range(0, length):
            boundary = keys[i]
            low, high = get_min_max(boundary)
            if target < low or target > high:
                continue
            else:
                count = dict[i]
    #return count
    return count.get_label_count(label)

def get_min_max(s):
    return s.split('-')


def is_out_of_range(target, r):
    return True if target < r[0] or target > r[1] else False

def main():
    LABEL = ['-1', '1']
    d1 = {'love': 3, "hate": -3}
    d2 = {'1-1': 1, '2-2': 2}
    #print str(find_categorical_p('love', 1, d1))
    #print str(find_continuous_p('1-1', 1, d2))


if __name__ == "__main__":
    main()