import pandas as pd
import networkx as nx
import xxhash
from matplotlib import pyplot as plt


class Collection:
    def __init__(self) -> None:
        self.h = xxhash.xxh64()
        self.dataframes = []
        self.relations = []
        self.name_columns = []
        self.df_map = {}
    
    def hash_dataframe(self, dataframe):
        self.h.update(pd.util.hash_pandas_object(dataframe).values)
        res = self.h.intdigest()
        self.h.reset()
        return res
    
    def get_index_of_dataframe(self, dataframe):
        return self.df_map[self.hash_dataframe(dataframe)]
    
    def register_name_columns(self, name_columns):
        self.name_columns = name_columns
    
    def register_dataframes(self, dataframelist):
        self.dataframes = dataframelist
        for i, entry in enumerate(self.dataframes):
            self.df_map[self.hash_dataframe(entry)] = i

    def register_relations(self, relationlist):
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
    
    def visualize(self):
        node_color = []
        labels = {}
        F = nx.Graph()
        for i, dataframe in enumerate(self.dataframes):
            for index, row in dataframe.iterrows():
                F.add_node(str(i) + "_" + str(index))
                labels[str(i) + "_" + str(index)] = row[self.name_columns[i]]
                node_color.append(i)

        for ind_s, ind_t, source_column, target_column in self.relations:
            s = self.dataframes[ind_s]
            t = self.dataframes[ind_t]
            res = s.reset_index().merge(t.reset_index(), left_on=source_column, right_on=target_column)[["index_x", "index_y", source_column, target_column]]
            for index, row in res.iterrows():
                F.add_edge(str(ind_s) + "_" + str(row[0]), str(ind_t) + "_" + str(row[1]))
        
        nx.draw(F, node_color=node_color, labels=labels, cmap=plt.cm.PiYG, node_size=2000)
        plt.draw()
        return