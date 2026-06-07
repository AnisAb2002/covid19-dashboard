
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from data_loader import load_who_data

# Initialisation de l'app
app = dash.Dash(
    __name__,
    title="Dashboard COVID-19",
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
server = app.server  # Pour le déploiement 

# Chargement des données 
df, df_latest = load_who_data()
countries = sorted(df["Country"].dropna().unique())
regions = sorted(df["WHO_region"].dropna().unique())

# Palette de couleurs 
COLORS = {
    "bg": "#0f172a",
    "card": "#1e293b",
    "border": "#334155",
    "text": "#f1f5f9",
    "muted": "#94a3b8",
    "blue": "#3b82f6",
    "red": "#ef4444",
    "green": "#22c55e",
    "yellow": "#f59e0b",
    "purple": "#a855f7",
}


def make_kpi_card(title, value, sub, color):
    return html.Div(
        [
            html.P(title, style={"color": COLORS["muted"], "fontSize": "0.85rem", "marginBottom": "6px"}),
            html.H2(value, style={"color": color, "fontSize": "2rem", "fontWeight": "700", "margin": "0"}),
            html.P(sub, style={"color": COLORS["muted"], "fontSize": "0.75rem", "marginTop": "4px"}),
        ],
        style={
            "backgroundColor": COLORS["card"],
            "border": f"1px solid {COLORS['border']}",
            "borderRadius": "12px",
            "padding": "20px 24px",
            "flex": "1",
            "minWidth": "180px",
        },
    )


#  KPI globaux
total_cases = df_latest["Cumulative_cases"].sum()
total_deaths = df_latest["Cumulative_deaths"].sum()
total_countries = df_latest["Country"].nunique()
cfr = (total_deaths / total_cases * 100) if total_cases > 0 else 0


def format_big(n):
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif n >= 1_000:
        return f"{n/1_000:.0f}K"
    return str(int(n))


#  Layout
app.layout = html.Div(
    style={"backgroundColor": COLORS["bg"], "minHeight": "100vh", "fontFamily": "'Inter', sans-serif", "color": COLORS["text"]},
    children=[
        # En-tête
        html.Div(
            [
                html.Div(
                    [
                        html.H1("Dashboard COVID-19", style={"margin": "0", "fontSize": "1.6rem", "fontWeight": "700"}),
                        html.P("Anis ABDAT - Projet étudiant", style={"color": COLORS["muted"], "margin": "4px 0 0", "fontSize": "0.85rem"}),
                    ]
                ),
                html.Div(
                    html.A(
                        " Données OMS",
                        href="https://covid19.who.int/data",
                        target="_blank",
                        style={"color": COLORS["blue"], "textDecoration": "none", "fontSize": "0.85rem"},
                    )
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "alignItems": "center",
                "padding": "20px 32px",
                "borderBottom": f"1px solid {COLORS['border']}",
                "backgroundColor": COLORS["card"],
            },
        ),

        # Corps principal
        html.Div(
            style={"padding": "24px 32px", "maxWidth": "1400px", "margin": "0 auto"},
            children=[

                # KPIs
                html.Div(
                    [
                        make_kpi_card("Cas confirmés", format_big(total_cases), "Cumulatif mondial", COLORS["blue"]),
                        make_kpi_card("Décès", format_big(total_deaths), "Cumulatif mondial", COLORS["red"]),
                        make_kpi_card("Létalité (CFR)", f"{cfr:.2f}%", "Décès / Cas confirmés", COLORS["yellow"]),
                        make_kpi_card("Pays touchés", str(total_countries), "Données disponibles", COLORS["green"]),
                    ],
                    style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginBottom": "24px"},
                ),

                #Filtres
                html.Div(
                    [
                        html.Div(
                            [
                                html.Label("Région OMS", style={"color": COLORS["muted"], "fontSize": "0.8rem", "marginBottom": "6px", "display": "block"}),
                                dcc.Dropdown(
                                    id="region-filter",
                                    options=[{"label": "Toutes les régions", "value": "ALL"}] + [{"label": r, "value": r} for r in regions],
                                    value="ALL",
                                    clearable=False,
                                    style={"backgroundColor": COLORS["card"], "color": "#000", "border": "none"},
                                ),
                            ],
                            style={"flex": "1", "minWidth": "200px"},
                        ),
                        html.Div(
                            [
                                html.Label("Pays (comparaison)", style={"color": COLORS["muted"], "fontSize": "0.8rem", "marginBottom": "6px", "display": "block"}),
                                dcc.Dropdown(
                                    id="country-filter",
                                    options=[{"label": c, "value": c} for c in countries],
                                    value=["France", "Germany", "Brazil", "United States of America", "India"],
                                    multi=True,
                                    placeholder="Choisir des pays...",
                                    style={"backgroundColor": COLORS["card"]},
                                ),
                            ],
                            style={"flex": "3", "minWidth": "300px"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "gap": "16px",
                        "flexWrap": "wrap",
                        "backgroundColor": COLORS["card"],
                        "border": f"1px solid {COLORS['border']}",
                        "borderRadius": "12px",
                        "padding": "16px 20px",
                        "marginBottom": "24px",
                    },
                ),

                #  Ligne 1 : carte + top pays
                html.Div(
                    [
                        html.Div(
                            [html.H3("Carte mondiale des cas cumulés", style={"margin": "0 0 12px", "fontSize": "1rem"}),
                             dcc.Graph(id="world-map", style={"height": "400px"}, config={"displayModeBar": False})],
                            style={"flex": "3", "backgroundColor": COLORS["card"], "border": f"1px solid {COLORS['border']}", "borderRadius": "12px", "padding": "20px"},
                        ),
                        html.Div(
                            [html.H3("Top 10 pays · Cas cumulés", style={"margin": "0 0 12px", "fontSize": "1rem"}),
                             dcc.Graph(id="top-countries", style={"height": "400px"}, config={"displayModeBar": False})],
                            style={"flex": "2", "backgroundColor": COLORS["card"], "border": f"1px solid {COLORS['border']}", "borderRadius": "12px", "padding": "20px"},
                        ),
                    ],
                    style={"display": "flex", "gap": "16px", "flexWrap": "wrap", "marginBottom": "24px"},
                ),

                # Ligne 2 : évolution temporell
                html.Div(
                    [
                        html.H3("Évolution des nouveaux cas (hebdomadaire)", style={"margin": "0 0 12px", "fontSize": "1rem"}),
                        dcc.Graph(id="time-series", style={"height": "350px"}, config={"displayModeBar": True}),
                    ],
                    style={"backgroundColor": COLORS["card"], "border": f"1px solid {COLORS['border']}", "borderRadius": "12px", "padding": "20px", "marginBottom": "24px"},
                ),

                # Ligne 3 : par région + scatter
                html.Div(
                    [
                        html.Div(
                            [html.H3("Répartition par région OMS", style={"margin": "0 0 12px", "fontSize": "1rem"}),
                             dcc.Graph(id="region-chart", style={"height": "320px"}, config={"displayModeBar": False})],
                            style={"flex": "1", "backgroundColor": COLORS["card"], "border": f"1px solid {COLORS['border']}", "borderRadius": "12px", "padding": "20px"},
                        ),
                        html.Div(
                            [html.H3("Cas vs Décès par pays", style={"margin": "0 0 12px", "fontSize": "1rem"}),
                             dcc.Graph(id="scatter-plot", style={"height": "320px"}, config={"displayModeBar": False})],
                            style={"flex": "1", "backgroundColor": COLORS["card"], "border": f"1px solid {COLORS['border']}", "borderRadius": "12px", "padding": "20px"},
                        ),
                    ],
                    style={"display": "flex", "gap": "16px", "flexWrap": "wrap"},
                ),

                # Footer
                html.Div(
                    "Anis  ABDAT -- Données OMS (WHO) -- Projet étudiant",
                    style={"textAlign": "center", "color": COLORS["muted"], "fontSize": "0.75rem", "padding": "32px 0 8px"},
                ),
            ],
        ),
    ],
)


# Callbacks 

@app.callback(
    Output("world-map", "figure"),
    Input("region-filter", "value"),
)
def update_map(region):
    data = df_latest if region == "ALL" else df_latest[df_latest["WHO_region"] == region]
    fig = px.choropleth(
        data,
        locations="iso_alpha",
        color="Cumulative_cases",
        hover_name="Country",
        hover_data={"Cumulative_cases": ":,", "Cumulative_deaths": ":,", "iso_alpha": False},
        color_continuous_scale="Blues",
        projection="natural earth",
    )
    fig.update_layout(
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["card"],
        geo=dict(bgcolor=COLORS["bg"], showframe=False, showcoastlines=True, coastlinecolor=COLORS["border"], landcolor="#1e293b", oceancolor=COLORS["bg"]),
        coloraxis_colorbar=dict(thickness=10, len=0.6, title="Cas", titlefont=dict(color=COLORS["muted"]), tickfont=dict(color=COLORS["muted"])),
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(color=COLORS["text"]),
    )
    return fig


@app.callback(
    Output("top-countries", "figure"),
    Input("region-filter", "value"),
)
def update_top(region):
    data = df_latest if region == "ALL" else df_latest[df_latest["WHO_region"] == region]
    top = data.nlargest(10, "Cumulative_cases").sort_values("Cumulative_cases")
    fig = px.bar(
        top,
        x="Cumulative_cases",
        y="Country",
        orientation="h",
        color="Cumulative_cases",
        color_continuous_scale="Blues",
        text="Cumulative_cases",
    )
    fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig.update_layout(
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["card"],
        xaxis=dict(showgrid=False, color=COLORS["muted"], title=""),
        yaxis=dict(color=COLORS["text"], title=""),
        coloraxis_showscale=False,
        margin=dict(l=0, r=40, t=0, b=0),
        font=dict(color=COLORS["text"], size=11),
    )
    return fig


@app.callback(
    Output("time-series", "figure"),
    Input("country-filter", "value"),
)
def update_timeseries(selected_countries):
    if not selected_countries:
        selected_countries = ["France"]
    filtered = df[df["Country"].isin(selected_countries)].copy()
    filtered = filtered.sort_values("Date_reported")
    # Lissage 7 jours
    filtered["cases_7d"] = filtered.groupby("Country")["New_cases"].transform(lambda x: x.rolling(7, min_periods=1).mean())

    fig = px.line(
        filtered,
        x="Date_reported",
        y="cases_7d",
        color="Country",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_traces(line_width=2)
    fig.update_layout(
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["card"],
        xaxis=dict(showgrid=False, color=COLORS["muted"], title=""),
        yaxis=dict(showgrid=True, gridcolor=COLORS["border"], color=COLORS["muted"], title="Nouveaux cas (moy. 7j)"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"])),
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(color=COLORS["text"]),
        hovermode="x unified",
    )
    return fig


@app.callback(
    Output("region-chart", "figure"),
    Input("region-filter", "value"),
)
def update_region(region):
    by_region = df_latest.groupby("WHO_region")[["Cumulative_cases", "Cumulative_deaths"]].sum().reset_index()
    fig = px.pie(
        by_region,
        names="WHO_region",
        values="Cumulative_cases",
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4,
    )
    fig.update_traces(textinfo="percent+label", textfont_size=11)
    fig.update_layout(
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["card"],
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"])),
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(color=COLORS["text"]),
    )
    return fig


@app.callback(
    Output("scatter-plot", "figure"),
    Input("region-filter", "value"),
)
def update_scatter(region):
    data = df_latest if region == "ALL" else df_latest[df_latest["WHO_region"] == region]
    data = data[data["Cumulative_cases"] > 10000].copy()
    fig = px.scatter(
        data,
        x="Cumulative_cases",
        y="Cumulative_deaths",
        size="Cumulative_cases",
        color="WHO_region",
        hover_name="Country",
        size_max=50,
        log_x=True,
        log_y=True,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(
        paper_bgcolor=COLORS["card"],
        plot_bgcolor=COLORS["card"],
        xaxis=dict(showgrid=True, gridcolor=COLORS["border"], color=COLORS["muted"], title="Cas (log)"),
        yaxis=dict(showgrid=True, gridcolor=COLORS["border"], color=COLORS["muted"], title="Décès (log)"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=COLORS["text"]), title=""),
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(color=COLORS["text"]),
    )
    return fig


# ─── Lancement ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(debug=True, port=8050)
