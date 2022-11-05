"""
Collection class that tracks the dataframes and their relations
as well as columns that can be used for naming entities.
"""
from typing import List, Sequence, Tuple
import pandas as pd
import networkx as nx
import xxhash
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

    def register_relations(self,
        relationlist: Sequence[Tuple[pd.DataFrame, pd.DataFrame, str, str]]):
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
            self.relations.append([
                self.get_index_of_dataframe(source),
                self.get_index_of_dataframe(target),
                source_column,
                target_column])

    def visualize(self) -> int:
        """Visualize the collection

        Returns:
            int: 1 if successful
        """
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
            res = src.reset_index().merge(trg.reset_index(),
                left_on=source_column,
                right_on=target_column)[["index_x", "index_y", source_column, target_column]]
            for index, row in res.iterrows():
                graph.add_edge(str(ind_s) + "_" + str(row[0]), str(ind_t) + "_" + str(row[1]))

        nx.draw(graph, node_color=node_color, labels=labels, cmap=plt.cm.PiYG, node_size=2000)
        plt.draw()
        return 1
