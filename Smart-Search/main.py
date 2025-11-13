import streamlit as st
import pandas as pd
import altair as alt

from utils import load_ner_model, parse_query_with_ner, search_products, load_data

st.set_page_config(
    page_title="Smart Search | Industrial Insight Console",
    page_icon="🔧",
    layout="wide"
)

CUSTOM_CSS = """
<style>
:root {
    --accent-primary: #0F4C75;
    --accent-secondary: #3282B8;
    --accent-soft: rgba(50, 130, 184, 0.12);
    --surface: #FFFFFF;
    --surface-muted: #F1F5F9;
    --text-strong: #12263A;
    --text-muted: #61748F;
}
body {
    color: var(--text-strong);
    background: var(--surface-muted);
}
div[data-testid="stAppViewContainer"] {
    background: var(--surface-muted);
}
.stAppHeader {
    background: #071529 !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}
div[data-testid="stAppViewContainer"] .block-container {
    color: var(--text-strong);
}
div[data-testid="stAppViewContainer"] .block-container :is(h1,h2,h3,h4,h5,h6,p,span,label,li,strong) {
    color: var(--text-strong);
}
.hero-card :is(h1,h2,h3,h4,p,span,strong) {
    color: #FFFFFF !important;
}
.hero-card {
    background: linear-gradient(135deg, rgba(15, 76, 117, 0.95), rgba(50, 130, 184, 0.85));
    color: white;
    padding: 2.4rem;
    border-radius: 1.8rem;
    margin-bottom: 1.8rem;
    box-shadow: 0 24px 48px rgba(15, 76, 117, 0.25);
}
.hero-card h1 {
    font-size: 2.35rem;
    margin-bottom: 0.6rem;
}
.hero-card p {
    font-size: 1.1rem;
    max-width: 620px;
    margin-bottom: 1.4rem;
}
.hero-metric-band {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
}
.hero-metric {
    background: rgba(255, 255, 255, 0.12);
    padding: 1rem 1.3rem;
    border-radius: 1rem;
    min-width: 140px;
}
.hero-metric strong {
    display: block;
    font-size: 1.35rem;
}
.pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: var(--accent-soft);
    color: var(--accent-primary);
    padding: 0.28rem 0.8rem;
    border-radius: 999px;
    font-size: 0.78rem;
    margin-right: 0.4rem;
    margin-bottom: 0.4rem;
}
.pill strong {
    color: var(--accent-primary);
}
.result-card {
    background: var(--surface);
    padding: 1.15rem 1.35rem;
    border-radius: 1.4rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 14px 32px rgba(18, 38, 58, 0.08);
    border: 1px solid rgba(15, 76, 117, 0.08);
}
.result-card h4 {
    margin-bottom: 0.4rem;
    color: var(--text-strong);
}
.result-card p {
    color: var(--text-muted);
    margin-bottom: 0.4rem;
}
.result-card p strong {
    color: var(--accent-primary);
}
.dashboard-card {
    background: var(--surface);
    border-radius: 1.4rem;
    padding: 1.4rem 1.6rem;
    border: 1px solid rgba(15, 76, 117, 0.08);
    box-shadow: 0 18px 40px rgba(18, 38, 58, 0.08);
}
.stTextInput div[data-baseweb="input"] {
    background: linear-gradient(135deg, #1F2933, #252F3F);
    border-radius: 1.1rem;
    border: 1px solid rgba(15, 76, 117, 0.35);
    box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.04);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.stTextInput div[data-baseweb="input"]:focus-within {
    border-color: rgba(50, 130, 184, 0.8);
    box-shadow: 0 0 0 4px rgba(50, 130, 184, 0.22);
}
.stTextInput input {
    color: #F8FBFF !important;
    font-weight: 600;
}
.stTextInput input::placeholder {
    color: rgba(240, 244, 248, 0.58) !important;
}
.stTextInput input:focus::placeholder {
    color: rgba(240, 244, 248, 0.38) !important;
}
.stDownloadButton button,
button[kind="primary"],
div[data-testid="stSidebar"] button {
    background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary)) !important;
    color: #FFFFFF !important;
    border-radius: 0.9rem !important;
    border: none !important;
    box-shadow: 0 12px 24px rgba(15, 76, 117, 0.25);
}
.stDownloadButton button:hover,
button[kind="primary"]:hover,
div[data-testid="stSidebar"] button:hover {
    box-shadow: 0 16px 28px rgba(15, 76, 117, 0.28);
}
.stToggle {
    background: rgba(15, 76, 117, 0.06);
    border-radius: 1.2rem;
    padding: 0.2rem 0.6rem;
}
.stToggle > div {
    color: var(--text-strong);
}
.stTabs [data-baseweb="tab-list"] {
    gap: 0.8rem;
    background: rgba(255, 255, 255, 0.7);
    border-radius: 1.2rem;
    padding: 0.4rem;
}
.stTabs [data-baseweb="tab"] {
    color: var(--text-muted);
    border-radius: 0.9rem;
    padding: 0.6rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(15, 76, 117, 0.95), rgba(50, 130, 184, 0.85));
    color: #FFFFFF !important;
    box-shadow: 0 12px 24px rgba(15, 76, 117, 0.24);
}
.stMetric label,
.stMetric p {
    color: var(--text-muted);
}
.stMetric span[data-testid="stMetricValue"] {
    color: var(--accent-primary);
}
div[data-testid="stSidebar"] p,
div[data-testid="stSidebar"] label,
div[data-testid="stSidebar"] span,
div[data-testid="stSidebar"] h1,
div[data-testid="stSidebar"] h2,
div[data-testid="stSidebar"] h3,
div[data-testid="stSidebar"] h4 {
    color: #F0F4F8 !important;
}
div[data-testid="stSidebar"] section[aria-label="sidebar"] {
    padding-top: 1rem;
}
div[data-testid="stSidebar"] {
    background: #102A43;
}
.stMarkdown a {
    color: var(--accent-primary) !important;
    text-decoration: none;
}
.stMarkdown a:hover {
    text-decoration: underline;
}
.metric-band-label {
    color: var(--text-muted);
}
.stAlert {
    border-radius: 1rem;
}
.stDataFrame div[role="grid"] {
    border-radius: 1rem;
    border: 1px solid rgba(15, 76, 117, 0.12);
}
.stDataFrame table {
    color: var(--text-strong);
}
.stDataFrame td {
    color: var(--text-muted);
}
.footer {
    margin-top: 2.5rem;
    padding: 1.2rem 0;
    text-align: center;
    color: var(--text-muted);
    font-size: 0.9rem;
}
.footer strong {
    color: var(--accent-primary);
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_resource
def initialize_app():
    """Load heavyweight assets once per session."""
    return load_ner_model()


model = initialize_app()
df = load_data()

if df.empty:
    st.stop()

price_series = df["price"].dropna()
catalog_size = len(df)
median_price = int(price_series.median()) if not price_series.empty else 0
avg_price = int(price_series.mean()) if not price_series.empty else 0
unique_brands = df["brand"].dropna().nunique()
unique_locations = df["location"].dropna().nunique() if "location" in df.columns else 0
battery_signal = (
    df["description"]
    .fillna("")
    .str.contains(r"\d+%", case=False)
    .mean()
    if "description" in df.columns
    else 0
)
battery_coverage = round(battery_signal * 100, 1)

if "search_query" not in st.session_state:
    st.session_state.search_query = "Industrial iPhone 13 Pro 256GB under 60000 with 80% battery"

hero_html = f"""
<div class="hero-card">
    <span class="pill">Industrial Engineering Procurement · Mobile Sourcing</span>
    <span class="pill">AI-powered Inventory Control</span>
    <h1>Industrial Engineering Procurement Scout App</h1>
    <p>
        Mobilise marketplace intelligence captured from curated OLX snapshots. Blend named-entity recognition with demand cues to
        locate high-fit devices, track supply readiness, and trigger reorder decisions aligned with industrial engineering needs—all from the packaged dataset.
    </p>
    <div class="hero-metric-band">
        <div class="hero-metric">
            <strong>{catalog_size:,}</strong>
            Listings monitored
        </div>
        <div class="hero-metric">
            <strong>{median_price:,.0f} EGP</strong>
            Median ask price
        </div>
        <div class="hero-metric">
            <strong>{unique_brands}</strong>
            Brands represented
        </div>
        <div class="hero-metric">
            <strong>{battery_coverage:.0f}%</strong>
            Battery telemetry coverage
        </div>
        <div class="hero-metric">
            <strong>{unique_locations}</strong>
            Locations indexed
        </div>
    </div>
