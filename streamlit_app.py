import sys
import zipfile
import urllib.request
import streamlit as st
import pandas as pd
sys.path.append("../")
import relationalpandas as rp

st.title("🦑🐼🐍 RelationalPandas - Enrich your DataFrames by Relations")

st.write("Let us load the chinook dataset. Especially let us work with tracks, genres and artists.")

@st.cache
def load_data():
    url = "https://www.sqlitetutorial.net/wp-content/uploads/2018/03/chinook.zip"

    urllib.request.urlretrieve(url, "chinook.zip")

    with zipfile.ZipFile("chinook.zip", 'r') as zip_ref:
        zip_ref.extractall("./")

    tracks = pd.read_sql_table("tracks", "sqlite:///chinook.db")
    artists = pd.read_sql_table("artists", "sqlite:///chinook.db")
    genres = pd.read_sql_table("genres", "sqlite:///chinook.db")
    tracks["TrackName"] = tracks.Name
    tracks = tracks[["TrackName", "Composer", "GenreId"]]
    genres["GenreName"] = genres.Name
    genres = genres[["GenreName", "GenreId"]]
    tracks = tracks[:200]
    return tracks, artists, genres

tracks, artists, genres = load_data()

st.header("📋 Raw Dataframes")

tab1, tab2, tab3 = st.tabs(["Tracks", "Artists", "Genres"])

with tab1:
    st.dataframe(tracks)

with tab2:
    st.dataframe(artists)

with tab3:
    st.dataframe(genres)

collection = rp.Collection()
scene = {
        "dataframes": [
            {
                "name": "Tracks",
                "data": tracks,
                "entity_column": "TrackName"
            },
            {
                "name": "Artists",
                "data": artists,
                "entity_column": "Name"
            },
            {
                "name": "Genres",
                "data": genres,
                "entity_column": "GenreName"
            }
        ],
        "relations": [
            [tracks, artists, "Composer", "Name"],
            [tracks, genres, "GenreId", "GenreId"]
        ]
    }
collection.register_scene(scene)

st.header("🧲 Relationships")

st.json(
    {
        "Tracks <-> Artists":
        {
            "SourceColumn": "Tracks.Composer",
            "TargetColumn": "Artists.Name"
        },
        "Tracks <-> Genres":
        {
            "SourceColumn": "Tracks.GenreId",
            "TargetColumn": "Genres.GenreId"
        }
    }
)

fig = collection.visualize_instances("plotly", return_figure=True)

st.header("👀 Visualize the Data")

st.plotly_chart(fig, use_container_width=True)
