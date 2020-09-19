## Initialisation

import pandas as pd
import matplotlib.pyplot as plt
from kneed import KneeLocator
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import seaborn as sns;

sns.set()  # for plot styling
def add_centroid (centroids, row):
   if row['group'] == 0 :
      return centroids[0]
   if row['group'] == 1 :
      return centroids[1]
   if row['group'] == 2 :
      return centroids[2]
   if row['group'] == 3 :
      return centroids[3]

def kmeans(personality_trait, number_cluster):
    df = pd.read_csv('final.csv')
    personality_traitx = personality_trait + ".x"
    personality_traity = personality_trait + ".y"

    # select columns with personality traits and pull requests
    df = df[[personality_traitx, personality_traity, "accepted"]]
    df = df.drop_duplicates(subset=[personality_traitx, personality_traity, "accepted"])

    df_trait = pd.DataFrame({
        'x': df[personality_traitx],
        'y': df[personality_traity],
    })

    df_accept = pd.DataFrame({
        'r': df["accepted"]
    })

    X = df_trait.to_numpy()
    true_labels = df_accept.to_numpy()

    #plot results
    plt.scatter(X[:, 0], X[:, 1], c=true_labels, s=50, cmap='viridis')
    plt.show()
    # scaler = StandardScaler()
    # X = scaler.fit_transform(features)

    #define kmeans parameters
    kmeans = KMeans(
        init="random",
        n_clusters=number_cluster,
        n_init=10,
        max_iter=300,
        random_state=42
    )
    kmeans.fit(X)
    y_kmeans = kmeans.predict(X)

    print(plt.scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis'))

    centers = kmeans.cluster_centers_
    plt.scatter(centers[:, 0], centers[:, 1], c='black', s=200, alpha=0.5);
    plt.show()
    # lowest SSE
    print("The lowest SSE value: ", kmeans.inertia_)

    # Final locations of the centroid
    print("Final centroid locations :", kmeans.cluster_centers_)
    centroids = kmeans.cluster_centers_

    # The number of iterations required to converge
    print("The number of iterations required to converge: ", kmeans.n_iter_)

    # print(kmeans.labels_[:500])
    df["group"] = pd.Series(y_kmeans, index=df.index)
    df["centroid"] = df.apply(lambda row: add_centroid(centroids, row), axis=1)
    output_file = personality_trait + "_cluster.csv"
    #write results
    df.to_csv(output_file, index=False)


def elbowmethod(personality_trait):
    df = pd.read_csv('final.csv')
    personality_traitx = personality_trait + ".x"
    personality_traity = personality_trait + ".y"
    # select columns with personality traits and pull requests
    df = df[[personality_traitx, personality_traity, "accepted"]]
    df = df.drop_duplicates(subset=[personality_traitx, personality_traity, "accepted"])

    df_trait = pd.DataFrame({
        'x': df[personality_traitx],
        'y': df[personality_traity],
    })

    df_accept = pd.DataFrame({
        'r': df["accepted"]
    })

    features = df_trait.to_numpy()
    true_labels = df_accept.to_numpy()

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "max_iter": 300,
        "random_state": 42,
    }

    # A list holds the SSE values for each k
    sse = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(scaled_features)
        sse.append(kmeans.inertia_)

    plt.style.use("fivethirtyeight")
    plt.plot(range(1, 11), sse)
    plt.xticks(range(1, 11))
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")
    plt.show()
    kl = KneeLocator(
        range(1, 11), sse, curve="convex", direction="decreasing"
    )
    print("Number of cluster: ", kl.elbow)
    return kl.elbow


if __name__ == "__main__":
    number_cluster_openness = elbowmethod("openness")
    kmeans("openness", number_cluster_openness)
    number_cluster_conscientiousness = elbowmethod("conscientiousness")
    kmeans("conscientiousness", number_cluster_conscientiousness)
    number_cluster_extraversion = elbowmethod("extraversion")
    kmeans("extraversion", number_cluster_extraversion)
    number_cluster_agreeableness = elbowmethod("agreeableness")
    kmeans("agreeableness", number_cluster_agreeableness)
    number_cluster_neuroticism = elbowmethod("neuroticism")
    kmeans("neuroticism", number_cluster_neuroticism)
