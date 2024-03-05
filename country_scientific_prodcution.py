"""Taller Presencial Evaluable"""

import pandas as pd
import folium


def load_affiliations():
    """Load affiliations from scopus-papers.csvi"""
    dataframe = pd.read_csv("https://raw.githubusercontent.com/jdvelasq/datalabs/master/datasets/scopus-papers.csv", sep=",", index_col=None)[['Affiliations']]
    return dataframe

def remove_na_rows(affiliations):
    """Elimina las filas con valores nulos en la columna 'Affiliations'"""
    affiliations = affiliations.copy()
    affiliations = affiliations.dropna(subset=["Affiliations"])
    return affiliations

def add_countries_column(affiliations):
    """Transforma la columna 'Affiliations' a una lista de paises."""

    affiliations = affiliations.copy()
    affiliations["countries"] = affiliations["Affiliations"].copy()
    affiliations["countries"] = affiliations["countries"].str.split(";")
    affiliations["countries"] = affiliations["countries"].map(
        lambda x: [y.split(",") for y in x]
    )
    affiliations["countries"] = affiliations["countries"].map(
        lambda x: [y[-1].strip() for y in x]
    )
    affiliations["countries"] = affiliations["countries"].map(set)
    affiliations["countries"] = affiliations["countries"].str.join(", ")

    return affiliations
  
def clean_countries(affiliations):

    affiliations = affiliations.copy()
    affiliations["countries"] = affiliations["countries"].str.replace(
        "United States", "United States"
    )
    return affiliations

def count_country_frequency(affiliations):
    """Cuenta la frecuencia de cada país en la columna 'countries'"""

    countries = affiliations["countries"].copy()
    countries = countries.str.split(", ")
    countries = countries.explode()
    countries = countries.value_counts()
    return countries

def plot_world_map(countries):
    """Grafica un mapa mundial con la frecuencia de cada país."""

    countries = countries.copy()
    countries = countries.to_frame()
    countries = countries.reset_index()

    m = folium.Map(location=[0, 0], zoom_start=2)

    folium.Choropleth(
        geo_data="https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json",
        data=countries,
        columns=["countries", "count"],
        key_on="feature.properties.name",
        fill_color="Greens",
    ).add_to(m)
    m.save("map.html")
  
def main():
    """Función principal"""
    affiliations = load_affiliations()
    affiliations = remove_na_rows(affiliations)
    affiliations = add_countries_column(affiliations)
    affiliations = clean_countries(affiliations)
    countries = count_country_frequency(affiliations)
    countries.to_csv("countries.csv")
    plot_world_map(countries)

if __name__ == "__main__":
    main()