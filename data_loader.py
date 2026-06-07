
import os
import requests
import pandas as pd
import numpy as np

# URL officiel OMS
WHO_URL = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
LOCAL_CACHE = "data/WHO-COVID-19-global-data.csv"

# Correspondance code ISO 2 lettres → 3 lettres pour la carte choroplèthe
ISO2_TO_ISO3 = {
    "AF": "AFG", "AL": "ALB", "DZ": "DZA", 
    "AD": "AND", "AO": "AGO",
    "AG": "ATG", "AR": "ARG", "AM": "ARM", 
    "AU": "AUS", "AT": "AUT",
    "AZ": "AZE", "BS": "BHS", "BH": "BHR", "BD": "BGD", "BB": "BRB",
    "BY": "BLR", "BE": "BEL", "BZ": "BLZ", "BJ": "BEN", "BT": "BTN",
    "BO": "BOL", "BA": "BIH", "BW": "BWA", "BR": "BRA", "BN": "BRN",
    "BG": "BGR", "BF": "BFA", "BI": "BDI",
      "CV": "CPV", "KH": "KHM",
    "CM": "CMR", "CA": "CAN", "CF": "CAF",
      "TD": "TCD", "CL": "CHL",
    "CN": "CHN", "CO": "COL", "KM": "COM", 
    "CG": "COG", "CD": "COD",
    "CR": "CRI", "CI": "CIV", "HR": "HRV", "CU": "CUB", "CY": "CYP",
    "CZ": "CZE", "DK": "DNK", "DJ": "DJI", "DM": "DMA", "DO": "DOM",
    "EC": "ECU", "EG": "EGY", "SV": "SLV", "GQ": "GNQ", "ER": "ERI",
    "EE": "EST", "SZ": "SWZ", "ET": "ETH", "FJ": "FJI", "FI": "FIN",
    "FR": "FRA", "GA": "GAB", "GM": "GMB", "GE": "GEO", "DE": "DEU",
    "GH": "GHA", "GR": "GRC", "GD": "GRD",
      "GT": "GTM", "GN": "GIN",
    "GW": "GNB", "GY": "GUY", "HT": "HTI",
      "HN": "HND", "HU": "HUN",
    "IS": "ISL", "IN": "IND", "ID": "IDN",
      "IR": "IRN", "IQ": "IRQ",
    "IE": "IRL", "IL": "ISR", 
    "IT": "ITA", "JM": "JAM", "JP": "JPN",
    "JO": "JOR", "KZ": "KAZ",
     
      "KE": "KEN", "KI": "KIR", "KP": "PRK",
    "KR": "KOR", "KW": "KWT",
      "KG": "KGZ", "LA": "LAO", "LV": "LVA",
    "LB": "LBN", "LS": "LSO",
      "LR": "LBR", "LY": "LBY", "LI": "LIE",
    "LT": "LTU", "LU": "LUX",
      "MG": "MDG", "MW": "MWI", "MY": "MYS",
    "MV": "MDV", "ML": "MLI", "MT": "MLT", "MH": "MHL",
      "MR": "MRT",
    "MU": "MUS", "MX": "MEX", "FM": "FSM", "MD": "MDA",
      "MC": "MCO",
    "MN": "MNG", "ME": "MNE", "MA": "MAR", 
    "MZ": "MOZ", "MM": "MMR",
    "NA": "NAM", "NR": "NRU", "NP": "NPL",
      "NL": "NLD", "NZ": "NZL",
    "NI": "NIC", "NE": "NER",
      "NG": "NGA", "NO": "NOR", "OM": "OMN",
    "PK": "PAK", "PW": "PLW", 
    "PA": "PAN", "PG": "PNG", 
    "PY": "PRY",
    "PE": "PER", "PH": "PHL", 
    "PL": "POL", "PT": "PRT", "QA": "QAT",
    "RO": "ROU", "RU": "RUS", "RW": "RWA", "KN": "KNA", "LC": "LCA",
    "VC": "VCT", "WS": "WSM", "SM": "SMR", "ST": "STP", "SA": "SAU",
    "SN": "SEN", "RS": "SRB", "SC": "SYC", "SL": "SLE", "SG": "SGP",
    "SK": "SVK", "SI": "SVN", 
    "SB": "SLB", "SO": "SOM", "ZA": "ZAF",
    "SS": "SSD", "ES": "ESP", 
    "LK": "LKA", "SD": "SDN", "SR": "SUR",
    "SE": "SWE", "CH": "CHE", "SY": "SYR", "TW": "TWN", "TJ": "TJK",
    "TZ": "TZA", "TH": "THA", 
    "TL": "TLS", "TG": "TGO", "TO": "TON",
    "TT": "TTO", "TN": "TUN", "TR": "TUR", "TM": "TKM", "TV": "TUV",
    "UG": "UGA", "UA": "UKR", "AE": "ARE", "GB": "GBR", "US": "USA",
    "UY": "URY", "UZ": "UZB", "VU": "VUT", "VE": "VEN", "VN": "VNM",
    "YE": "YEM", "ZM": "ZMB", 
    "ZW": "ZWE", "XK": "XKX", "PS": "PSE",
    "CX": "CXR", "PM": "SPM", 
    "TC": "TCA",
}


