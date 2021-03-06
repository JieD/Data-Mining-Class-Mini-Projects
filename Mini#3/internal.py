import itertools
import math


# import file and save value to data
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

        if cluster is not '?':  # dismiss outliers
            # check if the cluster is new to the dictionary
            if cluster not in data:
                data[cluster] = []
            length = len(words)
            for i in range(0, length - 1):  # skip the last attribute (class label)
                value.append(float(words[i]))
            #print value
            data[cluster].append(value)


# calculate the diameters of each cluster in the data
def get_diameter(data):
    clusters = data.keys()
    for cluster in clusters:
        points = data[cluster]
        size = len(points)

        pairs = itertools.permutations(points, 2)  # get all possible combinations
        total_distance = 0.0
        for pair in pairs:
            distance = compute_distance(pair[0], pair[1])
            total_distance += (distance * distance)
            #print pair, distance
        diameter = math.sqrt(total_distance / (size * (size - 1)))
        print "{0} size: {1}, diameter: {2}".format(cluster, size, diameter)


def compute_link(data):
    clusters = data.keys()
    cluster_pairs = itertools.combinations(clusters, 2)
    for cluster_pair in cluster_pairs:
        pts1 = data[cluster_pair[0]]
        pts2 = data[cluster_pair[1]]
        max_distance = 0.0
        avg_distance = 0.0
        for pt1 in pts1:
            for pt2 in pts2:
                distance = compute_distance(pt1, pt2)
                if distance > max_distance:
                    max_distance = distance
                avg_distance += distance

        avg_distance /= (len(pts1) * len(pts2))
        print "\n{0} and {1}:".format(cluster_pair[0], cluster_pair[1])
        print "average link: {0}". format(avg_distance)
        print "complete link: {0}". format(max_distance)


# compute the euclidean distance between two points
# the dimension of two points should be equal
def compute_distance(point1, point2):
    length = len(point1)
    distance = 0.0
    for i in range(0, length):
        d = point1[i] - point2[i]
        distance += d * d
    return math.sqrt(distance)


def main():
    files = {'kmeans': 'Statistics/iris/kmean_result.arff',
             'xmeans': 'Statistics/iris/xmean_result.arff',
             'dbscan_default': 'Statistics/iris/dbscan_default_result.arff',
             'dbscan_best'   : 'Statistics/iris/dbscan_best_result.arff'}
    datasets = {'kmeans': {}, 'xmeans': {}, 'dbscan_default': {}, 'dbscan_best': {}}

    for algorithm in datasets.keys():
        data_file = files[algorithm]
        import_data(data_file, datasets[algorithm])

        print algorithm
        data = datasets[algorithm]
        get_diameter(data)
        compute_link(data)
        print


if __name__ == "__main__":
    main()

