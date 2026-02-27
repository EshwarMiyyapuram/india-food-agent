"""
app.py  —  Streamlit Dashboard (Premium Redesign)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run with:  streamlit run app.py
"""

import streamlit as st
import json
import sys
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

# ── City Landmarks Data ──────────────────
CITY_LANDMARKS = {
    "Hyderabad": [
        {"name": "Charminar", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Charminar_Hyderabad_2015.jpg/480px-Charminar_Hyderabad_2015.jpg", "emoji": "🕌"},
        {"name": "Golconda Fort", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Golconda_fort_Hyderabad.jpg/480px-Golconda_fort_Hyderabad.jpg", "emoji": "🏯"},
        {"name": "Hussain Sagar", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Hussain_Sagar_Lake.jpg/480px-Hussain_Sagar_Lake.jpg", "emoji": "🏊"},
    ],
    "Chennai": [
        {"name": "Chepauk Stadium", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/MA_Chidambaram_Stadium.jpg/480px-MA_Chidambaram_Stadium.jpg", "emoji": "🏏"},
        {"name": "Marina Beach", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Chennai_Marina_beach.jpg/480px-Chennai_Marina_beach.jpg", "emoji": "🏖️"},
        {"name": "Kapaleeshwarar Temple", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Kapaleeswarar_temple_Chennai.jpg/480px-Kapaleeswarar_temple_Chennai.jpg", "emoji": "🛕"},
    ],
    "Mumbai": [
        {"name": "Gateway of India", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Mumbai_03-2016_30_Gateway_of_India.jpg/480px-Mumbai_03-2016_30_Gateway_of_India.jpg", "emoji": "🏛️"},
        {"name": "Marine Drive", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Marine_Drive_Mumbai.jpg/480px-Marine_Drive_Mumbai.jpg", "emoji": "🌊"},
        {"name": "Elephanta Caves", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Elephanta_Caves_3.jpg/480px-Elephanta_Caves_3.jpg", "emoji": "🗿"},
    ],
    "Delhi": [
        {"name": "Red Fort", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Delhi_collage.jpg/480px-Delhi_collage.jpg", "emoji": "🏰"},
        {"name": "Qutub Minar", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Qutab_Minar_mausoleum.jpg/480px-Qutab_Minar_mausoleum.jpg", "emoji": "🗼"},
        {"name": "India Gate", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/India_gate.jpg/480px-India_gate.jpg", "emoji": "🏛️"},
    ],
    "Bengaluru": [
        {"name": "Lalbagh Garden", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Lalbagh_Glass_House.jpg/480px-Lalbagh_Glass_House.jpg", "emoji": "🌿"},
        {"name": "Bangalore Palace", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Bangalore_Palace.jpg/480px-Bangalore_Palace.jpg", "emoji": "🏰"},
        {"name": "Cubbon Park", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Cubbon_Park_Bangalore.jpg/480px-Cubbon_Park_Bangalore.jpg", "emoji": "🌳"},
    ],
    "Kolkata": [
        {"name": "Victoria Memorial", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Victoria_Memorial%2C_Kolkata.jpg/480px-Victoria_Memorial%2C_Kolkata.jpg", "emoji": "🏛️"},
        {"name": "Howrah Bridge", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/00/Howrah_Bridge_View.jpg/480px-Howrah_Bridge_View.jpg", "emoji": "🌉"},
        {"name": "Dakshineswar Temple", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Dakshineswar_Kali_Temple.jpg/480px-Dakshineswar_Kali_Temple.jpg", "emoji": "🛕"},
    ],
    "Lucknow": [
        {"name": "Bara Imambara", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Bara_Imambara.jpg/480px-Bara_Imambara.jpg", "emoji": "🕌"},
        {"name": "Rumi Darwaza", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Rumi_Darwaza_Lucknow.jpg/480px-Rumi_Darwaza_Lucknow.jpg", "emoji": "🚪"},
        {"name": "Hazratganj Market", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/74/Hazratganj.jpg/480px-Hazratganj.jpg", "emoji": "🛍️"},
    ],
    "Amritsar": [
        {"name": "Golden Temple", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Golden_Temple_Amritsar_2012.jpg/480px-Golden_Temple_Amritsar_2012.jpg", "emoji": "✨"},
        {"name": "Jallianwala Bagh", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Jallianwala_Bagh_2013.jpg/480px-Jallianwala_Bagh_2013.jpg", "emoji": "🌺"},
        {"name": "Wagah Border", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Wagah_Border.jpg/480px-Wagah_Border.jpg", "emoji": "🚩"},
    ],
    "Goa": [
        {"name": "Basilica of Bom Jesus", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/BasilicaOfBomJesus.jpg/480px-BasilicaOfBomJesus.jpg", "emoji": "⛪"},
        {"name": "Calangute Beach", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Baga_Beach.jpg/480px-Baga_Beach.jpg", "emoji": "🏖️"},
        {"name": "Dudhsagar Falls", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Dudhsagar_Falls.jpg/480px-Dudhsagar_Falls.jpg", "emoji": "💧"},
    ],
    "Jaipur": [
        {"name": "Hawa Mahal", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Hawa_Mahal_-_Jaipur2.jpg/480px-Hawa_Mahal_-_Jaipur2.jpg", "emoji": "🏯"},
        {"name": "Amber Fort", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Amer_Fort_Jaipur_Rajasthan_India.jpg/480px-Amer_Fort_Jaipur_Rajasthan_India.jpg", "emoji": "🏰"},
        {"name": "City Palace", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/City_Palace_Jaipur_2012.jpg/480px-City_Palace_Jaipur_2012.jpg", "emoji": "👑"},
    ],
    "Kochi": [
        {"name": "Chinese Fishing Nets", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d2/Chinese_fishing_nets_Cochin.jpg/480px-Chinese_fishing_nets_Cochin.jpg", "emoji": "🎣"},
        {"name": "Fort Kochi Beach", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Fort_Kochi_Beach.jpg/480px-Fort_Kochi_Beach.jpg", "emoji": "🏖️"},
        {"name": "Mattancherry Palace", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/Mattancherry_Palace_Dutch_Palace_Kochi_Kerala_India.jpg/480px-Mattancherry_Palace_Dutch_Palace_Kochi_Kerala_India.jpg", "emoji": "🏛️"},
    ],
    "Indore": [
        {"name": "Rajwada Palace", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Rajwada%2C_Indore.jpg/480px-Rajwada%2C_Indore.jpg", "emoji": "🏰"},
        {"name": "Lal Bagh Palace", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Lal_Bagh_Palace_Indore.jpg/480px-Lal_Bagh_Palace_Indore.jpg", "emoji": "🌹"},
        {"name": "Sarafa Bazaar", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Sarafa_Bazaar_Indore.jpg/480px-Sarafa_Bazaar_Indore.jpg", "emoji": "🌙"},
    ],
    "Pune": [
        {"name": "Shaniwar Wada", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4d/Shaniwar_wada_pune.JPG/480px-Shaniwar_wada_pune.JPG", "emoji": "🏯"},
        {"name": "Aga Khan Palace", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Aga_Khan_Palace_-_Pune.jpg/480px-Aga_Khan_Palace_-_Pune.jpg", "emoji": "🕌"},
        {"name": "Sinhagad Fort", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Sinhagad_fort_Pune.jpg/480px-Sinhagad_fort_Pune.jpg", "emoji": "⛰️"},
    ],
    "Ahmedabad": [
        {"name": "Sabarmati Ashram", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Sabarmati_Ashram.jpg/480px-Sabarmati_Ashram.jpg", "emoji": "🕊️"},
        {"name": "Akshardham Temple", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Swaminarayan_Akshardham_Mandir%2C_Gandhinagar.jpg/480px-Swaminarayan_Akshardham_Mandir%2C_Gandhinagar.jpg", "emoji": "🛕"},
        {"name": "Kankaria Lake", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Kankaria_Lake.jpg/480px-Kankaria_Lake.jpg", "emoji": "🌅"},
    ],
    "Chandigarh": [
        {"name": "Rock Garden", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/06/Rock_Garden_of_Chandigarh.jpg/480px-Rock_Garden_of_Chandigarh.jpg", "emoji": "🪨"},
        {"name": "Sukhna Lake", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Sukhna_Lake_Chandigarh.jpg/480px-Sukhna_Lake_Chandigarh.jpg", "emoji": "🌊"},
        {"name": "Rose Garden", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ea/Rose_garden_chandigarh.jpg/480px-Rose_garden_chandigarh.jpg", "emoji": "🌹"},
    ],
    "Varanasi": [
        {"name": "Dashashwamedh Ghat", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Dashashwamedh_ghat%2C_Varanasi.jpg/480px-Dashashwamedh_ghat%2C_Varanasi.jpg", "emoji": "🪔"},
        {"name": "Kashi Vishwanath Temple", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Kashi_vishwanath.jpg/480px-Kashi_vishwanath.jpg", "emoji": "🛕"},
        {"name": "Sarnath", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/Sarnath_Mulagandhakuti_Vihar.jpg/480px-Sarnath_Mulagandhakuti_Vihar.jpg", "emoji": "☸️"},
    ],
    "Agra": [
        {"name": "Taj Mahal", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/67/Taj_Mahal_in_India_-_Uwe_Aranas.jpg/480px-Taj_Mahal_in_India_-_Uwe_Aranas.jpg", "emoji": "🕌"},
        {"name": "Agra Fort", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Agra_Fort%2C_India.jpg/480px-Agra_Fort%2C_India.jpg", "emoji": "🏰"},
        {"name": "Fatehpur Sikri", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/39/Fatehpur_Sikri_Buland_Darwaza_2010.jpg/480px-Fatehpur_Sikri_Buland_Darwaza_2010.jpg", "emoji": "🏛️"},
    ],
    "Vizag": [
        {"name": "RK Beach", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/Ramakrishna_Beach_Visakhapatnam.jpg/480px-Ramakrishna_Beach_Visakhapatnam.jpg", "emoji": "🏖️"},
        {"name": "Kailasagiri", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Kailasagiri_Park_Vizag.jpg/480px-Kailasagiri_Park_Vizag.jpg", "emoji": "⛰️"},
        {"name": "Submarine Museum", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/INS_Kurusura_Submarine_Museum.jpg/480px-INS_Kurusura_Submarine_Museum.jpg", "emoji": "🚢"},
    ],
    "Madurai": [
        {"name": "Meenakshi Temple", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d5/Madurai_Meenakshi_Amman_Temple.jpg/480px-Madurai_Meenakshi_Amman_Temple.jpg", "emoji": "🛕"},
        {"name": "Thirumalai Nayakkar Palace", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Thirumalai_Nayakkar_Palace.jpg/480px-Thirumalai_Nayakkar_Palace.jpg", "emoji": "🏰"},
        {"name": "Gandhi Museum", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Gandhi_Museum_Madurai.jpg/480px-Gandhi_Museum_Madurai.jpg", "emoji": "🕊️"},
    ],
    "Bhopal": [
        {"name": "Upper Lake", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Upper_Lake_Bhopal.jpg/480px-Upper_Lake_Bhopal.jpg", "emoji": "🌊"},
        {"name": "Bhimbetka Caves", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Bhimbetka_rock_paintings.jpg/480px-Bhimbetka_rock_paintings.jpg", "emoji": "🗿"},
        {"name": "Taj-ul-Masajid", "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Taj_ul_Masajid_Bhopal.jpg/480px-Taj_ul_Masajid_Bhopal.jpg", "emoji": "🕌"},
    ],
}

# ── Page Config ──────────────────────────
st.set_page_config(
    page_title="भारत FoodTrend Agent",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Premium CSS ────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

:root {
    --ink:       #0D0A08;
    --paper:     #F5EFE6;
    --cream:     #FDF9F4;
    --spice:     #C4411A;
    --spice-lt:  #E8572A;
    --gold:      #D4A017;
    --gold-lt:   #F0C040;
    --green:     #1A6B3A;
    --green-lt:  #22A05A;
    --purple:    #5B2D8E;
    --purple-lt: #8B5CF6;
    --border:    rgba(196,65,26,0.15);
    --muted:     #7A6F65;
    --card-bg:   #FFFCF8;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background: var(--paper) !important;
}
.main .block-container { padding: 1.5rem 2rem 3rem; max-width: 1400px; }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--paper); }
::-webkit-scrollbar-thumb { background: var(--spice); border-radius: 3px; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: var(--ink) !important;
    border-right: 1px solid rgba(196,65,26,0.3);
}
section[data-testid="stSidebar"] * { color: #E8DDD4 !important; }
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stCaption { color: #A89F97 !important; }
section[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(196,65,26,0.4) !important;
    border-radius: 8px !important;
    color: #F5EFE6 !important;
}
.sidebar-logo { padding: 24px 0 8px; border-bottom: 1px solid rgba(196,65,26,0.3); margin-bottom: 20px; }
.sidebar-logo-text { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 900; color: #F5EFE6; letter-spacing: -0.5px; line-height: 1.2; }
.sidebar-logo-text em { color: var(--spice-lt); font-style: italic; }
.sidebar-logo-sub { font-size: 9px; font-weight: 600; letter-spacing: 0.25em; text-transform: uppercase; color: #7A6F65; margin-top: 6px; }
.sidebar-section-label { font-size: 9px; font-weight: 600; letter-spacing: 0.2em; text-transform: uppercase; color: var(--spice-lt) !important; margin: 18px 0 6px; }

section[data-testid="stSidebar"] .stButton > button {
    border-radius: 8px !important; font-weight: 600 !important; font-size: 13px !important;
    letter-spacing: 0.03em !important; transition: all 0.2s !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(196,65,26,0.5) !important; color: #E8DDD4 !important;
}
section[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--spice) 0%, #E8572A 100%) !important;
    border: none !important; color: white !important;
    box-shadow: 0 4px 20px rgba(196,65,26,0.4) !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    transform: translateY(-1px) !important; box-shadow: 0 6px 24px rgba(196,65,26,0.5) !important;
}

/* ── HERO ── */
.hero {
    background: var(--ink); border-radius: 20px; padding: 36px 40px;
    margin-bottom: 28px; display: flex; align-items: center;
    justify-content: space-between; overflow: hidden; position: relative;
}
.hero::before {
    content: ''; position: absolute; top: -60px; right: -60px;
    width: 300px; height: 300px; border-radius: 50%;
    background: radial-gradient(circle, rgba(196,65,26,0.25) 0%, transparent 70%);
}
.hero::after {
    content: ''; position: absolute; bottom: -80px; left: 30%;
    width: 250px; height: 250px; border-radius: 50%;
    background: radial-gradient(circle, rgba(212,160,23,0.12) 0%, transparent 70%);
}
.hero-eyebrow { font-size: 10px; font-weight: 600; letter-spacing: 0.3em; text-transform: uppercase; color: var(--spice-lt); margin-bottom: 10px; }
.hero-title { font-family: 'Playfair Display', serif; font-size: 42px; font-weight: 900; color: #F5EFE6; line-height: 1.05; margin: 0 0 12px; }
.hero-title em { color: var(--gold-lt); font-style: italic; }
.hero-tagline { font-size: 13px; color: rgba(245,239,230,0.5); font-weight: 300; letter-spacing: 0.05em; }
.hero-stats { display: flex; gap: 32px; position: relative; z-index: 1; }
.hero-stat-item { text-align: center; }
.hero-stat-num { font-family: 'DM Mono', monospace; font-size: 28px; font-weight: 500; color: var(--gold-lt); line-height: 1; }
.hero-stat-lbl { font-size: 10px; color: rgba(245,239,230,0.4); text-transform: uppercase; letter-spacing: 0.12em; margin-top: 4px; font-weight: 500; }
.hero-divider { width: 1px; height: 50px; background: rgba(255,255,255,0.1); align-self: center; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] { gap: 0; border-bottom: 2px solid var(--border); background: transparent; }
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important; font-size: 12px !important;
    font-weight: 600 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important;
    color: var(--muted) !important; padding: 12px 24px !important;
    border-bottom: 2px solid transparent !important; margin-bottom: -2px !important; background: transparent !important;
}
.stTabs [aria-selected="true"] { color: var(--spice) !important; border-bottom-color: var(--spice) !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 24px !important; }

/* ── STATUS BANNERS ── */
.status-success {
    background: linear-gradient(135deg, #0F2818 0%, #143521 100%);
    border: 1px solid rgba(26,107,58,0.5); border-left: 4px solid var(--green-lt);
    border-radius: 12px; padding: 14px 20px; margin: 16px 0;
    display: flex; align-items: center; gap: 12px;
    font-size: 13px; color: #A7F3C8; font-weight: 500;
}
.status-info {
    background: linear-gradient(135deg, #0D1A2E 0%, #112040 100%);
    border: 1px solid rgba(59,130,246,0.3); border-left: 4px solid #60A5FA;
    border-radius: 12px; padding: 14px 20px; margin: 16px 0;
    font-size: 13px; color: #93C5FD;
}

/* ── SECTION HEADERS ── */
.sec-head { display: flex; align-items: center; gap: 14px; margin: 28px 0 16px; }
.sec-head-line { flex: 1; height: 1px; background: var(--border); }
.sec-head-text { font-size: 10px; font-weight: 700; letter-spacing: 0.22em; text-transform: uppercase; color: var(--spice); white-space: nowrap; }

/* ── KPI CARDS ── */
.kpi-card {
    background: var(--card-bg); border: 1px solid var(--border);
    border-radius: 16px; padding: 20px 22px; position: relative;
    overflow: hidden; transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: 0 8px 30px rgba(196,65,26,0.1); }
.kpi-card::after { content: attr(data-icon); position: absolute; right: 16px; top: 14px; font-size: 28px; opacity: 0.12; }
.kpi-label { font-size: 10px; font-weight: 600; letter-spacing: 0.18em; text-transform: uppercase; color: var(--muted); margin-bottom: 8px; }
.kpi-value { font-family: 'Playfair Display', serif; font-size: 32px; font-weight: 700; color: var(--ink); line-height: 1; margin-bottom: 6px; }
.kpi-delta { font-size: 11px; font-weight: 600; color: var(--green-lt); }
.kpi-accent { position: absolute; bottom: 0; left: 0; right: 0; height: 3px; }
.kpi-accent.spice  { background: linear-gradient(90deg, var(--spice), var(--spice-lt)); }
.kpi-accent.gold   { background: linear-gradient(90deg, var(--gold), var(--gold-lt)); }
.kpi-accent.green  { background: linear-gradient(90deg, var(--green), var(--green-lt)); }
.kpi-accent.purple { background: linear-gradient(90deg, var(--purple), var(--purple-lt)); }

/* ── ANALYSIS CALLOUT ── */
.analysis-callout {
    background: var(--ink); border-radius: 16px; padding: 24px 28px;
    margin-bottom: 28px; position: relative; overflow: hidden;
}
.analysis-callout::before {
    content: '"'; position: absolute; font-family: 'Playfair Display', serif;
    font-size: 160px; color: rgba(196,65,26,0.1); top: -20px; left: 20px; line-height: 1;
}
.analysis-eyebrow { font-size: 9px; letter-spacing: 0.25em; text-transform: uppercase; color: var(--spice-lt); font-weight: 600; margin-bottom: 10px; }
.analysis-text { font-family: 'Playfair Display', serif; font-size: 17px; font-style: italic; color: rgba(245,239,230,0.85); line-height: 1.8; position: relative; z-index: 1; }

/* ── SCRAPE PANELS ── */
.scrape-panel { background: var(--card-bg); border: 1px solid var(--border); border-radius: 16px; padding: 22px; height: 100%; }
.scrape-panel-title { font-size: 10px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; color: var(--muted); margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.scrape-panel-title span { flex: 1; height: 1px; background: var(--border); }

.google-result { border-left: 3px solid var(--spice); padding: 10px 14px; margin-bottom: 8px; border-radius: 0 8px 8px 0; background: rgba(196,65,26,0.04); transition: background 0.2s; }
.google-result:hover { background: rgba(196,65,26,0.08); }
.g-title { font-size: 13px; font-weight: 600; color: var(--ink); line-height: 1.4; }
.g-snippet { font-size: 11px; color: var(--muted); margin-top: 3px; line-height: 1.5; }

.zomato-item { display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 8px; margin-bottom: 6px; background: rgba(226,55,68,0.05); border: 1px solid rgba(226,55,68,0.1); transition: background 0.2s; }
.zomato-item:hover { background: rgba(226,55,68,0.1); }
.zomato-icon { font-size: 18px; }
.zomato-name { font-size: 13px; font-weight: 600; color: var(--ink); }
.zomato-type { font-size: 9px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #E23744; margin-top: 1px; }

.article-item { padding: 10px 14px; border-radius: 8px; margin-bottom: 7px; background: rgba(26,107,58,0.04); border-left: 3px solid var(--green-lt); }
.art-headline { font-size: 12px; font-weight: 600; color: var(--ink); line-height: 1.5; }
.art-source { font-size: 10px; color: var(--green); margin-top: 3px; font-weight: 500; }

/* ── HASHTAGS ── */
.htag { display: inline-block; padding: 5px 13px; border-radius: 20px; font-size: 11px; font-weight: 700; margin: 4px; font-family: 'DM Mono', monospace; transition: transform 0.15s; cursor: default; }
.htag:hover { transform: scale(1.05); }
.htag-viral  { background: #2D0A1A; color: #F472B6; border: 1px solid rgba(244,114,182,0.3); }
.htag-hot    { background: #2D1400; color: #FB923C; border: 1px solid rgba(251,146,60,0.3); }
.htag-rising { background: #0A1F12; color: #4ADE80; border: 1px solid rgba(74,222,128,0.3); }
.htag-new    { background: #0A1E2D; color: #38BDF8; border: 1px solid rgba(56,189,248,0.3); }

/* ── INGREDIENT PILLS ── */
.ing-pill {
    background: var(--card-bg); border: 1.5px solid var(--spice); border-radius: 14px;
    padding: 14px 16px; text-align: center; transition: all 0.2s;
}
.ing-pill:hover { background: rgba(196,65,26,0.05); transform: translateY(-2px); }
.ing-pill-icon { font-size: 22px; display: block; margin-bottom: 4px; }
.ing-rank { font-size: 9px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: var(--muted); }

/* ── DISH CARDS ── */
.dish-card {
    background: var(--card-bg); border-radius: 20px; border: 1px solid var(--border);
    margin-bottom: 20px; overflow: hidden; transition: transform 0.25s, box-shadow 0.25s;
}
.dish-card:hover { transform: translateY(-3px); box-shadow: 0 16px 50px rgba(0,0,0,0.12); }
.dish-card-header { padding: 22px 24px 18px; position: relative; }
.dish-card-header.margin    { background: linear-gradient(135deg, #071A0D 0%, #0F2818 100%); }
.dish-card-header.premium   { background: linear-gradient(135deg, #110825 0%, #1E1040 100%); }
.dish-card-header.insta     { background: linear-gradient(135deg, #1F0813 0%, #2D1020 100%); }
.dish-card-header.performer { background: linear-gradient(135deg, #1A0A02 0%, #2A1404 100%); }

.dish-header-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
.dish-badge { font-size: 9px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; padding: 4px 12px; border-radius: 20px; }
.badge-margin    { background: rgba(74,222,128,0.15);  color: #4ADE80;  border: 1px solid rgba(74,222,128,0.2); }
.badge-premium   { background: rgba(167,139,250,0.15); color: #A78BFA;  border: 1px solid rgba(167,139,250,0.2); }
.badge-insta     { background: rgba(244,114,182,0.15); color: #F472B6;  border: 1px solid rgba(244,114,182,0.2); }
.badge-performer { background: rgba(251,146,60,0.15);  color: #FB923C;  border: 1px solid rgba(251,146,60,0.2); }

.dish-price-badge { font-family: 'DM Mono', monospace; font-size: 15px; font-weight: 500; color: var(--gold-lt); text-align: right; }
.demand-dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%; margin-right: 5px; vertical-align: middle; }
.demand-label { font-size: 10px; font-weight: 600; letter-spacing: 0.05em; vertical-align: middle; }
.demand-high-wrap   .demand-dot { background: #4ADE80; box-shadow: 0 0 6px #4ADE80; }
.demand-medium-wrap .demand-dot { background: #FB923C; box-shadow: 0 0 6px #FB923C; }
.demand-low-wrap    .demand-dot { background: #94A3B8; }
.demand-high-wrap   .demand-label { color: #4ADE80; }
.demand-medium-wrap .demand-label { color: #FB923C; }
.demand-low-wrap    .demand-label { color: #94A3B8; }

.dish-name { font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 700; color: #F5EFE6; line-height: 1.2; margin-bottom: 6px; }
.dish-key-ing { font-size: 11px; font-weight: 500; color: rgba(245,239,230,0.45); font-style: italic; }
.dish-card-body { padding: 20px 24px; }
.dish-desc { font-size: 13px; color: #57534E; line-height: 1.8; margin-bottom: 18px; }
.dish-meta-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 12px; }
.dish-meta-item { background: rgba(196,65,26,0.04); border-radius: 10px; padding: 10px 14px; border: 1px solid var(--border); }
.dmi-label { font-size: 9px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: var(--muted); margin-bottom: 4px; }
.dmi-value { font-size: 13px; font-weight: 600; color: var(--ink); }
.dmi-value.green { color: var(--green-lt); }
.dmi-value.spice { color: var(--spice-lt); }
.dish-inspired { display: flex; align-items: center; gap: 8px; font-size: 11px; color: var(--muted); padding: 8px 14px; border-radius: 8px; background: rgba(196,65,26,0.04); border: 1px solid var(--border); }
.dish-inspired strong { color: var(--ink); font-weight: 600; }

/* ── TIPS ── */
.tip-block { background: var(--card-bg); border-radius: 12px; padding: 14px 18px; margin: 8px 0; border-left: 3px solid; }
.tip-block.plating { border-color: var(--gold); }
.tip-block.reels   { border-color: #F472B6; }
.tip-block.trend   { border-color: var(--green-lt); }
.tip-label { font-size: 9px; font-weight: 700; letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 6px; }
.tip-block.plating .tip-label { color: var(--gold); }
.tip-block.reels   .tip-label { color: #F472B6; }
.tip-block.trend   .tip-label { color: var(--green-lt); }
.tip-text { font-size: 13px; color: var(--ink); line-height: 1.7; }

/* ── INSIGHT BOX ── */
.insight-box { background: var(--ink); border-radius: 20px; padding: 32px 36px; margin-top: 28px; position: relative; overflow: hidden; }
.insight-box::before { content: '💡'; position: absolute; font-size: 120px; right: -10px; top: -20px; opacity: 0.04; filter: grayscale(1); }
.insight-eyebrow { font-size: 9px; font-weight: 700; letter-spacing: 0.25em; text-transform: uppercase; color: var(--gold-lt); margin-bottom: 14px; }
.insight-city { font-family: 'Playfair Display', serif; font-size: 26px; font-style: italic; color: #F5EFE6; margin-bottom: 14px; }
.insight-text { font-size: 15px; color: rgba(245,239,230,0.7); line-height: 1.9; margin-bottom: 20px; }
.insight-revenue { display: inline-flex; align-items: center; gap: 10px; background: rgba(212,160,23,0.12); border: 1px solid rgba(212,160,23,0.25); border-radius: 100px; padding: 8px 18px; font-size: 12px; color: var(--gold-lt); font-weight: 600; }

/* ── REPORT ── */
.report-header { background: var(--card-bg); border: 1px solid var(--border); border-radius: 16px; padding: 24px 28px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; }
.report-title { font-family: 'Playfair Display', serif; font-size: 28px; font-weight: 700; color: var(--ink); margin-bottom: 4px; }
.report-subtitle { font-size: 12px; color: var(--muted); }
/* ── LANDMARK GALLERY ── */
.landmark-gallery { display: flex; gap: 14px; margin: 20px 0 28px; flex-wrap: wrap; }
.landmark-card {
    flex: 1; min-width: 180px; max-width: 260px; border-radius: 16px;
    overflow: hidden; border: 1px solid var(--border);
    box-shadow: 0 4px 18px rgba(0,0,0,0.08);
    transition: transform 0.25s, box-shadow 0.25s;
    background: var(--card-bg);
}
.landmark-card:hover { transform: translateY(-4px); box-shadow: 0 12px 36px rgba(196,65,26,0.15); }
.landmark-card img { width: 100%; height: 150px; object-fit: cover; display: block; }
.landmark-label {
    padding: 10px 14px; font-size: 12px; font-weight: 700;
    color: var(--ink); background: var(--card-bg);
    display: flex; align-items: center; gap: 6px;
}
.landmark-label span { font-size: 16px; }
.landmark-header { display: flex; align-items: center; gap: 14px; margin: 24px 0 8px; }
.landmark-header-text { font-family: 'Playfair Display', serif; font-size: 15px; font-weight: 700; color: var(--ink); white-space: nowrap; }
.landmark-header-line { flex: 1; height: 1px; background: var(--border); }
.landmark-city-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: linear-gradient(135deg, var(--spice), var(--spice-lt));
    color: white; font-size: 10px; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; padding: 4px 14px; border-radius: 20px;
}

.report-body { background: var(--card-bg); border: 1px solid var(--border); border-radius: 16px; padding: 32px 36px; font-size: 14px; color: #3C3530; line-height: 1.9; }

/* ── EMPTY STATES ── */
.empty-state { text-align: center; padding: 60px 20px; background: var(--card-bg); border: 2px dashed var(--border); border-radius: 20px; }
.empty-icon { font-size: 48px; margin-bottom: 16px; opacity: 0.5; }
.empty-title { font-family: 'Playfair Display', serif; font-size: 22px; color: var(--ink); margin-bottom: 8px; }
.empty-sub { font-size: 13px; color: var(--muted); }

/* ── STREAMLIT OVERRIDES ── */
.stDataFrame { border-radius: 12px !important; overflow: hidden; }
div[data-testid="stExpander"] { border: 1px solid var(--border) !important; border-radius: 12px !important; background: var(--card-bg) !important; }
div[data-testid="stExpander"] summary { font-size: 12px !important; font-weight: 600 !important; }
.stDownloadButton > button {
    background: linear-gradient(135deg, var(--ink) 0%, #2A1F18 100%) !important;
    color: var(--gold-lt) !important; border: 1px solid rgba(212,160,23,0.3) !important;
    border-radius: 8px !important; font-weight: 600 !important; font-size: 12px !important; letter-spacing: 0.05em !important;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════
#  SESSION STATE
# ══════════════════════════════════════════
if "scraped"    not in st.session_state: st.session_state.scraped    = None
if "analysis"   not in st.session_state: st.session_state.analysis   = None
if "specials"   not in st.session_state: st.session_state.specials   = None
if "report_txt" not in st.session_state: st.session_state.report_txt = None


# ══════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-text">भारत<br><em>FoodTrend</em></div>
        <div class="sidebar-logo-sub">Intelligence Agent · v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">📍 Location</div>', unsafe_allow_html=True)
    city = st.selectbox("City", [
        "Hyderabad", "Chennai", "Mumbai", "Delhi", "Bengaluru",
        "Kolkata", "Lucknow", "Amritsar", "Goa", "Jaipur",
        "Kochi", "Indore", "Pune", "Ahmedabad", "Chandigarh",
        "Varanasi", "Agra", "Vizag", "Madurai", "Bhopal",
    ], label_visibility="collapsed")

    st.markdown('<div class="sidebar-section-label">🍽 Outlet Profile</div>', unsafe_allow_html=True)
    rtype = st.selectbox("Restaurant Type", [
        "Local Dhaba / Authentic", "Modern Café / Bistro", "Fine Dining",
        "Street Food Stall", "Cloud Kitchen / Delivery", "Family Restaurant",
        "Vegetarian / Pure Veg", "Seafood Specialty", "Biryani House", "Mughlai / Awadhi",
    ], label_visibility="collapsed")

    st.markdown('<div class="sidebar-section-label">💰 Pricing Tier</div>', unsafe_allow_html=True)
    price = st.selectbox("Price Range", [
        "₹ (under ₹200/head)", "₹₹ (₹200–600/head)",
        "₹₹₹ (₹600–1500/head)", "₹₹₹₹ (₹1500+/head)",
    ], index=2, label_visibility="collapsed")

    st.markdown('<div class="sidebar-section-label">🌦 Season</div>', unsafe_allow_html=True)
    season = st.selectbox("Season", [
        "Summer (Mar–Jun)", "Monsoon (Jul–Sep)",
        "Festive / Post-Monsoon (Oct–Nov)", "Winter (Dec–Feb)",
    ], index=1, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    scan_btn = st.button("📡 Scan Trends", use_container_width=True, type="secondary")
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    gen_btn  = st.button("✦ Generate Specials", use_container_width=True, type="primary")

    st.markdown("""
    <div style="margin-top:28px;padding-top:20px;border-top:1px solid rgba(196,65,26,0.2)">
        <div style="font-size:9px;letter-spacing:0.2em;text-transform:uppercase;color:#4A3F38;font-weight:600;margin-bottom:10px">Stack</div>
        <div style="font-size:11px;color:#7A6F65;line-height:2">Python · BeautifulSoup4<br>Anthropic Claude API<br>Streamlit · Plotly</div>
        <div style="font-size:9px;letter-spacing:0.2em;text-transform:uppercase;color:#4A3F38;font-weight:600;margin-top:14px;margin-bottom:10px">Sources</div>
        <div style="font-size:11px;color:#7A6F65;line-height:2">Google · Zomato<br>Times Food · NDTV Food<br>Instagram Hashtags</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════
#  HERO BANNER
# ══════════════════════════════════════════
scraped_pts = sum(len(v) for k,v in st.session_state.scraped.items() if isinstance(v,list)) if st.session_state.scraped else 0

st.markdown(f"""
<div class="hero">
  <div style="position:relative;z-index:1">
    <div class="hero-eyebrow">● Live Intelligence Dashboard</div>
    <div class="hero-title">भारत <em>FoodTrend</em><br>Agent</div>
    <div class="hero-tagline">Scraping · Analysing · Generating · Winning</div>
  </div>
  <div class="hero-stats" style="position:relative;z-index:1">
    <div class="hero-stat-item"><div class="hero-stat-num">20</div><div class="hero-stat-lbl">Cities</div></div>
    <div class="hero-divider"></div>
    <div class="hero-stat-item"><div class="hero-stat-num">4</div><div class="hero-stat-lbl">Sources</div></div>
    <div class="hero-divider"></div>
    <div class="hero-stat-item"><div class="hero-stat-num">{scraped_pts if scraped_pts else "—"}</div><div class="hero-stat-lbl">Data Points</div></div>
    <div class="hero-divider"></div>
    <div class="hero-stat-item"><div class="hero-stat-num">5</div><div class="hero-stat-lbl">AI Dishes</div></div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════
#  CITY LANDMARKS DATA
# ══════════════════════════════════════════
CITY_LANDMARKS = {
    "Hyderabad": {
        "color": "#7C3AED",
        "gradient": "linear-gradient(135deg,#2D1B69 0%,#1A0A3C 100%)",
        "accent": "#A78BFA",
        "places": [
            {"name": "Charminar", "emoji": "🕌", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Charminar_Hyderabad.jpg/320px-Charminar_Hyderabad.jpg"},
            {"name": "Golconda Fort", "emoji": "🏰", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4c/Golconda_fort_near_hyderabad.jpg/320px-Golconda_fort_near_hyderabad.jpg"},
            {"name": "Hussain Sagar", "emoji": "🌊", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Hussain_Sagar_Lake%2C_Hyderabad.jpg/320px-Hussain_Sagar_Lake%2C_Hyderabad.jpg"},
            {"name": "Ramoji Film City", "emoji": "🎬", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Ramoji_Film_City.jpg/320px-Ramoji_Film_City.jpg"},
        ],
        "tagline": "City of Nizams & Biryani",
        "food_icon": "🍛",
    },
    "Chennai": {
        "color": "#0891B2",
        "gradient": "linear-gradient(135deg,#0C4A6E 0%,#082F49 100%)",
        "accent": "#38BDF8",
        "places": [
            {"name": "Chepauk Stadium", "emoji": "🏏", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/MA_Chidambaram_Stadium.jpg/320px-MA_Chidambaram_Stadium.jpg"},
            {"name": "Marina Beach", "emoji": "🏖️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Marina_Beach_Chennai.jpg/320px-Marina_Beach_Chennai.jpg"},
            {"name": "Kapaleeshwarar Temple", "emoji": "🛕", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Kapaleeshwarar_temple.jpg/320px-Kapaleeshwarar_temple.jpg"},
            {"name": "Fort St. George", "emoji": "🏰", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Fort_St._George%2C_Chennai.jpg/320px-Fort_St._George%2C_Chennai.jpg"},
        ],
        "tagline": "Gateway of South India",
        "food_icon": "🍜",
    },
    "Mumbai": {
        "color": "#DC2626",
        "gradient": "linear-gradient(135deg,#7F1D1D 0%,#450A0A 100%)",
        "accent": "#FCA5A5",
        "places": [
            {"name": "Gateway of India", "emoji": "🏛️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Mumbai_03-2016_30_Gateway_of_India.jpg/320px-Mumbai_03-2016_30_Gateway_of_India.jpg"},
            {"name": "Marine Drive", "emoji": "🌃", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Marine_Drive_Mumbai.jpg/320px-Marine_Drive_Mumbai.jpg"},
            {"name": "Elephanta Caves", "emoji": "🗿", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Elephanta_Caves_entrance.jpg/320px-Elephanta_Caves_entrance.jpg"},
            {"name": "Chhatrapati Terminus", "emoji": "🚂", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Mumbai_CST_station_building.jpg/320px-Mumbai_CST_station_building.jpg"},
        ],
        "tagline": "City of Dreams & Street Food",
        "food_icon": "🥙",
    },
    "Delhi": {
        "color": "#D97706",
        "gradient": "linear-gradient(135deg,#78350F 0%,#451A03 100%)",
        "accent": "#FCD34D",
        "places": [
            {"name": "Red Fort", "emoji": "🏯", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/RedFort_Main_Gate.jpg/320px-RedFort_Main_Gate.jpg"},
            {"name": "India Gate", "emoji": "🏛️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5f/India_gate.jpg/320px-India_gate.jpg"},
            {"name": "Qutub Minar", "emoji": "🕌", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Qtub_Minar.JPG/320px-Qtub_Minar.JPG"},
            {"name": "Lotus Temple", "emoji": "🌸", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Delhi_Lotus_temple.jpg/320px-Delhi_Lotus_temple.jpg"},
        ],
        "tagline": "Heart of India & Mughlai Cuisine",
        "food_icon": "🍢",
    },
    "Bengaluru": {
        "color": "#059669",
        "gradient": "linear-gradient(135deg,#064E3B 0%,#022C22 100%)",
        "accent": "#6EE7B7",
        "places": [
            {"name": "Lalbagh Botanical Garden", "emoji": "🌿", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Lalbagh_Garden_Bangalore.jpg/320px-Lalbagh_Garden_Bangalore.jpg"},
            {"name": "Bangalore Palace", "emoji": "🏰", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/55/BangalorePalace.jpg/320px-BangalorePalace.jpg"},
            {"name": "Vidhana Soudha", "emoji": "🏛️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Vidhana_Soudha_Bangalore.jpg/320px-Vidhana_Soudha_Bangalore.jpg"},
            {"name": "ISKCON Temple", "emoji": "🛕", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/ISKCON_Bangalore.jpg/320px-ISKCON_Bangalore.jpg"},
        ],
        "tagline": "Silicon Valley & Filter Coffee Capital",
        "food_icon": "☕",
    },
    "Kolkata": {
        "color": "#BE185D",
        "gradient": "linear-gradient(135deg,#831843 0%,#500724 100%)",
        "accent": "#F9A8D4",
        "places": [
            {"name": "Victoria Memorial", "emoji": "🏛️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Victoria_Memorial_in_Kolkata.jpg/320px-Victoria_Memorial_in_Kolkata.jpg"},
            {"name": "Howrah Bridge", "emoji": "🌉", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Howrah_Bridge.jpg/320px-Howrah_Bridge.jpg"},
            {"name": "Dakshineswar Temple", "emoji": "🛕", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/DakshineswarTemple.jpg/320px-DakshineswarTemple.jpg"},
            {"name": "Park Street", "emoji": "🛍️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Park_Street_Kolkata.jpg/320px-Park_Street_Kolkata.jpg"},
        ],
        "tagline": "City of Joy & Rosogolla",
        "food_icon": "🍬",
    },
    "Lucknow": {
        "color": "#7C3AED",
        "gradient": "linear-gradient(135deg,#4C1D95 0%,#2E1065 100%)",
        "accent": "#C4B5FD",
        "places": [
            {"name": "Bara Imambara", "emoji": "🕌", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/Bara_Imambara.jpg/320px-Bara_Imambara.jpg"},
            {"name": "Chota Imambara", "emoji": "🏯", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ac/Chhota_Imambara.jpg/320px-Chhota_Imambara.jpg"},
            {"name": "Rumi Darwaza", "emoji": "🏛️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Rumi_Darwaza_Lucknow.jpg/320px-Rumi_Darwaza_Lucknow.jpg"},
            {"name": "Hazratganj", "emoji": "🛍️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Hazratganj_Lucknow.jpg/320px-Hazratganj_Lucknow.jpg"},
        ],
        "tagline": "City of Nawabs & Kebabs",
        "food_icon": "🥩",
    },
    "Amritsar": {
        "color": "#D97706",
        "gradient": "linear-gradient(135deg,#92400E 0%,#451A03 100%)",
        "accent": "#FDE68A",
        "places": [
            {"name": "Golden Temple", "emoji": "🛕", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Golden_Temple_Amritsar_2.jpg/320px-Golden_Temple_Amritsar_2.jpg"},
            {"name": "Jallianwala Bagh", "emoji": "🌺", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/46/Jallianwala_Bagh%2C_Amritsar.jpg/320px-Jallianwala_Bagh%2C_Amritsar.jpg"},
            {"name": "Wagah Border", "emoji": "🇮🇳", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7f/Wagah_border_ceremony.jpg/320px-Wagah_border_ceremony.jpg"},
            {"name": "Durgiana Temple", "emoji": "🏛️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Durgiana_Temple_Amritsar.jpg/320px-Durgiana_Temple_Amritsar.jpg"},
        ],
        "tagline": "Holy City & Makki di Roti Hub",
        "food_icon": "🫓",
    },
    "Goa": {
        "color": "#0891B2",
        "gradient": "linear-gradient(135deg,#164E63 0%,#0C2D40 100%)",
        "accent": "#67E8F9",
        "places": [
            {"name": "Calangute Beach", "emoji": "🏖️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Calangute_beach_goa.jpg/320px-Calangute_beach_goa.jpg"},
            {"name": "Basilica of Bom Jesus", "emoji": "⛪", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Bom_jesus_basilica_goa.jpg/320px-Bom_jesus_basilica_goa.jpg"},
            {"name": "Fort Aguada", "emoji": "🏰", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Aguada_Fort.jpg/320px-Aguada_Fort.jpg"},
            {"name": "Dudhsagar Falls", "emoji": "🌊", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/54/Dudhsagar_Falls-Goa.jpg/320px-Dudhsagar_Falls-Goa.jpg"},
        ],
        "tagline": "Beach Paradise & Seafood Heaven",
        "food_icon": "🦞",
    },
    "Jaipur": {
        "color": "#E11D48",
        "gradient": "linear-gradient(135deg,#881337 0%,#4C0519 100%)",
        "accent": "#FDA4AF",
        "places": [
            {"name": "Hawa Mahal", "emoji": "🏯", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Hawa_Mahal_Jaipur.jpg/320px-Hawa_Mahal_Jaipur.jpg"},
            {"name": "Amer Fort", "emoji": "🏰", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Amer_Fort_Jaipur.jpg/320px-Amer_Fort_Jaipur.jpg"},
            {"name": "City Palace", "emoji": "🏛️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/City_Palace_Jaipur.jpg/320px-City_Palace_Jaipur.jpg"},
            {"name": "Jantar Mantar", "emoji": "🔭", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/Jantar_Mantar_Jaipur.jpg/320px-Jantar_Mantar_Jaipur.jpg"},
        ],
        "tagline": "Pink City & Dal Baati Churma",
        "food_icon": "🍲",
    },
    "Kochi": {
        "color": "#047857",
        "gradient": "linear-gradient(135deg,#064E3B 0%,#022C22 100%)",
        "accent": "#6EE7B7",
        "places": [
            {"name": "Chinese Fishing Nets", "emoji": "🎣", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Chinese_fishing_nets_in_Kerala.jpg/320px-Chinese_fishing_nets_in_Kerala.jpg"},
            {"name": "Fort Kochi Beach", "emoji": "🏖️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Fort_Kochi_Beach.jpg/320px-Fort_Kochi_Beach.jpg"},
            {"name": "Mattancherry Palace", "emoji": "🏯", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Mattancherry_Dutch_Palace.jpg/320px-Mattancherry_Dutch_Palace.jpg"},
            {"name": "Jew Town Synagogue", "emoji": "🕍", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Paradesi_Synagogue%2C_Kochi.jpg/320px-Paradesi_Synagogue%2C_Kochi.jpg"},
        ],
        "tagline": "Queen of Arabian Sea & Seafood",
        "food_icon": "🐟",
    },
    "Indore": {
        "color": "#7C3AED",
        "gradient": "linear-gradient(135deg,#4C1D95 0%,#2E1065 100%)",
        "accent": "#DDD6FE",
        "places": [
            {"name": "Rajwada Palace", "emoji": "🏯", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f4/Rajwada_Palace%2C_Indore.jpg/320px-Rajwada_Palace%2C_Indore.jpg"},
            {"name": "Lal Bagh Palace", "emoji": "🏰", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Lalbagh_Palace_Indore.jpg/320px-Lalbagh_Palace_Indore.jpg"},
            {"name": "Sarafa Bazaar", "emoji": "🌃", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Sarafa_Bazaar_Indore.jpg/320px-Sarafa_Bazaar_Indore.jpg"},
            {"name": "Kanch Mandir", "emoji": "💎", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/52/Kanch_mandir_indore.jpg/320px-Kanch_mandir_indore.jpg"},
        ],
        "tagline": "Cleanest City & Street Food Capital",
        "food_icon": "🥘",
    },
    "Pune": {
        "color": "#B45309",
        "gradient": "linear-gradient(135deg,#78350F 0%,#451A03 100%)",
        "accent": "#FCD34D",
        "places": [
            {"name": "Shaniwar Wada", "emoji": "🏯", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/31/Shaniwar_Wada_Pune.jpg/320px-Shaniwar_Wada_Pune.jpg"},
            {"name": "Aga Khan Palace", "emoji": "🏛️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/Aga_Khan_Palace_Pune.jpg/320px-Aga_Khan_Palace_Pune.jpg"},
            {"name": "Sinhagad Fort", "emoji": "🏰", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/Sinhagad_Fort.jpg/320px-Sinhagad_Fort.jpg"},
            {"name": "Osho Ashram", "emoji": "🌸", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Osho_International_Meditation_Resort_Pune.jpg/320px-Osho_International_Meditation_Resort_Pune.jpg"},
        ],
        "tagline": "Oxford of East & Misal Pav",
        "food_icon": "🥗",
    },
    "Ahmedabad": {
        "color": "#0369A1",
        "gradient": "linear-gradient(135deg,#075985 0%,#0C4A6E 100%)",
        "accent": "#7DD3FC",
        "places": [
            {"name": "Sabarmati Ashram", "emoji": "🏛️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e2/Sabarmati_Ashram_Ahmedabad.jpg/320px-Sabarmati_Ashram_Ahmedabad.jpg"},
            {"name": "Adalaj Stepwell", "emoji": "🌊", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Adalaj_stepwell_-_perspective_view.jpg/320px-Adalaj_stepwell_-_perspective_view.jpg"},
            {"name": "Akshardham Temple", "emoji": "🛕", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/32/Akshardham_Temple_Gujarat.jpg/320px-Akshardham_Temple_Gujarat.jpg"},
            {"name": "Kankaria Lake", "emoji": "🌅", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Kankaria_Lake_at_Ahmedabad.jpg/320px-Kankaria_Lake_at_Ahmedabad.jpg"},
        ],
        "tagline": "Manchester of India & Dhokla City",
        "food_icon": "🫔",
    },
    "Chandigarh": {
        "color": "#0E7490",
        "gradient": "linear-gradient(135deg,#164E63 0%,#083344 100%)",
        "accent": "#A5F3FC",
        "places": [
            {"name": "Rock Garden", "emoji": "🪨", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/Rock_garden_Chandigarh.jpg/320px-Rock_garden_Chandigarh.jpg"},
            {"name": "Sukhna Lake", "emoji": "🚣", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Sukhna_Lake_Chandigarh.jpg/320px-Sukhna_Lake_Chandigarh.jpg"},
            {"name": "Rose Garden", "emoji": "🌹", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Chandigarh_Rose_Garden.jpg/320px-Chandigarh_Rose_Garden.jpg"},
            {"name": "Capitol Complex", "emoji": "🏛️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b3/Capitol_Complex_Chandigarh.jpg/320px-Capitol_Complex_Chandigarh.jpg"},
        ],
        "tagline": "City Beautiful & Punjabi Cuisine",
        "food_icon": "🍗",
    },
    "Varanasi": {
        "color": "#D97706",
        "gradient": "linear-gradient(135deg,#92400E 0%,#78350F 100%)",
        "accent": "#FDE68A",
        "places": [
            {"name": "Dashashwamedh Ghat", "emoji": "🛕", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Dashashwamedha_ghat_Varanasi.jpg/320px-Dashashwamedha_ghat_Varanasi.jpg"},
            {"name": "Kashi Vishwanath", "emoji": "🏛️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Kashi_Vishwanath_Temple.jpg/320px-Kashi_Vishwanath_Temple.jpg"},
            {"name": "Sarnath", "emoji": "☸️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Sarnath_stupa_%28dhamekh%29.jpg/320px-Sarnath_stupa_%28dhamekh%29.jpg"},
            {"name": "Manikarnika Ghat", "emoji": "🌅", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Manikarnika_Ghat.jpg/320px-Manikarnika_Ghat.jpg"},
        ],
        "tagline": "Spiritual Capital & Kashi Chaat",
        "food_icon": "🥙",
    },
    "Agra": {
        "color": "#BE185D",
        "gradient": "linear-gradient(135deg,#9D174D 0%,#500724 100%)",
        "accent": "#FBCFE8",
        "places": [
            {"name": "Taj Mahal", "emoji": "🕌", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Taj_Mahal%2C_Agra%2C_India_edit3.jpg/320px-Taj_Mahal%2C_Agra%2C_India_edit3.jpg"},
            {"name": "Agra Fort", "emoji": "🏰", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Agra_fort_at_India.jpg/320px-Agra_fort_at_India.jpg"},
            {"name": "Fatehpur Sikri", "emoji": "🏯", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Fatehpur_Sikri_Buland_Darwaza.jpg/320px-Fatehpur_Sikri_Buland_Darwaza.jpg"},
            {"name": "Mehtab Bagh", "emoji": "🌿", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Mehtab_Bagh_Agra.jpg/320px-Mehtab_Bagh_Agra.jpg"},
        ],
        "tagline": "City of Taj & Petha Sweets",
        "food_icon": "🍬",
    },
    "Vizag": {
        "color": "#0284C7",
        "gradient": "linear-gradient(135deg,#075985 0%,#0369A1 100%)",
        "accent": "#BAE6FD",
        "places": [
            {"name": "RK Beach", "emoji": "🏖️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/RK_Beach_Vizag.jpg/320px-RK_Beach_Vizag.jpg"},
            {"name": "Submarine Museum", "emoji": "⚓", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/INS_Kursura_Museum.jpg/320px-INS_Kursura_Museum.jpg"},
            {"name": "Borra Caves", "emoji": "🦇", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d6/Borra_Caves.jpg/320px-Borra_Caves.jpg"},
            {"name": "Araku Valley", "emoji": "🌄", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Araku_Valley.jpg/320px-Araku_Valley.jpg"},
        ],
        "tagline": "Jewel of East Coast & Seafood",
        "food_icon": "🦐",
    },
    "Madurai": {
        "color": "#B45309",
        "gradient": "linear-gradient(135deg,#92400E 0%,#451A03 100%)",
        "accent": "#FDE68A",
        "places": [
            {"name": "Meenakshi Amman Temple", "emoji": "🛕", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Madurai_Meenakshi_Amman_Temple.jpg/320px-Madurai_Meenakshi_Amman_Temple.jpg"},
            {"name": "Thirumalai Nayakkar Palace", "emoji": "🏛️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Thirumalai_Naicker_Mahal.jpg/320px-Thirumalai_Naicker_Mahal.jpg"},
            {"name": "Gandhi Museum", "emoji": "🏛️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/Gandhi_Museum_Madurai.jpg/320px-Gandhi_Museum_Madurai.jpg"},
            {"name": "Vandiyur Mariamman Teppakulam", "emoji": "🌊", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Vandiyur_Mariamman_Teppakulam%2C_Madurai.jpg/320px-Vandiyur_Mariamman_Teppakulam%2C_Madurai.jpg"},
        ],
        "tagline": "Athens of East & Jigarthanda",
        "food_icon": "🥤",
    },
    "Bhopal": {
        "color": "#047857",
        "gradient": "linear-gradient(135deg,#065F46 0%,#064E3B 100%)",
        "accent": "#A7F3D0",
        "places": [
            {"name": "Upper Lake", "emoji": "🌊", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/Upper_Lake_Bhopal.jpg/320px-Upper_Lake_Bhopal.jpg"},
            {"name": "Sanchi Stupa", "emoji": "☸️", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Sanchi_Stupa.jpg/320px-Sanchi_Stupa.jpg"},
            {"name": "Taj-ul-Masajid", "emoji": "🕌", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Taj-ul-Masajid_Bhopal.jpg/320px-Taj-ul-Masajid_Bhopal.jpg"},
            {"name": "Van Vihar National Park", "emoji": "🦁", "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Van_Vihar_National_Park_Bhopal.jpg/320px-Van_Vihar_National_Park_Bhopal.jpg"},
        ],
        "tagline": "City of Lakes & Kebab Culture",
        "food_icon": "🥩",
    },
}

# ── City Landmark Banner ─────────────────────────────────────────────────────
city_data = CITY_LANDMARKS.get(city, {})
if city_data:
    places = city_data["places"]
    accent = city_data["accent"]
    gradient = city_data["gradient"]
    tagline = city_data["tagline"]
    food_icon = city_data["food_icon"]

    # CSS for landmark cards
    st.markdown(f"""
    <style>
    .city-banner {{
        background: {gradient};
        border-radius: 20px;
        padding: 24px 28px 20px;
        margin-bottom: 24px;
        border: 1px solid {accent}33;
        position: relative;
        overflow: hidden;
    }}
    .city-banner::before {{
        content: '{food_icon}';
        position: absolute;
        font-size: 120px;
        right: 20px;
        top: -10px;
        opacity: 0.07;
        line-height: 1;
    }}
    .city-banner-eyebrow {{
        font-size: 9px;
        letter-spacing: 0.28em;
        text-transform: uppercase;
        color: {accent};
        font-weight: 700;
        margin-bottom: 6px;
    }}
    .city-banner-title {{
        font-family: 'Playfair Display', serif;
        font-size: 28px;
        font-weight: 900;
        color: #F5EFE6;
        margin-bottom: 4px;
    }}
    .city-banner-tagline {{
        font-size: 12px;
        color: rgba(245,239,230,0.5);
        margin-bottom: 18px;
        font-style: italic;
    }}
    .landmark-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-top: 4px;
    }}
    .landmark-card {{
        border-radius: 14px;
        overflow: hidden;
        position: relative;
        aspect-ratio: 4/3;
        border: 1.5px solid {accent}44;
        transition: transform 0.25s, box-shadow 0.25s;
        cursor: default;
    }}
    .landmark-card:hover {{
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    }}
    .landmark-card img {{
        width: 100%;
        height: 100%;
        object-fit: cover;
        display: block;
    }}
    .landmark-overlay {{
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(to top, rgba(0,0,0,0.85) 0%, transparent 100%);
        padding: 20px 10px 8px;
    }}
    .landmark-name {{
        font-size: 11px;
        font-weight: 700;
        color: #FFFFFF;
        line-height: 1.3;
        letter-spacing: 0.02em;
    }}
    .landmark-emoji {{
        font-size: 13px;
        margin-bottom: 2px;
        display: block;
    }}
    </style>
    """, unsafe_allow_html=True)

    landmark_cards = ""
    for p in places:
        landmark_cards += f"""
        <div class="landmark-card">
            <img src="{p['img']}" alt="{p['name']}" onerror="this.style.display='none';this.parentNode.style.background='rgba(255,255,255,0.08)'"/>
            <div class="landmark-overlay">
                <span class="landmark-emoji">{p['emoji']}</span>
                <div class="landmark-name">{p['name']}</div>
            </div>
        </div>"""

    st.markdown(f"""
    <div class="city-banner">
        <div class="city-banner-eyebrow">📍 Exploring</div>
        <div class="city-banner-title">{city}</div>
        <div class="city-banner-tagline">{tagline}</div>
        <div class="landmark-grid">{landmark_cards}</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════
#  CITY LANDMARK GALLERY
# ══════════════════════════════════════════
_city_data = CITY_LANDMARKS.get(city, {})
_landmarks = _city_data.get("places", []) if isinstance(_city_data, dict) else []
if _landmarks:
    st.markdown(f"""
    <div class="landmark-header">
      <div class="landmark-header-line"></div>
      <div class="landmark-header-text">📍 Famous Places in {city}</div>
      <span class="landmark-city-badge">📸 Must Visit</span>
      <div class="landmark-header-line"></div>
    </div>
    <div class="landmark-gallery">
    {"".join(f'''
      <div class="landmark-card">
        <img src="{lm['img']}" alt="{lm['name']}" onerror="this.parentElement.style.display='none'"/>
        <div class="landmark-label"><span>{lm['emoji']}</span>{lm['name']}</div>
      </div>''' for lm in _landmarks)}
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════
#  SCAN TRENDS HANDLER
# ══════════════════════════════════════════
if scan_btn:
    from scraper.trend_scraper import scrape_all_trends
    with st.spinner(f"📡 Scanning Google, Zomato & Instagram for {city}..."):
        scraped = scrape_all_trends(city, verbose=False)
        st.session_state.scraped = scraped
    total = sum(len(v) for k,v in scraped.items() if isinstance(v,list))
    st.markdown(f"""
    <div class="status-success">
        ✦ &nbsp; Scraped <strong>{total} data points</strong> from {city} &nbsp;·&nbsp;
        Google {len(scraped.get('google_results',[]))} &nbsp;·&nbsp;
        Zomato {len(scraped.get('zomato_data',[]))} &nbsp;·&nbsp;
        Articles {len(scraped.get('articles',[]))} &nbsp;·&nbsp;
        Hashtags {len(scraped.get('hashtags',[]))}
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════
#  SCRAPED DATA PREVIEW (before generate)
# ══════════════════════════════════════════
if st.session_state.scraped and not st.session_state.analysis:
    scraped = st.session_state.scraped
    type_icons = {"restaurant": "🍴", "collection": "🏷", "cuisine": "🌶"}

    st.markdown("""<div class="sec-head"><div class="sec-head-text">📡 Raw Scraped Data — Live Preview</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)

    col_g, col_z = st.columns(2)

    with col_g:
        google   = scraped.get("google_results", [])
        articles = scraped.get("articles", [])

        g_html = '<div class="scrape-panel"><div class="scrape-panel-title">🔍 Google Results <span></span></div>'
        if google:
            for r in google[:8]:
                g_html += f'<div class="google-result"><div class="g-title">{r.get("title","")[:70]}</div><div class="g-snippet">{r.get("snippet","")[:110]}</div></div>'
        else:
            g_html += '<div style="font-size:12px;color:#7A6F65;padding:8px 0">No results — Google may have blocked the request</div>'
        g_html += '</div>'
        st.markdown(g_html, unsafe_allow_html=True)

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        a_html = '<div class="scrape-panel"><div class="scrape-panel-title">📰 Food Articles <span></span></div>'
        if articles:
            for a in articles[:6]:
                a_html += f'<div class="article-item"><div class="art-headline">{a.get("headline","")}</div><div class="art-source">📰 {a.get("source","")}</div></div>'
        else:
            a_html += '<div style="font-size:12px;color:#7A6F65;padding:8px 0">No articles found</div>'
        a_html += '</div>'
        st.markdown(a_html, unsafe_allow_html=True)

    with col_z:
        zomato   = scraped.get("zomato_data", [])
        hashtags = scraped.get("hashtags", [])

        z_html = '<div class="scrape-panel"><div class="scrape-panel-title">🍽 Zomato Trending <span></span></div>'
        if zomato:
            for z in zomato[:12]:
                icon = type_icons.get(z.get("type",""), "•")
                z_html += f'<div class="zomato-item"><div class="zomato-icon">{icon}</div><div><div class="zomato-name">{z.get("name","")}</div><div class="zomato-type">{z.get("type","")}</div></div></div>'
        else:
            z_html += '<div style="font-size:12px;color:#7A6F65;padding:8px 0">No Zomato data — may have been blocked</div>'
        z_html += '</div>'
        st.markdown(z_html, unsafe_allow_html=True)

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

        h_html = '<div class="scrape-panel"><div class="scrape-panel-title">📸 Instagram Hashtags <span></span></div><div style="line-height:2.4">'
        if hashtags:
            for h in hashtags:
                t = h.get("type","hot")
                h_html += f'<span class="htag htag-{t}">{h["hashtag"]} +{h["estimated_growth_pct"]}%</span>'
        else:
            h_html += '<span style="font-size:12px;color:#7A6F65">No hashtag data</span>'
        h_html += '</div></div>'
        st.markdown(h_html, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="status-info" style="margin-top:20px">
        ✦ &nbsp; Scraped at {scraped.get('scraped_at','—')} &nbsp;·&nbsp;
        Data ready — click <strong>✦ Generate Specials</strong> in the sidebar to run AI analysis
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════
#  GENERATE SPECIALS HANDLER
# ══════════════════════════════════════════
if gen_btn:
    if not st.session_state.scraped:
        st.warning("⚠️ Please scan trends first!")
    else:
        from llm.dish_generator import run_full_pipeline
        with st.spinner("✦ Claude AI is analysing trends and crafting weekend specials..."):
            output = run_full_pipeline(
                scraped_data    = st.session_state.scraped,
                restaurant_type = rtype,
                price_range     = price,
                season          = season,
                verbose         = False,
            )
        st.session_state.analysis   = output["trend_analysis"]
        st.session_state.specials   = output["specials"]
        st.session_state.report_txt = output["weekly_report"]
        from reports.report_generator import save_all
        save_all(output)
        st.markdown('<div class="status-success">✦ &nbsp; AI analysis complete — JSON · TXT · CSV reports saved</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════
tab1, tab2, tab3 = st.tabs(["📊  Trend Analysis", "🍽  Weekend Specials", "📋  Weekly Report"])


# ════════════════════════════════════════════════════
#  TAB 1 — TREND ANALYSIS
# ════════════════════════════════════════════════════
with tab1:
    analysis = st.session_state.analysis

    if not analysis:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">📊</div>
          <div class="empty-title">No Analysis Yet</div>
          <div class="empty-sub">Select a city · Scan Trends · Generate Specials</div>
        </div>""", unsafe_allow_html=True)
    else:
        stats = analysis.get("stats", {})

        # KPI Row
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="kpi-card" data-icon="🌿">
              <div class="kpi-label">Ingredients Tracked</div>
              <div class="kpi-value">{len(analysis.get("trending_ingredients",[]))}</div>
              <div class="kpi-delta">↑ +3 new this week</div>
              <div class="kpi-accent spice"></div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="kpi-card" data-icon="📱">
              <div class="kpi-label">Posts Analysed</div>
              <div class="kpi-value">{stats.get("posts_analyzed","—")}</div>
              <div class="kpi-delta">↑ +18% vs last week</div>
              <div class="kpi-accent gold"></div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="kpi-card" data-icon="#️⃣">
              <div class="kpi-label">Viral Hashtags</div>
              <div class="kpi-value">{stats.get("hashtags_count", len(analysis.get("viral_hashtags",[])))}</div>
              <div class="kpi-delta">↑ +8 trending now</div>
              <div class="kpi-accent green"></div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="kpi-card" data-icon="❤️">
              <div class="kpi-label">Top Dish Saves</div>
              <div class="kpi-value">{stats.get("top_dish_saves","—")}</div>
              <div class="kpi-delta">↑ +24% engagement</div>
              <div class="kpi-accent purple"></div></div>""", unsafe_allow_html=True)

        # Analysis Callout
        st.markdown(f"""
        <div class="analysis-callout">
          <div class="analysis-eyebrow">AI Analysis Summary — {city}</div>
          <div class="analysis-text">{analysis.get('analysis_summary','')}</div>
        </div>""", unsafe_allow_html=True)

        col_l, col_r = st.columns(2)

        with col_l:
            st.markdown("""<div class="sec-head"><div class="sec-head-text">🔥 Trending Ingredients</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)
            ings = analysis.get("trending_ingredients", [])
            if ings:
                df = pd.DataFrame([{
                    "Ingredient": f"{i.get('emoji','')} {i.get('name','')}",
                    "Growth %":   i.get("growth_pct", 0),
                    "Status":     i.get("status", "rising"),
                } for i in ings])
                color_map = {"hot": "#C4411A", "rising": "#D4A017", "steady": "#1A6B3A"}
                fig = px.bar(df, x="Growth %", y="Ingredient", orientation="h",
                             color="Status", color_discrete_map=color_map,
                             template="simple_white",
                             labels={"Growth %": "Growth vs Last Week (%)"})
                fig.update_layout(
                    height=360, margin=dict(l=0,r=0,t=10,b=0), showlegend=True,
                    plot_bgcolor="#FFFCF8", paper_bgcolor="#FFFCF8",
                    font=dict(family="DM Sans", size=11, color="#3C3530"),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
                    xaxis=dict(gridcolor="#F0E8DF", tickfont=dict(size=10)),
                    yaxis=dict(tickfont=dict(size=11)), bargap=0.35,
                )
                fig.update_traces(marker_line_width=0)
                st.plotly_chart(fig, use_container_width=True)

        with col_r:
            st.markdown("""<div class="sec-head"><div class="sec-head-text">🏷 Viral Hashtags</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)
            tags = analysis.get("viral_hashtags", [])
            if tags:
                h_html = '<div style="line-height:2.4">'
                for h in tags:
                    h_html += f'<span class="htag htag-{h.get("type","hot")}">{h["tag"]} +{h["growth_pct"]}%</span>'
                h_html += '</div>'
                st.markdown(h_html, unsafe_allow_html=True)

            st.markdown("""<div class="sec-head" style="margin-top:24px"><div class="sec-head-text">📉 Declining — Avoid</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)
            for d in analysis.get("declining_trends", []):
                st.markdown(f"""
                <div style="display:flex;align-items:center;gap:10px;padding:8px 14px;border-radius:8px;
                            margin-bottom:6px;background:rgba(239,68,68,0.05);border:1px solid rgba(239,68,68,0.1);font-size:13px">
                    <span style="color:#EF4444;font-size:16px">↘</span>
                    <strong style="color:#1C1410">{d['name']}</strong>
                    <span style="font-family:'DM Mono',monospace;font-size:11px;color:#EF4444">{d['decline_pct']}</span>
                    <span style="color:#7A6F65;font-size:11px">— {d.get('reason','')}</span>
                </div>""", unsafe_allow_html=True)

        # Famous Dishes
        st.markdown("""<div class="sec-head"><div class="sec-head-text">🍜 Famous Dishes Trending Right Now</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)
        dishes_data = analysis.get("famous_dishes_trending", [])
        if dishes_data:
            df2 = pd.DataFrame([{
                "Dish":       d.get("dish_name",""),
                "Famous At":  d.get("famous_at",""),
                "Saves":      d.get("saves_estimate",""),
                "Engagement": d.get("engagement_pct", 0),
                "Why Famous": d.get("why_famous",""),
            } for d in dishes_data])
            st.dataframe(df2, use_container_width=True, hide_index=True,
                         column_config={"Engagement": st.column_config.ProgressColumn("Engagement %", min_value=0, max_value=100, format="%d%%")})

        # Raw Sources Expander
        scraped = st.session_state.scraped
        if scraped:
            type_icons = {"restaurant":"🍴","collection":"🏷","cuisine":"🌶"}
            with st.expander("📡 View Raw Scraped Sources — Google · Zomato · Articles · Hashtags"):
                sc1, sc2 = st.columns(2)
                with sc1:
                    st.markdown("**🔍 Google Results**")
                    for r in scraped.get("google_results", [])[:10]:
                        st.markdown(f'<div class="google-result"><div class="g-title">{r.get("title","")[:70]}</div><div class="g-snippet">{r.get("snippet","")[:100]}</div></div>', unsafe_allow_html=True)
                    st.markdown("<br>**📰 Articles**", unsafe_allow_html=True)
                    for a in scraped.get("articles", [])[:6]:
                        st.markdown(f'<div class="article-item"><div class="art-headline">{a.get("headline","")}</div><div class="art-source">📰 {a.get("source","")}</div></div>', unsafe_allow_html=True)
                with sc2:
                    st.markdown("**🍽 Zomato Trending**")
                    for z in scraped.get("zomato_data", [])[:12]:
                        icon = type_icons.get(z.get("type",""),"•")
                        st.markdown(f'<div class="zomato-item"><div class="zomato-icon">{icon}</div><div><div class="zomato-name">{z.get("name","")}</div><div class="zomato-type">{z.get("type","")}</div></div></div>', unsafe_allow_html=True)
                    st.markdown("<br>**📸 Instagram**", unsafe_allow_html=True)
                    ht = '<div style="line-height:2.2">'
                    for h in scraped.get("hashtags", []):
                        ht += f'<span class="htag htag-{h.get("type","hot")}">{h["hashtag"]} +{h["estimated_growth_pct"]}%</span>'
                    ht += '</div>'
                    st.markdown(ht, unsafe_allow_html=True)
                total_pts = sum(len(v) for k,v in scraped.items() if isinstance(v,list))
                st.caption(f"🗂 {total_pts} total data points · Scraped: {scraped.get('scraped_at','—')}")


# ════════════════════════════════════════════════════
#  TAB 2 — WEEKEND SPECIALS
# ════════════════════════════════════════════════════
with tab2:
    specials = st.session_state.specials

    if not specials:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">🍽</div>
          <div class="empty-title">No Specials Generated Yet</div>
          <div class="empty-sub">Click <strong>✦ Generate Specials</strong> in the sidebar</div>
        </div>""", unsafe_allow_html=True)
    else:
        top_ings = specials.get("top_weekend_ingredients", [])
        if top_ings:
            st.markdown("""<div class="sec-head"><div class="sec-head-text">🏆 Top Revenue Ingredients This Weekend</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)
            ing_icons = ["🌶","🧄","🫚","🌿","🥛","🍅","🧅","🫙"]
            cols = st.columns(len(top_ings))
            for i, (col, ing) in enumerate(zip(cols, top_ings)):
                with col:
                    st.markdown(f"""
                    <div class="ing-pill">
                      <span class="ing-pill-icon">{ing_icons[i % len(ing_icons)]}</span>
                      <div class="ing-rank">#{i+1} Pick</div>
                      <div style="margin-top:4px;font-size:13px;font-weight:700;color:#C4411A">{ing}</div>
                    </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown("""<div class="sec-head"><div class="sec-head-text">✦ Weekend Special Dishes</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)

        dishes = specials.get("weekend_specials", [])
        for i in range(0, len(dishes), 2):
            c1, c2 = st.columns(2)
            for col, dish in zip([c1, c2], dishes[i:i+2]):
                cat = dish.get("category","")
                if   "margin"    in cat.lower(): hdr_cls, badge_cls, badge_lbl = "margin",    "badge-margin",    "💰 High Margin"
                elif "premium"   in cat.lower(): hdr_cls, badge_cls, badge_lbl = "premium",   "badge-premium",   "👑 Premium Upsell"
                elif "instagram" in cat.lower(): hdr_cls, badge_cls, badge_lbl = "insta",     "badge-insta",     "📸 Reels-Worthy"
                else:                            hdr_cls, badge_cls, badge_lbl = "performer", "badge-performer", "🔥 Weekend Hit"

                demand   = dish.get("predicted_demand","Medium")
                d_wrap   = f"demand-{demand.lower()}-wrap"

                with col:
                    st.markdown(f"""
                    <div class="dish-card">
                      <div class="dish-card-header {hdr_cls}">
                        <div class="dish-header-top">
                          <span class="dish-badge {badge_cls}">{badge_lbl}</span>
                          <div>
                            <div class="dish-price-badge">{dish.get('suggested_price_range','')}</div>
                            <div class="{d_wrap}" style="margin-top:5px;text-align:right">
                              <span class="demand-dot"></span><span class="demand-label">{demand} Demand</span>
                            </div>
                          </div>
                        </div>
                        <div class="dish-name">{dish.get('dish_name','')}</div>
                        <div class="dish-key-ing">Key ingredient: {dish.get('key_trending_ingredient','')}</div>
                      </div>
                      <div class="dish-card-body">
                        <div class="dish-desc">{dish.get('description','')}</div>
                        <div class="dish-meta-row">
                          <div class="dish-meta-item">
                            <div class="dmi-label">Food Cost</div>
                            <div class="dmi-value spice">{dish.get('food_cost_level','')} · {dish.get('estimated_food_cost_inr','')}</div>
                          </div>
                          <div class="dish-meta-item">
                            <div class="dmi-label">Gross Margin</div>
                            <div class="dmi-value green">{dish.get('gross_margin_pct','')}</div>
                          </div>
                          <div class="dish-meta-item">
                            <div class="dmi-label">Prep Time</div>
                            <div class="dmi-value">{dish.get('prep_time_mins','')} mins</div>
                          </div>
                          <div class="dish-meta-item">
                            <div class="dmi-label">Best Served</div>
                            <div class="dmi-value">{str(dish.get('best_served','')).title()}</div>
                          </div>
                        </div>
                        <div class="dish-inspired">
                          <span style="font-size:16px">🏠</span>
                          Inspired by <strong>{dish.get('inspired_by','—')}</strong>
                        </div>
                      </div>
                    </div>""", unsafe_allow_html=True)

                    with st.expander("📸 Plating · Reels · Trend Tips"):
                        st.markdown(f"""
                        <div class="tip-block plating">
                          <div class="tip-label">🎨 Plating Tip</div>
                          <div class="tip-text">{dish.get('plating_tip','')}</div>
                        </div>
                        <div class="tip-block reels">
                          <div class="tip-label">🎬 Reels Tip</div>
                          <div class="tip-text">{dish.get('reels_tip','')}</div>
                        </div>
                        <div class="tip-block trend">
                          <div class="tip-label">🚀 Why It'll Trend</div>
                          <div class="tip-text">{dish.get('why_it_will_trend','')}</div>
                        </div>""", unsafe_allow_html=True)

        if specials.get("strategic_insight"):
            st.markdown(f"""
            <div class="insight-box">
              <div class="insight-eyebrow">✦ Strategic Intelligence</div>
              <div class="insight-city">{specials.get('city','')} — This Weekend</div>
              <div class="insight-text">{specials.get('strategic_insight','')}</div>
              <div class="insight-revenue">📈 &nbsp; Revenue Projection: {specials.get('revenue_projection','')}</div>
            </div>""", unsafe_allow_html=True)

        if dishes:
            st.markdown("<br>", unsafe_allow_html=True)
            df_dishes = pd.DataFrame([{
                "Dish": d.get("dish_name",""), "Category": d.get("category",""),
                "Price (₹)": d.get("suggested_price_range",""), "Food Cost": d.get("estimated_food_cost_inr",""),
                "Margin": d.get("gross_margin_pct",""), "Demand": d.get("predicted_demand",""),
                "Inspired By": d.get("inspired_by",""), "Key Ingredient": d.get("key_trending_ingredient",""),
                "Prep (mins)": d.get("prep_time_mins",""),
            } for d in dishes])
            st.download_button("⬇ Download Weekend Specials CSV", df_dishes.to_csv(index=False),
                               file_name=f"weekend_specials_{city.lower()}_{datetime.now().strftime('%Y%m%d')}.csv",
                               mime="text/csv")


# ════════════════════════════════════════════════════
#  TAB 3 — WEEKLY REPORT
# ════════════════════════════════════════════════════
with tab3:
    if not st.session_state.report_txt:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">📋</div>
          <div class="empty-title">No Report Generated Yet</div>
          <div class="empty-sub">Generate specials first to build your weekly trend report</div>
        </div>""", unsafe_allow_html=True)
    else:
        c1, c2 = st.columns([3,1])
        with c1:
            st.markdown(f"""
            <div class="report-header">
              <div>
                <div class="report-title">Weekly Trend Report — {city}</div>
                <div class="report-subtitle">{rtype} · {price} · {season} &nbsp;·&nbsp; Generated {datetime.now().strftime('%A, %d %B %Y at %I:%M %p')}</div>
              </div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button("⬇ Download Full Report", st.session_state.report_txt,
                               file_name=f"weekly_report_{city.lower()}_{datetime.now().strftime('%Y%m%d')}.txt",
                               mime="text/plain", use_container_width=True)

        st.markdown(f'<div class="report-body">{st.session_state.report_txt.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

        if st.session_state.specials:
            st.markdown("""<div class="sec-head" style="margin-top:28px"><div class="sec-head-text">📊 Recommended Weekend Menu Summary</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)
            dishes = st.session_state.specials.get("weekend_specials", [])
            if dishes:
                df3 = pd.DataFrame([{
                    "Dish": d.get("dish_name",""), "Category": d.get("category",""),
                    "Inspired By": d.get("inspired_by",""), "Price (₹)": d.get("suggested_price_range",""),
                    "Gross Margin": d.get("gross_margin_pct",""), "Demand": d.get("predicted_demand",""),
                } for d in dishes])
                st.dataframe(df3, use_container_width=True, hide_index=True)
