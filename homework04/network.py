import igraph
from igraph import Graph, plot

from api import get_friends


def get_network(user_id, as_edgelist=True):
    response = get_friends(user_id)
    my_friends = response['response']['items']
    friends_count = len(my_friends)

    result = [] if as_edgelist else [[0] * friends_count for _ in range(friends_count)]

    for i, my_friend in enumerate(my_friends):
        response = get_friends(my_friend)
        if response.get('error'):
            continue
        f_friends = response['response']['items']
        for j, my_friend_ in enumerate(my_friends, start=i + 1):
            if my_friend_ in f_friends:
                if as_edgelist:
                    result.append((i, j))
                else:
                    result[i][j] = 1
    return result


def plot_graph(user_id: int = 505540783):
    friends = get_friends(user_id, 'last_name')['response']['items']
    lables = [f"{friend['last_name']} {friend['first_name']}" for friend in friends]
    edges = get_network(user_id)
    g = Graph(vertex_attrs={"shape": "circle",
                            "label": lables,
                            "size": 10},
              edges=edges, directed=False)

    friends_num = len(friends)
    visual_style = {
        "vertex_size": 20,
        "bbox": (3000, 3000),
        "margin": 100,
        "vertex_label_dist": 1.6,
        "autocurve": True,
        "layout": g.layout_fruchterman_reingold(
            maxiter=10000,
            area=friends_num ** 2,
            repulserad=friends_num ** 2)
    }

    clusters = g.community_multilevel()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)

    plot(g, **visual_style)


if __name__ == '__main__':
    plot_graph(85671031)