def download_data():
    """Télécharger le CSV OMS si absent ou trop vieux (plus de 24h)."""
    os.makedirs("data", exist_ok=True)

    # Utiliser le cache local si dispoible
    if os.path.exists(LOCAL_CACHE):
        age_hours = (pd.Timestamp.now() - pd.Timestamp(os.path.getmtime(LOCAL_CACHE), unit="s")).total_seconds() / 3600
        if age_hours < 24:
            print(f" Cache local utilisé ({age_hours:.1f}h)")
            return LOCAL_CACHE

    print(" Téléchargement des données OMS...")
    try:
        r = requests.get(WHO_URL, timeout=30)
        r.raise_for_status()
        with open(LOCAL_CACHE, "wb") as f:
            f.write(r.content)
        print(" Données téléchargées avec succès.")
        return LOCAL_CACHE
    except Exception as e:
        print(f"Erreur téléchargement : {e}")
        return None


def generate_demo_data():
    """
    Génère des données de démonstration réalistes si le téléchargement échoue.
    Utile pour travailler hors ligne.
    """
    print("[data_loader] Génération de données de démonstration...")

    np.random.seed(42)
    countries_info = [
        ("United States of America", "US", "AMRO"), ("India", "IN", "SEARO"),
        ("France", "FR", "EURO"), ("Germany", "DE", "EURO"),
        ("Brazil", "BR", "AMRO"), ("United Kingdom", "GB", "EURO"),
        ("Russia", "RU", "EURO"), ("Turkey", "TR", "EURO"),
        ("Italy", "IT", "EURO"), ("Spain", "ES", "EURO"),
        ("Argentina", "AR", "AMRO"), ("Colombia", "CO", "AMRO"),
        ("Mexico", "MX", "AMRO"), ("Iran", "IR", "EMRO"),
        ("Poland", "PL", "EURO"), ("South Africa", "ZA", "AFRO"),
        ("Indonesia", "ID", "SEARO"), ("Ukraine", "UA", "EURO"),
        ("Netherlands", "NL", "EURO"), ("Czechia", "CZ", "EURO"),
        ("Canada", "CA", "AMRO"), ("Chile", "CL", "AMRO"),
        ("Romania", "RO", "EURO"), ("Belgium", "BE", "EURO"),
        ("Peru", "PE", "AMRO"), ("Portugal", "PT", "EURO"),
        ("Japan", "JP", "WPRO"), ("Australia", "AU", "WPRO"),
        ("China", "CN", "WPRO"), ("South Korea", "KR", "WPRO"),
    ]

    dates = pd.date_range("2020-01-01", "2023-12-31", freq="D")
    records = []

    for country, code, region in countries_info:
        base = np.random.randint(10_000, 5_000_000)
        for i, date in enumerate(dates):
            t = i / len(dates)
            wave = (np.sin(t * 12) + 1.5) * np.random.uniform(0.5, 2.0)
            new_c = max(0, int(base * wave * np.random.uniform(0.8, 1.2) / 500))
            new_d = max(0, int(new_c * np.random.uniform(0.005, 0.03)))
            records.append({
                "Date_reported": date,
                "Country_code": code,
                "Country": country,
                "WHO_region": region,
                "New_cases": new_c,
                "Cumulative_cases": 0,
                "New_deaths": new_d,
                "Cumulative_deaths": 0,
            })

    df = pd.DataFrame(records)
    df = df.sort_values(["Country", "Date_reported"])
    df["Cumulative_cases"] = df.groupby("Country")["New_cases"].cumsum()
    df["Cumulative_deaths"] = df.groupby("Country")["New_deaths"].cumsum()
    return df


def load_who_data():
    
    path = download_data()

    if path and os.path.exists(path):
        try:
            df = pd.read_csv(path, parse_dates=["Date_reported"])
        except Exception as e:
            print(f"[data_loader] Erreur lecture CSV : {e}")
            df = generate_demo_data()
    else:
        df = generate_demo_data()

    # Nettoyage
    df.columns = df.columns.str.strip()

    # Noms de colonnes flexibles (la colonne OMS peut changer)
    rename_map = {}
    for col in df.columns:
        col_clean = col.strip().lower().replace(" ", "_")
        if "date" in col_clean:
            rename_map[col] = "Date_reported"
        elif "country_code" in col_clean:
            rename_map[col] = "Country_code"
        elif "country" in col_clean and "code" not in col_clean:
            rename_map[col] = "Country"
        elif "who_region" in col_clean or "region" in col_clean:
            rename_map[col] = "WHO_region"
        elif "new_cases" in col_clean:
            rename_map[col] = "New_cases"
        elif "cumulative_cases" in col_clean:
            rename_map[col] = "Cumulative_cases"
        elif "new_deaths" in col_clean:
            rename_map[col] = "New_deaths"
        elif "cumulative_deaths" in col_clean:
            rename_map[col] = "Cumulative_deaths"
    df = df.rename(columns=rename_map)

    # Valeurs numériques
    for col in ["New_cases", "Cumulative_cases", "New_deaths", "Cumulative_deaths"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).clip(lower=0)

    # Code ISO 3 lettres pour la carte
    df["iso_alpha"] = df["Country_code"].map(ISO2_TO_ISO3)

    # Suppression des lignes sans pays valide
    df = df.dropna(subset=["Country"])

    # dernière date
    df_latest = df.sort_values("Date_reported").groupby("Country", as_index=False).last()

    print(f"[data_loader] ✅ {len(df):,} lignes | {df['Country'].nunique()} pays | jusqu'au {df['Date_reported'].max().date()}")
    return df, df_latest
