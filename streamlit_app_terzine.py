# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OSL6c0V-9lVSoh-WNS1K8baoI4Ryn7ZA
"""

from weaviate.classes.query import MetadataQuery
import streamlit as st
from sentence_transformers import SentenceTransformer
import weaviate
from weaviate.auth import Auth
from weaviate.collections.classes.filters import Filter

st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+Pro:wght@400;600&display=swap');

/* CSS Variables for color palette */
:root {
  --primary-bg: #f4f1e9;
  --secondary-bg: #e6e2d3;
  --primary-text: #2c2c2c;
  --secondary-text: #4a4a4a;
  --accent: #8b7d6b;
  --highlight: #b7a99a;
}

/* Base styles */
body {
  font-family: 'Source Sans Pro', sans-serif;
  background-color: var(--primary-bg);
  color: var(--primary-text);
  line-height: 1.6;
  padding: 20px;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
  font-family: 'Playfair Display', serif;
  color: var(--secondary-text);
}

h1 {
  font-size: 2.5em;
  border-bottom: 2px solid var(--accent);
  padding-bottom: 10px;
}

/* Streamlit specific styles */
.stTextInput > div > div > input {
  background-color: var(--secondary-bg);
  border: 1px solid var(--accent);
  color: var(--primary-text);
}

.stButton > button {
  background-color: var(--accent);
  color: var(--primary-bg);
  border: none;
  padding: 10px 20px;
  font-family: 'Playfair Display', serif;
  font-weight: 700;
  transition: background-color 0.3s ease;
}

.stButton > button:hover {
  background-color: var(--highlight);
}

/* Multiselect styles */
.stMultiSelect > div > div > div {
  background-color: var(--secondary-bg);
}

.stMultiSelect > div > div > div:hover {
  border-color: var(--highlight);
}

.stMultiSelect > div[data-baseweb="select"] > div > div > div[role="option"] {
  background-color: var(--accent);
  color: var(--primary-bg);
}

/* Slider styles */
.stSlider > div > div > div > div {
  background-color: var(--accent);
}

/* Expander styles */
.streamlit-expanderHeader {
  background-color: var(--secondary-bg);
  border: 1px solid var(--accent);
  border-radius: 4px;
  font-family: 'Playfair Display', serif;
  color: var(--secondary-text);
}

.streamlit-expanderContent {
  background-color: var(--primary-bg);
  border: 1px solid var(--accent);
  border-top: none;
  border-radius: 0 0 4px 4px;
  padding: 10px;
}

/* Progress bar styles */
.stProgress > div > div > div > div {
  background-color: var(--accent);
}

/* Custom classes */
.verse {
  font-style: italic;
  color: var(--secondary-text);
  margin: 10px 0;
  padding: 10px;
  background-color: var(--secondary-bg);
  border-left: 3px solid var(--accent);
}

.similarity-score {
  font-weight: 600;
  color: var(--accent);
}
""", unsafe_allow_html=True)


@st.cache_resource
def load_model():
    model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
    return model

def find_similar(query, model, limit=10, cantiche=[], canti=[]):
    results = []
    query_vector = model.encode([query])[0]

    filters = None
    if cantiche and canti:
        filters = (Filter.by_property("cantica").contains_any(cantiche)
            & Filter.by_property("canto").contains_any(canti)
        )
    elif cantiche:
        filters = Filter.by_property("cantica").contains_any(cantiche)
    elif canti:
        filters = Filter.by_property("canto").contains_any(canti)

    response = voci_dall_inferno.query.near_vector(
        near_vector=query_vector,
        limit=limit,
        return_metadata=MetadataQuery(distance=True),
        filters=filters
    )

    for o in response.objects:
         results.append({
                "cantica": o.properties["cantica"],
                "canto": o.properties["canto"],
                "range_versi": o.properties["range_versi"],
                "terzina": o.properties["terzina"],
                "distance": o.metadata.distance
            })
    return results

tot_cantiche = {"Inferno": "Inferno", "Purgatorio": "Purgatorio", "Paradiso": "Paradiso"}
tot_canti = {"Canto I": "I", "Canto II": "II", "Canto III": "III", "Canto IV": "IV", "Canto V": "V", "Canto VI": "VI", "Canto VII": "VII", "Canto VIII": "VIII", "Canto IX": "IX", "Canto X": "X", "Canto XI": "XI", "Canto XII": "XII", "Canto XIII": "XIII", "Canto XIV": "XIV", "Canto XV": "XV", "Canto XVI": "XVI", "Canto XVII": "XVII", "Canto XVIII": "XVIII", "Canto XIX": "XIX", "Canto XX": "XX", "Canto XXI": "XXI", "Canto XXII": "XXII", "Canto XXIII": "XXIII", "Canto XXIV": "XXIV", "Canto XXV": "XXV", "Canto XXVI": "XXVI", "Canto XXVII": "XXVII", "Canto XXVIII": "XXVIII", "Canto XXIX": "XXIX", "Canto XXX": "XXX", "Canto XXXI": "XXXI", "Canto XXXII": "XXXII", "Canto XXXIII": "XXXIII", "Canto XXXIV": "XXXIV"}

st.title("Voci dall'Inferno Verse Similarity Search")

model = load_model()

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=st.secrets["WEAVIATE_URL"],
    auth_credentials=Auth.api_key(st.secrets["WEAVIATE_API_KEY"]),
)
voci_dall_inferno = client.collections.get(st.secrets["COLLECTION_NAME"])

query = st.text_input("Enter your search query:")
cantiche = st.multiselect("Select cantica", tot_cantiche.keys())
select_cantiche = [tot_cantiche[cantica] for cantica in cantiche]
canti = st.multiselect("Select canto", tot_canti.keys())
select_canti = [tot_canti[canto] for canto in canti]
col1, col2 = st.columns(2)
#threshold = col1.slider("Similarity threshold:", 0.0, 1.0, value=0.5, step=0.01)
limit = col2.slider("Number of results:", 1, 10, value=5, step=1)

if st.button("Search"):
    #results = find_similar(query, model, threshold, limit, select_canti)
    results = find_similar(query, model, limit, select_cantiche, select_canti)

    if results:
        st.subheader(f"Found {len(results)} similar verses:")
        for i, result in enumerate(results, 1):
            with st.expander(f"{i}. {result ['cantica']} {result ['canto']}, vv. {result['range_versi']} (Similarity: {1 - result['distance']:.2f})", expanded=True):
                st.markdown(f"<div class='verse'>{result['terzina']}</div>", unsafe_allow_html=True)
                #st.progress(1 - result['distance'])
    else:
        st.warning("No results found. Try adjusting the similarity threshold or search query.")