</div>
"""

st.markdown(hero_html, unsafe_allow_html=True)
st.caption(
    "Industrial Engineering Procurement Scout for Mobile Sourcing Optimisation—turn the shipped OLX dataset into industrial-grade procurement signals."
)

problem_col, solution_col = st.columns([1.35, 1])
with problem_col:
    st.markdown("#### Problem Statement")
    st.markdown(
        "Industrial engineering teams often rely on manual marketplace scans to provision mobile devices for field crews, "
        "stretching planning cycles and risking misaligned stock levels."
    )
with solution_col:
    st.markdown("#### Solution")
    st.markdown(
        "This console layers NER-backed search on top of OLX market data to filter listings, surface supply signals, and estimate "
        "reorder batches—supporting faster alignment between procurement and shop-floor requirements."
    )

st.markdown("#### Methodology & Program Steps")
methodology_steps = [
    (
        "Data Prep",
        "Scrape OLX via `olx_scrapper.py` (requests/BS4) for 9K listings CSV; clean in `utils.py` (regex for price/battery, normalize Arabic), then ship as `data/olx_products_cleaned.csv`.",
    ),
    (
        "Core Logic",
        "Load GLiNER NER model for entity extraction (brand/model/price); filter DataFrame multi-criteria (e.g., price < threshold, battery >80%).",
    ),
    (
        "GUI Build",
        "Streamlit `main.py`—tabs for search (query bar + results table), ops dashboard (Altair charts for trends), playbook (sourcing tips), benefits (cost est. slider).",
    ),
    (
        "Industrial Engineering Integration",
        "Simple reorder calc in expanders (batch size slider x avg price = total cost); uses existing filters to flag high-supply pockets.",
    ),
    (
        "Tech Stack",
        "<ul style='padding-left:1.1rem;margin:0;'>"
        "<li>Python · Streamlit UI layer</li>"
        "<li>pandas data wrangling</li>"
        "<li>Altair analytics &amp; visuals</li>"
        "<li>PyTorch runtime for GLiNER</li>"
        "<li>BeautifulSoup requests-based scraper</li>"
        "</ul>",
    ),
]
methodology_cols = st.columns(2)
for idx, (title, body) in enumerate(methodology_steps):
    with methodology_cols[idx % 2]:
        st.markdown(
            f"""
            <div class="dashboard-card" style="margin-bottom:1.2rem;">
                <h4 style="margin-bottom:0.4rem;">{title}</h4>
                <p style="color: var(--text-muted); margin:0;">{body}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("#### Ops Workflow Highlights")
