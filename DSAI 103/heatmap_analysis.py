import numpy as np
import matplotlib.pyplot as plt
import math

def kde(d, h):
    if d <= h:
        dn = d / h
        return (1 - dn**2)**2
    else:
        return 0


def kde_heatmap(products):
    
    X = [p["price"] for p in products]
    Y = list(range(len(X)))

    R = 200  

    x_vals = np.linspace(min(X), max(X), 50)
    y_vals = np.linspace(min(Y), max(Y), 50)

    heatmap = np.zeros((len(y_vals), len(x_vals)))

    for i, x in enumerate(x_vals):
        for j, y in enumerate(y_vals):

            total_density = 0

            for xi, yi in zip(X, Y):
                d = math.sqrt((x - xi)**2 + (y - yi)**2)
                total_density += kde(d, R)

            heatmap[j][i] = total_density


    plt.figure(figsize=(8, 6))
    plt.imshow(heatmap, cmap="hot", origin="lower")
    plt.colorbar(label="Density")
    plt.title("KDE Heatmap (Prices)")
    plt.xlabel("Price")
    plt.ylabel("Index")
    plt.show()