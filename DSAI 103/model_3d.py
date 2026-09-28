import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


def plot_3d(products):

    X = [p["price"] for p in products]

    Y = list(range(len(products)))

    sources = list(set(p["source"] for p in products))
    source_map = {s: i for i, s in enumerate(sources)}

    Z = [source_map[p["source"]] for p in products]

    clusters = []

    for price in X:

        if price < 300:
            clusters.append(0)

        elif price < 700:
            clusters.append(1)

        else:
            clusters.append(2)

    cluster_colors = ["red", "blue", "green"]

    max_price = max(X)
    important_index = X.index(max_price)

    fig = plt.figure(figsize=(12, 8))

    ax = fig.add_subplot(projection='3d')

    for i in range(len(X)):

        size = 80

        if i == important_index:
            size = 300

        ax.scatter(
            X[i],
            Y[i],
            Z[i],
            color=cluster_colors[clusters[i]],
            s=size,
            alpha=0.8
        )

    for cluster_id in range(3):

        cluster_x = []
        cluster_y = []
        cluster_z = []

        for i in range(len(X)):

            if clusters[i] == cluster_id:

                cluster_x.append(X[i])
                cluster_y.append(Y[i])
                cluster_z.append(Z[i])

        if len(cluster_x) > 0:

            centroid_x = np.mean(cluster_x)
            centroid_y = np.mean(cluster_y)
            centroid_z = np.mean(cluster_z)

            ax.scatter(
                centroid_x,
                centroid_y,
                centroid_z,
                color="yellow",
                s=250,
                alpha=0.9
            )

            ax.text(
                centroid_x,
                centroid_y + 1,
                centroid_z,
                f"C{cluster_id}",
                color="black",
                fontsize=10,
                fontweight="bold"
            )

    important_product = products[important_index]["title"][:12]

    ax.text(
        X[important_index],
        Y[important_index],
        Z[important_index],
        f"TOP\n{important_product}",
        color="black"
    )

    ax.set_xlabel("Price")
    ax.set_ylabel("Product Index")
    ax.set_zlabel("Source")

    ax.set_zticks(list(source_map.values()))
    ax.set_zticklabels(list(source_map.keys()))

    ax.view_init(30, 45)

    plt.title("Advanced 3D Product Visualization")

    plt.show()