from math import log


def get_cluster_count(data, index):
    length = len(data)
    count = 0
    for i in range(0, length):
        count += data[i][index]
    return count


def get_combination_two(n):
    return n * (n - 1) / 2.0


# compute nomalized mutual information
def nmi(data):
    c = 50.0
    N = 150.0
    I = 0.0
    for k in range(0, 3):
        w = get_cluster_count(data, k)
        for j in range(0, 3):
            wc = data[j][k]
            if wc > 0:
                I += (wc * log(N * wc / (c * w))) / N
    return I


def main():
    kmeans =  [[0, 50, 0], [47, 0, 3],  [14, 0, 36]]
    xmeans =  [[0, 0, 50], [10, 40, 0], [42, 8, 0]]
    density = [[0, 0, 50], [10, 40, 0], [45, 5, 0]]

    print nmi(kmeans)


if __name__ == "__main__":
    main()
