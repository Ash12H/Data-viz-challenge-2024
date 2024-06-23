from dash import html, callback, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from dataviz_app import id

ENGLISH_CONTENT = """
    # Card            
    ---

    The first element is a world map with the Pacific island countries and territories **represented in
    this study**. These territories are coloured grey and you can **click** on them.

    By clicking on a territory, you can obtain information about it. You can **click on
    several areas** to compare them. Click again on a territory to **unselect** it.

    # Graphics
    ---

    Using the data available in the SPC-Hub and the New Caledonian Government Hub, we have created
    three graphs. The population studied is the **15-24 year olds** and we compare the data between **women
    and men**.

    There are 3 types of data:

    - 📖 **Literacy**: The percentage of the population that can read and write.
    - 👩‍🏫 **Education**: The percentage of the population that has achieved a certain level of education.
    - 💼 **Activity**: The percentage of the population not in education, employment or training.
"""

FRENCH_CONTENT = """
    # Carte            
    ---

    Le premier élément est une carte du monde avec les pays et territoires insulaires du Pacifique **représentés dans
    cette étude**. Ces territoires sont colorés en gris et vous pouvez **cliquer** dessus.

    En cliquant sur un territoire, vous pouvez obtenir des informations sur celui-ci. Vous pouvez **cliquer sur
    plusieurs territoires** pour les comparer comparer. Cliquez à nouveau sur un territoire pour le **désélectionner**.

    # Graphiques
    ---

    À partir des données disponibles dans le SPC-Hub et le Hub du Gouvernement de Nouvelle-Calédonie, nous avons créé
    trois graphiques. La population étudiée est celle des **15-24 ans** et nous comparons les données entre **les femmes
    et les hommes**.

    Il y a 3 types de données :

    - 📖 **Alphabétisation** : Le pourcentage de la population qui sait lire et écrire.
    - 👩‍🏫 **Éducation** : Le pourcentage de la population qui a atteint un certain niveau d'éducation.
    - 💼 **Activité** : Le pourcentage de la population qui ne suit pas d'études, d'emploi ou de formation.
"""

MENU_CONTENT = dbc.Container(
    children=[
        dcc.Markdown(ENGLISH_CONTENT, id="info_content"),
        dbc.Button(
            "English",
            id="language",
            style={
                "position": "absolute",
                "top": "10px",
                "right": "50px",
                "width": "100px",
            },
        ),
    ]
)


def menu() -> html.Div:
    canvas_menu = html.Div(
        [
            dbc.Button(
                children=[html.Span("Informations", className="button-menu-content")],
                id="button_menu",
                n_clicks=0,
                style={"position": "fixed", "top": "20px", "left": "10px"},
                className="button-menu",
            ),
            dbc.Offcanvas(
                MENU_CONTENT,
                id=id.MENU,
                title="DataViz Challenge 2024",
                is_open=False,
                placement="end",
                style={"height": "100vh", "width": "50vw", "overflowY": "auto"},
            ),
        ]
    )

    @callback(
        Output(id.MENU, "is_open"),
        Input("button_menu", "n_clicks"),
        [State(id.MENU, "is_open")],
    )
    def toggle_offcanvas(n1, is_open):
        if n1:
            return not is_open
        return is_open

    @callback(
        Output("info_content", "children"),
        Output("language", "children"),
        Input("language", "n_clicks"),
        State("language", "children"),
    )
    def toggle_language(n_click, button_text):
        if n_click and button_text == "Français":
            return FRENCH_CONTENT, "English"
        return ENGLISH_CONTENT, "Français"

    return canvas_menu
