class DirectedGraph:
    """A directed graph supporting path queries and topological sorting."""

    def __init__(self):
        """Initialize an empty directed graph."""
        pass  # TODO: Initialize your graph data structure

    def add_edge(self, from_node: str, to_node: str) -> None:
        """Add a directed edge from from_node to to_node.
        Both nodes should be created if they don't exist yet.
        """
        pass  # TODO: Implement

    def has_path(self, start: str, end: str) -> bool:
        """Return True if there is a directed path from start to end.
        Return False if either node doesn't exist or no path exists.
        """
        pass  # TODO: Implement using BFS or DFS

    def topological_sort(self) -> list:
        """Return a list of all nodes in topological order.
        If the graph contains a cycle, return an empty list.
        """
        pass  # TODO: Implement using Kahn's algorithm or DFS-based approach
