"""
ARIA Adaptation Dashboard - Main Application
Phase 2: Contributor + Portfolio Interfaces
"""

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="ARIA Adaptation Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

from contributor_view import render_contributor_interface
from portfolio_view import render_portfolio_interface

# Custom CSS for better styling
st.markdown("""
<style>
    .main > div {
        padding-top: 2rem;
    }
    h1 {
        color: #2c3e50;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
    }
    .stMetric label {
        color: #2c3e50 !important;
    }
    .stMetric [data-testid="stMetricValue"] {
        color: #1f1f1f !important;
    }
    .stMetric [data-testid="stMetricDelta"] {
        color: inherit !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🌱 ARIA")
    st.markdown("### Adaptation Tracker")
    st.markdown("---")

    # Interface selector
    interface_mode = st.radio(
        "Select Interface",
        options=["👥 Contributor View", "📊 Portfolio View (ARIA Managers)"],
        index=0
    )

    st.markdown("---")

    if "Portfolio" in interface_mode:
        st.markdown("""
        ### Portfolio Interface

        Compare all projects across teams:
        - View summary metrics
        - Filter and sort projects
        - Risk matrix analysis
        - Export data

        **For:** ARIA program managers
        """)
    else:
        st.markdown("""
        ### Contributor Interface

        Manage your team's projects:
        - Track adaptation progress
        - Input performance data
        - View projections
        - Get recommendations

        **For:** Research teams
        """)

    st.markdown("---")

    st.markdown("""
    ### Need Help?

    Click the **"📚 Help & FAQ"** button below
    for model explanations and guidance.
    """)

    st.markdown("---")

    # Help/FAQ expander
    with st.expander("📚 Help & FAQ"):
        st.markdown("""
        #### Which Model Should I Use?

        **Additive (Linear) Model**
        - Best for: Early experiments, simple trends
        - Assumes: Constant improvement per generation
        - Use when: You expect steady, linear progress
        - Example: Adding 0.5°C heat tolerance each generation

        **Multiplicative (Exponential) Model**
        - Best for: Exponential growth patterns
        - Assumes: Constant % improvement per generation
        - Use when: Progress compounds (improves faster over time)
        - Example: Population doubling each generation

        **Logistic (Plateau) Model**
        - Best for: Systems approaching genetic limits
        - Assumes: Progress slows as you near maximum
        - Use when: There's a known physiological ceiling
        - Example: Maximum possible yield of a crop variety

        #### Understanding Data Quality

        Projects are scored 0-5 stars based on:
        - ⭐ Sample size (100+ individuals)
        - ⭐ Observation duration (5+ generations)
        - ⭐ Realistic environment (field testing)
        - ⭐ Statistical rigor (SE provided)
        - ⭐ Replication (independent measurements)

        Higher quality = more reliable projections

        #### What Does "On Track" Mean?

        - **🟢 On Track**: Projected to hit target by deadline
        - **🟡 Behind Track**: May miss deadline at current rate
        - **🔴 At Risk**: Not improving or target unreachable

        #### Impact Score Components

        - **Ecological Value**: Biodiversity importance
        - **Economic Value**: Agricultural/commercial value
        - **Urgency**: How soon adaptation is needed
        - **Timeline**: Sooner achievement = higher score
        - **Scalability**: Can it be deployed widely?
        - **Feasibility**: Is the intervention tractable?
        """)

    st.markdown("---")

    # Contact section
    st.markdown("""
    ### Support

    For questions or issues, contact your ARIA program manager.
    """)

    st.markdown("---")
    st.markdown("**Version:** 2.0.0 (Phase 2)")
    st.markdown("**Last Updated:** December 2024")

# Main content - route based on interface selection
if "Portfolio" in interface_mode:
    render_portfolio_interface()
else:
    render_contributor_interface()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; font-size: 0.9em;'>
    ARIA Adaptation Dashboard | Built for tracking evolutionary adaptation progress
</div>
""", unsafe_allow_html=True)
