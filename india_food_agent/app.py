"""
app.py  —  Streamlit Dashboard with Wishlist + Feedback
Run with:  streamlit run app.py
"""

import streamlit as st
import json
import sys
import os
import pandas as pd
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

# ── Persistence helpers ───────────────────
WISHLIST_FILE = Path(__file__).parent / "data" / "wishlist.json"
FEEDBACK_FILE = Path(__file__).parent / "data" / "feedback.json"
WISHLIST_FILE.parent.mkdir(exist_ok=True)

def load_json(path):
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return []

def save_json(path, data):
    try:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

# ── CSS ───────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');
:root {
    --ink:#0D0A08;--paper:#F5EFE6;--cream:#FDF9F4;
    --spice:#C4411A;--spice-lt:#E8572A;
    --gold:#D4A017;--gold-lt:#F0C040;
    --green:#1A6B3A;--green-lt:#22A05A;
    --purple:#5B2D8E;--purple-lt:#8B5CF6;
    --border:rgba(196,65,26,0.15);--muted:#7A6F65;--card-bg:#FFFCF8;
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;background:var(--paper)!important;}
.main .block-container{padding:1.5rem 2rem 3rem;max-width:1400px;}
::-webkit-scrollbar{width:6px;height:6px;}
::-webkit-scrollbar-track{background:var(--paper);}
::-webkit-scrollbar-thumb{background:var(--spice);border-radius:3px;}

