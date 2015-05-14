from math import log


# count the size of a cluster
def get_cluster_count(data, index):
    num_class = len(data)
    count = 0
    for i in range(0, num_class):
        count += data[i][index]
    return count


# get a list of cluster counts
def get_all_cluster_counts(data):
    counts = []
    num_cluster = len(data[0])
    num_class = len(data)
    for i in range(0, num_cluster):
        counts.append(get_cluster_count(data, i))
    return counts


# count the size of each class
def get_class_count(data, index):
    num_cluster = len(data[0])
    count = 0
    for i in range(0, num_cluster):
        count += data[index][i]
    return count


# get a list of class counts
def get_all_class_counts(data):
    counts = []
    num_class = len(data)
    num_cluster = len(data[0])
    for i in range(0, num_class):
        counts.append(get_class_count(data, i))
    return counts


# total value in the list
def get_all_counts(count_list):
    total = 0.0
    for i in range(0, len(count_list)):
        total += count_list[i]
    return total


# compute n chooses 2
def get_combination_two(n):
    return n * (n - 1) / 2.0


# compute nomalized mutual information
def nmi(data):
    num_class = len(data)
    num_cluster = len(data[0])
    class_counts = get_all_class_counts(data)
    cluster_counts = get_all_cluster_counts(data)
    N = get_all_counts(class_counts)
    #print "N: {0}".format(N)

    Hc = 0.0
    for j in range(0, num_class):
        c = class_counts[j]
        Hc -= (c / N) * log(c / N, 2)
    #print "Hc: {0}".format(Hc)

    Hw = 0.0
    I = 0.0
    for k in range(0, num_cluster):
        w = cluster_counts[k]
        Hw -= (w / N) * log(w / N, 2)

        for j in range(0, num_class):
            i = 0.0
            wc = data[j][k]
            if wc > 0:
                i = (wc / N) * log(N * wc / (class_counts[j] * w), 2)
                I += i
                #print "wc: {0}, i: {1}".format(wc, i)
    #print "Hw: {0}".format(Hw)
    #print "I: {0}".format(I)

    return I * 2 / (Hw + Hc)


# compute the Rand index which penalizes both false positive and false negative decisions during clustering
# TP - assigns two similar documents to the same cluster
# TN - assigns two dissimilar documents to different clusters.
# FP - assigns two dissimilar documents to the same cluster.
# FN - assigns two similar documents to different clusters.
def rand_index(data):
    num_class = len(data)
    num_cluster = len(data[0])
    TP_FP = 0.0
    TP = 0.0
    cluster_counts = []
    for k in range(0, num_cluster):
        w = get_cluster_count(data, k)
        cluster_counts.append(w)
        c = get_combination_two(w)  # choose two from each clusters
        TP_FP += c
        #print "c: {0}, TP+FP: {1}".format(c, TP_FP)

        for j in range(0, num_class):
            wc = data[j][k]
            if wc > 1:
                TP += get_combination_two(wc)  # choose two from each class within a cluster
    FP = TP_FP - TP

    #print cluster_counts
    TN_FN = 0.0
    for i in range(0, num_cluster):
        for j in range(i + 1, num_cluster):
            TN_FN += cluster_counts[i] * cluster_counts[j]  # choose one from different clusters

    FN = 0.0
    for i in range(0, num_class):
        class_counts = data[i]
        for j in range(0, num_cluster):
            if class_counts[j] > 0:
                for k in range(j + 1, num_cluster):
                    if class_counts[k] > 0:
                        FN += class_counts[j] * class_counts[k]
    TN = TN_FN - FN

    ri = (TP + TN) / (TP_FP + TN_FN)
    #print "TP+FP: {0}".format(TP_FP)
    #print "TP: {0}, FP: {1}".format(TP, FP)
    #print "TN+FN: {0}".format(TN_FN)
    #print "TN: {0}, FN: {1}".format(TN, FN)
    print "ri: {0}".format(ri)
    f_measure(TP, FP, FN)


def f_measure(TP, FP, FN):
    BETA = 1
    bs = BETA * BETA
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f = (bs + 1) * precision * recall / ((bs * precision) + recall)
    print "F measure: {0}".format(f)


def main():
    kmeans =  [[0, 50, 0], [47, 0, 3],  [14, 0, 36]]
    xmeans =  [[0, 0, 50], [10, 40, 0], [42, 8, 0]]
    dbscan = [[47, 0, 0], [0, 4, 38], [0, 35, 0]]
    data = [kmeans, xmeans, dbscan]

    test = [[5, 1, 2], [1, 4, 0], [0, 1, 3]]
    #print "nmi: {0}".format(nmi(test))
    #rand_index(test)
    for element in data:
        print "nmi: {0}".format(nmi(element))
        rand_index(element)
        print


if __name__ == "__main__":
    main()
