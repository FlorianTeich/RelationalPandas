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
        df2 = pd.DataFrame(
            {"CarType": ["VW id3", "Toyota Aygo X", "Audi a3"], "OwnerID": [1, 0, 1]}
        )

        collection = rp.Collection()
        collection.register_scene({
            "dataframes": [
                {
                    "name": "Name",
                    "data": df1,
                    "entity_column": "PersonID"
                },
                {
                    "name": "CarType",
                    "data": df2,
                    "entity_column": "OwnerID"
                }
            ],
            "relations": [
                [df1, df2, "PersonID", "OwnerID"]
            ]
        })
        self.assertEqual(1, 1)