st.markdown(
    """
- Query bilingual briefs and watch GLiNER surface brand, model, price, and battery cues for filtering.
- Inspect ranked listings with imagery, location, and seller context drawn from the loaded OLX snapshot to vet sourcing options quickly.
- Use the reorder estimator to translate filtered matches into batch cost signals for inventory planning.
    """
)
outcome_cols = st.columns(2)
outcome_cols[0].metric("Catalog breadth", f"{catalog_size:,} listings")
outcome_cols[1].metric("Brands represented", f"{unique_brands}")
st.caption(f"Current dataset spans {unique_locations} sourcing locations with {battery_coverage:.0f}% battery telemetry coverage.")

impact_cols = st.columns(2)
with impact_cols[0]:
    st.markdown("#### Industrial Engineering Value")
    st.markdown(
        """
- Spots top suppliers (Pareto: 3 brands = 80% options)
- Flags reliable picks (battery >80%)
- Enables quick exports for procurement lists—cuts manual effort, improves stock turnover
        """
    )
with impact_cols[1]:
    st.markdown("#### Ease of Use")
    st.markdown(
        """
- Bilingual search
- One-click filters and export
- Demo workflow: Enter query -> View table/chart -> Use cost slider -> Export (under 1 min)
        """
    )

tabs = st.tabs(
    [
        "Scout Search",
        "Ops Dashboard",
        "Implementation Playbook",
        "Benefits & Impact",
    ]
)

