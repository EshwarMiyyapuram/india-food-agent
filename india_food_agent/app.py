"""
app.py  —  Streamlit Dashboard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
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
    page_title="🇮🇳 India Food Trend Agent",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif; }

.main { background: #FAF7F2; }

/* Header banner */
.hero-banner {
    background: linear-gradient(135deg, #1C1410 0%, #2d1f18 100%);
    border-bottom: 3px solid #FF6B00;
    padding: 20px 28px;
    border-radius: 14px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    gap: 16px;
}
.hero-title { font-size: 28px; font-weight: 800; color: #fff; margin: 0; }
.hero-title span { color: #FF9B45; }
.hero-sub { font-size: 12px; color: rgba(255,255,255,0.5); margin-top: 4px; letter-spacing: 0.15em; text-transform: uppercase; }

/* Metric cards */
.metric-card {
    background: white;
    border-radius: 14px;
    padding: 18px;
    border: 1.5px solid #EAE0D5;
    border-top: 3px solid #FF6B00;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    text-align: center;
}
.metric-label { font-size: 11px; font-weight: 600; color: #78716C; text-transform: uppercase; letter-spacing: 0.1em; }
.metric-value { font-size: 28px; font-weight: 800; color: #1C1410; margin: 6px 0; }
.metric-delta { font-size: 12px; color: #138808; font-weight: 600; }

/* Dish card */
.dish-card {
    background: white;
    border-radius: 16px;
    border: 1.5px solid #EAE0D5;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    position: relative;
    overflow: hidden;
}
.dish-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
}
.dish-card.margin::before  { background: linear-gradient(90deg, #138808, #00796B); }
.dish-card.premium::before { background: linear-gradient(90deg, #6D28D9, #A855F7); }
.dish-card.insta::before   { background: linear-gradient(90deg, #D81B60, #F97316); }
.dish-card.performer::before { background: linear-gradient(90deg, #FF6B00, #F5A623); }

.dish-name  { font-size: 19px; font-weight: 800; color: #1C1410; }
.dish-price { font-size: 17px; font-weight: 800; color: #FF6B00; font-family: monospace; }
.dish-desc  { font-size: 13px; color: #4B5563; line-height: 1.7; margin: 10px 0; }
.dish-badge {
    display: inline-block;
    padding: 3px 12px; border-radius: 20px;
    font-size: 10px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.06em;
    margin-bottom: 8px;
}
.badge-margin   { background: #E8F5E9; color: #138808; }
.badge-premium  { background: #EDE9FE; color: #6D28D9; }
.badge-insta    { background: #FCE4EC; color: #D81B60; }
.badge-performer { background: #FFF4EC; color: #CC5200; }

.demand-high   { background: #E8F5E9; color: #138808; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }
.demand-medium { background: #FFF4EC; color: #CC5200; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }
.demand-low    { background: #F5F0EB; color: #78716C; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }

/* Insight box */
.insight-box {
    background: #1C1410;
    color: white;
    border-radius: 14px;
    padding: 20px 24px;
    margin-top: 20px;
}
.insight-lbl { font-size: 10px; color: #F5A623; letter-spacing: 0.2em; text-transform: uppercase; font-weight: 700; margin-bottom: 8px; }
.insight-txt { font-size: 14px; color: #D1D5DB; line-height: 1.8; }

/* Hashtag chip */
.htag {
    display: inline-block;
    padding: 5px 12px; border-radius: 20px;
    font-size: 11px; font-weight: 700;
    margin: 3px;
}
.htag-viral  { background: #FCE4EC; color: #D81B60; border: 1px solid #D81B60; }
.htag-hot    { background: #FFF4EC; color: #CC5200; border: 1px solid #FF6B00; }
.htag-rising { background: #E8F5E9; color: #138808; border: 1px solid #138808; }
.htag-new    { background: #E0F2F1; color: #00796B; border: 1px solid #00796B; }

/* Section title */
.section-title {
    font-size: 11px; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.2em;
    color: #78716C; margin: 20px 0 12px;
    display: flex; align-items: center; gap: 10px;
}
.section-title::after { content: ''; flex: 1; height: 1px; background: #EAE0D5; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────
with st.sidebar:
    st.markdown("### 🇮🇳 Food Trend Agent")
    st.markdown("---")

    city = st.selectbox("📍 City", [
        "Hyderabad", "Chennai", "Mumbai", "Delhi", "Bengaluru",
        "Kolkata", "Lucknow", "Amritsar", "Goa", "Jaipur",
        "Kochi", "Indore", "Pune", "Ahmedabad", "Chandigarh",
        "Varanasi", "Agra", "Vizag", "Madurai", "Bhopal",
    ])

    rtype = st.selectbox("🍽 Restaurant Type", [
        "Local Dhaba / Authentic", "Modern Café / Bistro", "Fine Dining",
        "Street Food Stall", "Cloud Kitchen / Delivery", "Family Restaurant",
        "Vegetarian / Pure Veg", "Seafood Specialty", "Biryani House", "Mughlai / Awadhi",
    ])

    price = st.selectbox("💰 Price Range", [
        "₹ (under ₹200/head)", "₹₹ (₹200–600/head)",
        "₹₹₹ (₹600–1500/head)", "₹₹₹₹ (₹1500+/head)",
    ], index=2)

    season = st.selectbox("🌦 Season", [
        "Summer (Mar–Jun)", "Monsoon (Jul–Sep)",
        "Festive / Post-Monsoon (Oct–Nov)", "Winter (Dec–Feb)",
    ], index=1)

    st.markdown("---")
    scan_btn = st.button("📡 Scan Trends", use_container_width=True, type="secondary")
    gen_btn  = st.button("🤖 Generate Specials", use_container_width=True, type="primary")
    st.markdown("---")
    st.caption("**Stack:** Python · BeautifulSoup · Claude AI · Streamlit")
    st.caption("**Sources:** Google · Zomato · Times Food · Instagram")


# ── Session state ─────────────────────────
if "scraped"   not in st.session_state: st.session_state.scraped   = None
if "analysis"  not in st.session_state: st.session_state.analysis  = None
if "specials"  not in st.session_state: st.session_state.specials  = None
if "report_txt" not in st.session_state: st.session_state.report_txt = None


# ── Hero Banner ───────────────────────────
st.markdown("""
<div class="hero-banner">
  <div style="font-size:40px">🍛</div>
  <div>
    <div class="hero-title">भारत <span>FoodTrend</span> Agent</div>
    <div class="hero-sub">Python · Web Scraping · Claude AI · Every Indian State</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── SCAN TRENDS ───────────────────────────
