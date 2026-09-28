import networkx as nx
import matplotlib.pyplot as Plt 




def build_graph(products , threshold):
    G=nx.Graph()
    for product in products:
        G.add_node(product["title"],price=product["price"],source=product["source"])
    for i in range(len(products)):
        for j in range(i+1, len(products)):
            p1= products [i]
            p2= products [j]
            if abs(p1["price"]-p2["price"])<threshold :
                G.add_edge(p1["title"],p2["title"])
    return G



def get_isolated_nodes(G):
    return list(nx.isolated(G))


def remove_isolated_nodes(G):
    isolated = list(nx.isolates(G))
    G.remove_nodes_from(isolated)
    return G

def calculat_centrality(G):
    return nx. degree_centrality(G) 


def draw_graph(G):
    pos = nx.spring_layout(G, k=0.5, seed=42)

    centrality = calculat_centrality(G)

    sizes = [v * 3000 for v in centrality.values()]
    colors = list(centrality.values())

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=sizes,
        node_color=colors,
        cmap=Plt.cm.plasma,
        font_size=8
    )

    Plt.title("Product Graph (Price Similarity)")
    Plt.show()