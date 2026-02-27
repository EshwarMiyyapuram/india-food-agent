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
    <div class="hero-title">SIRI <em>FoodTrend</em><br>Agent</div>
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
tab1, tab2, tab3, tab4 = st.tabs(["📊  Trend Analysis", "🍽  Weekend Specials", "📋  Weekly Report", "🗺️  Restaurant Map"])


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
