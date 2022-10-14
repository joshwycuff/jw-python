# internal
from jw_graph.graph import (
    Vertex,
    Graph,
)


def reset_id_generator(func):
    def wrapper():
        Vertex.id_generator.reset()
        return func()
    return wrapper


@reset_id_generator
def test_vertex_ids():
    assert Vertex({}).id == 0
    assert Vertex({}).id == 1


@reset_id_generator
def test_vertex_data():
    assert Vertex({'x': 1}).data == {'x': 1}


@reset_id_generator
def test_vertex_neighbor():
    v1 = Vertex({})
    v2 = Vertex({})
    v1 >> v2
    assert v1.get_neighbors() == [v2]


@reset_id_generator
def test_vertex_no_duplicate_edges():
    v1 = Vertex({})
    v2 = Vertex({})
    v1 >> v2
    v1 >> v2
    assert v1.get_neighbors() == [v2]


@reset_id_generator
def test_vertex_neighbors():
    v1 = Vertex({})
    v2 = Vertex({})
    v3 = Vertex({})
    v1 >> v2
    v1 >> v3
    assert v1.get_neighbors() == [v2, v3]


@reset_id_generator
def test_graph_add_vertex():
    v1 = Vertex({})
    graph = Graph() + v1
    assert graph.vertices == [v1]


@reset_id_generator
def test_graph_add_vertices():
    v1 = Vertex({})
    v2 = Vertex({})
    v3 = Vertex({})
    graph = Graph() + (v1, v2, v3)
    assert graph.vertices == [v1, v2, v3]


@reset_id_generator
def test_graph_add_edge():
    v1 = Vertex({})
    v2 = Vertex({})
    graph = Graph().add_edge(v1, v2)
    assert graph.vertices == [v1, v2]


@reset_id_generator
def test_graph_add_vertices_once():
    v1 = Vertex({})
    v2 = Vertex({})
    graph = Graph().add_vertices(v1, v2).add_edge(v1, v2)
    assert graph.vertices == [v1, v2]


@reset_id_generator
def test_depth_first_search():
    v1 = Vertex({})
    v2 = Vertex({})
    v3 = Vertex({})
    v4 = Vertex({})
    v5 = Vertex({})
    v1 >> v2
    v2 >> v3
    v1 >> v4
    graph = Graph(v1, v2, v3, v4, v5)
    dfs = graph.depth_first_search()
    assert list(dfs) == [v3, v2, v4, v1, v5]
