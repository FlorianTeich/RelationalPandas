# RelationalPandas - Enrich your DataFrames by Relations

## Abstract

Define relationships between dataframes in order to visually inspect your data more comfortable.

## Introduction

Ever worked on multiple DataFrames that are somehow semantically related (e.g. by referencing each other)?
Take these two DataFrames for instance:

PersonID | Name
----------------
0        | Bob
1        | Alice

CarType | OwnerID
------------------
VW id3        | 1
Toyota Aygo X | 0
Audi a3       | 1

I wish there was a better way to inspect the data visually than to stare at these tables.
I want to be able to reorganize the entirety of data as a knowledge graph to reflect the inherent relationship between the involved objects.
Here is the same data but reorganized and visualized given the relation between the entities:

INSERT IMAGE HERE

## Installation

```
pip install
```

## Quickstart

```
import RelationalPandas as rp

df1 = {"PersonID": [0, 1], "Name": ["Bob", "Alice"]}
df2 = {"CarType": ["VW id3", "Toyota Aygo X", "Audi a3"], "OwnerID": [1, 0, 1]}

collection = rp.Collection()
collection.addRelation(df1, df2, "PersonID", "OwnerID")
collection.visualize()
```
