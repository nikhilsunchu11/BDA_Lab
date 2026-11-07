import numpy as np

np.random.seed(42)

# Generate three clusters
cluster1 = np.random.normal(loc=[2, 2], scale=0.7, size=(30, 2))
cluster2 = np.random.normal(loc=[8, 8], scale=0.7, size=(30, 2))
cluster3 = np.random.normal(loc=[2, 9], scale=0.7, size=(30, 2))

# Combinr all points
full_data = np.vstack([cluster1, cluster2, cluster3])

# Select 5 representative points from each cluster
sample_data = np.vstack([
    cluster1[[0, 5, 10, 15, 20]],
    cluster2[[0, 5, 10, 15, 20]],
    cluster3[[0, 5, 10, 15, 20]]
])

# Save coordinate files
np.savetxt("full_data.txt", full_data, delimiter=",", fmt="%.4f")
np.savetxt("sample_data.txt", sample_data, delimiter=",", fmt="%.4f")

print("Datasets generated successfully.")
print("Sample data points:", len(sample_data))
print("Full data points:", len(full_data))
