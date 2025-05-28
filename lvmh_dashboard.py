import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Données structurées pour les BU LVMH
business_units = {
    "Mode et Maroquinerie": {
        "focus": "Produits de luxe mode et accessoires",
        "potentiel": 9,
        "strategie": "Innovation produit et renforcement de l'expérience client",
        "regions": ["Asie", "Amérique du Nord", "Europe"]
    },
    "Vins et Spiritueux": {
        "focus": "Produits haut de gamme avec potentiel d'expansion",
        "potentiel": 7,
        "strategie": "Expansion géographique dans les marchés émergents",
        "regions": ["Asie", "Amérique Latine", "Europe"]
    },
    "Parfums et Cosmétiques": {
        "focus": "Luxe accessible et innovation produit",
        "potentiel": 8,
        "strategie": "Développement durable et marketing digital",
        "regions": ["Asie", "Europe", "Moyen-Orient"]
    }
}

st.title("Dashboard Stratégique LVMH à l'horizon 2030")

# Sélection Business Units
selected_bu = st.multiselect(
    "Sélectionnez les Business Units à analyser",
    options=list(business_units.keys()),
    default=list(business_units.keys())
)

# Filtrer les BU selon le potentiel minimum
threshold = st.slider("Filtrer par potentiel minimum", 0, 10, 7)

filtered_bu = {k: v for k, v in business_units.items() if v["potentiel"] >= threshold and k in selected_bu}

if not filtered_bu:
    st.warning("Aucune Business Unit ne correspond aux critères.")
else:
    # Affichage détaillé
    for bu_name, bu_data in filtered_bu.items():
        st.subheader(bu_name)
        st.write(f"**Focus :** {bu_data['focus']}")
        st.write(f"**Potentiel de croissance :** {bu_data['potentiel']} / 10")
        st.write(f"**Stratégie recommandée :** {bu_data['strategie']}")
        st.write(f"**Régions cibles :** {', '.join(bu_data['regions'])}")
        st.markdown("---")

    # Radar chart du potentiel par BU
    fig = go.Figure()

    categories = list(filtered_bu.keys())
    scores = [filtered_bu[bu]["potentiel"] for bu in categories]

    fig.add_trace(go.Scatterpolar(
        r=scores + [scores[0]],  # boucle pour fermer le radar
        theta=categories + [categories[0]],
        fill='toself',
        name='Potentiel de croissance'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=False,
        title="Potentiel de croissance par Business Unit"
    )

    st.plotly_chart(fig)

    # Carte simplifiée des régions cibles
    # Création d'un dataframe des régions avec coordonnées approximatives
    regions_coords = {
        "Asie": [34.0479, 100.6197],
        "Amérique du Nord": [54.5260, -105.2551],
        "Europe": [54.5260, 15.2551],
        "Amérique Latine": [-14.2350, -51.9253],
        "Moyen-Orient": [29.3759, 45.0209]
    }

    # Extraction des régions sélectionnées
    all_regions = set()
    for bu in filtered_bu.values():
        all_regions.update(bu["regions"])

    df_regions = pd.DataFrame([
        {"Region": region, "Latitude": regions_coords[region][0], "Longitude": regions_coords[region][1]}
        for region in all_regions
    ])

    fig_map = px.scatter_geo(
        df_regions,
        lat="Latitude",
        lon="Longitude",
        hover_name="Region",
        size_max=30,
        title="Régions cibles pour la croissance"
    )
    st.plotly_chart(fig_map)

# Recommandations stratégiques générales
st.markdown("### Recommandations stratégiques générales")

st.write("""
- Prioriser la croissance organique sur les Business Units avec un fort potentiel, particulièrement la Mode et Maroquinerie.
- Investir dans l’innovation produit, le développement durable et le marketing digital pour capter la clientèle jeune et connectée.
- Renforcer la présence dans les zones géographiques à forte croissance économique : Asie, Amérique du Nord et Moyen-Orient.
- Adapter la stratégie aux spécificités culturelles et économiques des marchés locaux.
""")
