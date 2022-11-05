"""
Tests
"""
import unittest
import pandas as pd
import relationalpandas as rp


class TestUseCase(unittest.TestCase):
    """
    Test Main Use Case
    """

    def test_use_case_01(self):
        """
        Test
        """
        df1 = pd.DataFrame({"PersonID": [0, 1], "Name": ["Bob", "Alice"]})
        df2 = pd.DataFrame({
            "CarType": ["VW id3", "Toyota Aygo X", "Audi a3"],
            "OwnerID": [1, 0, 1]})

        collection = rp.Collection()
        collection.register_dataframes([df1, df2])
        collection.register_name_columns(["Name", "CarType"])
        collection.register_relations([[df1, df2, "PersonID", "OwnerID"]])
        result = collection.visualize()
        self.assertEqual(result, 1)
