"""
Collection class that tracks the dataframes and their relations
as well as columns that can be used for naming entities.
"""
from typing import List, Sequence, Tuple, Dict
import pandas as pd
import networkx as nx
import xxhash
import random
from matplotlib import pyplot as plt

class Collection:
    """
    Collection class that tracks the dataframes and their relations
    as well as columns that can be used for naming entities.
    """

    def __init__(self) -> None:
        self.xxh = xxhash.xxh64()
        self.dataframes = []
        self.relations = []
        self.name_columns = []
        self.df_map = {}

    def hash_dataframe(self, dataframe: pd.DataFrame) -> int:
        """Returns hash of given dataframe

        Args:
            dataframe (pd.DataFrame): Input dataframe

        Returns:
            int: hash of dataframe
        """
        self.xxh.update(pd.util.hash_pandas_object(dataframe).values)
        res = self.xxh.intdigest()
        self.xxh.reset()
        return res

    def get_index_of_dataframe(self, dataframe: pd.DataFrame) -> int:
        """Returns index of the dataframe inside the tracked dataframelist

        Args:
            dataframe (pd.DataFrame): Input dataframe

        Returns:
            int: index of the dataframe inside the tracked dataframelist
        """
        return self.df_map[self.hash_dataframe(dataframe)]

    def register_name_columns(self, name_columns: List):
        """Registers the columns of the dataframes that are used for labeling entities

        Args:
            name_columns (List): List of strings (columnnames)
        """
        self.name_columns = name_columns

    def register_dataframes(self, dataframelist: List):
        """Registers the dataframes that are used in the collection

        Args:
            dataframelist (List): List of dataframes
        """
        self.dataframes = dataframelist
        for i, entry in enumerate(self.dataframes):
            self.df_map[self.hash_dataframe(entry)] = i

    def register_relations(
        self, relationlist: Sequence[Tuple[pd.DataFrame, pd.DataFrame, str, str]]
    ):
        """Register relations between the used dataframes

        Args:
            relationlist (List): List of lists, containing:
            dataframe, dataframe, columnname, columnname
        """
        for source, target, source_column, target_column in relationlist:
            assert self.hash_dataframe(source) in self.df_map
            assert self.hash_dataframe(target) in self.df_map
            assert source_column in source
            assert target_column in target
            self.relations.append(
                [
                    self.get_index_of_dataframe(source),
                    self.get_index_of_dataframe(target),
                    source_column,
                    target_column,
                ]
            )

    def register_scene(self, scene: Dict={
        "dataframes": [{
            "name": "Name",
            "data": pd.DataFrame({"PersonID": [0, 1], "Name": ["Bob", "Alice"]}),
            "entity_column": "PersonID"},
            {
            "name": "CarType",
            "data": pd.DataFrame({
                "CarType": ["VW id3", "Toyota Aygo X", "Audi a3"],
                "OwnerID": [1, 0, 1]}),
            "entity_column": "OwnerID"}],
        "relations": [[
            pd.DataFrame({"PersonID": [0, 1], "Name": ["Bob", "Alice"]}), 
            pd.DataFrame({
                "CarType": ["VW id3", "Toyota Aygo X", "Audi a3"],
                "OwnerID": [1, 0, 1]}),
            "PersonID",
            "OwnerID"]]
    }):
        """Single function call for registering all collection information.
        Why? Because before, one had to first call register_dataframes,
        then register_name_columns and afterwards register relations.
        So multiple function calls in specific order, which might not be intuitive for new users."""
        self.register_dataframes([entry["data"] for entry in scene["dataframes"]])
        self.register_name_columns([entry["entity_column"] for entry in scene["dataframes"]])
        self.register_relations(
            [(entry[0], entry[1], entry[2], entry[3]) for entry in scene["relations"]]
            )

    def visualize_instances(self, backend: str="matplotlib") -> int:
        """Visualize the collection

        Returns:
            int: 1 if successful
        """
        if backend in "matplotlib":
            node_color = []
            labels = {}
            graph = nx.Graph()
            for i, dataframe in enumerate(self.dataframes):
                for index, row in dataframe.iterrows():
                    graph.add_node(str(i) + "_" + str(index))
                    labels[str(i) + "_" + str(index)] = row[self.name_columns[i]]
                    node_color.append(i)

            for ind_s, ind_t, source_column, target_column in self.relations:
                src = self.dataframes[ind_s]
                trg = self.dataframes[ind_t]
                res = src.reset_index().merge(
                    trg.reset_index(), left_on=source_column, right_on=target_column
                )[["index_x", "index_y", source_column, target_column]]
                for index, row in res.iterrows():
                    graph.add_edge(
                        str(ind_s) + "_" + str(row[0]), str(ind_t) + "_" + str(row[1])
                    )

            nx.draw(
                graph,
                node_color=node_color,
                labels=labels,
                cmap=plt.cm.PiYG,
                node_size=2000,
            )
            plt.draw()
            return 1
        elif backend == "plotly":
            import plotly.graph_objects as go

            node_color = []
            labels = {}
            graph = nx.Graph()
            for i, dataframe in enumerate(self.dataframes):
                for index, row in dataframe.iterrows():
                    graph.add_node(str(i) + "_" + str(index))
                    labels[str(i) + "_" + str(index)] = row[self.name_columns[i]]
                    node_color.append(i)

            for ind_s, ind_t, source_column, target_column in self.relations:
                src = self.dataframes[ind_s]
                trg = self.dataframes[ind_t]
                res = src.reset_index().merge(
                    trg.reset_index(), left_on=source_column, right_on=target_column
                )[["index_x", "index_y", source_column, target_column]]
                for index, row in res.iterrows():
                    graph.add_edge(
                        str(ind_s) + "_" + str(row[0]), str(ind_t) + "_" + str(row[1])
                    )
            pos = nx.spring_layout(graph)
            nx.set_node_attributes(graph, pos, "pos")
            G = graph
            edge_x = []
            edge_y = []
            for edge in G.edges():
                x0, y0 = G.nodes[edge[0]]['pos']
                x1, y1 = G.nodes[edge[1]]['pos']
                edge_x.append(x0)
                edge_x.append(x1)
                edge_x.append(None)
                edge_y.append(y0)
                edge_y.append(y1)
                edge_y.append(None)

            edge_trace = go.Scatter(
                x=edge_x, y=edge_y,
                line=dict(width=0.5, color='#888'),
                hoverinfo='none',
                mode='lines')

            node_x = []
            node_y = []
            for node in G.nodes():
                x, y = G.nodes[node]['pos']
                node_x.append(x)
                node_y.append(y)

            node_trace = go.Scatter(
                x=node_x, y=node_y,
                mode='markers',
                hoverinfo='text',
                marker=dict(
                    showscale=True,
                    colorscale='YlGnBu',
                    reversescale=True,
                    color=[],
                    size=10,
                    colorbar=dict(
                        thickness=15,
                        title='Node Connections',
                        xanchor='left',
                        titleside='right'
                    ),
                    line_width=2))
            #node_adjacencies = []
            #node_text = []
            #for node, adjacencies in enumerate(G.adjacency()):
            #    node_adjacencies.append(len(adjacencies[1]))
            #    #node_text.append('# of connections: '+ str(len(adjacencies[1])))
            #    node_text.append(list(labels.values())[node])

            #node_trace.marker.color = node_adjacencies

            node_trace.marker.color = [int(i) for i in node_color]
            #node_trace.text = node_text
            node_trace.text = list(labels.values())
            fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title='',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20,l=5,r=5,t=40),
                            annotations=[ dict(
                                text="",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002 ) ],
                            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                            )
            fig.show()
            return 1
        else:
            return -1
