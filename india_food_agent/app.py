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
if "scraped"       not in st.session_state: st.session_state.scraped       = None
if "analysis"      not in st.session_state: st.session_state.analysis      = None
if "specials"      not in st.session_state: st.session_state.specials       = None
if "report_txt"    not in st.session_state: st.session_state.report_txt     = None
if "chat_history"  not in st.session_state: st.session_state.chat_history   = []


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
    <div class="hero-tagline">Done by HackSHEK</div>
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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊  Trend Analysis", "🍽  Weekend Specials", "📋  Weekly Report", "🗺️  Restaurant Map", "🏙️  City Top 10", "🤖  Recipe AI Chat"])


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


# ════════════════════════════════════════════════════
#  TAB 4 — RESTAURANT MAP
# ════════════════════════════════════════════════════

# ══════════════════════════════════════════
#  TOP 10 FOODS PER CITY (Static Curated Data)
# ══════════════════════════════════════════
CITY_TOP_10_FOODS = {
    "Hyderabad": [
        {"rank":1,"dish":"Hyderabadi Dum Biryani","emoji":"🍚","where":"Paradise, Shah Ghouse","price":"₹180–₹450","must_try":True,"description":"Aromatic slow-cooked rice with tender mutton or chicken sealed in a handi with saffron and fried onions."},
        {"rank":2,"dish":"Haleem","emoji":"🥘","where":"Shah Ghouse, Pista House","price":"₹120–₹250","must_try":True,"description":"Rich slow-cooked wheat and mutton stew — a Ramadan staple now loved year-round."},
        {"rank":3,"dish":"Irani Chai & Osmania Biscuits","emoji":"☕","where":"Nimrah Café, Charminar","price":"₹20–₹40","must_try":True,"description":"Creamy, cardamom-laced tea with crunchy buttery Osmania biscuits — a Hyderabadi morning ritual."},
        {"rank":4,"dish":"Pathar Gosht","emoji":"🥩","where":"Bawarchi Restaurant","price":"₹300–₹500","must_try":False,"description":"Spiced mutton marinated and cooked on a hot granite stone over charcoal."},
        {"rank":5,"dish":"Double Ka Meetha","emoji":"🍮","where":"Hotel Shadab, home kitchens","price":"₹80–₹150","must_try":False,"description":"Hyderabadi bread pudding soaked in sugar syrup, fried and topped with khoya and dry fruits."},
        {"rank":6,"dish":"Mirchi Ka Salan","emoji":"🌶️","where":"Most biryani joints","price":"₹60–₹120","must_try":False,"description":"Long green chilies cooked in a tangy peanut-sesame-tamarind gravy — the classic biryani side."},
        {"rank":7,"dish":"Qubani Ka Meetha","emoji":"🍑","where":"Shadab, Nayaab","price":"₹80–₹160","must_try":False,"description":"Slow-cooked dried apricot dessert served warm with a dollop of cream."},
        {"rank":8,"dish":"Lukhmi","emoji":"🥟","where":"Old City bakeries","price":"₹20–₹40","must_try":False,"description":"Crispy square-shaped pastry filled with spiced minced meat — Hyderabad's samosa cousin."},
        {"rank":9,"dish":"Gongura Mutton","emoji":"🌿","where":"Local Andhra restaurants","price":"₹250–₹400","must_try":False,"description":"Tangy sorrel-leaf based mutton curry unique to Telangana/Andhra."},
        {"rank":10,"dish":"Dil Khush","emoji":"🧁","where":"Hyderabad bakeries","price":"₹30–₹60","must_try":False,"description":"Flaky pastry with a sweet coconut and tutti-frutti filling — an old-school Hyderabadi bakery treat."},
    ],
    "Chennai": [
        {"rank":1,"dish":"Chettinad Chicken Curry","emoji":"🍗","where":"Hotel Palmgrove, Junior Kuppanna","price":"₹200–₹380","must_try":True,"description":"Fiery, aromatic curry from the Chettinad region with kalpasi and marathi mokku spices."},
        {"rank":2,"dish":"Idli Sambar","emoji":"🫓","where":"Murugan Idli Shop, Saravana Bhavan","price":"₹60–₹120","must_try":True,"description":"Fluffy steamed rice cakes dunked in a tangy vegetable lentil soup — Chennai's soul food."},
        {"rank":3,"dish":"Masala Dosa","emoji":"🫔","where":"Saravana Bhavan, Ratna Café","price":"₹70–₹150","must_try":True,"description":"Crispy fermented crepe filled with spiced potato masala, served with coconut chutney."},
        {"rank":4,"dish":"Filter Coffee","emoji":"☕","where":"Every Brahmin café, Ratna Café","price":"₹20–₹50","must_try":True,"description":"Strong chicory-blended decoction frothed to perfection in a steel tumbler-davara set."},
        {"rank":5,"dish":"Kothu Parotta","emoji":"🥙","where":"Street stalls across Chennai","price":"₹80–₹150","must_try":False,"description":"Shredded parotta stir-fried with egg, vegetables and spicy masala on a hot tawa."},
        {"rank":6,"dish":"Biryani (Chennai style)","emoji":"🍚","where":"Junior Kuppanna, Buhari","price":"₹150–₹300","must_try":False,"description":"Short-grain rice biryani with a distinct seeraga samba rice and Chettinad spice profile."},
        {"rank":7,"dish":"Paya Soup","emoji":"🍲","where":"Muslim quarters, Sowcarpet","price":"₹100–₹180","must_try":False,"description":"Rich collagen-heavy goat trotter soup slow-cooked overnight — a breakfast tradition."},
        {"rank":8,"dish":"Appam & Stew","emoji":"🥞","where":"Kerala restaurants, Kochi hotels","price":"₹120–₹200","must_try":False,"description":"Lacy rice hoppers paired with a mild coconut milk vegetable or chicken stew."},
        {"rank":9,"dish":"Sundal","emoji":"🫘","where":"Marina Beach vendors","price":"₹20–₹40","must_try":False,"description":"Boiled chickpeas or legumes tossed with mustard, curry leaves, and fresh coconut — beach snack."},
        {"rank":10,"dish":"Murukku","emoji":"🌀","where":"Sweet shops, Chettiar stores","price":"₹20–₹60","must_try":False,"description":"Deep-fried crunchy rice flour spirals with sesame and cumin — an addictive Tamil snack."},
    ],
    "Mumbai": [
        {"rank":1,"dish":"Vada Pav","emoji":"🍔","where":"Ashok Vada Pav, every street corner","price":"₹15–₹30","must_try":True,"description":"Spiced potato fritter in a soft pav with green chutney and dry garlic chutney — Mumbai's soul."},
        {"rank":2,"dish":"Pav Bhaji","emoji":"🫕","where":"Sardar, Cannon Pav Bhaji","price":"₹80–₹150","must_try":True,"description":"Buttery mixed vegetable mash served with toasted pav — a Mumbai street food icon."},
        {"rank":3,"dish":"Bombay Sandwich","emoji":"🥪","where":"Chowpatty vendors, dabawalas","price":"₹40–₹80","must_try":True,"description":"Layered grilled sandwich with cucumber, beets, green chutney and masala spices."},
        {"rank":4,"dish":"Bhelpuri","emoji":"🥗","where":"Chowpatty Beach, Marine Drive","price":"₹30–₹60","must_try":True,"description":"Puffed rice tossed with tamarind, chutneys, onion, sev and coriander — sea-breeze eating."},
        {"rank":5,"dish":"Misal Pav","emoji":"🫙","where":"Mamledar Misal, Warna Misal","price":"₹80–₹150","must_try":False,"description":"Sprouted moth beans in spicy rassa curry topped with farsan, onion, and served with pav."},
        {"rank":6,"dish":"Keema Pav","emoji":"🥩","where":"Bademiya, street stalls","price":"₹120–₹200","must_try":False,"description":"Spiced minced mutton served with butter-toasted pav — a late-night Mumbai staple."},
        {"rank":7,"dish":"Bombay Duck Fry","emoji":"🐟","where":"Konkan restaurants, Mahesh Lunch Home","price":"₹180–₹300","must_try":False,"description":"Crispy fried Bombil fish marinated in vinegar and Goan-spiced breadcrumbs."},
        {"rank":8,"dish":"Puran Poli","emoji":"🫓","where":"Aaswad, traditional homes","price":"₹60–₹100","must_try":False,"description":"Flatbread stuffed with sweetened lentil and jaggery filling — Maharashtra's festive bread."},
        {"rank":9,"dish":"Modak","emoji":"🍡","where":"Sweet shops across the city","price":"₹20–₹50 each","must_try":False,"description":"Steamed sweet dumplings filled with coconut and jaggery — Lord Ganesha's favourite."},
        {"rank":10,"dish":"Berry Pulao","emoji":"🍚","where":"Britannia & Co., Café Military","price":"₹350–₹500","must_try":False,"description":"Parsi-style rice pulao studded with imported barberries — a rare Mumbai heirloom dish."},
    ],
    "Delhi": [
        {"rank":1,"dish":"Butter Chicken","emoji":"🍗","where":"Moti Mahal (original), Gulati","price":"₹300–₹600","must_try":True,"description":"The dish that conquered the world — tender tandoori chicken in a silky tomato-butter-cream gravy."},
        {"rank":2,"dish":"Chole Bhature","emoji":"🫓","where":"Sita Ram Diwan Chand, Haldiram's","price":"₹80–₹150","must_try":True,"description":"Fluffy deep-fried bread with spiced white chickpea curry — Delhi's iconic Sunday breakfast."},
        {"rank":3,"dish":"Paranthe","emoji":"🥞","where":"Paranthe Wali Gali, Chandni Chowk","price":"₹60–₹120","must_try":True,"description":"Stuffed whole-wheat flatbreads fried in ghee — from aloo to dry fruit, 20+ fillings available."},
        {"rank":4,"dish":"Galouti Kebab","emoji":"🫔","where":"Karim's, Dum Pukht","price":"₹300–₹500","must_try":True,"description":"Melt-in-the-mouth minced mutton kebab with 100+ spices, perfected for toothless nawabs."},
        {"rank":5,"dish":"Nihari","emoji":"🍲","where":"Karim's, Al Jawahar","price":"₹200–₹400","must_try":False,"description":"Slow-cooked overnight bone-marrow mutton stew — Old Delhi's revered breakfast dish."},
        {"rank":6,"dish":"Dal Makhani","emoji":"🫕","where":"Bukhara, Punjab Grill","price":"₹250–₹500","must_try":False,"description":"Black lentils simmered for 24 hours with butter and cream — the Punjabi gold standard."},
        {"rank":7,"dish":"Daulat Ki Chaat","emoji":"🍮","where":"Chandni Chowk (winter only)","price":"₹30–₹60","must_try":False,"description":"Ethereal morning dew foam sweetened with sugar and saffron — a Delhi winter secret."},
        {"rank":8,"dish":"Rajma Chawal","emoji":"🍱","where":"Home kitchens, dhabas everywhere","price":"₹80–₹150","must_try":False,"description":"Slow-cooked red kidney beans in onion-tomato masala served over steamed basmati rice."},
        {"rank":9,"dish":"Jalebi","emoji":"🍥","where":"Old Famous Jalebi Wala, Chandni Chowk","price":"₹30–₹60","must_try":False,"description":"Crispy, syrup-soaked pretzel-shaped sweets — best eaten fresh and scalding hot."},
        {"rank":10,"dish":"Matar Kulcha","emoji":"🫛","where":"Street vendors near Jama Masjid","price":"₹40–₹80","must_try":False,"description":"Tangy dried peas curry topped with tamarind and chaat masala, eaten with soft kulcha."},
    ],
    "Bengaluru": [
        {"rank":1,"dish":"Benne Masala Dosa","emoji":"🫔","where":"CTR (Shivajinagar), Vidyarthi Bhavan","price":"₹60–₹120","must_try":True,"description":"Crispy dosa loaded with white butter and a spiced potato filling — Bangalore's breakfast crown."},
        {"rank":2,"dish":"Rava Idli","emoji":"🫓","where":"MTR (Mavalli Tiffin Room)","price":"₹80–₹150","must_try":True,"description":"Semolina idli invented during WWII rice shortage — now MTR's most celebrated dish."},
        {"rank":3,"dish":"Mangalorean Fish Curry","emoji":"🐟","where":"Coastal Karnataka restaurants","price":"₹200–₹380","must_try":False,"description":"Tangy coconut-based fish curry with byadagi chilies and kokum — coastal Karnataka at its best."},
        {"rank":4,"dish":"Ragi Mudde","emoji":"🫙","where":"Traditional Karnataka restaurants","price":"₹60–₹100","must_try":False,"description":"Finger millet balls eaten with saaru or sambar — the traditional Kannadiga staple."},
        {"rank":5,"dish":"Neer Dosa","emoji":"🫓","where":"Udupi restaurants across the city","price":"₹60–₹100","must_try":False,"description":"Lacy, paper-thin rice crepes served with coconut chutney — delicate and light."},
        {"rank":6,"dish":"Akki Roti","emoji":"🫔","where":"Home kitchens, traditional eateries","price":"₹40–₹80","must_try":False,"description":"Rice flour flatbread mixed with onion, curry leaves and green chili — eaten with chutney."},
        {"rank":7,"dish":"Mysore Masala Dosa","emoji":"🌶️","where":"Most Darshinis (fast-food joints)","price":"₹60–₹100","must_try":False,"description":"Dosa smeared with red chili-garlic chutney inside before adding potato filling — a spicy twist."},
        {"rank":8,"dish":"Crab Ghee Roast","emoji":"🦀","where":"Besharam, Coastal restaurants","price":"₹500–₹900","must_try":False,"description":"Mangalorean crab tossed in a dry, aromatic ghee roast masala with byadagi chilies."},
        {"rank":9,"dish":"Obbattu / Holige","emoji":"🍮","where":"Traditional sweet shops","price":"₹20–₹40","must_try":False,"description":"Karnataka's festive flatbread stuffed with jaggery-lentil or coconut-jaggery filling."},
        {"rank":10,"dish":"Filter Coffee (Degree Coffee)","emoji":"☕","where":"Every Darshini and Brahmin café","price":"₹15–₹30","must_try":True,"description":"The legendary South Indian filter decoction — dark, chicory-strong and served in steel tumbler."},
    ],
    "Kolkata": [
        {"rank":1,"dish":"Kolkata Biryani","emoji":"🍚","where":"Arsalan, Shiraz, Royal Indian Hotel","price":"₹180–₹350","must_try":True,"description":"Subtle Awadhi-origin biryani with boiled egg and potato added — uniquely Kolkata."},
        {"rank":2,"dish":"Kathi Roll","emoji":"🌯","where":"Nizam's (original), Campari","price":"₹80–₹160","must_try":True,"description":"Paratha wrap filled with egg, spiced chicken or mutton tikka — Kolkata's original fast food."},
        {"rank":3,"dish":"Mishti Doi","emoji":"🍮","where":"Sen Mahasay, Hindusthan Sweets","price":"₹40–₹80","must_try":True,"description":"Thick sweetened yogurt set in earthen pots — caramel-hued and velvety smooth."},
        {"rank":4,"dish":"Rasgulla","emoji":"🍡","where":"K.C. Das (inventors), Nalin Chandra Das","price":"₹15–₹30 each","must_try":True,"description":"Spongy cottage cheese balls soaked in light sugar syrup — Bengal's most iconic sweet."},
        {"rank":5,"dish":"Kosha Mangsho","emoji":"🥩","where":"Kasturi, Bhojohori Manna","price":"₹250–₹450","must_try":False,"description":"Dark, deeply spiced slow-cooked mutton curry — the pride of every Bengali kitchen."},
        {"rank":6,"dish":"Luchi Aloor Dom","emoji":"🫓","where":"Bengali homes, traditional eateries","price":"₹80–₹150","must_try":False,"description":"Fluffy deep-fried white flour bread with spicy potato curry — Sunday breakfast ritual."},
        {"rank":7,"dish":"Macher Jhol","emoji":"🐟","where":"Traditional Bengali restaurants","price":"₹180–₹300","must_try":False,"description":"Light, turmeric-based fish curry with potatoes and tomatoes — the everyday Bengali staple."},
        {"rank":8,"dish":"Phuchka","emoji":"🫙","where":"Street vendors across the city","price":"₹20–₹50","must_try":False,"description":"Kolkata's version of pani puri — thinner shells filled with spiced mashed potato and tamarind water."},
        {"rank":9,"dish":"Sandesh","emoji":"🍬","where":"Bhim Chandra Nag, Girish Ch. Dey","price":"₹20–₹60","must_try":False,"description":"Freshly made cottage cheese mithai flavoured with rose, pistachio or mango — pure elegance."},
        {"rank":10,"dish":"Jhal Muri","emoji":"🥗","where":"Street vendors, Maidan","price":"₹15–₹30","must_try":False,"description":"Puffed rice tossed with mustard oil, raw mustard, green chili and spices — Kolkata's street snack."},
    ],
    "Lucknow": [
        {"rank":1,"dish":"Galouti Kebab","emoji":"🫔","where":"Tunday Kababi (original)","price":"₹200–₹350","must_try":True,"description":"Ultra-soft minced mutton kebab with 160 spices, invented for a toothless Nawab of Awadh."},
        {"rank":2,"dish":"Lucknawi Biryani","emoji":"🍚","where":"Wahid Biryani, Idris ki Biryani","price":"₹150–₹300","must_try":True,"description":"Dum-cooked Awadhi biryani with subtle saffron aroma and long-grain basmati — milder than Hyderabadi."},
        {"rank":3,"dish":"Sheermal","emoji":"🫓","where":"Tunde Kababi area, old bakeries","price":"₹30–₹60","must_try":True,"description":"Saffron-laced sweet flatbread baked in a tandoor — the royal bread of Awadh."},
        {"rank":4,"dish":"Basket Chaat","emoji":"🫙","where":"Ram Asrey, Royal Café","price":"₹80–₹150","must_try":False,"description":"Crispy fried potato basket filled with dahi, chutney and spiced chickpeas — a Lucknow original."},
        {"rank":5,"dish":"Nihari Kulcha","emoji":"🍲","where":"Old City restaurants","price":"₹150–₹280","must_try":False,"description":"Silky slow-cooked bone marrow mutton stew with flaky kulcha — a breakfast luxury."},
        {"rank":6,"dish":"Seekh Kebab","emoji":"🥩","where":"Dastarkhwan, street tandoors","price":"₹150–₹250","must_try":False,"description":"Smoky minced mutton skewers cooked over charcoal — aromatic with mace and cardamom."},
        {"rank":7,"dish":"Kulfi Falooda","emoji":"🍧","where":"Ram Asrey, Chowk market","price":"₹60–₹120","must_try":False,"description":"Dense rose-flavoured ice cream over vermicelli in basil seeds and rose syrup — a cooling dessert."},
        {"rank":8,"dish":"Makkhan Malai","emoji":"🍮","where":"Morning vendors near Hazratganj (winter)","price":"₹40–₹80","must_try":False,"description":"Morning dew churned into a delicate frothy cream — a seasonal Lucknow winter delicacy."},
        {"rank":9,"dish":"Kakori Kebab","emoji":"🫔","where":"Kakori village restaurants","price":"₹250–₹400","must_try":False,"description":"Silkier and more refined than galouti — minced mutton on skewers with rose water and mace."},
        {"rank":10,"dish":"Shahi Tukda","emoji":"🍞","where":"Traditional mithai shops","price":"₹80–₹150","must_try":False,"description":"Fried bread soaked in rabri and garnished with saffron and silver leaf — royal Awadhi dessert."},
    ],
    "Amritsar": [
        {"rank":1,"dish":"Amritsari Kulcha","emoji":"🫓","where":"Kulcha Land, Bharawan Da Dhaba","price":"₹80–₹150","must_try":True,"description":"Crispy tandoor-baked stuffed bread with aloo or paneer filling, eaten with chole and butter."},
        {"rank":2,"dish":"Dal Makhani","emoji":"🫕","where":"Kesar Da Dhaba, Brothers' Dhaba","price":"₹150–₹250","must_try":True,"description":"The original slow-cooked black lentil dal with butter and cream — creamy, rich, addictive."},
        {"rank":3,"dish":"Amritsari Fish","emoji":"🐟","where":"Brothers' Dhaba, Surjit Food Plaza","price":"₹200–₹350","must_try":True,"description":"Spiced batter-fried sole fish with ajwain and chili — a Punjab street food institution."},
        {"rank":4,"dish":"Langar Prasad","emoji":"🙏","where":"Harmandir Sahib (Golden Temple)","price":"Free","must_try":True,"description":"Simple dal, sabzi and roti served with devotion to 100,000+ people daily — the world's largest free kitchen."},
        {"rank":5,"dish":"Pinni","emoji":"🍬","where":"Amritsar sweet shops","price":"₹20–₹40 each","must_try":False,"description":"Desi ghee and whole wheat flour sweet balls with dry fruits — a winter energy food."},
        {"rank":6,"dish":"Lassi","emoji":"🥛","where":"Gurdas Ram Lassiwala, Ahuja Milk","price":"₹60–₹120","must_try":False,"description":"Thick, churned curd with fresh cream and sugar served in tall steel glasses — heaven in summer."},
        {"rank":7,"dish":"Chole Bhature","emoji":"🫓","where":"Kanha Sweets, street stalls","price":"₹80–₹150","must_try":False,"description":"Spiced chickpea curry with puffed deep-fried bread — Punjab's favourite breakfast."},
        {"rank":8,"dish":"Sarson Da Saag & Makki Di Roti","emoji":"🌿","where":"Traditional dhabas (winter)","price":"₹100–₹180","must_try":False,"description":"Mustard greens cooked with spinach in desi ghee, eaten with corn flour flatbread — Punjab winter classic."},
        {"rank":9,"dish":"Pindi Chole","emoji":"🫘","where":"Dhabas around the Golden Temple","price":"₹80–₹150","must_try":False,"description":"Dark, intensely spiced chickpeas slow-cooked with pomegranate and black tea for colour and depth."},
        {"rank":10,"dish":"Tandoori Chicken","emoji":"🍗","where":"Makhan Fish & Chicken Corner","price":"₹250–₹450","must_try":False,"description":"Yogurt-marinated chicken cooked in a clay tandoor — the Punjab original that started a global trend."},
    ],
    "Goa": [
        {"rank":1,"dish":"Goan Fish Curry Rice","emoji":"🐟","where":"Ritz Classic, Vinayak Family Restaurant","price":"₹150–₹300","must_try":True,"description":"Tangy coconut milk curry with fresh catch of the day, served over Goa's famous parboiled rice."},
        {"rank":2,"dish":"Prawn Balchão","emoji":"🦐","where":"Fisherman's Wharf, local homes","price":"₹300–₹500","must_try":True,"description":"Fiery, vinegar-pickled prawn preparation with Goan masala — bold, sour and unforgettable."},
        {"rank":3,"dish":"Pork Sorpotel","emoji":"🐷","where":"Vinayak Restaurant, local Catholic homes","price":"₹250–₹450","must_try":True,"description":"Tangy slow-cooked pork offal curry with vinegar and Goan spices — a Goan Christmas staple."},
        {"rank":4,"dish":"Bebinca","emoji":"🍮","where":"Confeitaria 31 de Janeiro, bakeries","price":"₹60–₹120","must_try":True,"description":"Layered Goan coconut-egg pudding cooked one layer at a time — takes 4 hours to make."},
        {"rank":5,"dish":"Xacuti","emoji":"🍗","where":"Traditional Goan restaurants","price":"₹200–₹380","must_try":False,"description":"Chicken or lamb in a complex sauce of roasted coconut, poppy seeds and 15+ spices."},
        {"rank":6,"dish":"Crab Xec Xec","emoji":"🦀","where":"Seafood shacks, Fisherman's Wharf","price":"₹400–₹700","must_try":False,"description":"Whole crab cooked in a spicy roasted coconut masala — finger-licking and messy."},
        {"rank":7,"dish":"Feni Cocktails","emoji":"🍹","where":"Beach shacks, local bars","price":"₹80–₹150","must_try":False,"description":"Cashew apple or coconut toddy distilled into Goa's fiery local spirit — the soul of Goa."},
        {"rank":8,"dish":"Ros Omelette","emoji":"🥚","where":"Street carts near Mapusa, Old Goa","price":"₹50–₹80","must_try":False,"description":"Fried omelette drenched in a tangy Goan curry 'ros' — the ultimate street breakfast."},
        {"rank":9,"dish":"Goan Prawn Rawa Fry","emoji":"🍤","where":"Seafood restaurants","price":"₹250–₹400","must_try":False,"description":"Semolina-coated prawns shallow-fried in coconut oil — crispy outside, juicy inside."},
        {"rank":10,"dish":"Poee Bread","emoji":"🍞","where":"Old Goa bakeries, morning markets","price":"₹5–₹15 each","must_try":False,"description":"Crusty, hollow Goan local bread made with toddy — the traditional breakfast bread of Goa."},
    ],
    "Jaipur": [
        {"rank":1,"dish":"Dal Baati Churma","emoji":"🫙","where":"Chokhi Dhani, LMB, traditional dhabas","price":"₹150–₹300","must_try":True,"description":"Hard wheat dumplings baked in a clay oven, eaten with five-lentil dal and sweet crumbled wheat churma."},
        {"rank":2,"dish":"Laal Maas","emoji":"🥩","where":"Spice Court, Handi Restaurant","price":"₹350–₹600","must_try":True,"description":"Fiery Rajasthani mutton curry with mathania red chilies — intensely spiced and deeply flavoured."},
        {"rank":3,"dish":"Pyaaz Kachori","emoji":"🧅","where":"Rawat Misthan Bhandar","price":"₹20–₹40","must_try":True,"description":"Crispy deep-fried pastry stuffed with spiced onion filling — Jaipur's most beloved street snack."},
        {"rank":4,"dish":"Ghewar","emoji":"🍯","where":"LMB, Rawat, sweet shops","price":"₹60–₹150","must_try":False,"description":"Latticed disc-shaped sweet soaked in sugar syrup and topped with rabri and saffron — a Jaipur festive must."},
        {"rank":5,"dish":"Ker Sangri","emoji":"🫛","where":"Rajasthani thali restaurants","price":"₹150–₹250","must_try":False,"description":"Dried desert beans and berries cooked with spices — a Rajasthani desert survival food now a delicacy."},
        {"rank":6,"dish":"Mirchi Bada","emoji":"🌶️","where":"Street stalls near Johri Bazaar","price":"₹15–₹30","must_try":False,"description":"Large green chili stuffed with spiced potato, battered and deep-fried — hot and crispy."},
        {"rank":7,"dish":"Mawa Kachori","emoji":"🥐","where":"LMB Sweets, Rawat","price":"₹30–₹60","must_try":False,"description":"Sweet fried pastry stuffed with mawa (milk solids) and dry fruits — a Rajasthani dessert kachori."},
        {"rank":8,"dish":"Rajasthani Thali","emoji":"🍱","where":"Chokhi Dhani, Natraj Restaurant","price":"₹250–₹500","must_try":False,"description":"An unlimited spread of gatta curry, baati, dal, kadhi, and desserts — a complete Rajasthani meal."},
        {"rank":9,"dish":"Malpua","emoji":"🥞","where":"Sweet shops during festivals","price":"₹20–₹40","must_try":False,"description":"Soft, sweet pancakes fried in ghee and soaked in sugar syrup — served during Holi and Diwali."},
        {"rank":10,"dish":"Missi Roti","emoji":"🫓","where":"Dhabas and local restaurants","price":"₹30–₹60","must_try":False,"description":"Gram flour and wheat flatbread with fenugreek and spices — a nutritious Rajasthani staple."},
    ],
    "Kochi": [
        {"rank":1,"dish":"Kerala Fish Curry","emoji":"🐟","where":"Kayees Biryani Hotel, local homes","price":"₹150–₹300","must_try":True,"description":"Red coconut milk curry with kudampuli (Gamboge) giving it a distinctive tangy depth."},
        {"rank":2,"dish":"Appam & Stew","emoji":"🥞","where":"Coastal home restaurants","price":"₹120–₹200","must_try":True,"description":"Lacy fermented rice hoppers with a mild coconut milk and vegetable or chicken stew."},
        {"rank":3,"dish":"Kerala Prawn Moilee","emoji":"🦐","where":"Fort Kochi seafood restaurants","price":"₹300–₹500","must_try":False,"description":"Gently spiced coconut milk prawn curry — light, aromatic and quintessentially Kerala."},
        {"rank":4,"dish":"Puttu & Kadala Curry","emoji":"🫙","where":"Kerala breakfast spots","price":"₹60–₹100","must_try":True,"description":"Steamed rice flour cylinders with layered coconut, served with spicy black chickpea curry."},
        {"rank":5,"dish":"Karimeen Pollichathu","emoji":"🐠","where":"Backwater restaurants, Alleppey","price":"₹300–₹500","must_try":False,"description":"Pearl spot fish marinated in masala and grilled in banana leaf — Kerala's signature fish dish."},
        {"rank":6,"dish":"Beef Fry (Ularthiyathu)","emoji":"🥩","where":"Christian home restaurants, local toddy shops","price":"₹200–₹350","must_try":False,"description":"Slow-cooked dry beef with coconut pieces and spices — a Kerala Christian household staple."},
        {"rank":7,"dish":"Sadya (Onam Feast)","emoji":"🍱","where":"Traditional restaurants during festivals","price":"₹200–₹400","must_try":False,"description":"20+ dishes on a banana leaf — avial, thoran, sambar, payasam, and more — the pinnacle of Kerala cuisine."},
        {"rank":8,"dish":"Chemmeen (Prawn) Thoran","emoji":"🥬","where":"Kerala restaurants","price":"₹200–₹350","must_try":False,"description":"Stir-fried prawns with grated coconut, curry leaves and mustard — simple, fragrant, delicious."},
        {"rank":9,"dish":"Tapioca & Fish Curry","emoji":"🍠","where":"Local Kerala eateries","price":"₹80–₹150","must_try":False,"description":"Boiled tapioca (kappa) eaten with a fiery red fish curry — the comfort food of Kerala's coast."},
        {"rank":10,"dish":"Payasam","emoji":"🍮","where":"Every Kerala restaurant & sweet shop","price":"₹60–₹120","must_try":False,"description":"Coconut milk rice or vermicelli kheer with cardamom and cashews — Kerala's soul dessert."},
    ],
    "Pune": [
        {"rank":1,"dish":"Misal Pav","emoji":"🫙","where":"Bedekar Misal, Katakirr Misal","price":"₹80–₹150","must_try":True,"description":"Spicy sprouted moth bean curry with a fiery rassa, topped with farsan and served with pav."},
        {"rank":2,"dish":"Vada Pav","emoji":"🍔","where":"Rohit Vada Pav, street stalls","price":"₹15–₹30","must_try":True,"description":"Pune's beloved batata vada in pav — simpler and spicier than Mumbai's version."},
        {"rank":3,"dish":"Sabudana Khichdi","emoji":"🫛","where":"Brahmin households, traditional eateries","price":"₹60–₹100","must_try":False,"description":"Sago pearls cooked with peanuts and green chili — the quintessential Maharashtra fasting food."},
        {"rank":4,"dish":"Puran Poli","emoji":"🫓","where":"Traditional sweet shops, Kayani Bakery","price":"₹60–₹100","must_try":False,"description":"Flatbread stuffed with sweetened chana dal and jaggery — cooked in ghee, eaten with warm milk."},
        {"rank":5,"dish":"Mastani","emoji":"🥤","where":"Sujata Mastani, Café Goodluck","price":"₹80–₹150","must_try":False,"description":"Pune's iconic thick milkshake topped with ice cream, fruits and dry fruits — a dessert drink."},
        {"rank":6,"dish":"Kolhapuri Misal","emoji":"🌶️","where":"Kolhapuri restaurants in Pune","price":"₹80–₹150","must_try":False,"description":"Extra-spicy version of misal from Kolhapur with red garlic chutney — not for the faint-hearted."},
        {"rank":7,"dish":"Bharli Vangi","emoji":"🍆","where":"Maharashtrian restaurants","price":"₹150–₹250","must_try":False,"description":"Baby eggplants stuffed with coconut-peanut masala and slow-cooked in a semi-dry gravy."},
        {"rank":8,"dish":"Kande Pohe","emoji":"🫕","where":"Morning stalls, Pune breakfast culture","price":"₹30–₹60","must_try":False,"description":"Flattened rice cooked with onions, mustard and turmeric — the quintessential Pune morning breakfast."},
        {"rank":9,"dish":"Shreekhand","emoji":"🍮","where":"Brahmin sweet shops, Chitale Bandhu","price":"₹60–₹120","must_try":False,"description":"Hung curd whisked with sugar, saffron and cardamom — served chilled as a festive dessert."},
        {"rank":10,"dish":"Bakarwadi","emoji":"🌀","where":"Chitale Bandhu, Raju Bakarwadi","price":"₹20–₹50","must_try":False,"description":"Crispy pinwheel snack with a sweet-spicy coconut and sesame filling — a Pune iconic snack."},
    ],
    "Ahmedabad": [
        {"rank":1,"dish":"Dhokla","emoji":"🫓","where":"Agashiye, Gordhan Thal","price":"₹60–₹120","must_try":True,"description":"Steamed fermented chickpea flour cakes with mustard and curry leaf tempering — Gujarat's gift to India."},
        {"rank":2,"dish":"Gujarati Thali","emoji":"🍱","where":"Gordhan Thal, Agashiye, Vishalla","price":"₹200–₹450","must_try":True,"description":"Unlimited sweet-salty-tangy thali with rotli, dal, kadhi, shaak and the iconic Gujarati touch of sweetness."},
        {"rank":3,"dish":"Fafda Jalebi","emoji":"🍥","where":"Morning stalls across the city","price":"₹30–₹60","must_try":True,"description":"Crispy gram flour strips paired with syrupy jalebis — Ahmedabad's Sunday morning ritual."},
        {"rank":4,"dish":"Undhiyu","emoji":"🥘","where":"Gujarati restaurants (winter special)","price":"₹150–₹280","must_try":False,"description":"Slow-cooked mixed vegetable and muthia casserole with fenugreek dumplings — a Surat-origin winter dish."},
        {"rank":5,"dish":"Khandvi","emoji":"🌀","where":"Sweet shops, Gordhan Thal","price":"₹60–₹100","must_try":False,"description":"Silky gram flour rolls with coconut and sesame tempering — requires precise technique to make."},
        {"rank":6,"dish":"Sev Khamani","emoji":"🫕","where":"Locho stalls, chaat vendors","price":"₹40–₹80","must_try":False,"description":"Steamed and tempered lentil dish topped with sev and pomegranate — a Surat-style variant."},
        {"rank":7,"dish":"Shrikhand Puri","emoji":"🍮","where":"Traditional Gujarati restaurants","price":"₹100–₹180","must_try":False,"description":"Puffed fried bread served with thick saffron-cardamom hung curd — a festive Gujarati staple."},
        {"rank":8,"dish":"Lal Shak","emoji":"🌿","where":"Gujarati homes and dhabas","price":"₹80–₹140","must_try":False,"description":"Red amaranth greens stir-fried in sesame-mustard tempering — a healthy Gujarat seasonal saag."},
        {"rank":9,"dish":"Dabeli","emoji":"🌮","where":"Street vendors, Manek Chowk","price":"₹20–₹40","must_try":False,"description":"Spiced potato filling in a pav with pomegranate, sev and chutneys — a Kutch original street snack."},
        {"rank":10,"dish":"Makai No Chevdo","emoji":"🌽","where":"Snack shops across the city","price":"₹30–₹70","must_try":False,"description":"Corn poha chivda mixed with spices and nuts — a crunchy Gujarati tea-time snack."},
    ],
    "Chandigarh": [
        {"rank":1,"dish":"Amritsari Kulcha","emoji":"🫓","where":"Pal Dhaba, Gopal Sweets","price":"₹80–₹150","must_try":True,"description":"Crispy butter-baked stuffed kulcha from Amritsar influence — the signature breakfast of Punjab."},
        {"rank":2,"dish":"Butter Chicken","emoji":"🍗","where":"Pal Dhaba, Chandigarh Club","price":"₹250–₹450","must_try":True,"description":"Rich tomato-butter-cream chicken gravy — Punjab's pride and India's most exported dish."},
        {"rank":3,"dish":"Lassi","emoji":"🥛","where":"Chandigarh markets, Giani's","price":"₹60–₹120","must_try":True,"description":"Thick creamy churned yogurt drink — sweet, salty or mango — essential Punjab summer refreshment."},
        {"rank":4,"dish":"Sarson Da Saag Makki Di Roti","emoji":"🌿","where":"Traditional Punjabi restaurants (winter)","price":"₹150–₹250","must_try":False,"description":"Slow-cooked mustard greens with white butter, eaten with rustic corn flatbread — winter soul food."},
        {"rank":5,"dish":"Chole Bhature","emoji":"🫓","where":"Sindhi Sweets, Gopal Sweets","price":"₹80–₹150","must_try":False,"description":"Spiced chickpea curry with fluffy deep-fried bread — the quintessential Chandigarh lunch staple."},
        {"rank":6,"dish":"Pinni","emoji":"🍬","where":"Chandigarh sweet shops (winter)","price":"₹20–₹40 each","must_try":False,"description":"Ghee-roasted whole wheat and dry fruit balls — a Punjab winter energy booster."},
        {"rank":7,"dish":"Chilli Paneer","emoji":"🧀","where":"Chinese-Indian restaurants citywide","price":"₹150–₹250","must_try":False,"description":"Indo-Chinese stir-fried paneer with peppers in a soy-chilli sauce — Chandigarh's favourite fusion."},
        {"rank":8,"dish":"Kheer","emoji":"🍮","where":"Sweet shops, traditional restaurants","price":"₹60–₹100","must_try":False,"description":"Slow-cooked rice milk pudding with cardamom and almonds — Punjab's festive dessert."},
        {"rank":9,"dish":"Langar (nearby Gurudwaras)","emoji":"🙏","where":"Rock Garden Gurudwara, Sector 19","price":"Free","must_try":False,"description":"Simple langar food — dal, sabzi, roti served with seva (service) to all visitors."},
        {"rank":10,"dish":"Shahi Paneer","emoji":"🧀","where":"Punjabi restaurants","price":"₹200–₹350","must_try":False,"description":"Cottage cheese cubes in a rich cashew and cream gravy — a royal Mughal-inspired preparation."},
    ],
    "Varanasi": [
        {"rank":1,"dish":"Banarasi Paan","emoji":"🌿","where":"Keshav Paan, Godowlia Chowk","price":"₹20–₹100","must_try":True,"description":"Betel leaf stuffed with rose gulkand, fennel, sweet lime and exotic fillings — end every meal with this."},
        {"rank":2,"dish":"Kachori Sabzi","emoji":"🥮","where":"Kashi Chaat Bhandar, street stalls","price":"₹30–₹60","must_try":True,"description":"Crispy dal-stuffed kachori served with aloo sabzi and chutneys — the quintessential Banaras breakfast."},
        {"rank":3,"dish":"Malaiyyo","emoji":"🍮","where":"Morning vendors near Dashashwamedh Ghat (winter)","price":"₹30–₹60","must_try":True,"description":"Airy saffron foam made from morning dew and milk — a seasonal winter dawn delicacy."},
        {"rank":4,"dish":"Chena Dahi Vada","emoji":"🫙","where":"Traditional Varanasi sweet shops","price":"₹40–₹80","must_try":False,"description":"Soft lentil dumplings in yogurt with a drizzle of sweet imli chutney — Varanasi's version of dahi vada."},
        {"rank":5,"dish":"Tamatar Chaat","emoji":"🍅","where":"Deena Chat Bhandar","price":"₹40–₹80","must_try":False,"description":"Tomato-based tangy chaat unique to Varanasi — no puri, just tomatoes, curd and spices."},
        {"rank":6,"dish":"Baati Chokha","emoji":"🌾","where":"Traditional eateries near the ghats","price":"₹100–₹180","must_try":False,"description":"Charcoal-roasted wheat balls with mashed, flame-roasted eggplant and tomatoes — rustic and earthy."},
        {"rank":7,"dish":"Litti Chokha","emoji":"🫙","where":"Bihar-UP style restaurants","price":"₹80–₹150","must_try":False,"description":"Roasted wheat flour balls stuffed with sattu, eaten with spiced mashed vegetables."},
        {"rank":8,"dish":"Thandai","emoji":"🥛","where":"Kashi shops, especially during Holi","price":"₹40–₹80","must_try":False,"description":"Cold spiced milk drink with rose, saffron, almonds and fennel — the Banaras ritual drink."},
        {"rank":9,"dish":"Laung Lata","emoji":"🍬","where":"Traditional sweet shops","price":"₹20–₹40","must_try":False,"description":"Fried pastry folded like a clove, filled with mawa and dry fruits — Varanasi's traditional mithai."},
        {"rank":10,"dish":"Malai Toast","emoji":"🍞","where":"Old Varanasi cafes","price":"₹40–₹80","must_try":False,"description":"Thick bread soaked in saffron-infused cream and lightly fried — a rich morning treat."},
    ],
    "Vizag": [
        {"rank":1,"dish":"Chepa Pulusu","emoji":"🐟","where":"Local Andhra restaurants","price":"₹150–₹280","must_try":True,"description":"Tangy tamarind-based fish curry with tomato and green chilies — the soul of coastal Andhra cooking."},
        {"rank":2,"dish":"Pesarattu","emoji":"🫓","where":"Breakfast hotels across the city","price":"₹60–₹100","must_try":True,"description":"Green moong dal crepes with ginger and onion stuffing — Vizag's beloved Andhra breakfast."},
        {"rank":3,"dish":"Gongura Chicken","emoji":"🌿","where":"Andhra restaurants","price":"₹250–₹400","must_try":True,"description":"Sorrel leaf-based spicy chicken curry — the tangy, bold signature of Andhra Pradesh."},
        {"rank":4,"dish":"Royyala Vepudu (Prawn Fry)","emoji":"🦐","where":"Seafood stalls near Vizag beach","price":"₹300–₹500","must_try":False,"description":"Dry-stir-fried prawns with curry leaves, coconut and Andhra spices — the beachside favourite."},
        {"rank":5,"dish":"Bamboo Chicken","emoji":"🎋","where":"Tribal area restaurants, Lambasingi","price":"₹300–₹500","must_try":False,"description":"Spiced chicken marinated and slow-cooked inside sealed bamboo over open fire — tribal Andhra specialty."},
        {"rank":6,"dish":"Bobbatlu / Puran Poli","emoji":"🫓","where":"Traditional sweet shops","price":"₹30–₹60","must_try":False,"description":"Sweet flatbread with chana dal and jaggery filling — Andhra version of Maharashtra's puran poli."},
        {"rank":7,"dish":"Ulavacharu","emoji":"🫕","where":"Traditional Andhra restaurants","price":"₹150–₹250","must_try":False,"description":"Rich broth made from horse gram — Andhra's prized super-food dal served with rice."},
        {"rank":8,"dish":"Kodi Vepudu","emoji":"🍗","where":"Andhra restaurants, local dhabas","price":"₹200–₹350","must_try":False,"description":"Dry-spiced Andhra-style chicken fry with curry leaves and crispy onions — bold and aromatic."},
        {"rank":9,"dish":"Vizag Biryani","emoji":"🍚","where":"Local biryani joints","price":"₹150–₹300","must_try":False,"description":"Andhra-style biryani with a spicier profile and green chilies compared to Hyderabadi versions."},
        {"rank":10,"dish":"Attu (Rice Crepe)","emoji":"🫔","where":"Local breakfast stalls","price":"₹40–₹80","must_try":False,"description":"Thin rice and lentil crepes eaten with andhra-style coconut chutney and sambar."},
    ],
    "Madurai": [
        {"rank":1,"dish":"Mutton Kari Dosa","emoji":"🫔","where":"Famous Annaachi Kadai, Murugan Idli","price":"₹120–₹200","must_try":True,"description":"Crispy dosa stuffed with spiced mutton keema — Madurai's unique and meaty take on the classic dosa."},
        {"rank":2,"dish":"Jigarthanda","emoji":"🧋","where":"Famous Jigarthanda shops near Meenakshi","price":"₹40–₹80","must_try":True,"description":"Madurai's iconic cold drink with milk, almond gum, nannari syrup and ice cream — unlike anything else."},
        {"rank":3,"dish":"Madurai Biryani","emoji":"🍚","where":"Amma Mess, Thilaga Biryani","price":"₹120–₹250","must_try":True,"description":"Short-grain seeraga samba rice biryani cooked in earthy spices and raw-cut onions — distinct from other biryanis."},
        {"rank":4,"dish":"Parotta & Salna","emoji":"🫓","where":"Street side parotta stalls","price":"₹60–₹120","must_try":False,"description":"Layered flaky flatbread with a thin, spicy vegetable or mutton gravy — Tamil Nadu midnight food."},
        {"rank":5,"dish":"Kari Soru (Non-Veg Rice)","emoji":"🍱","where":"Mess-style restaurants","price":"₹100–₹180","must_try":False,"description":"Steamed rice with mutton gravy, rasam and papad — simple, no-frills Tamil non-veg plate."},
        {"rank":6,"dish":"Paruthi Paal","emoji":"🥛","where":"Morning vendors near the temple","price":"₹20–₹40","must_try":False,"description":"Cotton seed milk — a Madurai traditional health drink sold on the streets."},
        {"rank":7,"dish":"Vella Dosai","emoji":"🥞","where":"Traditional Tamil sweet shops","price":"₹30–₹60","must_try":False,"description":"Sweet rice dosa made with jaggery — a festival dosa popular during Karthigai and Pongal."},
        {"rank":8,"dish":"Kothu Parotta","emoji":"🥙","where":"Night stalls, Madurai streets","price":"₹80–₹150","must_try":False,"description":"Shredded parotta stir-fried with egg and masala on an iron griddle with a rhythmic chopping sound."},
        {"rank":9,"dish":"Keerai Masiyal","emoji":"🌿","where":"Traditional Tamil restaurants","price":"₹80–₹130","must_try":False,"description":"Mashed drumstick leaves or spinach in a mild gravy — the healthiest item on the Tamil plate."},
        {"rank":10,"dish":"Adhirasam","emoji":"🍬","where":"Sweet shops, festival markets","price":"₹20–₹40 each","must_try":False,"description":"Deep-fried rice flour and jaggery donuts — a traditional Tamil festival sweet."},
    ],
    "Bhopal": [
        {"rank":1,"dish":"Bhutte Ka Kees","emoji":"🌽","where":"Street vendors near Upper Lake","price":"₹30–₹60","must_try":True,"description":"Grated raw corn cooked in milk and spices — a unique Bhopal morning street food unlike any other."},
        {"rank":2,"dish":"Keema Samosa","emoji":"🥟","where":"Old Bhopal bakeries, Chatori Gali","price":"₹20–₹40","must_try":True,"description":"Spiced minced mutton in a crispy triangular pastry — Bhopal's must-have Muslim quarter snack."},
        {"rank":3,"dish":"Biryani (Bhopali style)","emoji":"🍚","where":"Javed Hotel, Bapu Ki Kutia","price":"₹150–₹280","must_try":True,"description":"Fragrant dum biryani with a Bhopali touch of kewra water and star anise."},
        {"rank":4,"dish":"Shahi Sheermal","emoji":"🫓","where":"Old Bhopal bakeries","price":"₹30–₹60","must_try":False,"description":"Saffron-scented flatbread baked in tandoor — the royal bread of Bhopal's Nawabi tradition."},
        {"rank":5,"dish":"Bhopali Gosht Korma","emoji":"🥘","where":"Muslim heritage restaurants","price":"₹250–₹400","must_try":False,"description":"Slow-cooked mutton in a rich yogurt and cashew nut gravy with Nawabi spicing."},
        {"rank":6,"dish":"Dal Bafla","emoji":"🫙","where":"Traditional Malwa restaurants","price":"₹120–₹200","must_try":False,"description":"Baked wheat dumplings served with five-lentil dal and ghee — Madhya Pradesh's cousin of Rajasthani dal baati."},
        {"rank":7,"dish":"Seekh Kebab","emoji":"🥩","where":"Bazaar street stalls, weekend markets","price":"₹150–₹250","must_try":False,"description":"Charcoal-grilled minced meat skewers with a Bhopali spice blend of ratan jot and javitri."},
        {"rank":8,"dish":"Mawa Bati","emoji":"🍬","where":"Sweet shops across the city","price":"₹20–₹40 each","must_try":False,"description":"Soft fried milk solids dumplings soaked in sugar syrup — a beloved Madhya Pradesh mithai."},
        {"rank":9,"dish":"Poha Jalebi","emoji":"🍥","where":"Morning vendors, Chatori Gali","price":"₹30–₹60","must_try":False,"description":"Flattened rice cooked with onion and mustard, paired with crispy fresh jalebis — the Bhopal breakfast."},
        {"rank":10,"dish":"Chakki Ki Shak","emoji":"🫕","where":"Traditional Bhopal eateries","price":"₹80–₹150","must_try":False,"description":"Cooked wheat gluten in a spiced tomato-onion gravy — a unique Bhopali vegetarian specialty."},
    ],
    "Indore": [
        {"rank":1,"dish":"Poha Jalebi","emoji":"🍥","where":"Vijay Chaat House, Chhappan Dukaan","price":"₹30–₹60","must_try":True,"description":"Thick, fluffy beaten rice cooked with onion and curry leaves, paired with crispy jalebis — Indore's morning ritual."},
        {"rank":2,"dish":"Sabudana Khichdi","emoji":"🫛","where":"Traditional Indori shops","price":"₹40–₹80","must_try":True,"description":"Sago pearls with crushed peanuts and green chili — the Indori version is coarser and more textured."},
        {"rank":3,"dish":"Garadu Chaat","emoji":"🥔","where":"Winter street stalls across Indore","price":"₹30–₹60","must_try":True,"description":"Deep-fried yam pieces tossed with lime, black salt and cumin — a unique Indore winter street snack."},
        {"rank":4,"dish":"Bhutte Ka Kees","emoji":"🌽","where":"Sarafa Bazaar night market","price":"₹30–₹60","must_try":False,"description":"Grated corn cooked with milk, green chilies and coconut — a classic Madhya Pradesh breakfast."},
        {"rank":5,"dish":"Dahi Vada","emoji":"🫙","where":"Chaat stalls, Vijay Chaat","price":"₹50–₹90","must_try":False,"description":"Lentil dumplings soaked in yogurt with tamarind and mint chutneys — Indori chaat at its finest."},
        {"rank":6,"dish":"Namkeen (Indori style)","emoji":"🌀","where":"Vijay Namkeen, Shree brand","price":"₹20–₹50","must_try":False,"description":"Indore is the namkeen capital of India — sev, ratlami sev and chakli are must-try tea-time snacks."},
        {"rank":7,"dish":"Dal Baafle","emoji":"🫙","where":"Traditional MP restaurants","price":"₹120–₹200","must_try":False,"description":"Wheat balls baked over coal embers, served with five-dal mix and ghee — hearty and wholesome."},
        {"rank":8,"dish":"Shikanji","emoji":"🍋","where":"Street vendors during summer","price":"₹20–₹40","must_try":False,"description":"Chilled lemonade with black salt, cumin and ginger — Indore's go-to summer street drink."},
        {"rank":9,"dish":"Mawa Bafla","emoji":"🍬","where":"Indore sweet shops","price":"₹20–₹40","must_try":False,"description":"Sweet fried dough balls soaked in sugar syrup — a Madhya Pradesh favourite."},
        {"rank":10,"dish":"Biryani (Indori style)","emoji":"🍚","where":"Local biryani joints","price":"₹120–₹250","must_try":False,"description":"Spiced rice biryani with a Malwa region twist — slightly lighter than Hyderabadi, aromatic."},
    ],
    "Agra": [
        {"rank":1,"dish":"Petha","emoji":"🍬","where":"Panchhi Petha, Old Agra","price":"₹20–₹100","must_try":True,"description":"Translucent white gourd candy in 20+ flavours — angoori, kesar, pan — Agra's world-famous sweet."},
        {"rank":2,"dish":"Mughlai Chicken","emoji":"🍗","where":"Pinch of Spice, Peshawri","price":"₹350–₹600","must_try":True,"description":"Slow-cooked chicken in a Mughal-era spice blend with mace, rose water and fried onions."},
        {"rank":3,"dish":"Dalmoth","emoji":"🌀","where":"Sweet shops near Taj Mahal area","price":"₹30–₹80","must_try":False,"description":"Spicy fried lentil and peanut mixture — Agra's quintessential savoury snack."},
        {"rank":4,"dish":"Bedai & Jalebi","emoji":"🍥","where":"Morning street stalls","price":"₹40–₹80","must_try":False,"description":"Spicy stuffed kachori with urad dal filling, paired with crispy jalebis — the Agra breakfast combo."},
        {"rank":5,"dish":"Mutton Biryani (Mughlai)","emoji":"🍚","where":"Mughal-era style restaurants","price":"₹200–₹350","must_try":False,"description":"Rich saffron-scented biryani with tender mutton, reflecting Agra's royal Mughal heritage."},
        {"rank":6,"dish":"Gajak","emoji":"🍫","where":"Agra sweet shops (winter)","price":"₹20–₹60","must_try":False,"description":"Sesame and jaggery brittle — a winter sweet also popular during Makar Sankranti."},
        {"rank":7,"dish":"Chaat (Agra style)","emoji":"🥗","where":"Deviram's Chaat, street stalls","price":"₹30–₹60","must_try":False,"description":"Agra-style tangy chaat with golgappes and aloo tikki — with a distinct pungent tamarind chutney."},
        {"rank":8,"dish":"Tandoori Roti & Dal","emoji":"🫓","where":"Local dhabas near the Taj","price":"₹80–₹150","must_try":False,"description":"Simple whole-wheat tandoor bread with yellow lentil dal — the everyman's Agra meal."},
        {"rank":9,"dish":"Korma (Agra Mughlai)","emoji":"🥘","where":"Traditional restaurants","price":"₹300–₹500","must_try":False,"description":"Rich almond and poppy seed-based mutton gravy — a recipe tracing back to the Mughal royal kitchen."},
        {"rank":10,"dish":"Sohan Papdi","emoji":"🍬","where":"Sweet shops citywide","price":"₹20–₹60","must_try":False,"description":"Flaky, melt-in-the-mouth cardamom sweet — the famous gift box sweet of Agra."},
    ],
}

