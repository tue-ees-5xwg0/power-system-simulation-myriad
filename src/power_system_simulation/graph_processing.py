"""
This is a skeleton for the graph processing assignment.

We define a graph processor class with some function skeletons.
"""


import networkx as nx
from typing import List, Tuple



class IDNotFoundError(Exception):
    pass


class InputLengthDoesNotMatchError(Exception):
    pass


class IDNotUniqueError(Exception):
    pass


class GraphNotFullyConnectedError(Exception):
    pass


class GraphCycleError(Exception):
    pass


class EdgeAlreadyDisabledError(Exception):
    pass


class GraphProcessor:
    """
    General documentation of this class.
    You need to describe the purpose of this class and the functions in it.
    We are using an undirected graph in the processor.
    """

    def __init__(
        self,
        vertex_ids: List[int],
        edge_ids: List[int],
        edge_vertex_id_pairs: List[Tuple[int, int]],
        edge_enabled: List[bool],
        source_vertex_id: int,
    ) -> None:
        """
        Initialize a graph processor object with an undirected graph.
        Only the edges which are enabled are taken into account.
        Check if the input is valid and raise exceptions if not.
        The following conditions should be checked:
            1. vertex_ids and edge_ids should be unique. (IDNotUniqueError)
            2. edge_vertex_id_pairs should have the same length as edge_ids. (InputLengthDoesNotMatchError)
            3. edge_vertex_id_pairs should contain valid vertex ids. (IDNotFoundError)
            4. edge_enabled should have the same length as edge_ids. (InputLengthDoesNotMatchError)
            5. source_vertex_id should be a valid vertex id. (IDNotFoundError)
            6. The graph should be fully connected. (GraphNotFullyConnectedError)
            7. The graph should not contain cycles. (GraphCycleError)
        If one certain condition is not satisfied, the error in the parentheses should be raised.

        Args:
            vertex_ids: list of vertex ids
            edge_ids: liest of edge ids
            edge_vertex_id_pairs: list of tuples of two integer
                Each tuple is a vertex id pair of the edge.
            edge_enabled: list of bools indicating of an edge is enabled or not
            source_vertex_id: vertex id of the source in the graph
        """
        # put your implementation here
        self.vertex_ids = vertex_ids
        self.edge_ids = edge_ids
        self.edge_vertex_id_pairs = edge_vertex_id_pairs
        self.edge_enabled = edge_enabled
        self.source_vertex_id = source_vertex_id
        pass
    
    def find_downstream_vertices(self, edge_id: int) -> List[int]:
        """
        Given an edge id, return all the vertices which are in the downstream of the edge,
            with respect to the source vertex.
            Including the downstream vertex of the edge itself!

        Only enabled edges should be taken into account in the analysis.
        If the given edge_id is a disabled edge, it should return empty list.
        If the given edge_id does not exist, it should raise IDNotFoundError.


        For example, given the following graph (all edges enabled):

            vertex_0 (source) --edge_1-- vertex_2 --edge_3-- vertex_4

        Call find_downstream_vertices with edge_id=1 will return [2, 4]
        Call find_downstream_vertices with edge_id=3 will return [4]

        Args:
            edge_id: edge id to be searched

        Returns:
            A list of all downstream vertices.
        """
        output = []
        
        # Calculate the index of the input edge
        input_index_edge = self.edge_ids.index(edge_id)

        # If the input edge is already disabled, return empty set
        if self.edge_enabled[input_index_edge] == False:
            return output
        
        # Check if disabled_edge_id exists
        if edge_id not in self.edge_ids:
            raise IDNotFoundError()
        
        # Step 1: Calculate the islands and store them
        # Step 2: Remove the input edge from the id_pairs list
        # Step 3: Calculate the new islands
        # Step 4: Remove the islands that were already there in Step 1
        # Step 5: Check which remaining islands contain the source vertex, the other one IS the output
        
        # List for storing all enabled edges, to use for finding out if the graph is fully connected
        edge_vertex_id_pairs_enabled_before = []   
        edge_ids_enabled_before = []
             
        # For loop for finding all enabled edges
        for edge_to_check in self.edge_vertex_id_pairs:          
            edge_to_check_index = self.edge_vertex_id_pairs.index(edge_to_check)
            
            if self.edge_enabled[edge_to_check_index] == True:
                edge_ids_enabled_before.append(self.edge_ids[edge_to_check_index])
                edge_vertex_id_pairs_enabled_before.append(edge_to_check)
                    
        # Step 1 is calculated here
        ## Island calculation before removing the input edge
        G = nx.Graph()
        G.add_nodes_from(self.vertex_ids)
        G.add_edges_from(edge_vertex_id_pairs_enabled_before)
        
        list_of_islands_before = []
             
        for i, c in enumerate(nx.connected_components(G)):
            list_of_islands_before.append(list(c))
            
        # Step 2 is calculated here
        # For loop for finding all enabled edges without the input edge
        edge_vertex_id_pairs_enabled_after = []   
        edge_ids_enabled_after = [] # The list with the input edge removed
        for edge_index in range(len(edge_ids_enabled_before)):
            if edge_ids_enabled_before[edge_index] != edge_id: 
                edge_ids_enabled_after.append(edge_ids_enabled_before[edge_index])
                edge_vertex_id_pairs_enabled_after.append(edge_vertex_id_pairs_enabled_before[edge_index])
        
        # Step 3: Calculate the new islands
        ## Island calculation after
        G = nx.Graph()
        G.add_nodes_from(self.vertex_ids)
        G.add_edges_from(edge_vertex_id_pairs_enabled_after)
        
        list_of_islands_after = []
        
        for i, c in enumerate(nx.connected_components(G)):
            list_of_islands_after.append(list(c))
        
        output_list = []
        
        # Step 4: Remove the islands that were already there in Step 1
        # Step 5: Check which remaining islands contain the source vertex, the other one IS the output
        # We loop through all the islands, if an island contains the source vertex it is removed, and if the island already existed initially it is also removed.
        # What you are left with is a list of the downstream vertices
        for id_list in list_of_islands_after:
            contains_source = False
            if id_list in list_of_islands_before:
                continue
            for id in id_list:
                if (id == self.source_vertex_id):
                    contains_source = True
            if not contains_source:
                output_list.append(id_list)
            
        output = output_list[0]
        return output

    def find_alternative_edges(self, disabled_edge_id: int) -> List[int]:
        """
        Given an enabled edge, do the following analysis:
            If the edge is going to be disabled,
                which (currently disabled) edge can be enabled to ensure
                that the graph is again fully connected and acyclic?
            Return a list of all alternative edges.
        If the disabled_edge_id is not a valid edge id, it should raise IDNotFoundError.
        If the disabled_edge_id is already disabled, it should raise EdgeAlreadyDisabledError.
        If there are no alternative to make the graph fully connected again, it should return empty list.


        For example, given the following graph:

        vertex_0 (source) --edge_1(enabled)-- vertex_2 --edge_9(enabled)-- vertex_10
                 |                               |
                 |                           edge_7(disabled)
                 |                               |
                 -----------edge_3(enabled)-- vertex_4
                 |                               |
                 |                           edge_8(disabled)
                 |                               |
                 -----------edge_5(enabled)-- vertex_6

        Call find_alternative_edges with disabled_edge_id=1 will return [7]
        Call find_alternative_edges with disabled_edge_id=3 will return [7, 8]
        Call find_alternative_edges with disabled_edge_id=5 will return [8]
        Call find_alternative_edges with disabled_edge_id=9 will return []

        Args:
            disabled_edge_id: edge id (which is currently enabled) to be disabled

        Returns:
            A list of alternative edge ids.
        """
        # put your implementation here
        pass

