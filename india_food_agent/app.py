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

/* ── TOP DISHES CARD ── */
.top-dish-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 14px;
    display: flex;
    align-items: flex-start;
    gap: 18px;
    transition: box-shadow 0.2s;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.top-dish-card:hover { box-shadow: 0 8px 28px rgba(196,65,26,0.12); }
.top-dish-rank {
    font-family: 'DM Mono', monospace;
    font-size: 28px;
    font-weight: 700;
    color: var(--spice);
    line-height: 1;
    min-width: 40px;
}
.top-dish-rank.top3 { color: var(--gold); font-size: 32px; }
.top-dish-content { flex: 1; }
.top-dish-name {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--ink);
    margin-bottom: 4px;
}
.top-dish-desc { font-size: 13px; color: var(--muted); line-height: 1.6; margin-bottom: 10px; }
.top-dish-tags { display: flex; flex-wrap: wrap; gap: 8px; }
.top-dish-tag {
    font-size: 11px; font-weight: 600; letter-spacing: 0.05em;
    padding: 4px 10px; border-radius: 20px;
    background: rgba(196,65,26,0.08); color: var(--spice);
    border: 1px solid rgba(196,65,26,0.2);
}
.top-dish-tag.green { background: rgba(26,107,58,0.08); color: var(--green); border-color: rgba(26,107,58,0.2); }
.top-dish-tag.gold { background: rgba(212,160,23,0.1); color: #8B6914; border-color: rgba(212,160,23,0.3); }
.top-dish-price {
    font-family: 'DM Mono', monospace;
    font-size: 18px; font-weight: 600;
    color: var(--green);
    white-space: nowrap;
    padding-top: 4px;
}
.top-dish-restaurant {
    font-size: 12px; color: var(--muted);
    margin-top: 6px;
}
.top-dish-restaurant strong { color: var(--ink); }

/* ── SECTION HEADERS ── */
.sec-head { display: flex; align-items: center; gap: 14px; margin: 28px 0 16px; }
.sec-head-line { flex: 1; height: 1px; background: var(--border); }
.sec-head-text {
    font-size: 11px; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase;
    color: var(--spice); white-space: nowrap;
}

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

/* ── DISH CARDS (specials) ── */
.dish-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 18px;
    overflow: hidden;
    margin-bottom: 18px;
    transition: box-shadow 0.2s, transform 0.15s;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
}
.dish-card:hover { box-shadow: 0 12px 40px rgba(196,65,26,0.14); transform: translateY(-2px); }
.dish-card-header {
    padding: 22px 24px 18px;
    position: relative;
}
.dish-card-header.margin  { background: linear-gradient(135deg, #1A0E08 0%, #2D1507 100%); }
.dish-card-header.premium { background: linear-gradient(135deg, #120D1A 0%, #1E1030 100%); }
.dish-card-header.insta   { background: linear-gradient(135deg, #0A1A1A 0%, #0D2929 100%); }
.dish-card-header.performer { background: linear-gradient(135deg, #0A0D1A 0%, #111830 100%); }
.dish-header-top { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
.dish-badge {
    font-size: 11px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
    padding: 5px 12px; border-radius: 20px;
}
.badge-margin   { background: rgba(212,160,23,0.2); color: #F0C040; border: 1px solid rgba(212,160,23,0.4); }
.badge-premium  { background: rgba(139,92,246,0.2); color: #C4B5FD; border: 1px solid rgba(139,92,246,0.4); }
.badge-insta    { background: rgba(34,160,90,0.2);  color: #6EE7B7; border: 1px solid rgba(34,160,90,0.4);  }
.badge-performer{ background: rgba(239,68,68,0.2);  color: #FCA5A5; border: 1px solid rgba(239,68,68,0.4);  }
.dish-price-badge {
    font-family: 'DM Mono', monospace; font-size: 14px; font-weight: 600;
    color: #F0C040; text-align: right;
}
.dish-name {
    font-family: 'Playfair Display', serif; font-size: 22px; font-weight: 800;
    color: #F5EFE6; line-height: 1.15; margin-bottom: 6px;
}
.dish-key-ing { font-size: 11px; color: rgba(245,239,230,0.45); letter-spacing: 0.06em; }
.dish-card-body { padding: 20px 24px; }
.dish-desc { font-size: 13.5px; color: #4A3F37; line-height: 1.7; margin-bottom: 18px; }
.dish-meta-row { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 16px; }
.dish-meta-item { flex: 1; min-width: 80px; }
.dmi-label { font-size: 10px; font-weight: 600; letter-spacing: 0.1em; text-transform: uppercase; color: #A89F97; margin-bottom: 4px; }
.dmi-value { font-size: 13px; font-weight: 600; color: var(--ink); }
.dmi-value.spice { color: var(--spice); }
.dmi-value.green { color: var(--green); }
.dish-inspired {
    background: var(--paper); border-radius: 10px; padding: 12px 16px;
    font-size: 13px; color: var(--muted); display: flex; align-items: center; gap: 10px;
}
.demand-high-wrap   .demand-dot { width:7px;height:7px;border-radius:50%;background:#22A05A;display:inline-block;margin-right:4px; }
.demand-medium-wrap .demand-dot { width:7px;height:7px;border-radius:50%;background:#F0C040;display:inline-block;margin-right:4px; }
.demand-low-wrap    .demand-dot { width:7px;height:7px;border-radius:50%;background:#EF4444;display:inline-block;margin-right:4px; }
.demand-label { font-size: 11px; font-weight: 600; }
.demand-high-wrap   .demand-label { color: #22A05A; }
.demand-medium-wrap .demand-label { color: #D4A017; }
.demand-low-wrap    .demand-label { color: #EF4444; }

/* ── TIPS ── */
.tip-block { border-radius: 10px; padding: 14px 16px; margin-bottom: 10px; }
.tip-block.plating { background: rgba(212,160,23,0.08); border-left: 3px solid var(--gold); }
.tip-block.reels   { background: rgba(26,107,58,0.08);  border-left: 3px solid var(--green); }
.tip-block.trend   { background: rgba(196,65,26,0.07);  border-left: 3px solid var(--spice); }
.tip-label { font-size: 11px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 6px; }
.tip-block.plating .tip-label { color: var(--gold); }
.tip-block.reels   .tip-label { color: var(--green); }
.tip-block.trend   .tip-label { color: var(--spice); }
.tip-text { font-size: 13px; color: var(--ink); line-height: 1.6; }

/* ── INSIGHT BOX ── */
.insight-box {
    background: var(--ink); border-radius: 18px; padding: 30px 36px;
    margin: 28px 0; position: relative; overflow: hidden;
}
.insight-box::before {
    content: ''; position: absolute; top: -40px; right: -40px;
    width: 200px; height: 200px; border-radius: 50%;
    background: radial-gradient(circle, rgba(212,160,23,0.2) 0%, transparent 70%);
}
.insight-eyebrow { font-size: 10px; font-weight: 700; letter-spacing: 0.3em; text-transform: uppercase; color: var(--spice-lt); margin-bottom: 8px; }
.insight-city { font-family: 'Playfair Display', serif; font-size: 24px; font-weight: 700; color: #F5EFE6; margin-bottom: 14px; }
.insight-text { font-size: 15px; color: rgba(245,239,230,0.75); line-height: 1.75; margin-bottom: 18px; }
.insight-revenue { font-size: 13px; color: var(--gold-lt); font-weight: 600; }

/* ── ING PILL ── */
.ing-pill {
    background: var(--card-bg); border: 1px solid var(--border);
    border-radius: 14px; padding: 16px 18px; text-align: center;
    transition: transform 0.15s;
}
.ing-pill:hover { transform: translateY(-2px); }
.ing-pill-icon { font-size: 24px; display: block; margin-bottom: 8px; }
.ing-rank { font-size: 10px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase; color: var(--muted); }

/* ── TREND CARDS ── */
.trend-card {
    background: var(--card-bg); border: 1px solid var(--border);
    border-radius: 14px; padding: 18px 20px; margin-bottom: 12px;
    display: flex; justify-content: space-between; align-items: center;
}
.trend-card-left { flex: 1; }
.trend-card-name { font-size: 16px; font-weight: 700; color: var(--ink); margin-bottom: 4px; }
.trend-card-context { font-size: 12px; color: var(--muted); }
.trend-badge {
    font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 20px;
    white-space: nowrap; margin-left: 12px;
}
.trend-badge.hot     { background: rgba(196,65,26,0.12); color: var(--spice); border: 1px solid rgba(196,65,26,0.3); }
.trend-badge.rising  { background: rgba(212,160,23,0.12); color: #8B6914; border: 1px solid rgba(212,160,23,0.3); }
.trend-badge.steady  { background: rgba(26,107,58,0.1);  color: var(--green); border: 1px solid rgba(26,107,58,0.25); }
.trend-pct { font-family: 'DM Mono', monospace; font-size: 18px; font-weight: 700; color: var(--spice); margin-left: 16px; white-space: nowrap; }

/* ── EMPTY STATE ── */
.empty-state {
    text-align: center; padding: 80px 40px;
    background: var(--card-bg); border: 2px dashed var(--border); border-radius: 20px;
}
.empty-icon { font-size: 48px; margin-bottom: 16px; }
.empty-title { font-family: 'Playfair Display', serif; font-size: 24px; font-weight: 700; color: var(--ink); margin-bottom: 8px; }
.empty-sub { font-size: 14px; color: var(--muted); }

/* ── REPORT ── */
.report-header {
    background: var(--ink); border-radius: 16px; padding: 24px 28px;
    margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;
}
.report-title { font-family: 'Playfair Display', serif; font-size: 26px; font-weight: 700; color: #F5EFE6; }
.report-subtitle { font-size: 12px; color: rgba(245,239,230,0.5); margin-top: 6px; }
.report-body {
    background: var(--card-bg); border: 1px solid var(--border);
    border-radius: 16px; padding: 32px 36px;
    font-size: 14px; color: var(--ink); line-height: 1.9;
    white-space: pre-wrap;
}

/* ── HASHTAG ── */
.hashtag-pill {
    display: inline-block;
    background: rgba(196,65,26,0.08); color: var(--spice);
    border: 1px solid rgba(196,65,26,0.2);
    border-radius: 20px; padding: 6px 14px;
    font-size: 13px; font-weight: 600; margin: 4px;
}
.hashtag-pill.viral { background: rgba(196,65,26,0.15); font-size: 14px; }
.hashtag-pill.hot   { background: rgba(212,160,23,0.12); color: #8B6914; border-color: rgba(212,160,23,0.3); }
.hashtag-pill.rising{ background: rgba(26,107,58,0.1);  color: var(--green); border-color: rgba(26,107,58,0.25); }
</style>
""", unsafe_allow_html=True)


# ── Session State Init ──────────────────────
for k, v in {
    "trend_analysis": None,
    "specials": None,
    "report_txt": None,
    "top_dishes": None,   # ← NEW
    "last_city": None,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── Imports (lazy, with graceful fallback) ──
@st.cache_resource(show_spinner=False)
def load_modules():
    try:
        from scraper.trend_scraper    import scrape_all_trends
        from llm.dish_generator       import run_full_pipeline
        from reports.report_generator import save_all
        return scrape_all_trends, run_full_pipeline, save_all, True
    except Exception as e:
        return None, None, None, False

scrape_fn, pipeline_fn, save_fn, modules_ok = load_modules()


# ══════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
      <div class="sidebar-logo-text">भारत<br><em>FoodTrend</em></div>
      <div class="sidebar-logo-sub">Intelligence Agent · V2.0</div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label">📍 Location</div>', unsafe_allow_html=True)
    city = st.selectbox("", [
        "Hyderabad", "Chennai", "Mumbai", "Delhi", "Bengaluru",
        "Kolkata", "Lucknow", "Amritsar", "Goa", "Jaipur",
        "Kochi", "Indore", "Pune", "Ahmedabad", "Chandigarh",
        "Varanasi", "Agra", "Vizag", "Madurai", "Bhopal",
    ], label_visibility="collapsed")

    st.markdown('<div class="sidebar-section-label">🍽 Outlet Profile</div>', unsafe_allow_html=True)
    rtype = st.selectbox("", [
        "Local Dhaba / Authentic", "Modern Café / Bistro", "Fine Dining",
        "Street Food Stall", "Cloud Kitchen / Delivery", "Family Restaurant",
        "Vegetarian / Pure Veg", "Seafood Specialty", "Biryani House", "Mughlai / Awadhi",
    ], label_visibility="collapsed")

    st.markdown('<div class="sidebar-section-label">💰 Pricing Tier</div>', unsafe_allow_html=True)
    price = st.selectbox("", [
        "₹ (under ₹200/head)", "₹₹ (₹200–600/head)",
        "₹₹₹ (₹600–1500/head)", "₹₹₹₹ (₹1500+/head)",
    ], label_visibility="collapsed")

    st.markdown('<div class="sidebar-section-label">🌦 Season</div>', unsafe_allow_html=True)
    season = st.selectbox("", [
        "Summer (Mar–Jun)", "Monsoon (Jul–Sep)",
        "Festive / Post-Monsoon (Oct–Nov)", "Winter (Dec–Feb)",
    ], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    scan_btn     = st.button("🕷 Scan Trends",     use_container_width=True, type="secondary")
    generate_btn = st.button("✦ Generate Specials", use_container_width=True, type="primary")

    if not modules_ok:
        st.markdown("""
        <div style="background:rgba(196,65,26,0.15);border:1px solid rgba(196,65,26,0.4);
        border-radius:8px;padding:12px;margin-top:16px;font-size:11px;color:#E8DDD4;">
        ⚠️ Scraper/LLM modules not found.<br>Running in demo mode.
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════
data_pts = len(st.session_state.trend_analysis.get("trending_ingredients", [])) * 12 if st.session_state.trend_analysis else "—"
dishes_n = len(st.session_state.specials.get("weekend_specials", [])) if st.session_state.specials else (
           len(st.session_state.top_dishes) if st.session_state.top_dishes else 0)

st.markdown(f"""
<div class="hero">
  <div style="position:relative;z-index:1">
    <div class="hero-eyebrow">● Live Intelligence Dashboard</div>
    <div class="hero-title">भारत <em>FoodTrend</em><br>Agent</div>
    <div class="hero-tagline">Scraping · Analysing · Generating · Winning</div>
  </div>
  <div class="hero-stats">
    <div class="hero-stat-item"><div class="hero-stat-num">20</div><div class="hero-stat-lbl">Cities</div></div>
    <div class="hero-divider"></div>
    <div class="hero-stat-item"><div class="hero-stat-num">4</div><div class="hero-stat-lbl">Sources</div></div>
    <div class="hero-divider"></div>
    <div class="hero-stat-item"><div class="hero-stat-num">{data_pts}</div><div class="hero-stat-lbl">Data Points</div></div>
    <div class="hero-divider"></div>
    <div class="hero-stat-item"><div class="hero-stat-num">{dishes_n or "—"}</div><div class="hero-stat-lbl">AI Dishes</div></div>
  </div>
</div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Trend Analysis",
    "🏆 Top 10 Dishes",
    "🍽 Weekend Specials",
    "📋 Weekly Report",
])


# ════════════════════════════════════════════════════
#  SCAN TRENDS LOGIC
# ════════════════════════════════════════════════════
if scan_btn:
    with st.spinner(f"🕷 Scraping food trends for {city}…"):
        if modules_ok:
            try:
                scraped = scrape_fn(city, verbose=False)
                from llm.dish_generator import analyze_scraped_data
                st.session_state.trend_analysis = analyze_scraped_data(scraped)
                st.session_state.last_city = city
                st.success(f"✅ Trends loaded for {city}!")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            # Demo mode
            import random
            st.session_state.trend_analysis = {
                "city": city,
                "analysis_summary": f"{city} is experiencing a surge in fusion street food and premium biryani variants. Cloud kitchens are dominating delivery while local cafés push instagrammable desserts.",
                "trending_ingredients": [
                    {"name": "Smoked Butter", "emoji": "🧈", "growth_pct": 420, "context": f"Trending across cafés in {city}", "status": "hot"},
                    {"name": "Black Garlic", "emoji": "🧄", "growth_pct": 310, "context": "Premium ingredient in modern Indian", "status": "hot"},
                    {"name": "Kokum", "emoji": "🍇", "growth_pct": 280, "context": "Regional sourness replacing tamarind", "status": "rising"},
                    {"name": "Miso", "emoji": "🫙", "growth_pct": 195, "context": "Fusion Indo-Japanese wave", "status": "rising"},
                    {"name": "Jackfruit", "emoji": "🌿", "growth_pct": 165, "context": "Plant-based meat alternative", "status": "rising"},
                ],
                "famous_dishes_trending": [
                    {"dish_name": "Biryani", "famous_at": "Paradise Restaurant", "saves_estimate": "82k", "engagement_pct": 94, "why_famous": "Original Hyderabadi recipe, 70 years old"},
                    {"dish_name": "Haleem", "famous_at": "Shah Ghouse", "saves_estimate": "56k", "engagement_pct": 88, "why_famous": "Slow-cooked 8 hours, iconic texture"},
                ],
                "viral_hashtags": [
                    {"tag": f"#{city}Food", "growth_pct": 720, "type": "viral"},
                    {"tag": "#IndianFoodLover", "growth_pct": 450, "type": "hot"},
                    {"tag": "#StreetFoodIndia", "growth_pct": 330, "type": "rising"},
                ],
                "declining_trends": [
                    {"name": "Plain Paneer Tikka", "decline_pct": "-28%", "reason": "Over-saturated"},
                ],
                "engagement_patterns": "Short-form Reels showing live cooking get 3× more saves than static food photos",
                "stats": {"posts_analyzed": "142k", "top_dish_saves": "82k", "hashtags_count": 18},
            }
            st.session_state.last_city = city


# ════════════════════════════════════════════════════
#  GENERATE SPECIALS + TOP 10 DISHES LOGIC
# ════════════════════════════════════════════════════
if generate_btn:
    with st.spinner(f"🤖 Claude AI generating top dishes & specials for {city}…"):
        if modules_ok:
            try:
                # Ensure we have scraped data
                if not st.session_state.trend_analysis or st.session_state.last_city != city:
                    scraped = scrape_fn(city, verbose=False)
                else:
                    scraped = {"city": city, "google_results": [], "zomato_data": [], "articles": [], "hashtags": []}

                output = pipeline_fn(
                    scraped_data=scraped,
                    restaurant_type=rtype,
                    price_range=price,
                    season=season,
                    verbose=False,
                )
                st.session_state.trend_analysis = output["trend_analysis"]
                st.session_state.specials        = output["specials"]
                st.session_state.report_txt      = output["weekly_report"]
                st.session_state.last_city       = city

                # Generate top 10 dishes via separate Claude call
                from llm.dish_generator import generate_top_dishes
                st.session_state.top_dishes = generate_top_dishes(city)

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            # Demo mode — generate top 10 dishes inline
            import anthropic, os, json, re
            from dotenv import load_dotenv
            load_dotenv()

            try:
                client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
                prompt = f"""You are India's top food expert. List the top 10 BEST and most iconic dishes to eat in {city}, India.
For each dish include:
- Real famous restaurant where it's best eaten
- What makes it unique
- Best time to eat
- Price range in INR
- Why tourists/locals love it

Return ONLY valid JSON (no markdown):
{{
  "city": "{city}",
  "top_dishes": [
    {{
      "rank": 1,
      "dish_name": "",
      "restaurant": "Best place to eat it in {city}",
      "why_famous": "2 sentence description",
      "unique_factor": "What makes this version special",
      "price_range": "₹XXX–₹YYY",
      "best_time": "breakfast|lunch|dinner|anytime",
      "must_try_reason": "One compelling sentence",
      "tags": ["tag1", "tag2", "tag3"]
    }}
  ],
  "city_food_culture": "2 sentence summary of {city}'s food identity"
}}"""
                resp = client.messages.create(
                    model="claude-opus-4-6",
                    max_tokens=3000,
                    messages=[{"role": "user", "content": prompt}]
                )
                raw = re.sub(r"```json|```", "", resp.content[0].text).strip()
                st.session_state.top_dishes = json.loads(raw)
            except Exception as e:
                # Fallback demo data
                st.session_state.top_dishes = {
                    "city": city,
                    "city_food_culture": f"{city} is celebrated for its bold spices, slow-cooked traditions, and a street food culture that draws food lovers from across India.",
                    "top_dishes": [
                        {"rank": i+1, "dish_name": n, "restaurant": r, "why_famous": w,
                         "unique_factor": u, "price_range": p, "best_time": t,
                         "must_try_reason": m, "tags": tg}
                        for i, (n, r, w, u, p, t, m, tg) in enumerate([
                            ("Hyderabadi Dum Biryani", "Paradise Restaurant", "Slow-cooked for 4 hours with aged basmati and premium mutton. The iconic saffron aroma fills the entire street.", "Sealed dam cooking technique, 70-year-old recipe", "₹280–₹450", "lunch", "The gold standard of Indian biryani — everything else is imitation.", ["Iconic", "Must-Try", "Non-Veg"]),
                            ("Haleem", "Shah Ghouse Café", "Eight-hour slow cook of wheat, barley and meat into a silky porridge. Ramadan staple now loved year-round.", "Ghee tempering with crispy onions", "₹150–₹220", "dinner", "Once you try Shah Ghouse Haleem, no other version will satisfy.", ["Street Food", "Iconic", "Non-Veg"]),
                            ("Irani Chai + Osmania Biscuit", "Nimrah Café, Charminar", "Persian-influenced milky tea brewed for hours, paired with melt-in-mouth butter biscuits.", "Tea brewed on low flame for 2+ hours", "₹20–₹40", "breakfast", "The most Hyderabadi experience you can have for under ₹50.", ["Budget", "Iconic", "Veg"]),
                            ("Pathar Gosht", "Bawarchi Restaurant", "Mutton cooked on a heated stone slab, getting a beautiful crust while staying juicy inside.", "Stone-slab cooking gives unique char", "₹350–₹500", "dinner", "Theatrical cooking meets incredible flavour — unforgettable.", ["Premium", "Non-Veg", "Unique"]),
                            ("Double Ka Meetha", "Hotel Shadab", "Bread pudding soaked in reduced milk, garnished with dry fruits and silver leaf.", "Uses day-old bread for better texture", "₹80–₹120", "anytime", "The royal Nizam dessert that ends every proper Hyderabadi feast.", ["Dessert", "Veg", "Royal"]),
                        ])[:10]
                    ]
                }

            # Also generate demo specials
            st.session_state.specials = {
                "city": city, "generated_at": datetime.now().isoformat(),
                "top_weekend_ingredients": ["Smoked Butter", "Black Garlic", "Saffron"],
                "weekend_specials": [
                    {"dish_name": "Charcoal Dum Biryani", "category": "low-cost high-margin",
                     "key_trending_ingredient": "Activated Charcoal", "inspired_by": "Paradise Biryani",
                     "description": "Classic dum biryani elevated with activated charcoal rice for a dramatic visual. Served in a sealed handi at the table.", 
                     "ingredients_needed": ["Aged basmati", "Mutton", "Charcoal dye", "Saffron"],
                     "prep_time_mins": 90, "food_cost_level": "Low", "estimated_food_cost_inr": "₹80–₹120",
                     "suggested_price_range": "₹380–₹450", "gross_margin_pct": "approx 72%",
                     "plating_tip": "Serve in black ceramic handi, crack seal tableside for dramatic steam effect",
                     "reels_tip": "Film the handi crack moment in slow motion — guaranteed viral",
                     "why_it_will_trend": "Charcoal aesthetics + classic taste = perfect Reels content",
                     "predicted_demand": "High", "best_served": "dinner"},
                ],
                "strategic_insight": f"Focus on instagrammable presentation this weekend in {city}. The monsoon season drives indoor dining — premium experiences command 40% more spend.",
                "revenue_projection": "₹45,000–₹65,000 additional weekend revenue with all 5 specials"
            }
            st.session_state.report_txt = f"WEEKLY FOOD TREND REPORT — {city.upper()}\n\nThis week {city} shows strong momentum in fusion and premium street food categories. Weekend footfall expected to be 20% above average due to festive proximity.\n\nRECOMMENDED STRATEGY: Lead with visual-first dishes that drive social sharing. Price the premium upsell at ₹100 above baseline to test elasticity."
            st.session_state.last_city = city


# ════════════════════════════════════════════════════
#  TAB 1 — TREND ANALYSIS
# ════════════════════════════════════════════════════
with tab1:
    if not st.session_state.trend_analysis:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">📊</div>
          <div class="empty-title">No Analysis Yet</div>
          <div class="empty-sub">Select a city · Scan Trends · Generate Specials</div>
        </div>""", unsafe_allow_html=True)
    else:
        ta = st.session_state.trend_analysis
        st.markdown(f"""
        <div class="status-success">
          <span style="font-size:18px">✅</span>
          <div>
            <strong>{ta.get('city',city)} — Trend Analysis Complete</strong><br>
            <span style="opacity:0.7;font-size:12px">{ta.get('analysis_summary','')}</span>
          </div>
        </div>""", unsafe_allow_html=True)

        # Trending ingredients
        ingredients = ta.get("trending_ingredients", [])
        if ingredients:
            st.markdown("""<div class="sec-head"><div class="sec-head-text">🔥 Trending Ingredients</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)
            for ing in ingredients:
                status = ing.get("status","hot")
                pct    = ing.get("growth_pct", 0)
                st.markdown(f"""
                <div class="trend-card">
                  <div class="trend-card-left">
                    <div class="trend-card-name">{ing.get('emoji','')} {ing.get('name','')}</div>
                    <div class="trend-card-context">{ing.get('context','')}</div>
                  </div>
                  <span class="trend-badge {status}">{status.upper()}</span>
                  <div class="trend-pct">+{pct}%</div>
                </div>""", unsafe_allow_html=True)

        # Viral hashtags
        hashtags = ta.get("viral_hashtags", [])
        if hashtags:
            st.markdown("""<div class="sec-head"><div class="sec-head-text">📲 Viral Hashtags</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)
            pills = " ".join([
                f'<span class="hashtag-pill {h.get("type","")}">{h.get("tag","")} +{h.get("growth_pct",0)}%</span>'
                for h in hashtags
            ])
            st.markdown(f'<div style="margin:8px 0 20px">{pills}</div>', unsafe_allow_html=True)

        # Famous dishes
        famous = ta.get("famous_dishes_trending", [])
        if famous:
            st.markdown("""<div class="sec-head"><div class="sec-head-text">🏅 Famous Dishes Trending</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)
            cols = st.columns(min(len(famous), 3))
            for col, d in zip(cols, famous[:3]):
                with col:
                    st.markdown(f"""
                    <div class="trend-card" style="flex-direction:column;gap:10px;align-items:flex-start">
                      <div>
                        <div class="trend-card-name">🍽 {d.get('dish_name','')}</div>
                        <div class="trend-card-context">@ {d.get('famous_at','')}</div>
                      </div>
                      <div style="display:flex;gap:10px;align-items:center">
                        <span class="trend-badge hot">{d.get('saves_estimate','?')} saves</span>
                        <span style="font-size:12px;color:var(--muted)">{d.get('why_famous','')}</span>
                      </div>
                    </div>""", unsafe_allow_html=True)

        # Engagement + declining
        engagement = ta.get("engagement_patterns","")
        if engagement:
            st.markdown(f"""
            <div class="status-info" style="margin-top:20px">
              📲 <strong>Engagement Pattern:</strong> {engagement}
            </div>""", unsafe_allow_html=True)

        declining = ta.get("declining_trends", [])
        if declining:
            st.markdown("""<div class="sec-head"><div class="sec-head-text">📉 Declining Trends (Avoid)</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)
            for d in declining:
                st.markdown(f"""
                <div class="trend-card">
                  <div class="trend-card-left">
                    <div class="trend-card-name">⚠️ {d.get('name','')}</div>
                    <div class="trend-card-context">{d.get('reason','')}</div>
                  </div>
                  <div class="trend-pct" style="color:#EF4444">{d.get('decline_pct','')}</div>
                </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════
#  TAB 2 — TOP 10 DISHES  ← NEW
# ════════════════════════════════════════════════════
with tab2:
    if not st.session_state.top_dishes:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">🏆</div>
          <div class="empty-title">No Top Dishes Yet</div>
          <div class="empty-sub">Click <strong>✦ Generate Specials</strong> to discover the top 10 iconic dishes for your selected city</div>
        </div>""", unsafe_allow_html=True)
    else:
        td = st.session_state.top_dishes
        city_name = td.get("city", city)
        culture   = td.get("city_food_culture", "")

        st.markdown(f"""
        <div class="status-success">
          <span style="font-size:22px">🏆</span>
          <div>
            <strong>Top 10 Must-Eat Dishes in {city_name}</strong><br>
            <span style="opacity:0.75;font-size:13px">{culture}</span>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("""<div class="sec-head"><div class="sec-head-text">🥇 The Definitive List</div><div class="sec-head-line"></div></div>""", unsafe_allow_html=True)

        dishes = td.get("top_dishes", [])
        for dish in dishes:
            rank     = dish.get("rank", 0)
            is_top3  = rank <= 3
            rank_cls = "top3" if is_top3 else ""
            tags     = dish.get("tags", [])
            tag_colors = ["", "green", "gold"]

            tag_html = " ".join([
                f'<span class="top-dish-tag {tag_colors[i % len(tag_colors)]}">{t}</span>'
                for i, t in enumerate(tags)
            ])

            st.markdown(f"""
            <div class="top-dish-card">
              <div class="top-dish-rank {rank_cls}">#{rank}</div>
              <div class="top-dish-content">
                <div class="top-dish-name">{dish.get('dish_name','')}</div>
                <div class="top-dish-desc">{dish.get('why_famous','')} {dish.get('unique_factor','')}</div>
                <div class="top-dish-tags">{tag_html}</div>
                <div class="top-dish-restaurant">
                  🏠 Best at: <strong>{dish.get('restaurant','')}</strong>
                  &nbsp;·&nbsp; 🕐 {str(dish.get('best_time','anytime')).title()}
                </div>
                <div style="margin-top:10px;font-size:13px;color:var(--spice);font-style:italic">
                  ✦ {dish.get('must_try_reason','')}
                </div>
              </div>
              <div class="top-dish-price">{dish.get('price_range','')}</div>
            </div>""", unsafe_allow_html=True)

        # Download CSV of top dishes
        if dishes:
            st.markdown("<br>", unsafe_allow_html=True)
            df_top = pd.DataFrame([{
                "Rank": d.get("rank",""), "Dish": d.get("dish_name",""),
                "Restaurant": d.get("restaurant",""), "Price (₹)": d.get("price_range",""),
                "Best Time": d.get("best_time",""), "Why Famous": d.get("why_famous",""),
            } for d in dishes])
            st.download_button(
                "⬇ Download Top 10 Dishes CSV",
                df_top.to_csv(index=False),
                file_name=f"top_dishes_{city_name.lower()}_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )


# ════════════════════════════════════════════════════
#  TAB 3 — WEEKEND SPECIALS
# ════════════════════════════════════════════════════
with tab3:
    specials = st.session_state.specials
    if not specials:
        st.markdown("""
        <div class="empty-state">
          <div class="empty-icon">🍽</div>
          <div class="empty-title">No Specials Generated Yet</div>
          <div class="empty-sub">Click <strong>✦ Generate Specials</strong> to create AI-powered weekend dishes</div>
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

                demand = dish.get("predicted_demand","Medium")
                d_wrap = f"demand-{demand.lower()}-wrap"

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
#  TAB 4 — WEEKLY REPORT
# ════════════════════════════════════════════════════
with tab4:
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
