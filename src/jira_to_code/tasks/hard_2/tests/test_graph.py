from graph import DirectedGraph

def test_simple_path():
    g = DirectedGraph()
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    assert g.has_path("a", "c") == True
    assert g.has_path("c", "a") == False

def test_no_path():
    g = DirectedGraph()
    g.add_edge("a", "b")
    g.add_edge("c", "d")
    assert g.has_path("a", "d") == False

def test_nonexistent_node():
    g = DirectedGraph()
    g.add_edge("a", "b")
    assert g.has_path("a", "z") == False
    assert g.has_path("z", "a") == False

def test_topological_sort_basic():
    g = DirectedGraph()
    g.add_edge("a", "b")
    g.add_edge("a", "c")
    g.add_edge("b", "d")
    g.add_edge("c", "d")
    result = g.topological_sort()
    assert len(result) == 4
    assert result.index("a") < result.index("b")
    assert result.index("a") < result.index("c")
    assert result.index("b") < result.index("d")
    assert result.index("c") < result.index("d")

def test_cycle_detection():
    g = DirectedGraph()
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    g.add_edge("c", "a")
    assert g.topological_sort() == []

def test_self_loop():
    g = DirectedGraph()
    g.add_edge("a", "a")
    assert g.topological_sort() == []

def test_direct_path():
    g = DirectedGraph()
    g.add_edge("x", "y")
    assert g.has_path("x", "y") == True