with tabs[0]:
    st.subheader("Scout Search · Procurement Console")
    st.markdown(
        """
        Phrase industrial sourcing briefs in Arabic or English and convert them into structured filters instantly. The NER pipeline
        aligns brands, models, and guardrails with OLX marketplace intelligence so planners can shrink procurement cycle time.
        """
    )

    query_col, helper_col = st.columns([2.2, 1])
    with query_col:
        query = st.text_input(
            "Natural-language query",
            value=st.session_state.search_query,
            placeholder="Example: Rugged iPhone 13 Pro 256GB below 60000 EGP with 80% battery",
            help="Use industrial scenarios, constraints, or performance KPIs in Arabic or English.",
        )
    with helper_col:
        st.markdown(
            """
            **Search accelerators**

            - Reference team, task, or environment (shift maintenance, offshore, retrofit)
            - Stack constraints (budget, battery health, memory, cosmetics)
            - Mix Arabic and English freely for bilingual sourcing briefs
            """
)

    if query:
        with st.spinner("Interpreting requirements and probing catalog..."):
            parsed = parse_query_with_ner(query, model)
            results, applied_filters = search_products(df, parsed)

        st.session_state.search_query = query

        analytic_col, result_col = st.columns([1, 2])

        with analytic_col:
            st.markdown("#### Requirement decomposition")
            if parsed["entities_found"]:
                for entity in parsed["entities_found"]:
                    st.markdown(
                        f"<span class='pill'>{entity['label'].title()} · {entity['text']}</span>",
                        unsafe_allow_html=True,
                    )
            else:
                st.info("No explicit entities detected—fallback to semantic keyword matching.")

            st.markdown("#### Operational filters")
            if applied_filters:
                for pill in applied_filters:
                    st.markdown(f"- {pill}")
            else:
                st.write("No filters applied; results ranked via semantic relevance.")

            st.metric("Matching listings", f"{len(results):,}")

            if parsed.get("price_max"):
                st.metric(
                    "Budget guardrail",
                    f"{parsed['price_max']:,.0f} EGP",
                    help="Max price inferred from your query.",
                )

        with result_col:
            st.markdown("#### Candidate lineup")

            if results.empty:
                st.warning("No listings fit the requirement. Adjust your constraints or try a scenario from the sidebar.")
            else:
                with st.expander("Reorder batch estimator", expanded=False):
                    batch_size = st.slider("Batch size", min_value=5, max_value=200, value=20, step=5)
                    average_price = int(results["price"].mean()) if "price" in results.columns and not results["price"].isna().all() else avg_price
                    estimated_total = batch_size * average_price
                    st.metric("Estimated total cost", f"{estimated_total:,.0f} EGP")
                    st.caption("Leverages current filtered listings; adjust batch size to align with maintenance cycles.")
                    if len(results) >= 100:
                        st.success("High-supply window detected—sufficient listings to support bulk procurement.")

                st.download_button(
                    "📥 Download filtered dataset (CSV)",
                    data=results.to_csv(index=False).encode("utf-8"),
                    file_name="smart_search_results.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

                toggle_table = st.toggle("Switch to tabular view", value=False, help="View all columns in a grid.")

                if toggle_table:
                    st.dataframe(results.reset_index(drop=True), use_container_width=True, height=420)
                else:
                    for _, row in results.head(10).iterrows():
                        with st.container():
                            card_col1, card_col2 = st.columns([1, 3])
                            with card_col1:
                                if pd.notna(row.get("main_image")) and row.get("main_image"):
                                    try:
                                        st.image(row["main_image"], width=140)
                                    except Exception:
                                        st.write("🖼️ Preview not available")
                                else:
                                    st.write("🖼️ Preview not available")
                            with card_col2:
                                info_parts = []
                                if pd.notna(row.get("location")) and row.get("location"):
                                    info_parts.append(f"📍 {row['location']}")
                                if pd.notna(row.get("brand")) and row.get("brand"):
                                    info_parts.append(f"🏷️ {row['brand']}")
                                if pd.notna(row.get("seller_name")) and row.get("seller_name"):
                                    info_parts.append(f"👤 {row['seller_name']}")

                                snippet = ""
                                if pd.notna(row.get("description")) and row.get("description"):
                                    snippet_raw = str(row["description"])
                                    snippet = snippet_raw if len(snippet_raw) < 220 else snippet_raw[:220] + "..."

                                product_link = ""
                                if pd.notna(row.get("product_url")) and row.get("product_url"):
                                    product_link = f"<a href='{row['product_url']}' target='_blank'>🔗 Inspect listing</a>"

                                info_line = " | ".join(info_parts)
                                snippet_line = f"<p>📝 {snippet}</p>" if snippet else ""

                                card_html = f"""
                                <div class='result-card'>
                                    <h4>{row['title']}</h4>
                                    <p><strong>💰 {row['price']:,.0f} EGP</strong></p>
                                    {f"<p>{info_line}</p>" if info_line else ""}
                                    {snippet_line}
                                    {product_link}
                                </div>
                                """
                                st.markdown(card_html, unsafe_allow_html=True)

with tabs[1]:
    st.subheader("Ops Dashboard")
    st.markdown(
        """
        Convert the loaded OLX dataset into industrial engineering cues. Use these diagnostics to size inventory buffers, target supplier outreach,
        and balance budget posture for the procurement scout workflow. Metrics below are computed on the packaged snapshot.
        """
    )

    kpi_cols = st.columns(4)
    kpi_cols[0].metric("95th percentile price", f"{price_series.quantile(0.95):,.0f} EGP" if not price_series.empty else "—")
    kpi_cols[1].metric(
        "Mean vs median spread",
        f"{avg_price - median_price:,.0f} EGP",
        help="Positive spread highlights premium-heavy catalog regions.",
    )
    kpi_cols[2].metric("Top 5 brands share", f"{df['brand'].value_counts(normalize=True).head(5).sum()*100:,.1f}%")
    kpi_cols[3].metric("Distinct storage options", df["storage"].dropna().nunique() if "storage" in df.columns else "—")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("##### Brand penetration")
        top_brands = (
            df["brand"].fillna("Unclassified").value_counts().head(10).reset_index()
        )
        top_brands.columns = ["brand", "count"]
        brand_chart = (
            alt.Chart(top_brands)
            .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
            .encode(
                x=alt.X("count:Q", title="Listings"),
                y=alt.Y("brand:N", sort="-x", title=""),
                color=alt.Color(
                    "brand:N", legend=None, scale=alt.Scale(scheme="blues")
                ),
                tooltip=["brand", "count"],
            )
            .properties(height=320)
        )
        st.altair_chart(brand_chart, use_container_width=True)

    with chart_col2:
        st.markdown("##### Price posture by brand")
        price_insights = (
            df.dropna(subset=["brand", "price"])
            .groupby("brand")["price"]
            .median()
            .sort_values(ascending=False)
            .head(8)
            .reset_index()
        )
        price_insights.columns = ["brand", "median_price"]
        price_chart = (
            alt.Chart(price_insights)
            .mark_circle(size=200)
            .encode(
                x=alt.X("median_price:Q", title="Median ask (EGP)"),
                y=alt.Y("brand:N", sort="-x", title=""),
                color=alt.Color("brand:N", legend=None, scale=alt.Scale(scheme="tealblues")),
                tooltip=["brand", alt.Tooltip("median_price:Q", format=",")],
            )
            .properties(height=320)
        )
        st.altair_chart(price_chart, use_container_width=True)

    st.markdown("##### Tactical drill-down")
    focus_options = sorted(df["brand"].dropna().unique().tolist())[:40]
    focus_brand = st.selectbox("Focus brand for quick audit", options=focus_options if focus_options else ["No data"])

    if focus_options:
        detail_columns = [col for col in ["title", "price", "storage", "ram", "location"] if col in df.columns]
        if not detail_columns:
            st.info("Detailed attributes unavailable for this dataset.")
        else:
            focus_frame = df[df["brand"] == focus_brand][detail_columns].head(15)
            st.dataframe(focus_frame.reset_index(drop=True), use_container_width=True)
    else:
        st.info("Brand data not available in the current dataset.")

    with st.expander("Inventory posture recommendations"):
        st.markdown(
            """
            - **Lean procurement loops**: Harness brands with high listing density and low price variance to stabilize replenishment.
            - **Battery-sensitive assignments**: Prioritize models with rich battery telemetry coverage when planning shift handovers.
            - **Capability uplift**: Target median-plus pricing pockets for engineering teams that require higher compute and graphics throughput.
            """
        )

with tabs[2]:
    st.subheader("Implementation Playbook")
    st.markdown(
        """
        The playbook walks industrial engineering teams through the core building blocks shipped in this app—every strand is implemented
        with the current codebase and can be tuned with new marketplace drops.
        """
    )
    st.markdown(
        """
        **Why it matters to Industrial Engineering teams**

        - **Accelerates procurement intelligence** by turning natural-language intents into machine-readable sourcing actions, closing the loop between maintenance crews and planning desks.
        - **Supports lean inventory strategy** through continuous feedback on stock breadth, cost posture, and telemetry coverage, reducing overstock and emergency purchases.
        - **Strengthens cross-functional decisions** by aligning analytics, scenario presets, and ML-driven recommendations with workforce enablement and retrofit initiatives.
        """
    )

    playbook_tracks = [
        (
            "OLX data ingestion & cleanup",
            "Use `olx_scrapper.py` to harvest listings, then normalise price, storage, and battery traits through regex-driven utilities to keep analytics tidy.",
        ),
        (
            "NER-powered intent parsing",
            "Leverage the GLiNER model (`load_ner_model`) to recognise brand, model, and budget cues from bilingual natural-language briefs.",
        ),
        (
            "Filter construction & ranking",
            "`search_products` converts parsed entities into DataFrame filters (price caps, battery thresholds, storage checks) and returns ranked listings.",
        ),
        (
            "Ops dashboard analytics",
            "Altair charts surface brand penetration, price posture, and detail grids so planners can validate supply readiness quickly.",
        ),
        (
            "Reorder batch estimator",
            "The front-end slider multiplies inferred average price by batch size to give rapid cost projections tied to filtered search results.",
        ),
        (
            "Export & collaboration",
            "One-click CSV export shares filtered procurement shortlists with sourcing teams for negotiation and vendor engagement.",
        ),
    ]

    for track, narrative in playbook_tracks:
        with st.expander(track):
            st.write(narrative)

with tabs[3]:
    st.subheader("Benefits & Impact")
    st.markdown(
        """
        **Industrial Engineering Procurement Scout amplifies Industrial Engineering outcomes by unifying procurement, analytics, and AI guidance in a single console.**
        """
    )

    benefit_cards = [
        {
            "title": "Procurement intelligence, accelerated",
            "description": "Translate free-text maintenance or retrofit requests into structured filters using GLiNER-based named-entity recognition—no more manual spreadsheet triage."
        },
        {
            "title": "AI-powered intent parsing",
            "description": "GLiNER extracts brands, models, budgets, and battery targets from bilingual briefs so filters auto-align with industrial sourcing constraints."
        },
        {
            "title": "Real-time supply readiness",
            "description": "Monitor catalog breadth, price posture, and battery telemetry coverage inside the console to size buffers and plan replacements using live marketplace evidence."
        },
        {
            "title": "Negotiation leverage",
            "description": "Harness brand penetration and price posture analytics to benchmark supplier quotes against marketplace behaviour during procurement reviews."
        },
        {
            "title": "Tactical decision support",
            "description": "Scenario presets, bilingual search, and reorder estimators align device allocations with shift profiles, environments, and KPI requirements."
        },
        {
            "title": "Continuous improvement loop",
            "description": "Extend the solution with fine-tuned entity extraction, richer seller telemetry, and MRP-aligned budgeting to keep procurement and inventory aligned."
        },
    ]

    benefit_columns = st.columns(2)
    for idx, benefit in enumerate(benefit_cards):
        with benefit_columns[idx % 2]:
            st.markdown(
                f"""
                <div class="dashboard-card" style="margin-bottom:1.2rem;">
                    <h4 style="margin-bottom:0.4rem;">{benefit['title']}</h4>
                    <p style="color:var(--text-muted);">{benefit['description']}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("##### Performance checkpoints")
    st.markdown(
        """
        - Track query-to-insight cycle time as planners adopt natural-language sourcing.
        - Measure sourced-device battery health compliance using the telemetry coverage metric.
        - Compare supplier quotes against the console's live market medians during negotiation prep.
        """
    )

with st.sidebar:
    st.markdown("### Quick Experiments")
    quick_examples = [
        "Industrial iPhone 13 Pro 256GB under 60000 with 80% battery",
        "Samsung A54 8GB RAM below 15000 EGP",
        "Apple Watch Series with 90% battery health under 20000",
        "iPhone 11 128GB white under 20000 good condition",
        "ايفون 14 برو بطارية فوق 80 اقل من 70000",
        "شاومي ريدمي نوت 12 للمهندسين اقل من 10000",
        "OPPO Reno 8 128GB high battery health",
        "Samsung S23 8GB RAM for night shifts",
    ]
    for example in quick_examples:
        if st.button(example, key=f"example_{example}", use_container_width=True):
            st.session_state.search_query = example
            st.rerun()

    st.markdown("---")
    st.markdown("### Budget lens")
    max_price = int(price_series.max()) if not price_series.empty else 100000
    budget_threshold = st.slider(
        "Budget threshold (EGP)",
        min_value=5000,
        max_value=max_price,
        value=min(35000, max_price),
        step=1000,
    )
    budget_items = (df["price"] <= budget_threshold).sum()
    st.metric("Listings within threshold", f"{budget_items:,}")

    st.markdown("---")
    st.markdown("### Tech Stack")
    st.markdown("[NAMAA-Space/gliner_arabic-v2.1](https://huggingface.co/NAMAA-Space/gliner_arabic-v2.1)")
    st.markdown(
        """
- Python · Streamlit UI layer
- pandas data wrangling
- Altair analytics & visuals
- PyTorch runtime for GLiNER
- BeautifulSoup requests-based scraper
        """
    )

st.markdown(
    """
    <div class="footer">
        Developed by <strong>Aaditya Suryawanshi</strong>
    </div>
    """,
    unsafe_allow_html=True,
)