# Curated coordinates for famous restaurants in each city
CITY_COORDS = {
    "Hyderabad": (17.3850, 78.4867),
    "Chennai":   (13.0827, 80.2707),
    "Mumbai":    (19.0760, 72.8777),
    "Delhi":     (28.6139, 77.2090),
    "Bengaluru": (12.9716, 77.5946),
    "Kolkata":   (22.5726, 88.3639),
    "Lucknow":   (26.8467, 80.9462),
    "Amritsar":  (31.6340, 74.8723),
    "Goa":       (15.2993, 74.1240),
    "Jaipur":    (26.9124, 75.7873),
    "Kochi":     (9.9312,  76.2673),
    "Indore":    (22.7196, 75.8577),
    "Pune":      (18.5204, 73.8567),
    "Ahmedabad": (23.0225, 72.5714),
    "Chandigarh":(30.7333, 76.7794),
    "Varanasi":  (25.3176, 82.9739),
    "Agra":      (27.1767, 78.0081),
    "Vizag":     (17.6868, 83.2185),
    "Madurai":   (9.9252,  78.1198),
    "Bhopal":    (23.2599, 77.4126),
}

FAMOUS_RESTAURANTS = {
    "Hyderabad": [
        {"name": "Paradise Biryani", "lat": 17.4484, "lon": 78.4952, "specialty": "Dum Biryani", "type": "Biryani"},
        {"name": "Shah Ghouse Café", "lat": 17.3616, "lon": 78.4747, "specialty": "Haleem & Biryani", "type": "Mughlai"},
        {"name": "Nimrah Café", "lat": 17.3596, "lon": 78.4756, "specialty": "Irani Chai & Osmania Biscuits", "type": "Irani"},
        {"name": "Bawarchi", "lat": 17.4007, "lon": 78.4769, "specialty": "Pathar Gosht", "type": "Mughlai"},
        {"name": "Hotel Shadab", "lat": 17.3620, "lon": 78.4761, "specialty": "Dum Biryani & Haleem", "type": "Mughlai"},
        {"name": "Chutneys", "lat": 17.4265, "lon": 78.4489, "specialty": "South Indian Breakfast", "type": "South Indian"},
        {"name": "Pista House", "lat": 17.3630, "lon": 78.4770, "specialty": "Haleem", "type": "Mughlai"},
        {"name": "B2 (Breakfast to Biryani)", "lat": 17.4503, "lon": 78.3820, "specialty": "Fusion Biryani", "type": "Café"},
    ],
    "Chennai": [
        {"name": "Murugan Idli Shop", "lat": 13.0490, "lon": 80.2141, "specialty": "Idli & Sambar", "type": "South Indian"},
        {"name": "Saravana Bhavan", "lat": 13.0731, "lon": 80.2609, "specialty": "Thali & Dosas", "type": "South Indian"},
        {"name": "Hotel Palmgrove", "lat": 13.0570, "lon": 80.2458, "specialty": "Chettinad Cuisine", "type": "Chettinad"},
        {"name": "Ratna Café", "lat": 13.0730, "lon": 80.2610, "specialty": "Filter Coffee & Idlis", "type": "Traditional"},
        {"name": "Junior Kuppanna", "lat": 13.0530, "lon": 80.2491, "specialty": "Biriyani & Chettinad", "type": "Biryani"},
        {"name": "Dakshin (ITC)", "lat": 13.0602, "lon": 80.2572, "specialty": "Coastal South Indian", "type": "Fine Dining"},
    ],
    "Mumbai": [
        {"name": "Britannia & Co.", "lat": 18.9288, "lon": 72.8356, "specialty": "Berry Pulao & Dhansak", "type": "Parsi"},
        {"name": "Leopold Café", "lat": 18.9219, "lon": 72.8325, "specialty": "Continental & Cocktails", "type": "Café"},
        {"name": "Trishna", "lat": 18.9322, "lon": 72.8346, "specialty": "Seafood", "type": "Seafood"},
        {"name": "Bademiya", "lat": 18.9227, "lon": 72.8326, "specialty": "Seekh Kebabs", "type": "Street Food"},
        {"name": "Café Mondegar", "lat": 18.9225, "lon": 72.8333, "specialty": "Goan & Continental", "type": "Café"},
        {"name": "Swati Snacks", "lat": 18.9712, "lon": 72.8095, "specialty": "Gujarati Street Food", "type": "Street Food"},
        {"name": "Sarjan Restaurant", "lat": 19.0560, "lon": 73.0002, "specialty": "Malvani Seafood", "type": "Seafood"},
    ],
    "Delhi": [
        {"name": "Karim's", "lat": 28.6555, "lon": 77.2333, "specialty": "Mutton Korma & Seekh Kebab", "type": "Mughlai"},
        {"name": "Al Jawahar", "lat": 28.6549, "lon": 77.2330, "specialty": "Old Delhi Mughlai", "type": "Mughlai"},
        {"name": "Bukhara (ITC Maurya)", "lat": 28.5993, "lon": 77.1710, "specialty": "Dal Bukhara & Tandoori", "type": "Fine Dining"},
        {"name": "Paranthe Wali Gali", "lat": 28.6557, "lon": 77.2303, "specialty": "Stuffed Paranthas", "type": "Street Food"},
        {"name": "Moti Mahal", "lat": 28.6557, "lon": 77.2293, "specialty": "Butter Chicken (original)", "type": "Mughlai"},
        {"name": "Indian Accent", "lat": 28.5933, "lon": 77.1967, "specialty": "New Indian Cuisine", "type": "Fine Dining"},
    ],
    "Bengaluru": [
        {"name": "MTR (Mavalli Tiffin Room)", "lat": 12.9433, "lon": 77.5787, "specialty": "Rava Idli & Filter Coffee", "type": "South Indian"},
        {"name": "Vidyarthi Bhavan", "lat": 12.9431, "lon": 77.5815, "specialty": "Masala Dosa", "type": "South Indian"},
        {"name": "CTR (Central Tiffin Room)", "lat": 13.0082, "lon": 77.5576, "specialty": "Benne Masala Dosa", "type": "South Indian"},
        {"name": "Empire Restaurant", "lat": 12.9716, "lon": 77.6012, "specialty": "Biryani & Kebabs", "type": "Biryani"},
        {"name": "Koshy's", "lat": 12.9753, "lon": 77.6083, "specialty": "Anglo-Indian", "type": "Café"},
        {"name": "Toit Brewpub", "lat": 12.9747, "lon": 77.6090, "specialty": "Craft Beer & Burgers", "type": "Brewpub"},
    ],
    "Goa": [
        {"name": "Fisherman's Wharf", "lat": 15.5070, "lon": 73.9710, "specialty": "Goan Seafood", "type": "Seafood"},
        {"name": "Vinayak Family Restaurant", "lat": 15.5537, "lon": 73.7605, "specialty": "Pork Sorpotel & Fish Curry", "type": "Goan"},
        {"name": "Britto's", "lat": 15.5517, "lon": 73.7620, "specialty": "Seafood & Goan Specials", "type": "Seafood"},
        {"name": "Thalassa", "lat": 15.6053, "lon": 73.7382, "specialty": "Greek-Goan Fusion", "type": "Fusion"},
        {"name": "Ritz Classic", "lat": 15.4909, "lon": 73.8278, "specialty": "Goan Thali & Fish Curry Rice", "type": "Goan"},
    ],
    "Jaipur": [
        {"name": "Laxmi Misthan Bhandar (LMB)", "lat": 26.9196, "lon": 75.8298, "specialty": "Rajasthani Thali & Ghewar", "type": "Rajasthani"},
        {"name": "Chokhi Dhani", "lat": 26.8130, "lon": 75.8298, "specialty": "Authentic Rajasthani Thali", "type": "Rajasthani"},
        {"name": "Niro's", "lat": 26.9142, "lon": 75.8237, "specialty": "North Indian & Continental", "type": "Multi-cuisine"},
        {"name": "Rawat Misthan Bhandar", "lat": 26.9095, "lon": 75.8180, "specialty": "Pyaaz Kachori & Sweets", "type": "Street Food"},
    ],
    "Kolkata": [
        {"name": "Peter Cat", "lat": 22.5508, "lon": 88.3517, "specialty": "Chelo Kebab", "type": "Continental"},
        {"name": "Flurys", "lat": 22.5499, "lon": 88.3510, "specialty": "English Breakfast & Pastries", "type": "Café"},
        {"name": "Kewpie's Kitchen", "lat": 22.5252, "lon": 88.3598, "specialty": "Bengali Home Cooking", "type": "Bengali"},
        {"name": "Arsalan", "lat": 22.5205, "lon": 88.3710, "specialty": "Kolkata Biryani", "type": "Biryani"},
    ],
    "Lucknow": [
        {"name": "Tunday Kababi", "lat": 26.8621, "lon": 80.9123, "specialty": "Galouti Kebab", "type": "Mughlai"},
        {"name": "Wahid Biryani", "lat": 26.8679, "lon": 80.9209, "specialty": "Lucknawi Biryani", "type": "Biryani"},
        {"name": "Idris ki Biryani", "lat": 26.8610, "lon": 80.9200, "specialty": "Pakki Biryani", "type": "Biryani"},
        {"name": "Dastarkhwan", "lat": 26.8434, "lon": 80.9341, "specialty": "Awadhi Cuisine", "type": "Mughlai"},
    ],
    "Amritsar": [
        {"name": "Langar (Golden Temple)", "lat": 31.6200, "lon": 74.8765, "specialty": "Free Community Meal", "type": "Traditional"},
        {"name": "Bharawan Da Dhaba", "lat": 31.6241, "lon": 74.8756, "specialty": "Amritsari Kulcha & Dal Makhani", "type": "Dhaba"},
        {"name": "Brothers' Dhaba", "lat": 31.6248, "lon": 74.8753, "specialty": "Amritsari Fish & Kulcha", "type": "Dhaba"},
        {"name": "Kesar Da Dhaba", "lat": 31.6232, "lon": 74.8748, "specialty": "Dal Makhani & Paneer", "type": "Dhaba"},
    ],
}