if scan_btn:
    from scraper.trend_scraper import scrape_all_trends
    with st.spinner(f"📡 Scraping Google, Zomato & Instagram for {city}..."):
        scraped = scrape_all_trends(city, verbose=False)
        st.session_state.scraped = scraped
    total = sum(len(v) for k,v in scraped.items() if isinstance(v,list))
    st.success(f"✅ Scraped {total} data points from {city}!")


# ── SHOW SCRAPED DATA PREVIEW ─────────────
if st.session_state.scraped and not st.session_state.analysis:
    scraped = st.session_state.scraped
    st.markdown("---")
    st.markdown("### 📡 Raw Scraped Data Preview")

    col_g, col_z = st.columns(2)

    with col_g:
        st.markdown("#### 🔍 Google Results")
        google = scraped.get("google_results", [])
        if google:
            for r in google[:8]:
                st.markdown(f"""
                <div style="background:white;border:1px solid #EAE0D5;border-left:3px solid #FF6B00;
                            border-radius:8px;padding:10px 14px;margin-bottom:8px;">
                    <div style="font-weight:700;font-size:13px;color:#1C1410">{r.get('title','')}</div>
                    <div style="font-size:11px;color:#78716C;margin-top:4px">{r.get('snippet','')[:120]}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No Google results scraped (network may have blocked)")

    with col_z:
        st.markdown("#### 🍽 Zomato Trending")
        zomato = scraped.get("zomato_data", [])
        if zomato:
            for z in zomato[:10]:
                icon = "🍴" if z.get("type") == "restaurant" else ("🏷" if z.get("type") == "collection" else "🌶")
                st.markdown(f"""
                <div style="background:white;border:1px solid #EAE0D5;border-left:3px solid #E23744;
                            border-radius:8px;padding:8px 14px;margin-bottom:6px;
                            font-size:13px;font-weight:600;color:#1C1410">
                    {icon} {z.get('name','')} <span style="font-size:10px;color:#78716C;font-weight:400">[{z.get('type','')}]</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No Zomato data scraped (Zomato may have blocked the request)")

    col_a, col_h = st.columns(2)

    with col_a:
        st.markdown("#### 📰 Food Articles")
        articles = scraped.get("articles", [])
        if articles:
            for a in articles[:6]:
                st.markdown(f"""
                <div style="background:white;border:1px solid #EAE0D5;border-left:3px solid #138808;
                            border-radius:8px;padding:8px 14px;margin-bottom:6px;">
                    <div style="font-size:12px;font-weight:700;color:#1C1410">{a.get('headline','')}</div>
                    <div style="font-size:10px;color:#78716C;margin-top:2px">📰 {a.get('source','')}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No articles scraped")

    with col_h:
        st.markdown("#### 📸 Instagram Hashtags")
        hashtags = scraped.get("hashtags", [])
        if hashtags:
            html = ""
            for h in hashtags:
                t = h.get("type", "hot")
                cls = f"htag-{t}"
                html += f'<span class="htag {cls}">{h["hashtag"]} +{h["estimated_growth_pct"]}%</span> '
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.info("No hashtag data")

    st.markdown("---")
    st.info("👆 Scraped data ready! Now click **🤖 Generate Specials** to analyze with Claude AI.")


# ── GENERATE SPECIALS ─────────────────────
if gen_btn:
    if not st.session_state.scraped:
        st.warning("⚠️ Please scan trends first!")
    else:
        from llm.dish_generator import run_full_pipeline
        with st.spinner("🤖 Claude AI is analyzing trends and crafting specials..."):
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
        paths = save_all(output)
        st.success(f"✅ Reports saved! JSON + TXT + CSV")


# ── TABS ──────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊 Trend Analysis", "🍽 Weekend Specials", "📋 Weekly Report"])


# ════════════════════════════════
#  TAB 1: TREND ANALYSIS
# ════════════════════════════════
with tab1:
    analysis = st.session_state.analysis

    if not analysis:
        st.info("👈 Select a city and click **Scan Trends**, then **Generate Specials** to see the analysis.")
    else:
        # Stats row
        stats = analysis.get("stats", {})
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Ingredients Tracked",
                      len(analysis.get("trending_ingredients", [])),
                      "+3 new this week")
        with c2:
            st.metric("Posts Analyzed", stats.get("posts_analyzed", "—"), "+18%")
        with c3:
            st.metric("Viral Hashtags",
                      stats.get("hashtags_count", len(analysis.get("viral_hashtags", []))),
                      "+8 new")
        with c4:
            st.metric("Top Dish Saves", stats.get("top_dish_saves", "—"), "+24%")

        st.markdown(f"> 💬 **Analysis:** {analysis.get('analysis_summary','')}")
        st.markdown("---")

        col_left, col_right = st.columns(2)

        # ── Trending Ingredients Bar Chart ──
        with col_left:
            st.markdown('<div class="section-title">🔥 Trending Ingredients</div>', unsafe_allow_html=True)
            ings = analysis.get("trending_ingredients", [])
            if ings:
                df = pd.DataFrame([{
                    "Ingredient": f"{i.get('emoji','')} {i.get('name','')}",
                    "Growth %":   i.get("growth_pct", 0),
                    "Status":     i.get("status", "rising"),
                } for i in ings])
                color_map = {"hot": "#FF6B00", "rising": "#F5A623", "steady": "#138808"}
                fig = px.bar(df, x="Growth %", y="Ingredient", orientation="h",
                             color="Status", color_discrete_map=color_map,
                             template="simple_white",
                             labels={"Growth %": "Growth vs Last Week (%)"})
                fig.update_layout(height=350, margin=dict(l=0,r=0,t=20,b=0),
                                  showlegend=True, plot_bgcolor="#FAF7F2",
                                  paper_bgcolor="#FAF7F2",
                                  font=dict(family="Syne"))
                st.plotly_chart(fig, use_container_width=True)

        # ── Hashtag Grid ──
        with col_right:
            st.markdown('<div class="section-title">🏷 Viral Hashtags</div>', unsafe_allow_html=True)
            tags = analysis.get("viral_hashtags", [])
            html = ""
            for h in tags:
                cls = f"htag-{h.get('type','hot')}"
                html += f'<span class="htag {cls}">{h["tag"]} +{h["growth_pct"]}%</span>'
            st.markdown(html, unsafe_allow_html=True)

            st.markdown('<br><div class="section-title">📉 Declining — Avoid</div>', unsafe_allow_html=True)
            for d in analysis.get("declining_trends", []):
                st.markdown(f"🔻 **{d['name']}** — `{d['decline_pct']}` — *{d.get('reason','')}*")

        # ── Raw Scraped Sources ──
        scraped = st.session_state.scraped
        if scraped:
            with st.expander("📡 View Raw Scraped Data (Google · Zomato · Articles · Hashtags)", expanded=False):
                sc1, sc2 = st.columns(2)
                with sc1:
                    st.markdown("**🔍 Google Results**")
                    google = scraped.get("google_results", [])
                    if google:
                        for r in google[:10]:
                            st.markdown(f"""
                            <div style="background:#FAF7F2;border-left:3px solid #FF6B00;
                                        border-radius:6px;padding:8px 12px;margin-bottom:6px;">
                                <div style="font-weight:700;font-size:12px">{r.get('title','')}</div>
                                <div style="font-size:11px;color:#78716C">{r.get('snippet','')[:100]}</div>
                            </div>""", unsafe_allow_html=True)
                    else:
                        st.caption("No Google results (may have been blocked)")

                    st.markdown("**📰 Articles Found**")
                    articles = scraped.get("articles", [])
                    if articles:
                        for a in articles[:6]:
                            st.markdown(f"📄 **{a.get('headline','')}** — `{a.get('source','')}`")
                    else:
                        st.caption("No articles found")

                with sc2:
                    st.markdown("**🍽 Zomato Trending**")
                    zomato = scraped.get("zomato_data", [])
                    if zomato:
                        for z in zomato[:12]:
                            icon = "🍴" if z.get("type") == "restaurant" else ("🏷" if z.get("type") == "collection" else "🌶")
                            st.markdown(f"{icon} **{z.get('name','')}** `{z.get('type','')}`")
                    else:
                        st.caption("No Zomato data (may have been blocked)")

                    st.markdown("**📸 Instagram Hashtags**")
                    hashtags = scraped.get("hashtags", [])
                    if hashtags:
                        html = ""
                        for h in hashtags:
                            t = h.get("type", "hot")
                            html += f'<span class="htag htag-{t}">{h["hashtag"]} +{h["estimated_growth_pct"]}%</span> '
                        st.markdown(html, unsafe_allow_html=True)

                total_pts = sum(len(v) for k,v in scraped.items() if isinstance(v,list))
                st.caption(f"🗂 Total data points collected: **{total_pts}** · Scraped at: {scraped.get('scraped_at','—')}")

        # ── Famous Dishes ──
        st.markdown('<div class="section-title">🍜 Famous Dishes Trending Right Now</div>', unsafe_allow_html=True)
        dishes = analysis.get("famous_dishes_trending", [])
        if dishes:
            df2 = pd.DataFrame([{
                "Dish":        d.get("dish_name",""),
                "Famous At":   d.get("famous_at",""),
                "Saves":       d.get("saves_estimate",""),
                "Engagement":  d.get("engagement_pct",0),
                "Why Famous":  d.get("why_famous",""),
            } for d in dishes])
            st.dataframe(df2, use_container_width=True, hide_index=True,
                         column_config={
                             "Engagement": st.column_config.ProgressColumn(
                                 "Engagement", min_value=0, max_value=100, format="%d%%"
                             )
                         })


# ════════════════════════════════
#  TAB 2: WEEKEND SPECIALS
# ════════════════════════════════
with tab2:
    specials = st.session_state.specials

    if not specials:
        st.info("👈 Click **Generate Specials** in the sidebar to get AI-crafted dishes.")
    else:
        # Top ingredients
        top_ings = specials.get("top_weekend_ingredients", [])
        if top_ings:
            st.markdown('<div class="section-title">🏆 Top Revenue Ingredients This Weekend</div>', unsafe_allow_html=True)
            cols = st.columns(len(top_ings))
            for i, (col, ing) in enumerate(zip(cols, top_ings)):
                with col:
                    st.markdown(f"""
                    <div style="background:#FFF4EC;border:1.5px solid #FF6B00;border-radius:12px;
                                padding:14px;text-align:center;font-weight:700;color:#CC5200">
                        ✦ {ing}
                    </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # Dish cards — 2 columns
        dishes = specials.get("weekend_specials", [])
        for i in range(0, len(dishes), 2):
            c1, c2 = st.columns(2)
            for col, dish in zip([c1, c2], dishes[i:i+2]):
                cat = dish.get("category", "")
                if   "margin"    in cat.lower(): cls, badge_cls, badge_lbl = "margin",    "badge-margin",   "💰 High Margin"
                elif "premium"   in cat.lower(): cls, badge_cls, badge_lbl = "premium",   "badge-premium",  "👑 Premium Upsell"
                elif "instagram" in cat.lower(): cls, badge_cls, badge_lbl = "insta",     "badge-insta",    "📸 Reels-Worthy"
                else:                            cls, badge_cls, badge_lbl = "performer", "badge-performer","🔥 Weekend Hit"

                demand = dish.get("predicted_demand","Medium")
                d_cls = "demand-high" if demand=="High" else ("demand-medium" if demand=="Medium" else "demand-low")

                with col:
                    st.markdown(f"""
                    <div class="dish-card {cls}">
                      <div style="display:flex;justify-content:space-between;align-items:flex-start">
                        <div>
                          <div class="dish-badge {badge_cls}">{badge_lbl}</div>
                          <div class="dish-name">{dish.get('dish_name','')}</div>
                          <div style="font-size:11px;color:#FF6B00;margin-top:4px">
                            🔑 {dish.get('key_trending_ingredient','')}
                          </div>
                        </div>
                        <div style="text-align:right">
                          <div class="dish-price">{dish.get('suggested_price_range','')}</div>
                          <span class="{d_cls}">{demand} Demand</span>
                        </div>
                      </div>
                      <div class="dish-desc">{dish.get('description','')}</div>
                      <hr style="border-color:#EAE0D5;margin:10px 0">
                      <table style="width:100%;font-size:12px;border-collapse:collapse">
                        <tr>
                          <td style="color:#78716C;padding:3px 0">🏠 Inspired By</td>
                          <td style="font-weight:600;text-align:right">{dish.get('inspired_by','—')}</td>
                        </tr>
                        <tr>
                          <td style="color:#78716C;padding:3px 0">💸 Food Cost</td>
                          <td style="font-weight:600;text-align:right">{dish.get('food_cost_level','')} · {dish.get('estimated_food_cost_inr','')}</td>
                        </tr>
                        <tr>
                          <td style="color:#78716C;padding:3px 0">📈 Gross Margin</td>
                          <td style="font-weight:600;text-align:right;color:#138808">{dish.get('gross_margin_pct','')}</td>
                        </tr>
                        <tr>
                          <td style="color:#78716C;padding:3px 0">⏱ Prep Time</td>
                          <td style="font-weight:600;text-align:right">{dish.get('prep_time_mins','')} mins</td>
                        </tr>
                        <tr>
                          <td style="color:#78716C;padding:3px 0">🍽 Best Served</td>
                          <td style="font-weight:600;text-align:right">{dish.get('best_served','')}</td>
                        </tr>
                      </table>
                    </div>
                    """, unsafe_allow_html=True)

                    with st.expander("📸 Plating & Reels Tips"):
                        st.write(f"**Plating:** {dish.get('plating_tip','')}")
                        st.write(f"**Reels Tip:** {dish.get('reels_tip','')}")
                        st.write(f"**Why It'll Trend:** {dish.get('why_it_will_trend','')}")

        # Strategic insight
        if specials.get("strategic_insight"):
            st.markdown(f"""
            <div class="insight-box">
              <div class="insight-lbl">💡 Strategic Insight for {specials.get('city','')}</div>
              <div class="insight-txt">{specials.get('strategic_insight','')}</div>
              <div style="margin-top:12px;font-size:12px;color:#9CA3AF">
                📈 Revenue Projection: {specials.get('revenue_projection','')}
              </div>
            </div>
            """, unsafe_allow_html=True)

        # Download CSV
        if dishes:
            df_dishes = pd.DataFrame([{
                "Dish":         d.get("dish_name",""),
                "Category":     d.get("category",""),
                "Price (₹)":    d.get("suggested_price_range",""),
                "Food Cost":    d.get("estimated_food_cost_inr",""),
                "Margin":       d.get("gross_margin_pct",""),
                "Demand":       d.get("predicted_demand",""),
                "Inspired By":  d.get("inspired_by",""),
                "Key Ingredient": d.get("key_trending_ingredient",""),
                "Prep (mins)":  d.get("prep_time_mins",""),
            } for d in dishes])
            csv = df_dishes.to_csv(index=False)
            st.download_button("⬇ Download Dishes CSV", csv,
                               file_name=f"weekend_specials_{city.lower()}.csv",
                               mime="text/csv")


# ════════════════════════════════
#  TAB 3: WEEKLY REPORT
# ════════════════════════════════
with tab3:
    if not st.session_state.report_txt:
        st.info("👈 Generate specials to build the weekly report.")
    else:
        c1, c2 = st.columns([3, 1])
        with c1:
            st.markdown(f"### 📋 Weekly Food Trend Report — {city}")
            st.caption(f"Generated: {datetime.now().strftime('%A, %d %B %Y at %I:%M %p')}")

        with c2:
            if st.session_state.report_txt:
                st.download_button(
                    "⬇ Download Full Report",
                    st.session_state.report_txt,
                    file_name=f"weekly_report_{city.lower()}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

        st.markdown("---")
        st.markdown(st.session_state.report_txt)

        # Summary table
        if st.session_state.specials:
            st.markdown("---")
            st.markdown("#### 📊 Recommended Weekend Menu")
            dishes = st.session_state.specials.get("weekend_specials", [])
            if dishes:
                df3 = pd.DataFrame([{
                    "Dish":           d.get("dish_name",""),
                    "Category":       d.get("category",""),
                    "Inspired By":    d.get("inspired_by",""),
                    "Price (₹)":      d.get("suggested_price_range",""),
                    "Gross Margin":   d.get("gross_margin_pct",""),
                    "Demand":         d.get("predicted_demand",""),
                } for d in dishes])
                st.dataframe(df3, use_container_width=True, hide_index=True)
