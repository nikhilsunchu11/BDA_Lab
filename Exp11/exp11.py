
from functools import cmp_to_key
from functools import reduce
import matplotlib.pyplot as plt
import numpy as np
import sys
import datetime

# Compare coordinates
def comparator(x, y):
    if x[0] < y[0]:
        return -1
    if x[0] == y[0]:
        if x[1] < y[1]:
            return -1
        if x[1] > y[1]:
            return 1
        return 0
    return 1


# Dataset paths and parameters
samplefile = "sample_data.txt"
fullfile = "full_data.txt"

ratio = 0.2
k = 3
representative_count = 3

start = datetime.datetime.now()

# STEP 1: Read sample data and initialize clusters
clusters = []

with open(samplefile, "r") as file:
    for line in file:
        value = line.strip().split(",")
        point = [float(value[0]), float(value[1])]
        clusters.append([point, 1, [point]])

print("Initial sample clusters:", len(clusters))


# STEP 2: Merge closest clusters until k clusters remain
while len(clusters) > k:
    min_coordinate = None
    min_distance = sys.maxsize

    for i in range(len(clusters)):
        cluster1 = clusters[i]
        centroid1 = np.array(cluster1[0]) / cluster1[1]

        for j in range(i + 1, len(clusters)):
            cluster2 = clusters[j]
            centroid2 = np.array(cluster2[0]) / cluster2[1]

            distance = np.sum((centroid2 - centroid1) ** 2)

            if distance < min_distance:
                min_coordinate = [i, j]
                min_distance = distance

    i, j = min_coordinate
    cor1 = clusters[i]
    cor2 = clusters[j]

    new_cluster = [
        np.ndarray.tolist(
            np.array(cor1[0]) + np.array(cor2[0])
        ),
        cor1[1] + cor2[1],
        cor1[2] + cor2[2]
    ]

    clusters.pop(j)
    clusters.pop(i)
    clusters.append(new_cluster)

print("Clusters after merging:", len(clusters))


# STEP 3: Find representative points and centroids
centroids = []
representatives = []

for cluster in clusters:
    sortedcluster = sorted(
        cluster[2],
        key=cmp_to_key(comparator)
    )

    repre = [sortedcluster[0]]

    while len(repre) < representative_count:
        center = np.mean(np.array(repre), axis=0)

        candidate = None
        max_distance = -1

        for coor in sortedcluster:
            if coor not in repre:
                distance = np.sum(
                    (center - np.array(coor)) ** 2
                )

                if distance > max_distance:
                    max_distance = distance
                    candidate = coor

        if candidate is None:
            break

        repre.append(candidate)

    cluster_centroid = np.mean(
        np.array(cluster[2]), axis=0
    )

    centroids.append(cluster_centroid)

    # Shrink representative points towards centroid
    shrunk = []

    for representative in repre:
        point = np.array(representative) + ratio * (
            cluster_centroid - np.array(representative)
        )
        shrunk.append(point)

    representatives.append(shrunk)

print("Representative points selected.")


# STEP 4: Assign full dataset points to nearest representative
final_clusters = [[] for _ in range(k)]

with open(fullfile, "r") as file:
    for line in file:
        values = line.strip().split(",")
        point = np.array([float(values[0]), float(values[1])])

        min_distance = sys.maxsize
        index_cluster = 0

        for i, cluster in enumerate(representatives):
            for representative in cluster:
                distance = np.sum(
                    (np.array(representative) - point) ** 2
                )

                if distance < min_distance:
                    min_distance = distance
                    index_cluster = i

        final_clusters[index_cluster].append(point)

print("\nFinal Cluster Results")

for i, cluster in enumerate(final_clusters):
    print(f"Cluster {i + 1}: {len(cluster)} points")


# STEP 5: Plot final clusters
plt.figure(figsize=(10, 7))

for i, cluster in enumerate(final_clusters):
    points = np.array(cluster)

    plt.scatter(
        points[:, 0],
        points[:, 1],
        label=f"Cluster {i + 1}"
    )

    plt.scatter(
        centroids[i][0],
        centroids[i][1],
        marker="X",
        s=150,
        edgecolors="black"
    )

plt.title("CURE Clustering Results")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.legend()
plt.grid(True)

plt.savefig("plots/clustering.png", dpi=150)
plt.show()


# STEP 6: Display execution time
end = datetime.datetime.now()

print("\nExecution Time:", end - start)


# STEP 7: Generate overall dendrogram
from scipy.cluster.hierarchy import dendrogram, linkage

# Load complete dataset
full_data = np.loadtxt(fullfile, delimiter=",")

linked = linkage(full_data, method="single")

plt.figure(figsize=(12, 7))

dendrogram(
    linked,
    orientation="top",
    distance_sort="descending",
    show_leaf_counts=True
)

plt.title("Hierarchical Clustering Dendrogram - Full Dataset")
plt.xlabel("Data Points")
plt.ylabel("Distance")
plt.tight_layout()

plt.savefig("plots/full_dendrogram.png", dpi=150)
plt.show()


# STEP 8: Generate individual cluster dendrograms
for i in range(len(final_clusters)):

    cluster_data = np.array(final_clusters[i])

    linked = linkage(cluster_data, method="single")

    plt.figure(figsize=(12, 7))

    dendrogram(
        linked,
        orientation="top",
        distance_sort="descending",
        show_leaf_counts=True
    )

    plt.title(f"Dendrogram - Cluster {i + 1}")
    plt.xlabel("Data Points")
    plt.ylabel("Distance")
    plt.tight_layout()

    plt.savefig(
        f"plots/cluster_{i + 1}_dendrogram.png",
        dpi=150
    )

    plt.show()

print("\nAll dendrograms generated successfully.")