/* SIDEBAR */
section[data-testid="stSidebar"]{background:var(--ink)!important;border-right:1px solid rgba(196,65,26,0.3);}
section[data-testid="stSidebar"] *{color:#E8DDD4!important;}
section[data-testid="stSidebar"] .stSelectbox>div>div{background:rgba(255,255,255,0.07)!important;border:1px solid rgba(196,65,26,0.4)!important;border-radius:8px!important;}
.sidebar-logo{padding:24px 0 8px;border-bottom:1px solid rgba(196,65,26,0.3);margin-bottom:20px;}
.sidebar-logo-text{font-family:'Playfair Display',serif;font-size:22px;font-weight:900;color:#F5EFE6;letter-spacing:-0.5px;line-height:1.2;}
.sidebar-logo-text em{color:var(--spice-lt);font-style:italic;}
.sidebar-logo-sub{font-size:9px;font-weight:600;letter-spacing:0.25em;text-transform:uppercase;color:#7A6F65;margin-top:6px;}
.sidebar-section-label{font-size:9px;font-weight:600;letter-spacing:0.2em;text-transform:uppercase;color:var(--spice-lt)!important;margin:18px 0 6px;}
section[data-testid="stSidebar"] .stButton>button{border-radius:8px!important;font-weight:600!important;font-size:13px!important;transition:all 0.2s!important;}
section[data-testid="stSidebar"] .stButton>button[kind="secondary"]{background:rgba(255,255,255,0.06)!important;border:1px solid rgba(196,65,26,0.5)!important;color:#E8DDD4!important;}
section[data-testid="stSidebar"] .stButton>button[kind="primary"]{background:linear-gradient(135deg,var(--spice) 0%,#E8572A 100%)!important;border:none!important;color:white!important;box-shadow:0 4px 20px rgba(196,65,26,0.4)!important;}

/* HERO */
.hero{background:var(--ink);border-radius:20px;padding:36px 40px;margin-bottom:28px;display:flex;align-items:center;justify-content:space-between;overflow:hidden;position:relative;}
.hero::before{content:'';position:absolute;top:-60px;right:-60px;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(196,65,26,0.25) 0%,transparent 70%);}
.hero-eyebrow{font-size:10px;font-weight:600;letter-spacing:0.3em;text-transform:uppercase;color:var(--spice-lt);margin-bottom:10px;}
.hero-title{font-family:'Playfair Display',serif;font-size:42px;font-weight:900;color:#F5EFE6;line-height:1.05;margin:0 0 12px;}
.hero-title em{color:var(--gold-lt);font-style:italic;}
.hero-tagline{font-size:13px;color:rgba(245,239,230,0.5);font-weight:300;letter-spacing:0.05em;}
.hero-stats{display:flex;gap:32px;position:relative;z-index:1;}
.hero-stat-item{text-align:center;}
.hero-stat-num{font-family:'DM Mono',monospace;font-size:28px;font-weight:500;color:var(--gold-lt);line-height:1;}
.hero-stat-lbl{font-size:10px;color:rgba(245,239,230,0.4);text-transform:uppercase;letter-spacing:0.12em;margin-top:4px;font-weight:500;}
.hero-divider{width:1px;height:50px;background:rgba(255,255,255,0.1);align-self:center;}

/* TABS */
.stTabs [data-baseweb="tab-list"]{gap:0;border-bottom:2px solid var(--border);background:transparent;}
.stTabs [data-baseweb="tab"]{font-family:'DM Sans',sans-serif!important;font-size:12px!important;font-weight:600!important;letter-spacing:0.1em!important;text-transform:uppercase!important;color:var(--muted)!important;padding:12px 20px!important;border-bottom:2px solid transparent!important;margin-bottom:-2px!important;background:transparent!important;}
.stTabs [aria-selected="true"]{color:var(--spice)!important;border-bottom-color:var(--spice)!important;}
.stTabs [data-baseweb="tab-panel"]{padding-top:24px!important;}

/* SECTION HEADERS */
.sec-head{display:flex;align-items:center;gap:14px;margin:28px 0 16px;}
.sec-head-line{flex:1;height:1px;background:var(--border);}
.sec-head-text{font-size:11px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:var(--spice);white-space:nowrap;}

/* STATUS BANNERS */
.status-success{background:linear-gradient(135deg,#0F2818,#143521);border:1px solid rgba(26,107,58,0.5);border-left:4px solid var(--green-lt);border-radius:12px;padding:14px 20px;margin:16px 0;display:flex;align-items:center;gap:12px;font-size:13px;color:#A7F3C8;font-weight:500;}
.status-info{background:linear-gradient(135deg,#0D1A2E,#112040);border:1px solid rgba(59,130,246,0.3);border-left:4px solid #60A5FA;border-radius:12px;padding:14px 20px;margin:16px 0;font-size:13px;color:#93C5FD;}

/* TOP 10 DISH CARD */
.top-dish-card{background:var(--card-bg);border:1px solid var(--border);border-radius:16px;padding:20px 24px;margin-bottom:6px;display:flex;align-items:flex-start;gap:18px;transition:box-shadow 0.2s;box-shadow:0 2px 8px rgba(0,0,0,0.04);}
.top-dish-card:hover{box-shadow:0 8px 28px rgba(196,65,26,0.12);}
.top-dish-card.wishlisted{border-color:rgba(139,92,246,0.4);background:rgba(139,92,246,0.04);}
.top-dish-rank{font-family:'DM Mono',monospace;font-size:28px;font-weight:700;color:var(--spice);line-height:1;min-width:40px;}
.top-dish-rank.top3{color:var(--gold);font-size:32px;}
.top-dish-content{flex:1;}
.top-dish-name{font-family:'Playfair Display',serif;font-size:20px;font-weight:700;color:var(--ink);margin-bottom:4px;}
.top-dish-desc{font-size:13px;color:var(--muted);line-height:1.6;margin-bottom:10px;}
.top-dish-tags{display:flex;flex-wrap:wrap;gap:8px;}
.top-dish-tag{font-size:11px;font-weight:600;letter-spacing:0.05em;padding:4px 10px;border-radius:20px;background:rgba(196,65,26,0.08);color:var(--spice);border:1px solid rgba(196,65,26,0.2);}
.top-dish-tag.green{background:rgba(26,107,58,0.08);color:var(--green);border-color:rgba(26,107,58,0.2);}
.top-dish-tag.gold{background:rgba(212,160,23,0.1);color:#8B6914;border-color:rgba(212,160,23,0.3);}
.top-dish-price{font-family:'DM Mono',monospace;font-size:18px;font-weight:600;color:var(--green);white-space:nowrap;padding-top:4px;}
.top-dish-restaurant{font-size:12px;color:var(--muted);margin-top:6px;}
.top-dish-restaurant strong{color:var(--ink);}
.top-dish-must-try{font-size:12px;color:var(--spice);font-style:italic;margin-top:5px;}

/* WISHLIST */
.wish-card{background:var(--card-bg);border:1px solid rgba(139,92,246,0.25);border-radius:16px;padding:20px 22px;margin-bottom:14px;box-shadow:0 2px 10px rgba(139,92,246,0.06);}
.wish-card-city{font-size:10px;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:var(--purple-lt);margin-bottom:4px;}
.wish-card-name{font-family:'Playfair Display',serif;font-size:18px;font-weight:700;color:var(--ink);}
.wish-card-rest{font-size:12px;color:var(--muted);margin-top:3px;}
.wish-card-price{font-family:'DM Mono',monospace;font-size:15px;font-weight:600;color:var(--green);}
.wish-note{background:rgba(139,92,246,0.06);border:1px solid rgba(139,92,246,0.15);border-radius:8px;padding:10px 12px;font-size:12px;color:#4A3F37;font-style:italic;margin-top:10px;line-height:1.5;}

/* FEEDBACK */
.fb-card{background:var(--card-bg);border:1px solid var(--border);border-radius:16px;padding:20px 22px;margin-bottom:14px;box-shadow:0 2px 8px rgba(0,0,0,0.04);}
.fb-author{font-size:15px;font-weight:700;color:var(--ink);}
.fb-city{font-size:11px;color:var(--muted);margin-top:2px;}
.fb-category{display:inline-block;font-size:10px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:3px 10px;border-radius:20px;background:rgba(196,65,26,0.08);color:var(--spice);border:1px solid rgba(196,65,26,0.2);margin-top:6px;}
.fb-comment{font-size:13px;color:#4A3F37;line-height:1.7;margin-top:10px;}

/* STATS ROW */
.stats-row{display:flex;gap:16px;margin-bottom:24px;}
.stat-pill{flex:1;background:var(--card-bg);border:1px solid var(--border);border-radius:14px;padding:18px 20px;text-align:center;}
.stat-pill-num{font-family:'DM Mono',monospace;font-size:28px;font-weight:700;color:var(--spice);line-height:1;}
.stat-pill-lbl{font-size:11px;color:var(--muted);margin-top:4px;font-weight:500;}

/* DISH SPECIALS */
.dish-card{background:var(--card-bg);border:1px solid var(--border);border-radius:18px;overflow:hidden;margin-bottom:18px;transition:box-shadow 0.2s,transform 0.15s;box-shadow:0 2px 12px rgba(0,0,0,0.04);}
.dish-card:hover{box-shadow:0 12px 40px rgba(196,65,26,0.14);transform:translateY(-2px);}
.dish-card-header{padding:22px 24px 18px;position:relative;}
.dish-card-header.margin{background:linear-gradient(135deg,#1A0E08,#2D1507);}
.dish-card-header.premium{background:linear-gradient(135deg,#120D1A,#1E1030);}
.dish-card-header.insta{background:linear-gradient(135deg,#0A1A1A,#0D2929);}
.dish-card-header.performer{background:linear-gradient(135deg,#0A0D1A,#111830);}
.dish-header-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:12px;}
.dish-badge{font-size:11px;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;padding:5px 12px;border-radius:20px;}
.badge-margin{background:rgba(212,160,23,0.2);color:#F0C040;border:1px solid rgba(212,160,23,0.4);}
.badge-premium{background:rgba(139,92,246,0.2);color:#C4B5FD;border:1px solid rgba(139,92,246,0.4);}
.badge-insta{background:rgba(34,160,90,0.2);color:#6EE7B7;border:1px solid rgba(34,160,90,0.4);}
.badge-performer{background:rgba(239,68,68,0.2);color:#FCA5A5;border:1px solid rgba(239,68,68,0.4);}
.dish-price-badge{font-family:'DM Mono',monospace;font-size:14px;font-weight:600;color:#F0C040;text-align:right;}
.dish-name{font-family:'Playfair Display',serif;font-size:22px;font-weight:800;color:#F5EFE6;line-height:1.15;margin-bottom:6px;}
.dish-key-ing{font-size:11px;color:rgba(245,239,230,0.45);letter-spacing:0.06em;}
.dish-card-body{padding:20px 24px;}
.dish-desc{font-size:13.5px;color:#4A3F37;line-height:1.7;margin-bottom:18px;}
.dish-meta-row{display:flex;gap:16px;flex-wrap:wrap;margin-bottom:16px;}
.dish-meta-item{flex:1;min-width:80px;}
.dmi-label{font-size:10px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#A89F97;margin-bottom:4px;}
.dmi-value{font-size:13px;font-weight:600;color:var(--ink);}
.dmi-value.spice{color:var(--spice);}
.dmi-value.green{color:var(--green);}
.dish-inspired{background:var(--paper);border-radius:10px;padding:12px 16px;font-size:13px;color:var(--muted);display:flex;align-items:center;gap:10px;}
.demand-high-wrap .demand-dot{width:7px;height:7px;border-radius:50%;background:#22A05A;display:inline-block;margin-right:4px;}
.demand-medium-wrap .demand-dot{width:7px;height:7px;border-radius:50%;background:#F0C040;display:inline-block;margin-right:4px;}
.demand-low-wrap .demand-dot{width:7px;height:7px;border-radius:50%;background:#EF4444;display:inline-block;margin-right:4px;}
.demand-label{font-size:11px;font-weight:600;}
.demand-high-wrap .demand-label{color:#22A05A;}
.demand-medium-wrap .demand-label{color:#D4A017;}
.demand-low-wrap .demand-label{color:#EF4444;}
.tip-block{border-radius:10px;padding:14px 16px;margin-bottom:10px;}
.tip-block.plating{background:rgba(212,160,23,0.08);border-left:3px solid var(--gold);}
.tip-block.reels{background:rgba(26,107,58,0.08);border-left:3px solid var(--green);}
.tip-block.trend{background:rgba(196,65,26,0.07);border-left:3px solid var(--spice);}
.tip-label{font-size:11px;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:6px;}
.tip-block.plating .tip-label{color:var(--gold);}
.tip-block.reels .tip-label{color:var(--green);}
.tip-block.trend .tip-label{color:var(--spice);}
.tip-text{font-size:13px;color:var(--ink);line-height:1.6;}
.insight-box{background:var(--ink);border-radius:18px;padding:30px 36px;margin:28px 0;position:relative;overflow:hidden;}
.insight-eyebrow{font-size:10px;font-weight:700;letter-spacing:0.3em;text-transform:uppercase;color:var(--spice-lt);margin-bottom:8px;}
.insight-city{font-family:'Playfair Display',serif;font-size:24px;font-weight:700;color:#F5EFE6;margin-bottom:14px;}
.insight-text{font-size:15px;color:rgba(245,239,230,0.75);line-height:1.75;margin-bottom:18px;}
.insight-revenue{font-size:13px;color:var(--gold-lt);font-weight:600;}
.ing-pill{background:var(--card-bg);border:1px solid var(--border);border-radius:14px;padding:16px 18px;text-align:center;}
.ing-pill-icon{font-size:24px;display:block;margin-bottom:8px;}
.ing-rank{font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:var(--muted);}
.trend-card{background:var(--card-bg);border:1px solid var(--border);border-radius:14px;padding:18px 20px;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center;}
.trend-card-left{flex:1;}
.trend-card-name{font-size:16px;font-weight:700;color:var(--ink);margin-bottom:4px;}
.trend-card-context{font-size:12px;color:var(--muted);}
.trend-badge{font-size:11px;font-weight:700;padding:4px 12px;border-radius:20px;white-space:nowrap;margin-left:12px;}
.trend-badge.hot{background:rgba(196,65,26,0.12);color:var(--spice);border:1px solid rgba(196,65,26,0.3);}
.trend-badge.rising{background:rgba(212,160,23,0.12);color:#8B6914;border:1px solid rgba(212,160,23,0.3);}
.trend-badge.steady{background:rgba(26,107,58,0.1);color:var(--green);border:1px solid rgba(26,107,58,0.25);}
.trend-pct{font-family:'DM Mono',monospace;font-size:18px;font-weight:700;color:var(--spice);margin-left:16px;white-space:nowrap;}
.hashtag-pill{display:inline-block;background:rgba(196,65,26,0.08);color:var(--spice);border:1px solid rgba(196,65,26,0.2);border-radius:20px;padding:6px 14px;font-size:13px;font-weight:600;margin:4px;}
.hashtag-pill.viral{background:rgba(196,65,26,0.15);font-size:14px;}
.hashtag-pill.hot{background:rgba(212,160,23,0.12);color:#8B6914;border-color:rgba(212,160,23,0.3);}
.hashtag-pill.rising{background:rgba(26,107,58,0.1);color:var(--green);border-color:rgba(26,107,58,0.25);}
.empty-state{text-align:center;padding:80px 40px;background:var(--card-bg);border:2px dashed var(--border);border-radius:20px;}
.empty-icon{font-size:48px;margin-bottom:16px;}
.empty-title{font-family:'Playfair Display',serif;font-size:24px;font-weight:700;color:var(--ink);margin-bottom:8px;}
.empty-sub{font-size:14px;color:var(--muted);}
.report-header{background:var(--ink);border-radius:16px;padding:24px 28px;margin-bottom:20px;display:flex;justify-content:space-between;align-items:center;}
.report-title{font-family:'Playfair Display',serif;font-size:26px;font-weight:700;color:#F5EFE6;}
.report-subtitle{font-size:12px;color:rgba(245,239,230,0.5);margin-top:6px;}
.report-body{background:var(--card-bg);border:1px solid var(--border);border-radius:16px;padding:32px 36px;font-size:14px;color:var(--ink);line-height:1.9;white-space:pre-wrap;}
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────
defaults = {
    "trend_analysis": None, "specials": None, "report_txt": None,
    "top_dishes": None, "last_city": None,
    "wishlist": None, "feedbacks": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

if st.session_state.wishlist is None:
    st.session_state.wishlist = load_json(WISHLIST_FILE)
if st.session_state.feedbacks is None:
    st.session_state.feedbacks = load_json(FEEDBACK_FILE)

# ── Lazy-load modules ──────────────────────────
@st.cache_resource(show_spinner=False)
def load_modules():
    try:
        from scraper.trend_scraper    import scrape_all_trends
        from llm.dish_generator       import run_full_pipeline
        from reports.report_generator import save_all
        return scrape_all_trends, run_full_pipeline, save_all, True
    except Exception:
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
        "Hyderabad","Chennai","Mumbai","Delhi","Bengaluru",
        "Kolkata","Lucknow","Amritsar","Goa","Jaipur",
        "Kochi","Indore","Pune","Ahmedabad","Chandigarh",
        "Varanasi","Agra","Vizag","Madurai","Bhopal",
    ], label_visibility="collapsed")

    st.markdown('<div class="sidebar-section-label">🍽 Outlet Profile</div>', unsafe_allow_html=True)
    rtype = st.selectbox("", [
        "Local Dhaba / Authentic","Modern Café / Bistro","Fine Dining",
        "Street Food Stall","Cloud Kitchen / Delivery","Family Restaurant",
        "Vegetarian / Pure Veg","Seafood Specialty","Biryani House","Mughlai / Awadhi",
    ], label_visibility="collapsed")

    st.markdown('<div class="sidebar-section-label">💰 Pricing Tier</div>', unsafe_allow_html=True)
    price = st.selectbox("", [
        "₹ (under ₹200/head)","₹₹ (₹200–600/head)",
        "₹₹₹ (₹600–1500/head)","₹₹₹₹ (₹1500+/head)",
    ], label_visibility="collapsed")

    st.markdown('<div class="sidebar-section-label">🌦 Season</div>', unsafe_allow_html=True)
    season = st.selectbox("", [
        "Summer (Mar–Jun)","Monsoon (Jul–Sep)",
        "Festive / Post-Monsoon (Oct–Nov)","Winter (Dec–Feb)",
    ], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    scan_btn     = st.button("🕷 Scan Trends",      use_container_width=True, type="secondary")
    generate_btn = st.button("✦ Generate Specials",  use_container_width=True, type="primary")

    wl_count = len(st.session_state.wishlist)
    if wl_count:
        st.markdown(f"""
        <div style="margin-top:14px;background:rgba(139,92,246,0.12);border:1px solid rgba(139,92,246,0.3);
        border-radius:10px;padding:11px 14px;text-align:center;font-size:13px;color:#C4B5FD;font-weight:600;">
        💜 {wl_count} item{"s" if wl_count!=1 else ""} saved in Wishlist
        </div>""", unsafe_allow_html=True)

    if not modules_ok:
        st.markdown("""
        <div style="background:rgba(196,65,26,0.15);border:1px solid rgba(196,65,26,0.4);
        border-radius:8px;padding:12px;margin-top:16px;font-size:11px;color:#E8DDD4;">
        ⚠️ Add ANTHROPIC_API_KEY to .env to enable AI generation.
        </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
#  HERO
# ══════════════════════════════════════════════════════
data_pts  = len(st.session_state.trend_analysis.get("trending_ingredients",[])) * 12 if st.session_state.trend_analysis else "—"
dishes_n  = len(st.session_state.specials.get("weekend_specials",[])) if st.session_state.specials else (
            len(st.session_state.top_dishes.get("top_dishes",[])) if st.session_state.top_dishes else 0)

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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Trend Analysis",
    "🏆 Top 10 Dishes",
    "🍽 Weekend Specials",
    "📋 Weekly Report",
    f"💜 Wishlist  ({len(st.session_state.wishlist)})",
    "⭐ Feedback",
])

# ════════════════════════════════════════════════════
#  SCAN TRENDS
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
            st.session_state.trend_analysis = {
                "city": city,
                "analysis_summary": f"{city} is experiencing a surge in fusion street food and premium biryani variants.",
                "trending_ingredients": [
                    {"name":"Smoked Butter","emoji":"🧈","growth_pct":420,"context":f"Trending across cafés in {city}","status":"hot"},
                    {"name":"Black Garlic","emoji":"🧄","growth_pct":310,"context":"Premium modern Indian ingredient","status":"hot"},
                    {"name":"Kokum","emoji":"🍇","growth_pct":280,"context":"Regional sourness replacing tamarind","status":"rising"},
                ],
                "famous_dishes_trending": [
                    {"dish_name":"Biryani","famous_at":"Paradise Restaurant","saves_estimate":"82k","engagement_pct":94,"why_famous":"70-year recipe"},
                    {"dish_name":"Haleem","famous_at":"Shah Ghouse","saves_estimate":"56k","engagement_pct":88,"why_famous":"Slow-cooked 8 hours"},
                ],
                "viral_hashtags": [
                    {"tag":f"#{city}Food","growth_pct":720,"type":"viral"},
                    {"tag":"#IndianFoodLover","growth_pct":450,"type":"hot"},
                ],
                "declining_trends": [{"name":"Plain Paneer Tikka","decline_pct":"-28%","reason":"Over-saturated"}],
                "engagement_patterns": "Short-form Reels showing live cooking get 3× more saves",
                "stats": {"posts_analyzed":"142k","top_dish_saves":"82k","hashtags_count":18},
            }
            st.session_state.last_city = city

# ════════════════════════════════════════════════════
#  GENERATE SPECIALS + TOP 10
# ════════════════════════════════════════════════════
if generate_btn:
    with st.spinner(f"🤖 Generating top dishes & specials for {city}…"):
        if modules_ok:
            try:
                if not st.session_state.trend_analysis or st.session_state.last_city != city:
                    scraped = scrape_fn(city, verbose=False)
                else:
                    scraped = {"city":city,"google_results":[],"zomato_data":[],"articles":[],"hashtags":[]}
                output = pipeline_fn(scraped_data=scraped, restaurant_type=rtype, price_range=price, season=season, verbose=False)
                st.session_state.trend_analysis = output["trend_analysis"]
                st.session_state.specials        = output["specials"]
                st.session_state.report_txt      = output["weekly_report"]
                st.session_state.last_city       = city
                from llm.dish_generator import generate_top_dishes
                st.session_state.top_dishes = generate_top_dishes(city)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            import anthropic, re
            api_key = os.getenv("ANTHROPIC_API_KEY","")
            generated_ok = False
            if api_key:
                try:
                    client = anthropic.Anthropic(api_key=api_key)
                    prompt = f"""You are India's top food expert. List the top 10 BEST iconic dishes in {city}, India.
Return ONLY valid JSON (no markdown):
{{"city":"{city}","top_dishes":[{{"rank":1,"dish_name":"","restaurant":"Best place in {city}","why_famous":"2 sentences","unique_factor":"what makes it special","price_range":"₹XXX–₹YYY","best_time":"breakfast|lunch|dinner|anytime","must_try_reason":"one compelling sentence","tags":["tag1","tag2"]}}],"city_food_culture":"2 sentence summary"}}"""
                    resp = client.messages.create(model="claude-opus-4-6", max_tokens=3000, messages=[{"role":"user","content":prompt}])
                    raw  = re.sub(r"```json|```","", resp.content[0].text).strip()
                    st.session_state.top_dishes = json.loads(raw)
                    generated_ok = True
                except Exception:
                    pass

            if not generated_ok:
                st.session_state.top_dishes = {
                    "city": city,
                    "city_food_culture": f"{city} is celebrated for bold spices, slow-cooked traditions, and street food culture.",
                    "top_dishes": [
                        {"rank":1,"dish_name":"Hyderabadi Dum Biryani","restaurant":"Paradise Restaurant","why_famous":"Slow-cooked 4 hrs with aged basmati & premium mutton. Saffron aroma fills the street.","unique_factor":"Sealed dum, 70-year recipe","price_range":"₹280–₹450","best_time":"lunch","must_try_reason":"The gold standard of Indian biryani.","tags":["Iconic","Must-Try","Non-Veg"]},
                        {"rank":2,"dish_name":"Haleem","restaurant":"Shah Ghouse Café","why_famous":"Eight-hour slow cook of wheat, barley and meat into silky porridge.","unique_factor":"Ghee tempering with crispy onions","price_range":"₹150–₹220","best_time":"dinner","must_try_reason":"Once you try Shah Ghouse Haleem, no other will satisfy.","tags":["Street Food","Iconic"]},
                        {"rank":3,"dish_name":"Irani Chai + Osmania Biscuit","restaurant":"Nimrah Café, Charminar","why_famous":"Persian-influenced milky tea brewed for hours with melt-in-mouth butter biscuits.","unique_factor":"Tea brewed on low flame 2+ hrs","price_range":"₹20–₹40","best_time":"breakfast","must_try_reason":"Most Hyderabadi experience under ₹50.","tags":["Budget","Iconic","Veg"]},
                        {"rank":4,"dish_name":"Pathar Gosht","restaurant":"Bawarchi Restaurant","why_famous":"Mutton cooked on heated stone slab, beautiful crust while staying juicy.","unique_factor":"Stone-slab gives unique char","price_range":"₹350–₹500","best_time":"dinner","must_try_reason":"Theatrical cooking meets incredible flavour.","tags":["Premium","Non-Veg"]},
                        {"rank":5,"dish_name":"Double Ka Meetha","restaurant":"Hotel Shadab","why_famous":"Bread pudding soaked in reduced milk, dry fruits and silver leaf.","unique_factor":"Day-old bread for better texture","price_range":"₹80–₹120","best_time":"anytime","must_try_reason":"The royal Nizam dessert.","tags":["Dessert","Veg","Royal"]},
                    ]
                }

            st.session_state.specials = {
                "city":city,"generated_at":datetime.now().isoformat(),
                "top_weekend_ingredients":["Smoked Butter","Black Garlic","Saffron"],
                "weekend_specials":[
                    {"dish_name":"Charcoal Dum Biryani","category":"low-cost high-margin",
                     "key_trending_ingredient":"Activated Charcoal","inspired_by":"Paradise Biryani",
                     "description":"Classic dum biryani with activated charcoal rice. Served in a sealed handi at the table.",
                     "ingredients_needed":["Aged basmati","Mutton","Charcoal dye","Saffron"],
                     "prep_time_mins":90,"food_cost_level":"Low","estimated_food_cost_inr":"₹80–₹120",
                     "suggested_price_range":"₹380–₹450","gross_margin_pct":"approx 72%",
                     "plating_tip":"Black ceramic handi, crack seal tableside for steam effect",
                     "reels_tip":"Film the handi crack in slow motion — guaranteed viral",
                     "why_it_will_trend":"Charcoal aesthetics + classic taste = perfect Reels",
                     "predicted_demand":"High","best_served":"dinner"},
                ],
                "strategic_insight":f"Focus on instagrammable presentation in {city} this weekend.",
                "revenue_projection":"₹45,000–₹65,000 additional weekend revenue"
            }
            st.session_state.report_txt = f"WEEKLY FOOD TREND REPORT — {city.upper()}\n\nThis week {city} shows strong momentum in fusion and premium street food. Weekend footfall expected 20% above average.\n\nSTRATEGY: Lead with visual-first dishes that drive social sharing."
            st.session_state.last_city  = city

# ════════════════════════════════════════════════════
#  TAB 1 — TREND ANALYSIS
# ════════════════════════════════════════════════════
with tab1:
    if not st.session_state.trend_analysis:
        st.markdown('<div class="empty-state"><div class="empty-icon">📊</div><div class="empty-title">No Analysis Yet</div><div class="empty-sub">Select a city · Scan Trends · Generate Specials</div></div>', unsafe_allow_html=True)
    else:
        ta = st.session_state.trend_analysis
        st.markdown(f'<div class="status-success"><span style="font-size:18px">✅</span><div><strong>{ta.get("city",city)} — Trend Analysis Complete</strong><br><span style="opacity:0.7;font-size:12px">{ta.get("analysis_summary","")}</span></div></div>', unsafe_allow_html=True)

        for ing in ta.get("trending_ingredients",[]):
            status = ing.get("status","hot")
            st.markdown(f'<div class="trend-card"><div class="trend-card-left"><div class="trend-card-name">{ing.get("emoji","")} {ing.get("name","")}</div><div class="trend-card-context">{ing.get("context","")}</div></div><span class="trend-badge {status}">{status.upper()}</span><div class="trend-pct">+{ing.get("growth_pct",0)}%</div></div>', unsafe_allow_html=True)

        hashtags = ta.get("viral_hashtags",[])
        if hashtags:
            st.markdown('<div class="sec-head"><div class="sec-head-text">📲 Viral Hashtags</div><div class="sec-head-line"></div></div>', unsafe_allow_html=True)
            pills = " ".join([f'<span class="hashtag-pill {h.get("type","")}">{h.get("tag","")} +{h.get("growth_pct",0)}%</span>' for h in hashtags])
            st.markdown(f'<div style="margin:8px 0 20px">{pills}</div>', unsafe_allow_html=True)

        if ta.get("engagement_patterns"):
            st.markdown(f'<div class="status-info" style="margin-top:16px">📲 <strong>Engagement Pattern:</strong> {ta["engagement_patterns"]}</div>', unsafe_allow_html=True)

        for d in ta.get("declining_trends",[]):
            st.markdown(f'<div class="trend-card"><div class="trend-card-left"><div class="trend-card-name">⚠️ {d.get("name","")}</div><div class="trend-card-context">{d.get("reason","")}</div></div><div class="trend-pct" style="color:#EF4444">{d.get("decline_pct","")}</div></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════
#  TAB 2 — TOP 10 DISHES  (♥ Wishlist)
# ════════════════════════════════════════════════════
with tab2:
    if not st.session_state.top_dishes:
        st.markdown('<div class="empty-state"><div class="empty-icon">🏆</div><div class="empty-title">No Top Dishes Yet</div><div class="empty-sub">Click <strong>✦ Generate Specials</strong> to discover the top 10 iconic dishes for your city</div></div>', unsafe_allow_html=True)
    else:
        td        = st.session_state.top_dishes
        city_name = td.get("city", city)
        culture   = td.get("city_food_culture","")

        st.markdown(f'<div class="status-success"><span style="font-size:22px">🏆</span><div><strong>Top 10 Must-Eat Dishes in {city_name}</strong><br><span style="opacity:0.75;font-size:13px">{culture}</span></div></div>', unsafe_allow_html=True)
        st.markdown('<div class="sec-head"><div class="sec-head-text">🥇 Click 🤍 on any dish to save it to your Wishlist</div><div class="sec-head-line"></div></div>', unsafe_allow_html=True)

        for dish in td.get("top_dishes",[]):
            rank    = dish.get("rank",0)
            tags    = dish.get("tags",[])
            tag_cls = ["","green","gold"]
            tag_html = " ".join([f'<span class="top-dish-tag {tag_cls[i%3]}">{t}</span>' for i,t in enumerate(tags)])
            wl_key  = f"{city_name}::{dish.get('dish_name','')}"
            in_wl   = any(w["id"] == wl_key for w in st.session_state.wishlist)
            card_cls = "top-dish-card wishlisted" if in_wl else "top-dish-card"

            st.markdown(f"""
            <div class="{card_cls}">
              <div class="top-dish-rank {'top3' if rank<=3 else ''}">#{rank}</div>
              <div class="top-dish-content">
                <div class="top-dish-name">{dish.get('dish_name','')}</div>
                <div class="top-dish-desc">{dish.get('why_famous','')} {dish.get('unique_factor','')}</div>
                <div class="top-dish-tags">{tag_html}</div>
                <div class="top-dish-restaurant">🏠 Best at: <strong>{dish.get('restaurant','')}</strong> &nbsp;·&nbsp; 🕐 {str(dish.get('best_time','anytime')).title()}</div>
                <div class="top-dish-must-try">✦ {dish.get('must_try_reason','')}</div>
              </div>
              <div style="text-align:right;flex-shrink:0">
                <div class="top-dish-price">{dish.get('price_range','')}</div>
              </div>
            </div>""", unsafe_allow_html=True)

            btn_col, _ = st.columns([1,5])
            with btn_col:
                wish_label = "💜 Wishlisted" if in_wl else "🤍 Save to Wishlist"
                if st.button(wish_label, key=f"wb_{wl_key}", use_container_width=True):
                    if in_wl:
                        st.session_state.wishlist = [w for w in st.session_state.wishlist if w["id"] != wl_key]
                    else:
                        st.session_state.wishlist.append({
                            "id": wl_key, "city": city_name,
                            "dish_name":  dish.get("dish_name",""),
                            "restaurant": dish.get("restaurant",""),
                            "price_range":dish.get("price_range",""),
                            "best_time":  dish.get("best_time",""),
                            "tags": tags, "note": "",
                            "added_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                        })
                    save_json(WISHLIST_FILE, st.session_state.wishlist)
                    st.rerun()

        if td.get("top_dishes"):
            df_top = pd.DataFrame([{"Rank":d.get("rank",""),"Dish":d.get("dish_name",""),"Restaurant":d.get("restaurant",""),"Price":d.get("price_range",""),"Best Time":d.get("best_time","")} for d in td["top_dishes"]])
            st.download_button("⬇ Download Top 10 CSV", df_top.to_csv(index=False), file_name=f"top10_{city_name.lower()}_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

# ════════════════════════════════════════════════════
#  TAB 3 — WEEKEND SPECIALS
# ════════════════════════════════════════════════════
with tab3:
    specials = st.session_state.specials
    if not specials:
        st.markdown('<div class="empty-state"><div class="empty-icon">🍽</div><div class="empty-title">No Specials Generated Yet</div><div class="empty-sub">Click <strong>✦ Generate Specials</strong></div></div>', unsafe_allow_html=True)
    else:
        top_ings = specials.get("top_weekend_ingredients",[])
        if top_ings:
            st.markdown('<div class="sec-head"><div class="sec-head-text">🏆 Top Revenue Ingredients</div><div class="sec-head-line"></div></div>', unsafe_allow_html=True)
            ing_icons = ["🌶","🧄","🫚","🌿","🥛","🍅","🧅","🫙"]
            cols = st.columns(len(top_ings))
            for i,(col,ing) in enumerate(zip(cols,top_ings)):
                with col:
                    st.markdown(f'<div class="ing-pill"><span class="ing-pill-icon">{ing_icons[i%8]}</span><div class="ing-rank">#{i+1} Pick</div><div style="margin-top:4px;font-size:13px;font-weight:700;color:#C4411A">{ing}</div></div>', unsafe_allow_html=True)

        st.markdown('<div class="sec-head"><div class="sec-head-text">✦ Weekend Special Dishes</div><div class="sec-head-line"></div></div>', unsafe_allow_html=True)
        dishes = specials.get("weekend_specials",[])
        for i in range(0, len(dishes), 2):
            c1,c2 = st.columns(2)
            for col,dish in zip([c1,c2], dishes[i:i+2]):
                cat = dish.get("category","")
                if   "margin"    in cat.lower(): hdr_cls,badge_cls,badge_lbl = "margin","badge-margin","💰 High Margin"
                elif "premium"   in cat.lower(): hdr_cls,badge_cls,badge_lbl = "premium","badge-premium","👑 Premium Upsell"
                elif "instagram" in cat.lower(): hdr_cls,badge_cls,badge_lbl = "insta","badge-insta","📸 Reels-Worthy"
                else:                            hdr_cls,badge_cls,badge_lbl = "performer","badge-performer","🔥 Weekend Hit"
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
                            <div class="{d_wrap}" style="margin-top:5px;text-align:right"><span class="demand-dot"></span><span class="demand-label">{demand} Demand</span></div>
                          </div>
                        </div>
                        <div class="dish-name">{dish.get('dish_name','')}</div>
                        <div class="dish-key-ing">Key ingredient: {dish.get('key_trending_ingredient','')}</div>
                      </div>
                      <div class="dish-card-body">
                        <div class="dish-desc">{dish.get('description','')}</div>
                        <div class="dish-meta-row">
                          <div class="dish-meta-item"><div class="dmi-label">Food Cost</div><div class="dmi-value spice">{dish.get('food_cost_level','')} · {dish.get('estimated_food_cost_inr','')}</div></div>
                          <div class="dish-meta-item"><div class="dmi-label">Gross Margin</div><div class="dmi-value green">{dish.get('gross_margin_pct','')}</div></div>
                          <div class="dish-meta-item"><div class="dmi-label">Prep Time</div><div class="dmi-value">{dish.get('prep_time_mins','')} mins</div></div>
                          <div class="dish-meta-item"><div class="dmi-label">Best Served</div><div class="dmi-value">{str(dish.get('best_served','')).title()}</div></div>
                        </div>
                        <div class="dish-inspired"><span style="font-size:16px">🏠</span> Inspired by <strong>{dish.get('inspired_by','—')}</strong></div>
                      </div>
                    </div>""", unsafe_allow_html=True)
                    with st.expander("📸 Plating · Reels · Trend Tips"):
                        st.markdown(f"""
                        <div class="tip-block plating"><div class="tip-label">🎨 Plating Tip</div><div class="tip-text">{dish.get('plating_tip','')}</div></div>
                        <div class="tip-block reels"><div class="tip-label">🎬 Reels Tip</div><div class="tip-text">{dish.get('reels_tip','')}</div></div>
                        <div class="tip-block trend"><div class="tip-label">🚀 Why It'll Trend</div><div class="tip-text">{dish.get('why_it_will_trend','')}</div></div>""", unsafe_allow_html=True)

        if specials.get("strategic_insight"):
            st.markdown(f'<div class="insight-box"><div class="insight-eyebrow">✦ Strategic Intelligence</div><div class="insight-city">{specials.get("city","")} — This Weekend</div><div class="insight-text">{specials.get("strategic_insight","")}</div><div class="insight-revenue">📈 &nbsp; Revenue Projection: {specials.get("revenue_projection","")}</div></div>', unsafe_allow_html=True)

        if dishes:
            df_d = pd.DataFrame([{"Dish":d.get("dish_name",""),"Category":d.get("category",""),"Price":d.get("suggested_price_range",""),"Margin":d.get("gross_margin_pct",""),"Demand":d.get("predicted_demand","")} for d in dishes])
            st.download_button("⬇ Download Specials CSV", df_d.to_csv(index=False), file_name=f"specials_{city.lower()}_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

# ════════════════════════════════════════════════════
#  TAB 4 — WEEKLY REPORT
# ════════════════════════════════════════════════════
with tab4:
    if not st.session_state.report_txt:
        st.markdown('<div class="empty-state"><div class="empty-icon">📋</div><div class="empty-title">No Report Yet</div><div class="empty-sub">Generate specials first</div></div>', unsafe_allow_html=True)
    else:
        c1,c2 = st.columns([3,1])
        with c1:
            st.markdown(f'<div class="report-header"><div><div class="report-title">Weekly Trend Report — {city}</div><div class="report-subtitle">{rtype} · {price} · {season} &nbsp;·&nbsp; {datetime.now().strftime("%A, %d %B %Y")}</div></div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.download_button("⬇ Download Report", st.session_state.report_txt, file_name=f"report_{city.lower()}_{datetime.now().strftime('%Y%m%d')}.txt", mime="text/plain", use_container_width=True)
        st.markdown(f'<div class="report-body">{st.session_state.report_txt.replace(chr(10),"<br>")}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════
#  TAB 5 — 💜 WISHLIST
# ════════════════════════════════════════════════════
with tab5:
    wishlist = st.session_state.wishlist
    cities_in_wl = list({w["city"] for w in wishlist}) if wishlist else []

    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-pill"><div class="stat-pill-num">{len(wishlist)}</div><div class="stat-pill-lbl">Items Saved</div></div>
      <div class="stat-pill"><div class="stat-pill-num">{len(cities_in_wl)}</div><div class="stat-pill-lbl">Cities</div></div>
      <div class="stat-pill"><div class="stat-pill-num">{len([w for w in wishlist if w.get("note")])}</div><div class="stat-pill-lbl">With Notes</div></div>
    </div>""", unsafe_allow_html=True)

    if not wishlist:
        st.markdown('<div class="empty-state"><div class="empty-icon">💜</div><div class="empty-title">Your Wishlist is Empty</div><div class="empty-sub">Go to <strong>🏆 Top 10 Dishes</strong> and click<br><strong>🤍 Save to Wishlist</strong> on any dish!</div></div>', unsafe_allow_html=True)
    else:
        clr_col, _ = st.columns([1,4])
        with clr_col:
            if st.button("🗑 Clear All", type="secondary", use_container_width=True):
                st.session_state.wishlist = []
                save_json(WISHLIST_FILE, [])
                st.rerun()

        # Group by city
        city_groups = {}
        for w in wishlist:
            city_groups.setdefault(w.get("city","Unknown"), []).append(w)

        for grp_city, items in city_groups.items():
            st.markdown(f'<div class="sec-head"><div class="sec-head-text">📍 {grp_city} — {len(items)} dish{"es" if len(items)!=1 else ""}</div><div class="sec-head-line"></div></div>', unsafe_allow_html=True)

            for item in items:
                wl_id    = item["id"]
                note_val = item.get("note","")
                tags     = item.get("tags",[])
                tag_html = " ".join([f'<span class="top-dish-tag">{t}</span>' for t in tags[:3]])

                st.markdown(f"""
                <div class="wish-card">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px;">
                    <div>
                      <div class="wish-card-city">💜 {item.get('city','')}</div>
                      <div class="wish-card-name">{item.get('dish_name','')}</div>
                      <div class="wish-card-rest">🏠 {item.get('restaurant','')}</div>
                    </div>
                    <div style="text-align:right">
                      <div class="wish-card-price">{item.get('price_range','')}</div>
                      <div style="font-size:11px;color:var(--muted);margin-top:3px">🕐 {str(item.get('best_time','anytime')).title()}</div>
                      <div style="font-size:10px;color:var(--muted);margin-top:4px">Saved {item.get('added_at','')}</div>
                    </div>
                  </div>
                  <div class="top-dish-tags" style="margin-bottom:0">{tag_html}</div>
                  {f'<div class="wish-note">📝 {note_val}</div>' if note_val else ''}
                </div>""", unsafe_allow_html=True)

                n_col, r_col = st.columns([5,1])
                with n_col:
                    new_note = st.text_input(
                        "Note", value=note_val, key=f"note_{wl_id}",
                        placeholder="📝 Add a personal note (e.g. Try on Sunday with family!)",
                        label_visibility="collapsed",
                    )
                    if new_note != note_val:
                        st.session_state.wishlist = [{**w,"note":new_note} if w["id"]==wl_id else w for w in st.session_state.wishlist]
                        save_json(WISHLIST_FILE, st.session_state.wishlist)

                with r_col:
                    if st.button("🗑 Remove", key=f"rm_{wl_id}", use_container_width=True):
                        st.session_state.wishlist = [w for w in st.session_state.wishlist if w["id"]!=wl_id]
                        save_json(WISHLIST_FILE, st.session_state.wishlist)
                        st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        df_wl = pd.DataFrame([{"City":w.get("city",""),"Dish":w.get("dish_name",""),"Restaurant":w.get("restaurant",""),"Price":w.get("price_range",""),"Best Time":w.get("best_time",""),"My Note":w.get("note",""),"Saved On":w.get("added_at","")} for w in wishlist])
        st.download_button("⬇ Download My Wishlist CSV", df_wl.to_csv(index=False), file_name=f"my_wishlist_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")

# ════════════════════════════════════════════════════
#  TAB 6 — ⭐ FEEDBACK
# ════════════════════════════════════════════════════
with tab6:
    feedbacks = st.session_state.feedbacks
    avg_rating = round(sum(f.get("rating",0) for f in feedbacks)/len(feedbacks),1) if feedbacks else 0
    pos_count  = len([f for f in feedbacks if f.get("rating",0)>=4])

    st.markdown(f"""
    <div class="stats-row">
      <div class="stat-pill"><div class="stat-pill-num">{len(feedbacks)}</div><div class="stat-pill-lbl">Total Reviews</div></div>
      <div class="stat-pill"><div class="stat-pill-num">{"⭐ "+str(avg_rating) if feedbacks else "—"}</div><div class="stat-pill-lbl">Avg Rating</div></div>
      <div class="stat-pill"><div class="stat-pill-num">{pos_count}</div><div class="stat-pill-lbl">Positive (4-5 ★)</div></div>
    </div>""", unsafe_allow_html=True)

    left_col, right_col = st.columns([1,1], gap="large")

    # ── FORM ──────────────────────────────────────────
    with left_col:
        st.markdown('<div class="sec-head"><div class="sec-head-text">✍ Leave a Review</div><div class="sec-head-line"></div></div>', unsafe_allow_html=True)

        fb_name = st.text_input("Your Name (optional)", placeholder="e.g. Ravi Kumar", key="fb_name")

        st.markdown("<p style='font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--spice);margin:14px 0 6px'>⭐ Rating</p>", unsafe_allow_html=True)
        rating_map = {"1 ★ — Poor":1,"2 ★★ — Fair":2,"3 ★★★ — Good":3,"4 ★★★★ — Great":4,"5 ★★★★★ — Excellent":5}
        fb_rating_lbl = st.selectbox("Rating", list(rating_map.keys()), index=4, label_visibility="collapsed", key="fb_rating")
        fb_rating_val = rating_map[fb_rating_lbl]

        st.markdown("<p style='font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--spice);margin:14px 0 6px'>📂 Category</p>", unsafe_allow_html=True)
        fb_category = st.selectbox("Category", [
            "Overall App","Top 10 Dishes Accuracy","Weekend Specials Quality",
            "Trend Analysis","Wishlist Feature","UI & Design","Other Suggestion",
        ], label_visibility="collapsed", key="fb_cat")

        st.markdown("<p style='font-size:11px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;color:var(--spice);margin:14px 0 6px'>💬 Your Feedback</p>", unsafe_allow_html=True)
        fb_comment = st.text_area("Feedback", placeholder="Tell us what you think — what worked, what didn't, what you'd love to see next…", height=120, label_visibility="collapsed", key="fb_comment")

        if st.button("✦ Submit Review", type="primary", use_container_width=True, key="fb_submit"):
            if not fb_comment.strip():
                st.warning("Please write your feedback before submitting.")
            else:
                entry = {
                    "id":       datetime.now().timestamp(),
                    "name":     fb_name.strip() or "Anonymous",
                    "city":     st.session_state.last_city or city,
                    "rating":   fb_rating_val,
                    "category": fb_category,
                    "comment":  fb_comment.strip(),
                    "added_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                }
                updated_fb = [entry] + feedbacks
                st.session_state.feedbacks = updated_fb
                save_json(FEEDBACK_FILE, updated_fb)
                st.success("✅ Thanks for your review! It helps us improve 🙏")
                st.rerun()

    # ── REVIEWS LIST ──────────────────────────────────
    with right_col:
        st.markdown('<div class="sec-head"><div class="sec-head-text">💬 All Reviews</div><div class="sec-head-line"></div></div>', unsafe_allow_html=True)

        if not feedbacks:
            st.markdown('<div class="empty-state" style="padding:40px"><div class="empty-icon">💬</div><div class="empty-title" style="font-size:18px">No Reviews Yet</div><div class="empty-sub">Be the first to leave a review!</div></div>', unsafe_allow_html=True)
        else:
            f_col, _ = st.columns([1,2])
            with f_col:
                filter_opt = st.selectbox("Filter", ["All ⭐","5 ★","4 ★","3 ★","2 ★","1 ★"], label_visibility="collapsed", key="fb_filter")
            filter_val = 0 if filter_opt.startswith("All") else int(filter_opt[0])
            shown = [f for f in feedbacks if filter_val==0 or f.get("rating",0)==filter_val]

            for fb in shown:
                r = fb.get("rating",0)
                stars = "★"*r + "☆"*(5-r)
                star_color = "#F0C040" if r>=4 else ("#E8572A" if r>=3 else "#EF4444")
                st.markdown(f"""
                <div class="fb-card">
                  <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:6px">
                    <div>
                      <div class="fb-author">{fb.get('name','Anonymous')}</div>
                      <div class="fb-city">📍 {fb.get('city','')} &nbsp;·&nbsp; {fb.get('added_at','')}</div>
                    </div>
                    <div style="text-align:right">
                      <div style="font-size:18px;color:{star_color}">{stars}</div>
                      <span class="fb-category">{fb.get('category','')}</span>
                    </div>
                  </div>
                  <div class="fb-comment">"{fb.get('comment','')}"</div>
                </div>""", unsafe_allow_html=True)

                del_col, _ = st.columns([1,6])
                with del_col:
                    if st.button("🗑 Delete", key=f"del_{fb['id']}", help="Delete review"):
                        st.session_state.feedbacks = [f for f in st.session_state.feedbacks if f["id"]!=fb["id"]]
                        save_json(FEEDBACK_FILE, st.session_state.feedbacks)
                        st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)
            df_fb = pd.DataFrame([{"Name":f.get("name",""),"City":f.get("city",""),"Rating":f.get("rating",""),"Category":f.get("category",""),"Comment":f.get("comment",""),"Date":f.get("added_at","")} for f in feedbacks])
            st.download_button("⬇ Export Reviews CSV", df_fb.to_csv(index=False), file_name=f"feedback_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")