# Default fallback with a few generic entries
DEFAULT_RESTAURANTS = [
    {"name": "Famous Local Restaurant 1", "lat": 0, "lon": 0, "specialty": "Local Specialties", "type": "Traditional"},
]

TYPE_COLORS = {
    "Biryani":     "#E23744",
    "Mughlai":     "#8B4513",
    "South Indian":"#22A05A",
    "Irani":       "#D4A017",
    "Café":        "#8B5CF6",
    "Seafood":     "#0EA5E9",
    "Street Food": "#FB923C",
    "Fine Dining": "#6366F1",
    "Parsi":       "#EC4899",
    "Rajasthani":  "#F59E0B",
    "Bengali":     "#10B981",
    "Traditional": "#64748B",
    "Dhaba":       "#92400E",
    "Goan":        "#14B8A6",
    "Brewpub":     "#A3E635",
    "Fusion":      "#F43F5E",
    "Chettinad":   "#7C3AED",
    "Multi-cuisine":"#0F766E",
    "Continental": "#2563EB",
}

with tab4:
    try:
        import folium
        from streamlit_folium import st_folium
        HAS_FOLIUM = True
    except ImportError:
        HAS_FOLIUM = False

    st.markdown("""
    <div class="sec-head" style="margin-top:4px">
      <div class="sec-head-text">🗺️ Famous & Trending Restaurant Locations</div>
      <div class="sec-head-line"></div>
    </div>""", unsafe_allow_html=True)

    if not HAS_FOLIUM:
        st.error("📦 Please install map dependencies: `pip install folium streamlit-folium`")
        st.code("pip install folium streamlit-folium", language="bash")
    else:
        # ── Controls ─────────────────────────────────────────────
        col_ctrl1, col_ctrl2, col_ctrl3 = st.columns([2, 2, 3])
        with col_ctrl1:
            map_city = st.selectbox("📍 Map City", list(CITY_COORDS.keys()),
                                    index=list(CITY_COORDS.keys()).index(city) if city in CITY_COORDS else 0,
                                    key="map_city_sel")
        with col_ctrl2:
            all_types = sorted(set(r["type"] for r in FAMOUS_RESTAURANTS.get(map_city, DEFAULT_RESTAURANTS)))
            selected_types = st.multiselect("Filter by Type", all_types, default=all_types, key="map_type_filter")
        with col_ctrl3:
            show_ai = st.toggle("📡 Include AI-detected restaurants (if available)", value=True, key="map_ai_toggle")

        restaurants = FAMOUS_RESTAURANTS.get(map_city, [])

        # Merge AI-detected restaurants from trend analysis if available
        ai_restaurants = []
        if show_ai and st.session_state.analysis and st.session_state.analysis.get("city","") == map_city:
            famous_dishes = st.session_state.analysis.get("famous_dishes_trending", [])
            center = CITY_COORDS.get(map_city, (20.5937, 78.9629))
            import random
            random.seed(42)
            for d in famous_dishes:
                rest_name = d.get("famous_at","")
                # Check if not already in curated list
                if rest_name and not any(r["name"] == rest_name for r in restaurants):
                    # Place near city center with small jitter
                    ai_restaurants.append({
                        "name": rest_name,
                        "lat": center[0] + random.uniform(-0.04, 0.04),
                        "lon": center[1] + random.uniform(-0.04, 0.04),
                        "specialty": d.get("dish_name",""),
                        "type": "AI-Detected",
                        "saves": d.get("saves_estimate",""),
                        "ai": True,
                    })

        all_restaurants = restaurants + ai_restaurants

        # Filter
        filtered = [r for r in all_restaurants if r["type"] in selected_types or r.get("ai") and "AI-Detected" in selected_types]
        # re-filter properly
        type_filter_set = set(selected_types)
        if show_ai:
            type_filter_set.add("AI-Detected")
        filtered = [r for r in all_restaurants if r["type"] in type_filter_set]

        # ── Legend ─────────────────────────────────────────────
        legend_html = '<div style="display:flex;flex-wrap:wrap;gap:8px;margin:12px 0 16px">'
        present_types = sorted(set(r["type"] for r in filtered))
        for t in present_types:
            color = TYPE_COLORS.get(t, "#64748B")
            legend_html += f'<span style="display:inline-flex;align-items:center;gap:5px;padding:4px 12px;border-radius:20px;background:{color}22;border:1px solid {color}44;font-size:11px;font-weight:600;color:{color}"><span style="width:8px;height:8px;border-radius:50%;background:{color};display:inline-block"></span>{t}</span>'
        legend_html += '</div>'
        st.markdown(legend_html, unsafe_allow_html=True)

        # ── Build Folium Map ────────────────────────────────────
        center = CITY_COORDS.get(map_city, (20.5937, 78.9629))
        m = folium.Map(
            location=center,
            zoom_start=13,
            tiles=None,
        )

        # Dark tile layer matching dashboard aesthetic
        folium.TileLayer(
            tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
            attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
            name="Dark",
            max_zoom=19,
        ).add_to(m)

        for r in filtered:
            color = TYPE_COLORS.get(r["type"], "#64748B")
            is_ai = r.get("ai", False)

            popup_html = f"""
            <div style="font-family:DM Sans,sans-serif;min-width:200px;padding:4px">
              <div style="font-size:15px;font-weight:700;color:#1C1410;margin-bottom:4px">{r['name']}</div>
              <div style="display:inline-block;padding:2px 10px;border-radius:12px;background:{color}22;
                          border:1px solid {color}66;font-size:10px;font-weight:700;color:{color};margin-bottom:8px">{r['type']}</div>
              <div style="font-size:12px;color:#57534E;margin-top:4px">🍽 <strong>Specialty:</strong> {r.get('specialty','')}</div>
              {'<div style="font-size:11px;color:#C4411A;margin-top:4px">📸 ' + r.get('saves','') + ' saves (AI trend)</div>' if is_ai else ''}
              {'<div style="font-size:10px;color:#9CA3AF;margin-top:6px;font-style:italic">⚡ AI-detected trending spot</div>' if is_ai else ''}
            </div>
            """

            icon_color = "white" if not is_ai else "orange"
            folium.CircleMarker(
                location=[r["lat"], r["lon"]],
                radius=10 if not is_ai else 8,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.85,
                weight=2,
                popup=folium.Popup(popup_html, max_width=260),
                tooltip=folium.Tooltip(
                    f"<b>{r['name']}</b><br><small>{r.get('specialty','')}</small>",
                    style="font-family:DM Sans,sans-serif;font-size:12px;background:#0D0A08;color:#F5EFE6;border:1px solid #C4411A;padding:6px 10px;border-radius:8px;"
                ),
            ).add_to(m)

        # City center marker
        folium.Marker(
            location=center,
            tooltip=f"📍 {map_city} City Centre",
            icon=folium.DivIcon(
                html=f'<div style="font-size:20px;text-align:center;margin-top:-10px">📍</div>',
                icon_size=(30, 30), icon_anchor=(15, 15),
            )
        ).add_to(m)

        # ── Render Map ─────────────────────────────────────────
        st_folium(m, width="100%", height=520, returned_objects=[])

        # ── Restaurant List Below Map ───────────────────────────
        st.markdown("""<div class="sec-head" style="margin-top:24px"><div class="sec-head-text">📋 Restaurant Directory</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)

        if filtered:
            cols_per_row = 3
            for i in range(0, len(filtered), cols_per_row):
                cols = st.columns(cols_per_row)
                for col, rest in zip(cols, filtered[i:i+cols_per_row]):
                    color = TYPE_COLORS.get(rest["type"], "#64748B")
                    ai_badge = ' <span style="font-size:9px;background:#FB923C22;color:#FB923C;padding:2px 6px;border-radius:10px;border:1px solid #FB923C44">⚡ AI</span>' if rest.get("ai") else ""
                    with col:
                        st.markdown(f"""
                        <div style="background:#FFFCF8;border:1px solid rgba(196,65,26,0.15);border-left:3px solid {color};
                                    border-radius:12px;padding:14px 16px;margin-bottom:12px;transition:all 0.2s">
                          <div style="font-size:13px;font-weight:700;color:#1C1410;margin-bottom:4px">{rest['name']}{ai_badge}</div>
                          <div style="display:inline-block;padding:2px 10px;border-radius:12px;background:{color}15;
                                      font-size:9px;font-weight:700;color:{color};margin-bottom:6px;letter-spacing:0.1em;text-transform:uppercase">{rest['type']}</div>
                          <div style="font-size:11px;color:#7A6F65">🍽 {rest.get('specialty','')}</div>
                        </div>""", unsafe_allow_html=True)
        else:
            st.info("No restaurants match the selected filters.")

        # ── Note ───────────────────────────────────────────────
        st.markdown(f"""
        <div class="status-info" style="margin-top:8px">
            🗺️ &nbsp; Showing <strong>{len(filtered)} restaurants</strong> in <strong>{map_city}</strong>
            &nbsp;·&nbsp; Curated: {len([r for r in filtered if not r.get('ai')])}
            &nbsp;·&nbsp; AI-detected: {len([r for r in filtered if r.get('ai')])}
            &nbsp;·&nbsp; Click any marker for details
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════
#  TAB 5 — CITY TOP 10 FOODS
# ════════════════════════════════════════════════════
with tab5:
    st.markdown("""
    <div class="sec-head" style="margin-top:4px">
      <div class="sec-head-text">🏙️ Top 10 Must-Try Foods by City</div>
      <div class="sec-head-line"></div>
    </div>""", unsafe_allow_html=True)

    # City selector
    top10_city = st.selectbox(
        "Choose a city to explore its top 10 iconic dishes:",
        list(CITY_TOP_10_FOODS.keys()),
        index=list(CITY_TOP_10_FOODS.keys()).index(city) if city in CITY_TOP_10_FOODS else 0,
        key="top10_city_sel"
    )

    foods = CITY_TOP_10_FOODS.get(top10_city, [])

    if foods:
        # Hero intro
        must_try_count = sum(1 for f in foods if f.get("must_try"))
        avg_price = "₹20–₹600"
        st.markdown(f"""
        <div style="background:var(--ink);border-radius:16px;padding:20px 28px;margin-bottom:24px;display:flex;align-items:center;justify-content:space-between">
          <div>
            <div style="font-size:10px;letter-spacing:0.25em;text-transform:uppercase;color:var(--spice-lt);font-weight:700;margin-bottom:8px">Curated Food Guide</div>
            <div style="font-family:'Playfair Display',serif;font-size:28px;font-weight:900;color:#F5EFE6">{top10_city}'s <em style="color:var(--gold-lt)">Food Icons</em></div>
          </div>
          <div style="display:flex;gap:24px">
            <div style="text-align:center">
              <div style="font-family:'DM Mono',monospace;font-size:28px;font-weight:500;color:var(--gold-lt)">{len(foods)}</div>
              <div style="font-size:10px;color:rgba(245,239,230,0.4);text-transform:uppercase;letter-spacing:0.12em;margin-top:4px">Dishes</div>
            </div>
            <div style="width:1px;height:50px;background:rgba(255,255,255,0.1);align-self:center"></div>
            <div style="text-align:center">
              <div style="font-family:'DM Mono',monospace;font-size:28px;font-weight:500;color:#F472B6">{must_try_count}</div>
              <div style="font-size:10px;color:rgba(245,239,230,0.4);text-transform:uppercase;letter-spacing:0.12em;margin-top:4px">Must Try</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        # Filter toggle
        show_must_try_only = st.toggle("⭐ Show Must-Try dishes only", value=False, key="must_try_toggle")
        display_foods = [f for f in foods if f.get("must_try")] if show_must_try_only else foods

        # Render food cards in grid
        for i in range(0, len(display_foods), 2):
            c1, c2 = st.columns(2)
            for col, food in zip([c1, c2], display_foods[i:i+2]):
                must_try_badge = ""
                if food.get("must_try"):
                    must_try_badge = '<span style="display:inline-block;padding:2px 10px;border-radius:20px;background:rgba(250,204,21,0.15);border:1px solid rgba(250,204,21,0.3);font-size:9px;font-weight:700;color:#FACC15;letter-spacing:0.12em;text-transform:uppercase;margin-left:8px">⭐ MUST TRY</span>'
                with col:
                    st.markdown(f"""
                    <div style="background:#FFFCF8;border:1px solid rgba(196,65,26,0.15);border-radius:16px;
                                margin-bottom:16px;overflow:hidden;transition:transform 0.2s,box-shadow 0.2s">
                      <div style="background:linear-gradient(135deg,#0D0A08 0%,#1C1410 100%);padding:16px 20px">
                        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px">
                          <div style="font-family:'DM Mono',monospace;font-size:22px;font-weight:700;color:var(--spice-lt)">#{food['rank']}</div>
                          <div style="font-size:32px">{food['emoji']}</div>
                        </div>
                        <div style="font-family:'Playfair Display',serif;font-size:18px;font-weight:700;color:#F5EFE6;line-height:1.3">
                          {food['dish']}{must_try_badge}
                        </div>
                      </div>
                      <div style="padding:16px 20px">
                        <div style="font-size:13px;color:#57534E;line-height:1.7;margin-bottom:12px">{food['description']}</div>
                        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
                          <div style="background:rgba(196,65,26,0.04);border:1px solid rgba(196,65,26,0.1);border-radius:8px;padding:8px 12px">
                            <div style="font-size:9px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#7A6F65;margin-bottom:3px">WHERE TO EAT</div>
                            <div style="font-size:12px;font-weight:600;color:#C4411A">{food['where']}</div>
                          </div>
                          <div style="background:rgba(212,160,23,0.05);border:1px solid rgba(212,160,23,0.15);border-radius:8px;padding:8px 12px">
                            <div style="font-size:9px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#7A6F65;margin-bottom:3px">PRICE RANGE</div>
                            <div style="font-family:'DM Mono',monospace;font-size:12px;font-weight:600;color:#D4A017">{food['price']}</div>
                          </div>
                        </div>
                      </div>
                    </div>""", unsafe_allow_html=True)

        # Summary chart
        st.markdown("""<div class="sec-head" style="margin-top:8px"><div class="sec-head-text">📊 Price Range Overview</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)
        df_foods = pd.DataFrame([{
            "Dish": f"{f['emoji']} {f['dish'][:30]}",
            "Rank": f['rank'],
            "Must Try": "⭐ Must Try" if f.get("must_try") else "Good to Try",
        } for f in foods])
        fig_bar = px.bar(
            df_foods, x="Dish", y="Rank",
            color="Must Try",
            color_discrete_map={"⭐ Must Try": "#C4411A", "Good to Try": "#D4A017"},
            template="simple_white",
            title=f"Top 10 Dishes of {top10_city} — Ranked",
        )
        fig_bar.update_layout(
            height=320, margin=dict(l=0, r=0, t=40, b=0),
            plot_bgcolor="#FFFCF8", paper_bgcolor="#FFFCF8",
            font=dict(family="DM Sans", size=11),
            xaxis=dict(tickangle=-30, tickfont=dict(size=9)),
            yaxis=dict(autorange="reversed", title="Rank"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    else:
        st.info(f"Top 10 food data for {top10_city} is being curated. Check back soon!")


# ════════════════════════════════════════════════════
#  TAB 6 — RECIPE CHATBOT (No API Key Required)
# ════════════════════════════════════════════════════

# ── Built-in Recipe Knowledge Base ──────────────────
RECIPE_KB = {
    "biryani": {
        "title": "🍚 Hyderabadi Dum Biryani",
        "serves": "4-5",
        "time": "90 mins",
        "difficulty": "Medium-Hard",
        "ingredients": [
            "750g basmati rice (soaked 30 mins)",
            "1 kg mutton / chicken (bone-in)",
            "3 large onions (thinly sliced, for birista)",
            "1 cup yogurt",
            "4 tbsp ghee + 3 tbsp oil",
            "2 tsp biryani masala",
            "1 tsp red chili powder",
            "1 tsp turmeric",
            "1 tbsp ginger-garlic paste",
            "1 tsp shah jeera (caraway seeds)",
            "4-5 green cardamom, 2 black cardamom",
            "2 inch cinnamon stick, 6-8 cloves",
            "Saffron soaked in ½ cup warm milk",
            "Fresh mint & coriander leaves",
            "Salt to taste",
            "Kewra water (1 tbsp) — optional",
        ],
        "steps": [
            "**Birista (Fried Onions):** Deep-fry sliced onions in oil until golden-brown and crispy. Drain on paper. This is the soul of Hyderabadi biryani.",
            "**Marinate Meat:** Mix meat with yogurt, ginger-garlic paste, red chili, turmeric, biryani masala, half the birista, mint, coriander, 1 tbsp ghee. Marinate 2–4 hours (overnight best).",
            "**Parboil Rice:** Boil rice with whole spices (cardamom, cloves, cinnamon, shah jeera) and salt until 70% cooked (grains still have a bite). Drain immediately.",
            "**Layer:** In a heavy-bottomed pot, spread marinated meat at the bottom. Layer parboiled rice on top. Drizzle saffron milk, remaining ghee, kewra water, mint leaves, and remaining birista.",
            "**Dum:** Seal the pot with dough or tight foil. Cook on high for 5 mins, then very low heat for 35–45 mins. Place a tawa/griddle under the pot to avoid burning.",
            "**Rest & Serve:** Let rest 10 mins before opening. Gently mix from bottom. Serve with mirchi ka salan and raita.",
        ],
        "tips": [
            "70% cooked rice = when you press a grain, it breaks but still has a chalky white center",
            "Never skip birista — it adds the signature sweetness and colour",
            "Seal tightly for proper dum — steam is everything",
            "Use Daawat/India Gate Extra Long basmati for best results",
            "If meat is raw at top, add ¼ cup water and dum for 10 more mins",
        ],
        "variations": "Chicken biryani: marinate 45 mins, dum for 25 mins. Veg biryani: replace meat with mixed vegetables + paneer. Kolkata biryani: add boiled egg and potato.",
    },
    "butter chicken": {
        "title": "🍗 Butter Chicken (Murgh Makhani)",
        "serves": "4",
        "time": "45 mins",
        "difficulty": "Easy-Medium",
        "ingredients": [
            "700g chicken (boneless, cubed)",
            "**Marinade:** 1 cup yogurt, 1 tsp red chili, 1 tsp garam masala, 1 tbsp ginger-garlic paste, 1 tbsp lemon juice, 1 tbsp oil",
            "**Makhani Sauce:** 4 large tomatoes (pureed), 1 large onion, ½ cup cashews (soaked)",
            "3 tbsp butter + 2 tbsp oil",
            "1 cup fresh cream",
            "1 tsp kasuri methi (dried fenugreek leaves) — the SECRET ingredient",
            "1 tsp sugar",
            "1 tsp red chili powder, 1 tsp coriander powder",
            "½ tsp garam masala",
            "Salt to taste",
        ],
        "steps": [
            "**Marinate & Grill:** Marinate chicken for 2 hours. Grill in oven at 220°C for 20 mins or cook in tandoor/air fryer until slightly charred. Set aside.",
            "**Make Base:** Sauté onions in butter+oil until golden. Add ginger-garlic paste, cook 2 mins. Add tomato puree and cashew paste, cook on medium until oil separates (~15 mins).",
            "**Blend:** Cool and blend the base until silky smooth. Strain through a sieve for restaurant texture.",
            "**Build the Makhani:** Return strained sauce to pan. Add red chili, coriander powder. Simmer 5 mins. Add grilled chicken.",
            "**Finish:** Add cream, sugar, kasuri methi (crush between palms before adding). Simmer 5 mins. Add butter at the end for gloss.",
            "Serve with butter naan or jeera rice.",
        ],
        "tips": [
            "Kasuri methi is non-negotiable — it's what makes butter chicken taste like a restaurant",
            "Straining the sauce is the difference between home and restaurant quality",
            "The char on chicken is essential — don't skip grilling",
            "Add a pinch of beetroot powder for that signature orange-red colour naturally",
            "Sugar balances the tomato acidity — don't skip it",
        ],
        "variations": "Veg version: replace chicken with paneer cubes + mushrooms. Malai Kofta: use kofta balls instead. Dhaba style: skip cream, use more butter.",
    },
    "dosa": {
        "title": "🫔 Perfect Crispy Masala Dosa",
        "serves": "8-10 dosas",
        "time": "Batter: 8 hrs ferment | Cook: 30 mins",
        "difficulty": "Medium",
        "ingredients": [
            "**Dosa Batter:** 3 cups idli rice (or parboiled rice), 1 cup urad dal, ½ tsp fenugreek seeds",
            "Salt to taste",
            "**Potato Masala:** 4 large potatoes (boiled, mashed), 2 onions (sliced), 2 green chilies",
            "1 tsp mustard seeds, 1 tsp chana dal, 1 tsp urad dal",
            "8-10 curry leaves, 1 tsp turmeric, 2 tbsp oil",
            "Fresh coriander, salt to taste",
            "**For cooking:** Oil or ghee for the tawa",
        ],
        "steps": [
            "**Soak:** Soak rice and urad dal+fenugreek separately for 6-8 hours.",
            "**Grind:** Grind urad dal first until fluffy and white (add ice-cold water). Grind rice coarser. Mix both, add salt. Batter should coat a spoon.",
            "**Ferment:** Cover and keep in a warm place for 8-12 hours until batter doubles and smells slightly sour.",
            "**Masala:** Temper mustard seeds, dals, curry leaves in oil. Add onions, sauté until soft. Add green chilies, turmeric, mashed potatoes. Mix well. Set aside.",
            "**Cook Dosa:** Heat cast iron tawa until very hot. Sprinkle water — it should evaporate instantly. Add a drop of oil. Pour a ladle of batter in the center. Spread in circular motion outward quickly.",
            "**Crisp it:** Drizzle oil/ghee on edges and top. Cook on medium-high until edges lift and bottom is golden-brown. Add masala, fold and serve immediately.",
        ],
        "tips": [
            "Ice-cold water while grinding urad dal = fluffier batter (the cold prevents overheating)",
            "The tawa temperature is everything — too cold = batter sticks; too hot = spreads unevenly",
            "Fermentation is key — warm oven (light on) works great in winter",
            "Never wash the tawa with soap — season it with oil after every use",
            "Leftover batter: refrigerate up to 4 days, it gets more sour and crispy",
        ],
        "variations": "Neer Dosa: thin rice-only batter, no fermentation. Rava Dosa: semolina, rice flour, no fermentation (instant). Set Dosa: thick and soft, Bengaluru style. Pesarattu: moong dal dosa, Andhra style.",
    },
    "haleem": {
        "title": "🥘 Hyderabadi Haleem",
        "serves": "6-8",
        "time": "4-5 hours (slow cook)",
        "difficulty": "Hard",
        "ingredients": [
            "500g mutton (boneless, with some bone)",
            "½ cup broken wheat (dalia)",
            "¼ cup chana dal, ¼ cup masoor dal, ¼ cup moong dal",
            "2 large onions (for birista)",
            "1 tbsp ginger-garlic paste",
            "2 tsp red chili powder, 1 tsp turmeric",
            "2 tsp haleem masala (or garam masala)",
            "½ cup yogurt",
            "4 tbsp ghee",
            "**Garnish:** Fried onions, fresh lime, mint, coriander, green chilies",
        ],
        "steps": [
            "**Soak:** Soak broken wheat and all dals together for 1 hour.",
            "**Cook Wheat & Dals:** Pressure cook wheat+dals with 4 cups water and turmeric for 4-5 whistles until completely mushy.",
            "**Cook Meat:** In a heavy pot, cook mutton with ginger-garlic paste, red chili, yogurt, haleem masala and salt until meat is falling off the bone (45 mins pressure or 2 hrs open).",
            "**Shred:** Remove bones. Shred/pull the mutton apart with two forks.",
            "**Combine & Bhunao:** Add mushy dals+wheat to the mutton pot. Stir and bhuno (stir-fry) constantly on medium heat, breaking down the mixture until it becomes a thick, smooth paste. This takes 30-40 mins.",
            "**Tarka:** Pour sizzling ghee tempered with whole spices over the haleem.",
            "Serve topped with birista, lime, mint, green chilies and coriander.",
        ],
        "tips": [
            "The bhunao step is what makes haleem — you must stir it until it becomes one unified mass",
            "Add ghee generously at the end — haleem should be slightly glossy",
            "Lemon at serving time is non-negotiable",
            "Haleem tastes even better the next day",
            "Pista House Hyderabad style: they use more wheat than dal for a thicker texture",
        ],
        "variations": "Kheema Haleem: use minced meat for faster cooking. Veg Haleem: replace meat with mushrooms + soya chunks. Chicken Haleem: 1.5 hrs instead of 4+ hrs.",
    },
    "idli": {
        "title": "🫓 Fluffy Idli & Sambar",
        "serves": "20 idlis",
        "time": "Batter: overnight | Steam: 15 mins",
        "difficulty": "Easy",
        "ingredients": [
            "**Idli Batter:** 2 cups idli rice, 1 cup urad dal, ½ tsp fenugreek seeds",
            "Salt to taste, water as needed",
            "**Sambar:** ½ cup toor dal (pigeon peas), 2 tomatoes, 1 drumstick (moringa)",
            "1 small onion, 1 tsp tamarind paste",
            "2 tsp sambar powder, 1 tsp turmeric",
            "**Sambar Tarka:** Mustard, curry leaves, dry red chili, asafoetida (hing), oil",
        ],
        "steps": [
            "**Soak:** Soak rice and (urad dal + fenugreek) separately for 6 hours.",
            "**Grind:** Grind urad dal with ice-cold water until very fluffy and airy (10-12 mins in wet grinder). Grind rice coarsely. Mix, add salt. Batter should be thick but pourable.",
            "**Ferment:** Leave covered at room temperature 10-14 hours (or overnight). It should rise and have tiny bubbles.",
            "**Steam:** Grease idli moulds. Pour batter ¾ full. Steam in idli cooker for exactly 10-12 mins. Test with a wet finger — it should come out clean.",
            "**Sambar:** Pressure cook toor dal with tomatoes and turmeric (3 whistles). Add drumstick, onion, tamarind, sambar powder. Simmer 15 mins. Finish with tarka.",
            "Serve hot idlis with sambar and fresh coconut chutney.",
        ],
        "tips": [
            "MTR secret: they use a 2:1 ratio of rice to urad dal. Some use 3:1 for crispier idlis.",
            "The urad dal must be ground until completely white and fluffy — this traps air",
            "Over-fermented batter = sour idlis. Under-fermented = dense idlis",
            "Wet your finger before testing — a dry finger sticks to idli",
            "Don't open the steamer during cooking — the steam drop ruins texture",
        ],
        "variations": "Rava Idli (MTR style): no fermentation, instant. Kanchipuram Idli: with pepper and cumin. Mini Button Idli: for kids. Stuffed Idli: with cheese or vegetable filling.",
    },
    "chole": {
        "title": "🫘 Authentic Punjabi Chole Bhature",
        "serves": "4",
        "time": "30 mins (+ soaking)",
        "difficulty": "Easy",
        "ingredients": [
            "2 cups white chickpeas (soaked overnight)",
            "2 tea bags (for dark colour) — the restaurant secret",
            "3 large onions (2 for paste, 1 sliced)",
            "3 tomatoes (pureed)",
            "1 tbsp ginger-garlic paste",
            "2 tsp chole masala (Everest/MDH)",
            "1 tsp anardana (pomegranate powder)",
            "1 tsp amchur (dry mango powder)",
            "1 tsp red chili powder, 1 tsp turmeric",
            "1 tsp cumin seeds, 2 tbsp oil",
            "**Bhature:** 2 cups maida, ½ cup yogurt, 1 tsp baking powder, salt, oil for deep frying",
        ],
        "steps": [
            "**Cook Chickpeas:** Pressure cook soaked chickpeas with tea bags, salt and water for 5-6 whistles until very soft. Remove tea bags.",
            "**Make Masala:** Sauté cumin in oil. Add sliced onions, cook until golden. Add ginger-garlic paste. Add onion paste (blended raw onions). Cook until raw smell goes.",
            "**Add Tomatoes:** Add tomato puree, all spice powders. Bhuno (stir-fry) until oil separates (~10 mins).",
            "**Combine:** Add cooked chickpeas with their water. Simmer 15-20 mins. Mash some chickpeas against the pot for thick gravy. Add anardana and amchur at the end.",
            "**Bhature:** Mix maida, yogurt, baking powder, salt. Knead soft dough. Rest 30 mins. Roll slightly thick. Deep fry in hot oil — it puffs up immediately.",
            "Serve with raw onion, green chili, pickle and lemon.",
        ],
        "tips": [
            "Tea bags give the authentic dark grey-brown colour — without it, chole looks yellow",
            "Anardana is what gives Punjabi chole its signature tangy depth — don't skip",
            "Bhature must be fried in very hot oil — it should puff within 3 seconds",
            "Mash 20% of chickpeas for naturally thick gravy without any flour",
            "Sita Ram Diwan Chand (Delhi) secret: they add ½ tsp black cardamom powder",
        ],
        "variations": "Amritsari Chole: served with kulcha instead of bhature. Pindi Chole: dry version with pomegranate seeds. Vegan Chole: already vegan — just skip the yogurt in bhature, use water.",
    },
    "dal makhani": {
        "title": "🫕 Dal Makhani (Bukhara Style)",
        "serves": "4-6",
        "time": "Overnight slow cook ideal | 3 hrs minimum",
        "difficulty": "Easy (but requires patience)",
        "ingredients": [
            "1 cup whole black urad dal (whole black lentils)",
            "¼ cup kidney beans (rajma)",
            "2 large tomatoes (pureed) + 1 tbsp tomato paste",
            "1 large onion (finely chopped)",
            "1 tbsp ginger-garlic paste",
            "100g butter (4 tbsp)",
            "½ cup heavy cream",
            "1 tsp red chili powder, 1 tsp coriander powder",
            "½ tsp garam masala",
            "Salt to taste",
        ],
        "steps": [
            "**Soak:** Soak black dal and rajma together overnight (8+ hours).",
            "**First Cook:** Pressure cook with salt for 8-10 whistles until completely soft and mushy. The dal should be so soft you can crush it between fingers.",
            "**Bhuno Base:** Sauté onions in butter until golden. Add ginger-garlic paste. Add tomato puree + paste. Bhuno on low-medium heat for 20-25 mins until butter floats on top.",
            "**Slow Simmer:** Add cooked dal to the masala. Stir well. Simmer on the lowest heat possible for at least 1.5-2 hours, stirring every 15 mins.",
            "**Finish:** Add cream and half the butter. Simmer 15 more mins. Add garam masala. Top with remaining butter.",
            "Serve with butter naan. The next day it tastes even better.",
        ],
        "tips": [
            "Bukhara ITC does 18+ hours of slow cooking — longer = richer, creamier dal",
            "The fat in butter emulsifies with the dal for a velvety texture",
            "Never add water after the final simmer begins — it dilutes the flavour",
            "Tomato paste (not just fresh tomatoes) gives that deep, rich base",
            "Dhungar technique: place a small piece of coal in a steel bowl in the dal, add ghee, cover — instant smoky flavour",
        ],
        "variations": "Langar Dal (without cream/butter): pure urad dal with simple tomato-cumin tarka. Quick version: 30 mins pressure + 30 mins simmer.",
    },
    "samosa": {
        "title": "🥟 Crispy Punjabi Samosa",
        "serves": "12-15 samosas",
        "time": "1 hour",
        "difficulty": "Medium",
        "ingredients": [
            "**Pastry:** 2 cups maida, ¼ tsp ajwain (carom seeds), ½ tsp salt, 4 tbsp oil/ghee, cold water to knead",
            "**Filling:** 4 boiled potatoes (mashed), ½ cup green peas",
            "1 tsp cumin seeds, 1 tsp coriander seeds (crushed)",
            "1 tsp amchur, 1 tsp red chili, ½ tsp garam masala",
            "1 tsp fennel seeds (saunf)",
            "Fresh coriander, green chili (finely chopped)",
            "Salt to taste",
            "Oil for deep frying",
        ],
        "steps": [
            "**Make Pastry:** Mix maida, salt, ajwain, oil. Rub oil into flour until it resembles breadcrumbs (this is moyan — creates flakiness). Add cold water slowly, knead into a stiff dough. Rest 20 mins.",
            "**Make Filling:** Dry-roast cumin and coriander, crush roughly. Mix with mashed potatoes, peas, amchur, chili, garam masala, fennel, coriander, green chili, salt.",
            "**Shape:** Divide dough into balls. Roll into ovals. Cut in half. Form a cone, seal edges with water. Fill, seal the top tightly into a pleated edge.",
            "**Fry:** Deep fry in medium-hot oil (160°C) — NOT hot oil. Fry slowly for 12-15 mins until golden brown and crispy. Start cold/medium oil = crispy shell.",
            "Serve with green mint chutney and tamarind chutney.",
        ],
        "tips": [
            "Moyan (oil rubbing into flour) = the KEY to flaky, non-doughy pastry",
            "Frying at low-medium temperature is the street vendor secret — slow frying = super crispy",
            "Stiff dough = crispier samosa. Soft dough = chewy and oily",
            "Amchur is essential for that tangy potato filling",
            "Seal edges very well or they'll open and absorb oil",
        ],
        "variations": "Baked samosa: brush with oil, bake 200°C 20-25 mins. Keema samosa: use spiced minced mutton. Chocolate samosa: Nutella + banana filling. Mini cocktail samosa: party size.",
    },
    "rasgulla": {
        "title": "🍡 Bengali Rasgulla (Spongy)",
        "serves": "20-25 rasgullas",
        "time": "1 hour",
        "difficulty": "Medium",
        "ingredients": [
            "1 litre full-fat milk",
            "3 tbsp lemon juice or white vinegar (to curdle)",
            "**Sugar Syrup:** 1.5 cups sugar, 5 cups water",
            "1 tsp rose water (optional)",
            "2-3 green cardamom pods",
        ],
        "steps": [
            "**Make Chenna:** Boil milk. Add lemon juice slowly while stirring until milk curdles completely. Pour through muslin cloth, rinse with cold water (removes sourness). Hang for 30 mins to drain.",
            "**Knead:** Knead the chenna on a flat surface for 8-10 mins until completely smooth and slightly greasy. No cracks = smooth rasgulla. This is the most important step.",
            "**Shape:** Roll into smooth crack-free balls (they expand 2x while cooking).",
            "**Cook Syrup:** Boil sugar + water + cardamom in a wide pot. Syrup should be thin (not sticky).",
            "**Cook Rasgullas:** Add balls to boiling syrup. Cover and cook on MEDIUM-HIGH (syrup must boil vigorously) for exactly 15-18 mins without lifting the lid.",
            "**Test:** A rasgulla is done when it doubles in size and doesn't spring back when pressed lightly.",
        ],
        "tips": [
            "Kneading is everything — under-kneaded chenna = hard/dense rasgullas",
            "The syrup must boil actively during cooking — low heat = dense and rubbery",
            "Use full-fat milk only — skimmed milk won't work",
            "Add cold water to syrup if it gets too thick while boiling",
            "K.C. Das (Kolkata) secret: they add a tiny bit of semolina to chenna for firmness",
        ],
        "variations": "Rasgulla Cake: layer rasgullas with cream. Chocolate Rasgulla: add cocoa to chenna. Rajbhog: larger stuffed version with dry fruits.",
    },
    "filter coffee": {
        "title": "☕ South Indian Filter Coffee (Degree Coffee)",
        "serves": "2 cups",
        "time": "15 mins",
        "difficulty": "Easy",
        "ingredients": [
            "3 tbsp South Indian filter coffee powder (80% coffee, 20% chicory — Cothas/Leo/Narasu's brand)",
            "1.5 cups water (for decoction)",
            "1.5 cups full-fat milk",
            "Sugar to taste",
            "**Equipment:** South Indian metal coffee filter (percolator)",
        ],
        "steps": [
            "**Brew Decoction:** Add coffee powder to the upper chamber of the filter. Pour hot water (just off boil) over it. Press the plunger lightly. Wait 15-20 mins for decoction to drip into the lower chamber. The decoction should be dark, strong and aromatic.",
            "**Heat Milk:** Boil full-fat milk until it froths. The milk quality is crucial — thin milk makes weak coffee.",
            "**Mix:** Pour 2-3 tbsp dark decoction into the tumbler (steel cup). Add hot frothing milk. Adjust ratio to taste (more decoction = stronger).",
            "**Froth (Metre Coffee):** Pour back and forth between tumbler and davara (the wide dish) from a height 5-10 times to create froth and cool it slightly.",
            "Serve in the steel tumbler-davara set. Sip from the davara — it cools faster.",
        ],
        "tips": [
            "The chicory blend is non-negotiable — it gives that unique bittersweet flavour",
            "Boil milk — don't just warm it. The slight caramelisation of hot milk is key",
            "The metre coffee (pouring from height) is a ritual — it aerates and creates the signature froth",
            "Decoction ratio: 2 tbsp per cup is standard. Adjust for strength",
            "Nimrah Café Hyderabad adds cardamom; Coorg style uses 100% coffee (no chicory)",
        ],
        "variations": "Kaapi with jaggery instead of sugar. Beaten coffee (whipped). Cold brew: steep ground coffee in cold water 12 hours, mix with cold milk.",
    },
    "lassi": {
        "title": "🥛 Authentic Punjabi Lassi",
        "serves": "2",
        "time": "5 mins",
        "difficulty": "Very Easy",
        "ingredients": [
            "2 cups thick yogurt (full-fat, freshly set)",
            "½ cup chilled water or milk",
            "3-4 tbsp sugar (or to taste)",
            "A pinch of cardamom powder",
            "**Optional toppings:** Fresh cream, a dollop of butter, rose petals, saffron",
        ],
        "steps": [
            "**Churn:** Add yogurt, water/milk, and sugar to a blender or use a traditional wooden churner (madhani).",
            "**Blend:** Blend for 2-3 mins until frothy and smooth. The more you blend = more froth.",
            "**Chill:** Add ice cubes or serve immediately with toppings.",
            "Pour into tall steel glasses (Gurdas Ram Lassiwala style) or clay kulhads.",
            "Top with a generous spoon of fresh cream and a small pat of butter for the Amritsar experience.",
        ],
        "tips": [
            "Fresh homemade yogurt churned with a madhani (wooden churner) gives the most authentic result",
            "Full-fat yogurt is essential — low-fat lassi is thin and disappointing",
            "Gurdas Ram (Amritsar) serves it in such thick glasses that a spoon can stand in it",
            "Sweet lassi: as above | Salty lassi: replace sugar with black salt and roasted cumin powder",
            "Mango lassi: add 3 tbsp alphonso mango pulp while blending",
        ],
        "variations": "Mango lassi: add aamras. Salty lassi: black salt + cumin. Rose lassi: rose syrup + cardamom. Bhang lassi (festival): traditional Holi drink with bhang (regional preparation).",
    },
    "pav bhaji": {
        "title": "🫕 Mumbai Pav Bhaji",
        "serves": "4",
        "time": "30 mins",
        "difficulty": "Easy",
        "ingredients": [
            "3 potatoes (boiled + mashed), 1 cup cauliflower (boiled)",
            "½ cup green peas (boiled), 1 capsicum (finely chopped)",
            "3 tomatoes (finely chopped), 2 onions (1 for bhaji, 1 raw for garnish)",
            "2 tbsp butter (lots of it!)",
            "2 tsp pav bhaji masala (Everest brand)",
            "1 tsp red chili powder, 1 tsp turmeric",
            "1 tbsp ginger-garlic paste",
            "Fresh coriander, lemon wedges",
            "**Pav:** 8 soft dinner rolls",
        ],
        "steps": [
            "**Start Bhaji:** Heat butter in a wide pan. Add onions, sauté until soft. Add capsicum, cook 3 mins. Add ginger-garlic paste.",
            "**Add Tomatoes:** Add tomatoes, cook until mushy and oil separates. Add pav bhaji masala, red chili, turmeric.",
            "**Add Veggies:** Add all mashed/boiled vegetables. Mix and mash together vigorously with a masher directly in the pan.",
            "**Bhuno:** Keep mashing and stirring on medium heat for 10 mins. Add ½ cup water if too thick. Keep mashing. The mashing IS the cooking.",
            "**Butter Finish:** Add more butter at the end. Top with raw onion, coriander, lemon.",
            "**Toast Pav:** Slice pav, apply butter, toast on the same hot pan until golden.",
        ],
        "tips": [
            "The masher technique: you should mash and stir simultaneously — this is Mumbai street technique",
            "Sardar Pav Bhaji (Mumbai) uses extra butter — don't hold back",
            "Cauliflower is the secret ingredient that most people skip",
            "The pan should be very hot — bhaji should sizzle loudly when mashed",
            "Add a charcoal piece and ghee for dhungar smoky flavour (optional)",
        ],
        "variations": "Jain Pav Bhaji: no onion, garlic, potato. Use raw banana instead. Cheese Pav Bhaji: add processed cheese on top. Mushroom Pav Bhaji: add mushrooms.",
    },
    "vada pav": {
        "title": "🍔 Mumbai Vada Pav",
        "serves": "8",
        "time": "30 mins",
        "difficulty": "Easy",
        "ingredients": [
            "**Batata Vada:** 4 boiled potatoes (mashed), 1 tsp mustard seeds, 8-10 curry leaves",
            "2 green chilies (finely chopped), 1 tsp ginger paste",
            "1 tsp turmeric, fresh coriander, salt",
            "**Batter:** 1 cup besan, ½ tsp turmeric, ½ tsp red chili, salt, water (thick batter)",
            "**Dry Garlic Chutney:** ½ cup dry coconut (desiccated), 8-10 garlic cloves, 2 tsp red chili, salt",
            "**Green Chutney:** Fresh coriander, green chilies, garlic, lemon",
            "8 pav (soft dinner rolls), oil for frying",
        ],
        "steps": [
            "**Vada Filling:** Temper mustard seeds in oil. Add curry leaves, ginger, green chili, turmeric. Add mashed potatoes, coriander, salt. Mix well. Cool completely. Shape into balls.",
            "**Batter:** Mix besan with spices and enough water to make a thick coating batter.",
            "**Fry:** Dip potato balls in batter, deep fry in hot oil until golden and crispy.",
            "**Dry Chutney:** Blend dry coconut, garlic, red chili, salt until coarse powder. No water.",
            "**Assemble:** Slice pav, apply green chutney on one side, dry garlic chutney on other. Place hot vada inside. Serve immediately.",
        ],
        "tips": [
            "The DRY garlic-coconut chutney is what separates authentic vada pav from copies",
            "Vada filling must be completely cooled before frying or it'll burst",
            "Ashok Vada Pav (Kirti College, Mumbai) fries in very hot oil for a super crispy shell",
            "Green chutney: coriander + garlic + green chili + lemon only — no extras",
            "Eat immediately — vada pav gets soggy within 10 mins",
        ],
        "variations": "Schezwan Vada Pav: schezwan chutney instead of green. Cheese Vada Pav: cheese slice inside. Jain version: no garlic, no onion in filling.",
    },
    "kheer": {
        "title": "🍮 Rice Kheer (Payasam)",
        "serves": "6",
        "time": "45 mins",
        "difficulty": "Easy",
        "ingredients": [
            "1 litre full-fat milk",
            "¼ cup basmati rice (or vermicelli for seviyan)",
            "½ cup sugar (or condensed milk)",
            "¼ tsp cardamom powder",
            "A pinch of saffron soaked in 2 tbsp warm milk",
            "2 tbsp cashews, almonds, pistachios (sliced)",
            "1 tsp rose water (optional)",
        ],
        "steps": [
            "**Reduce Milk:** Bring milk to boil in a heavy bottom pan. Reduce to medium and simmer, stirring every few minutes until it reduces to ¾ volume (~15 mins).",
            "**Add Rice:** Add washed rice (or soaked rice for creamier texture). Cook on low-medium, stirring often, for 25-30 mins until rice is fully cooked and milk is thick.",
            "**Sweeten:** Add sugar, stir until dissolved. Cook 5 more mins.",
            "**Finish:** Add saffron milk, cardamom, rose water. Stir. Remove from heat.",
            "Top with dry fruits. Serve warm or chilled.",
        ],
        "tips": [
            "Stir frequently — milk burns easily at the bottom (use a heavy pan)",
            "Soak rice for 30 mins for faster, creamier cooking",
            "Condensed milk instead of sugar = richer, faster kheer",
            "Refrigerate overnight for best flavour — it thickens beautifully",
            "Kerala Payasam: use jaggery instead of sugar and coconut milk instead of dairy milk",
        ],
        "variations": "Vermicelli Kheer (Seviyan): fry vermicelli in ghee first. Sabudana Kheer: sago pearls. Mango Kheer: add mango pulp after removing from heat. Carrot Halwa adjacent: add grated carrot.",
    },
    "golgappa": {
        "title": "🫙 Golgappa / Pani Puri",
        "serves": "30-35 puris",
        "time": "45 mins",
        "difficulty": "Medium",
        "ingredients": [
            "**Puri:** 1 cup rava/sooji (fine semolina), ¼ cup maida, salt, water, oil for frying",
            "**Pani (Spiced Water):** 1 cup fresh mint, ½ cup coriander, 2 green chilies",
            "2 tbsp tamarind paste, 1 tsp roasted cumin powder",
            "1 tsp black salt, ½ tsp chaat masala, sugar to taste",
            "4 cups chilled water",
            "**Filling:** 2 boiled potatoes (mashed), ½ cup boiled chickpeas",
            "Black salt, cumin powder, red chili, coriander",
        ],
        "steps": [
            "**Puri Dough:** Mix rava, maida, salt. Add just enough water to make a stiff dough. Knead well. Rest 20 mins covered.",
            "**Roll & Cut:** Roll dough very thin (1-2mm). Cut into small circles using a small cutter or bottle cap.",
            "**Fry:** Fry in medium-hot oil. Press with a spoon immediately as they go in — they puff up. Flip and fry until golden. Drain.",
            "**Pani:** Blend mint, coriander, green chili with little water. Strain. Add tamarind, black salt, cumin, chaat masala, sugar. Mix with 4 cups chilled water. Taste and adjust.",
            "**Assemble:** Make a small hole in puri, add filling, dip in chilled pani and eat immediately.",
        ],
        "tips": [
            "The puri must be pressed with a spoon as soon as it hits the oil — this is what makes it puff",
            "Rava-heavy dough = crispier puri that holds its shape in pani",
            "Pani must be ice cold — warm pani makes soggy puris",
            "Delhi pani: minty, thin, very chilled. Mumbai pani: slightly sweeter with more tamarind",
            "Kolkata phuchka: uses spiced mashed potato + mustard oil, no chickpeas",
        ],
        "variations": "Dahi puri: fill with yogurt + chutneys instead of pani. Dry puri: fill with sev + chutneys. Ragda pattis: white pea filling.",
    },
}

# ── Smart Search Function ────────────────────────────
def _search_recipe_kb(query: str):
    """Search the knowledge base and return best match."""
    q = query.lower()
    
    # Direct keyword mapping
    keyword_map = {
        "biryani": "biryani",
        "dum biryani": "biryani",
        "butter chicken": "butter chicken",
        "murgh makhani": "butter chicken",
        "makhani": "butter chicken",
        "dosa": "dosa",
        "masala dosa": "dosa",
        "idli": "idli",
        "sambar": "idli",
        "haleem": "haleem",
        "chole": "chole",
        "chhole": "chole",
        "chole bhature": "chole",
        "dal makhani": "dal makhani",
        "makhani dal": "dal makhani",
        "dal bukhara": "dal makhani",
        "samosa": "samosa",
        "rasgulla": "rasgulla",
        "filter coffee": "filter coffee",
        "coffee": "filter coffee",
        "kaapi": "filter coffee",
        "lassi": "lassi",
        "pav bhaji": "pav bhaji",
        "vada pav": "vada pav",
        "wada pav": "vada pav",
        "batata vada": "vada pav",
        "kheer": "kheer",
        "payasam": "kheer",
        "golgappa": "golgappa",
        "pani puri": "golgappa",
        "puchka": "golgappa",
        "phuchka": "golgappa",
        "gol gappe": "golgappa",
    }

    for kw, key in keyword_map.items():
        if kw in q:
            return key, RECIPE_KB[key]

    # Ingredient/topic matching
    topic_responses = {
        ("spice", "masala", "garam masala"): "spice_guide",
        ("vegetarian", "veg", "no meat", "paneer"): "veg_tip",
        ("fry", "deep fry", "oil", "frying"): "fry_tip",
        ("ferment", "batter", "idli batter", "dosa batter"): "ferment_tip",
        ("substitute", "replace", "alternative", "without"): "substitute_tip",
        ("street food", "chaat", "snack"): "street_food",
        ("sweet", "dessert", "mithai", "halwa"): "dessert_tip",
    }

    for keywords, topic in topic_responses.items():
        if any(kw in q for kw in keywords):
            return topic, None

    return None, None


def _get_topic_response(topic: str, query: str) -> str:
    topic_answers = {
        "spice_guide": """🌶️ **Essential Indian Spice Guide**

**The 10 Must-Have Spices:**
1. **Cumin (Jeera)** — earthy, warm base for almost every dish
2. **Coriander (Dhania)** — citrusy, used as powder or whole seeds  
3. **Turmeric (Haldi)** — anti-inflammatory, adds colour and earthiness
4. **Red Chili Powder** — heat level varies by region (Kashmiri = mild+colour, Mathania = hot)
5. **Garam Masala** — blend of warming spices, added at the end of cooking
6. **Mustard Seeds (Rai)** — essential for South Indian tadka/tempering
7. **Fenugreek (Methi)** — slightly bitter; seeds, leaves (kasuri methi) or fresh
8. **Cardamom (Elaichi)** — green for sweets & biryani; black for gravies
9. **Asafoetida (Hing)** — strong flavour in tempering; use sparingly
10. **Bay Leaves (Tej Patta)** — aromatic, used in biryani and kormas

**Garam Masala from Scratch:**
Dry roast and grind: 2 tbsp coriander, 1 tbsp cumin, 1 tsp black pepper, 5 cardamom, 3 cloves, 1 inch cinnamon, 2 bay leaves, ½ tsp nutmeg, ½ tsp mace.

**Regional Masala Differences:**
- **Chettinad Masala:** adds kalpasi (stone flower), marathi mokku, kalpasi
- **Goan Masala:** lots of dried red chilies + coconut vinegar base
- **Sindhi Masala:** heavy on coriander and dry mango powder
- **Biryani Masala:** adds star anise, kewra, rose petals""",

        "veg_tip": """🥦 **Vegetarian Indian Cooking — Tips & Substitutions**

**Replacing Meat in Indian Dishes:**
- **Paneer** (cottage cheese) → Butter Chicken → Paneer Makhani ✅
- **Jackfruit (Kathal)** → Mutton/Pulled pork dishes → Biryani, Korma ✅
- **Mushrooms** → Chicken in most gravies → Mushroom Do Pyaza ✅
- **Soya Chunks** → Keema dishes → Soya Keema Pav, Keema Pao ✅
- **Raw Banana (Kela)** → Lamb in some coastal dishes ✅
- **Lotus Stem (Kamal Kakdi)** → Slow-braised curries ✅
- **Chickpeas/Rajma** → Dense meat gravies ✅

**Classic Pure Veg Indian Dishes (No Substitution Needed):**
Dal Makhani | Baingan Bharta | Aloo Gobi | Palak Paneer | Malai Kofta | Rajma Chawal | Undhiyu | Saag | Bhindi Masala | Kadhi Pakora

**Protein-Rich Veg Indian Meals:**
- Dal + Rice = complete protein (ancient food wisdom)
- Chana (chickpea) curries — high protein
- Paneer dishes — full protein
- Sattu (roasted Bengal gram) — Bihar's superfood protein drink""",

        "fry_tip": """🔥 **Indian Deep Frying Secrets**

**Oil Temperature Guide:**
- **160°C — LOW:** Samosa, kachori (crispy without burning)
- **170°C — MEDIUM:** Pakoras, bhajiya, vada
- **180-190°C — HIGH:** Puri, bhature, jalebi

**How to Test Without a Thermometer:**
- Drop a small bit of dough → sinks then rises slowly = 160°C (samosa temp)
- Dough rises quickly = 170°C (pakora temp)
- Dough rises immediately and browns fast = 190°C+ (too hot for most)

**Why Your Fried Food Fails:**
- **Too oily:** Oil not hot enough when food went in
- **Burnt outside, raw inside:** Oil too hot
- **Soggy after frying:** Didn't drain on paper properly; or added too many pieces at once
- **Didn't puff (puri/bhature):** Dough too soft; or oil not hot enough

**Healthy Frying Tips:**
- Use fresh oil for better taste
- Never reuse oil more than 2-3 times
- Cast iron kadai maintains temperature better than steel""",

        "ferment_tip": """🧫 **The Art of Fermentation in Indian Cooking**

**Idli/Dosa Batter Fermentation:**
- Ideal temperature: 26–32°C (room temp in India)
- Cold climates trick: Preheat oven to lowest setting, turn off, put batter inside
- How to know it's ready: Batter doubles, smells slightly sour, has small bubbles
- Over-fermented: Very sour, slightly pink — still usable, good for uttapam!
- Under-fermented: Dense idlis, won't spread for dosa

**Grinder vs. Blender:**
- Wet grinder (stone) = fluffier urad dal = softer idlis
- Blender = acceptable but not as airy
- Trick: Add ice cubes when blending in mixer to keep it cool

**Fermentation Timeline:**
- Mumbai/Chennai (hot): 6-8 hours
- Hyderabad: 8-10 hours  
- Delhi/North (cooler): 12-16 hours
- Winter: Add a pinch of soda only as emergency backup

**Other Fermented Indian Foods:**
Kanji (fermented black carrot drink) | Gundruk (Nepali fermented greens) | Ambali (fermented ragi porridge) | Dhokla | Jalebi batter""",

        "substitute_tip": """🔄 **Indian Ingredient Substitutions**

| Original | Substitute | Notes |
|---------|-----------|-------|
| Tamarind | Kokum / Amchur / Lemon | Kokum for coastal dishes |
| Kasuri Methi | Fresh fenugreek leaves | Use 2x quantity |
| Hing (Asafoetida) | Garlic + leek | Different but similar function |
| Coconut milk | Cashew cream | Blend cashews with water |
| Ghee | Butter + drop of oil | Not the same but workable |
| Yogurt | Coconut yogurt (vegan) | For marinating |
| Chana Dal | Yellow moong dal | Softer texture |
| Basmati Rice | Any long-grain rice | Biryani won't be the same |
| Fresh curry leaves | Dried curry leaves | Use 2x, less fragrant |
| Jaggery | Dark brown sugar | Same quantity |
| Kewra water | Rose water | Different fragrance |
| Fresh grated coconut | Desiccated coconut (soaked) | Soak in warm water 30 mins |""",

        "street_food": """🛒 **Indian Street Food Guide — City by City**

**Mumbai:** Vada Pav → Pav Bhaji → Bhelpuri → Sev Puri → Misal Pav → Bombay Sandwich
**Delhi:** Chole Bhature → Paranthe → Golgappa → Dahi Bhalla → Aloo Tikki → Ram Laddoo
**Kolkata:** Kathi Roll → Phuchka → Jhalmuri → Tele Bhaja → Egg Roll → Mughlai Paratha
**Hyderabad:** Mirchi Bajji → Lukhmi → Dahi Vada → Haleem Slider → Irani Chai
**Chennai:** Sundal → Murukku → Bajji → Paniyaram → Kaara Paniyaram → Kothu Parotta
**Lucknow:** Basket Chaat → Tikki Chaat → Dahi Vada → Makkhan Malai → Ram Laddoo
**Amritsar:** Amritsari Kulcha → Amritsari Fish → Pinni → Gajjar Halwa
**Jaipur:** Pyaaz Kachori → Mawa Kachori → Mirchi Bada → Ghewar → Dal Baati

**Chaat Essentials:**
Every chaat needs: Tamarind chutney (imli) + Green chutney (pudina) + Sev + Chaat masala
Master these two chutneys and you can make any chaat at home!""",

        "dessert_tip": """🍬 **Indian Sweets & Desserts Guide**

**By Region:**
- **North India:** Gulab Jamun, Jalebi, Barfi, Halwa, Shahi Tukda, Kheer
- **Bengal:** Rasgulla, Sandesh, Mishti Doi, Rajbhog, Pantua
- **Maharashtra:** Puran Poli, Modak, Shrikhand, Basundi, Kheer (Doodhi)
- **Tamil Nadu:** Adhirasam, Mysurpa, Thirattipaal, Paal Payasam
- **Kerala:** Palada Payasam, Ada Pradaman (with jaggery+coconut milk), Unniyappam
- **Gujarat:** Shrikhand, Mohanthal, Lapsi (broken wheat halwa)
- **Hyderabad:** Double Ka Meetha, Qubani Ka Meetha, Shahi Tukda

**Common Mistakes in Indian Sweets:**
- Gulab Jamun too hard: Overworked dough or too much maida
- Kheer too thin: Didn't reduce milk enough; cook longer
- Rasgulla rubbery: Under-kneaded chenna
- Halwa grainy: Sugar added before ghee was properly absorbed
- Jalebi flat: Batter fermentation incomplete; needs slight sourness

**3 Easiest Indian Sweets to Make:**
1. **Rava Ladoo** (5 ingredients, 15 mins)
2. **Coconut Barfi** (3 ingredients, 20 mins)
3. **Kheer** (4 ingredients, 45 mins patience)""",
    }
    return topic_answers.get(topic, "")


def _format_recipe_response(recipe: dict) -> str:
    """Format a recipe dict into a clean chat response."""
    lines = [
        f"## {recipe['title']}",
        f"**Serves:** {recipe['serves']} &nbsp;|&nbsp; **Time:** {recipe['time']} &nbsp;|&nbsp; **Difficulty:** {recipe['difficulty']}",
        "",
        "### 🛒 Ingredients",
    ]
    for ing in recipe["ingredients"]:
        lines.append(f"- {ing}")

    lines += ["", "### 👨‍🍳 Method"]
    for i, step in enumerate(recipe["steps"], 1):
        lines.append(f"**Step {i}:** {step}")
        lines.append("")

    lines += ["### 💡 Pro Tips"]
    for tip in recipe["tips"]:
        lines.append(f"✅ {tip}")

    lines += ["", f"### 🔄 Variations", recipe["variations"]]
    return "\n".join(lines)


def _generate_chat_response(user_msg: str, history: list) -> str:
    """Generate a response using the built-in knowledge base."""
    q = user_msg.lower().strip()

    # Greeting
    if any(w in q for w in ["hi", "hello", "hey", "namaste", "hola"]):
        return """🙏 **Namaste! Welcome to your Indian Food Expert!**

I'm your personal Indian cuisine assistant with deep knowledge of recipes, techniques, and food culture from all across India!

**Ask me about:**
- 🍚 Recipes with full ingredients & step-by-step method
- 🌶️ Spice guides & masala blends
- 🔄 Ingredient substitutions
- 🏙️ City-wise street food guides
- 🥦 Vegetarian alternatives
- 🍬 Indian sweets & desserts
- 🔥 Frying & fermentation tips

**I know recipes for:** Biryani · Butter Chicken · Dosa · Idli · Haleem · Chole · Dal Makhani · Samosa · Rasgulla · Filter Coffee · Lassi · Pav Bhaji · Vada Pav · Kheer · Golgappa · and many more!

What would you like to cook today? 😊"""

    # Help / What can you do
    if any(w in q for w in ["what can you", "help", "what do you know", "topics", "list"]):
        return """📚 **Here's what I can help you with:**

**🍽️ Full Recipes (with tips & variations):**
Biryani | Butter Chicken | Dosa | Idli & Sambar | Haleem | Chole Bhature | Dal Makhani | Samosa | Rasgulla | Filter Coffee | Lassi | Pav Bhaji | Vada Pav | Kheer | Golgappa/Pani Puri

**📖 Knowledge Topics:**
- 🌶️ Indian spice guide & garam masala recipe
- 🥦 Vegetarian substitutions for any dish
- 🔥 Deep frying temperatures & secrets
- 🧫 Fermentation guide (idli, dosa, dhokla)
- 🔄 Ingredient substitutions
- 🛒 Street food guide — city by city
- 🍬 Indian sweets & desserts guide

**Just type what you want to know!** Examples:
- *"How to make biryani?"*
- *"Vegetarian butter chicken"*
- *"Indian spice guide"*
- *"Street food of Mumbai"*"""

    # Check knowledge base for recipes
    key, recipe = _search_recipe_kb(q)

    if recipe:
        return _format_recipe_response(recipe)

    if key:  # topic response
        return _get_topic_response(key, q)

    # Thank you
    if any(w in q for w in ["thank", "thanks", "shukriya", "dhanyawad"]):
        return "🙏 You're most welcome! Happy cooking! Do ask if you need any more recipes or tips. **Khana khao, mast raho!** 😄🍛"

    # Goodbye
    if any(w in q for w in ["bye", "goodbye", "alvida"]):
        return "👋 **Alvida!** Come back anytime for more Indian food wisdom. Happy cooking! 🍛✨"

    # Unknown — helpful fallback
    nearby = []
    all_dishes = list(RECIPE_KB.keys())
    for dish in all_dishes:
        if any(word in dish for word in q.split() if len(word) > 3):
            nearby.append(dish.title())

    fallback = f"""🤔 I don't have a specific answer for **"{user_msg}"**, but I can help with:

**Available Recipes:**
{" · ".join([k.title() for k in RECIPE_KB.keys()])}

**Knowledge Topics:**
Spice Guide · Vegetarian Tips · Frying Secrets · Fermentation Guide · Ingredient Substitutions · Street Food by City · Desserts Guide

Try asking like:
- *"How to make [dish name]?"*
- *"Recipe for dosa"*
- *"Indian spice guide"*
- *"Street food of Kolkata"*"""

    return fallback


with tab6:
    st.markdown("""
    <div class="sec-head" style="margin-top:4px">
      <div class="sec-head-text">🤖 AI Recipe & Food Knowledge Assistant</div>
      <div class="sec-head-line"></div>
    </div>""", unsafe_allow_html=True)

    # Header card
    st.markdown("""
    <div style="background:var(--ink);border-radius:16px;padding:20px 28px;margin-bottom:20px;display:flex;align-items:center;justify-content:space-between">
      <div>
        <div style="font-size:10px;letter-spacing:0.25em;text-transform:uppercase;color:var(--spice-lt);font-weight:700;margin-bottom:8px">Built-in Knowledge · No API Key Needed</div>
        <div style="font-family:'Playfair Display',serif;font-size:22px;color:#F5EFE6;margin-bottom:8px">
          Your Personal <em style="color:var(--gold-lt)">Indian Food Expert</em>
        </div>
        <div style="font-size:12px;color:rgba(245,239,230,0.5);line-height:1.8">
          Full recipes · Spice guides · Substitutions · Street food by city · Dessert tips — works 100% offline!
        </div>
      </div>
      <div style="font-size:48px;opacity:0.6">👨‍🍳</div>
    </div>""", unsafe_allow_html=True)

    # Quick suggestion buttons
    st.markdown("<div style='font-size:11px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#7A6F65;margin-bottom:8px'>⚡ Quick Ask</div>", unsafe_allow_html=True)
    sug_cols = st.columns(4)
    suggestions = [
        ("🍚", "Biryani recipe?"),
        ("🍗", "Butter Chicken recipe?"),
        ("🫔", "How to make Dosa?"),
        ("🌶️", "Indian spice guide"),
        ("🥦", "Vegetarian tips"),
        ("🛒", "Mumbai street food"),
        ("🍬", "Indian desserts guide"),
        ("☕", "Filter coffee recipe?"),
    ]
    row1 = st.columns(4)
    row2 = st.columns(4)
    for col, (emoji, label) in zip(row1 + row2, suggestions):
        with col:
            if st.button(f"{emoji} {label}", key=f"sug_{label[:12]}", use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": label})
                reply = _generate_chat_response(label, st.session_state.chat_history)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # Display chat history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-end;margin-bottom:12px">
              <div style="max-width:75%;background:linear-gradient(135deg,#C4411A 0%,#E8572A 100%);
                          border-radius:18px 18px 4px 18px;padding:12px 18px;color:white;
                          font-size:14px;line-height:1.6;box-shadow:0 4px 16px rgba(196,65,26,0.25)">
                {msg['content']}
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            # Render markdown in response
            st.markdown(f"""
            <div style="display:flex;justify-content:flex-start;margin-bottom:12px;gap:12px">
              <div style="width:36px;height:36px;border-radius:50%;background:linear-gradient(135deg,#0D0A08,#2A1F18);
                          border:2px solid rgba(196,65,26,0.4);display:flex;align-items:center;justify-content:center;
                          font-size:18px;flex-shrink:0;margin-top:4px">👨‍🍳</div>
              <div style="max-width:85%;background:#FFFCF8;border:1px solid rgba(196,65,26,0.15);
                          border-radius:4px 18px 18px 18px;padding:16px 20px;
                          font-size:13px;line-height:1.8;color:#3C3530;box-shadow:0 2px 8px rgba(0,0,0,0.05)">
            """, unsafe_allow_html=True)
            st.markdown(msg["content"])
            st.markdown("</div></div>", unsafe_allow_html=True)

    # Input area
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    col_inp, col_send = st.columns([5, 1])
    with col_inp:
        user_input = st.text_input(
            "Ask anything...",
            key="chat_input_v2",
            label_visibility="collapsed",
            placeholder="e.g. How do I make fluffy idlis? What spices go in biryani? Mumbai street food?",
        )
    with col_send:
        send_btn = st.button("Send 🚀", type="primary", use_container_width=True, key="send_chat")

    if send_btn and user_input.strip():
        user_msg = user_input.strip()
        st.session_state.chat_history.append({"role": "user", "content": user_msg})
        reply = _generate_chat_response(user_msg, st.session_state.chat_history)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()

    # Clear
    if st.session_state.chat_history:
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("🗑️ Clear Chat", type="secondary", key="clear_chat_v2"):
            st.session_state.chat_history = []
            st.rerun()

    # Footer
    st.markdown("""
    <div class="status-info" style="margin-top:16px">
        👨‍🍳 &nbsp; <strong>15+ full recipes</strong> · Spice guides · Substitutions · Street food · Desserts ·
        <strong>Zero API key needed</strong> — all knowledge is built right in!
    </div>""", unsafe_allow_html=True)
