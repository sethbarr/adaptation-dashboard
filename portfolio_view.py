"""
Portfolio interface for program managers to view and compare all projects.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from storage import load_all_projects, Project
from models import (
    compute_additive_projection,
    compute_multiplicative_projection,
    compute_logistic_projection,
    compute_time_to_target,
    get_target_value
)
from data_quality import compute_data_quality_score, get_quality_label, get_quality_stars
from impact import compute_impact_score, get_impact_interpretation
from plots import plot_multiple_trajectories, plot_risk_matrix
import plotly.graph_objects as go


def render_portfolio_interface():
    """Render the portfolio management interface."""
    st.title("📊 Portfolio Dashboard")

    # Load all projects
    projects = load_all_projects()

    if not projects:
        st.warning("No projects found. Teams need to create projects first.")
        st.info("Switch to Contributor Interface to create projects.")
        return

    # Compute metrics for all projects
    project_data = []
    for project in projects:
        try:
            metrics = compute_project_metrics(project)
            project_data.append(metrics)
        except Exception as e:
            st.warning(f"Error computing metrics for {project.system_name}: {str(e)}")

    if not project_data:
        st.error("Could not compute metrics for any projects.")
        return

    df = pd.DataFrame(project_data)

    # Portfolio summary
    render_portfolio_summary(df)

    st.markdown("---")

    # Filters and table
    render_project_table(df, projects)

    st.markdown("---")

    # Analytics
    render_portfolio_analytics(df, projects)


def compute_project_metrics(project: Project) -> dict:
    """Compute all metrics for a project."""
    # Get projection
    if project.model_type == 'additive':
        projection = compute_additive_projection(
            project.W0, project.W_current, project.t_gen_elapsed,
            project.gen_time_years, project.projection_generations,
            project.dW_se, project.confidence_level
        )
    elif project.model_type == 'multiplicative':
        projection = compute_multiplicative_projection(
            project.W0, project.W_current, project.t_gen_elapsed,
            project.gen_time_years, project.projection_generations,
            project.dW_se, project.confidence_level
        )
    else:  # logistic
        projection = compute_logistic_projection(
            project.W0, project.W_current, project.plateau_performance,
            project.t_gen_elapsed, project.gen_time_years,
            project.projection_generations, project.dW_se, project.confidence_level
        )

    # Target
    W_target = get_target_value(project.W0, project.target_type, project.target_value)

    # Time to target
    time_result = compute_time_to_target(
        project.W_current, W_target, projection['rate_per_gen'],
        project.gen_time_years, project.model_type,
        projection.get('rate_lower'), projection.get('rate_upper'),
        project.plateau_performance
    )

    # Data quality
    quality_score, _ = compute_data_quality_score(
        project.sample_size, project.t_gen_elapsed,
        project.environment, project.dW_se
    )

    # Impact score
    impact_result = compute_impact_score(
        project.ecological_value, project.economic_value,
        project.urgency, project.technical_feasibility,
        project.scalability, time_result['years_to_target'],
        project.target_date
    )

    # Status
    current_year = datetime.now().year
    if projection['rate_per_gen'] <= 0:
        status = "At Risk"
    elif not time_result['reachable']:
        status = "At Risk"
    elif 'years_upper' in time_result and np.isfinite(time_result['years_upper']):
        if current_year + time_result['years_upper'] > project.target_date:
            status = "Behind Track"
        else:
            status = "On Track"
    elif np.isfinite(time_result['years_to_target']):
        if current_year + time_result['years_to_target'] > project.target_date:
            status = "Behind Track"
        else:
            status = "On Track"
    else:
        status = "At Risk"

    # Progress percentage
    if W_target > project.W0:
        progress_pct = ((project.W_current - project.W0) / (W_target - project.W0)) * 100
    else:
        progress_pct = 0

    return {
        'project_id': project.project_id,
        'team_name': project.team_name,
        'system_name': project.system_name,
        'phenotype': project.phenotype,
        'status': status,
        'quality_score': quality_score,
        'quality_stars': get_quality_stars(quality_score),
        'quality_label': get_quality_label(quality_score),
        'impact_score': impact_result['total_score'],
        'impact_label': get_impact_interpretation(impact_result['total_score']),
        'years_to_target': time_result['years_to_target'] if np.isfinite(time_result['years_to_target']) else np.inf,
        'target_date': project.target_date,
        'current_year': current_year,
        'W0': project.W0,
        'W_current': project.W_current,
        'W_target': W_target,
        'W0_units': project.W0_units,
        'progress_pct': progress_pct,
        'rate_per_gen': projection['rate_per_gen'],
        'rate_per_year': projection['rate_per_year'],
        'program_year': project.program_year,
        'environment': project.environment,
        'model_type': project.model_type
    }


def render_portfolio_summary(df: pd.DataFrame):
    """Render summary metrics for the portfolio."""
    st.markdown("## Portfolio Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Active Projects", len(df))

    with col2:
        on_track = len(df[df['status'] == 'On Track'])
        st.metric("On Track", on_track, delta=f"{on_track/len(df)*100:.0f}%")

    with col3:
        behind = len(df[df['status'] == 'Behind Track'])
        st.metric("Behind Track", behind, delta=f"{behind/len(df)*100:.0f}%" if behind > 0 else None)

    with col4:
        at_risk = len(df[df['status'] == 'At Risk'])
        st.metric("At Risk", at_risk, delta=f"{at_risk/len(df)*100:.0f}%" if at_risk > 0 else None)


def render_project_table(df: pd.DataFrame, projects: list):
    """Render sortable/filterable project table."""
    st.markdown("## Project Comparison Table")

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        status_filter = st.multiselect(
            "Filter by Status",
            options=['On Track', 'Behind Track', 'At Risk'],
            default=[]
        )

    with col2:
        quality_filter = st.multiselect(
            "Filter by Quality",
            options=['High', 'Moderate', 'Preliminary'],
            default=[]
        )

    with col3:
        team_filter = st.multiselect(
            "Filter by Team",
            options=sorted(df['team_name'].unique()),
            default=[]
        )

    # Apply filters
    filtered_df = df.copy()
    if status_filter:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]
    if quality_filter:
        filtered_df = filtered_df[filtered_df['quality_label'].isin(quality_filter)]
    if team_filter:
        filtered_df = filtered_df[filtered_df['team_name'].isin(team_filter)]

    # Display controls
    col1, col2 = st.columns([3, 1])
    with col1:
        sort_by = st.selectbox(
            "Sort by",
            options=['Impact Score', 'Years to Target', 'Progress %', 'Quality Score', 'Team Name'],
            index=0
        )
    with col2:
        if st.button("📥 Export to CSV"):
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                "Download CSV",
                csv,
                "aria_portfolio.csv",
                "text/csv",
                key='download-csv'
            )

    # Sort mapping
    sort_map = {
        'Impact Score': 'impact_score',
        'Years to Target': 'years_to_target',
        'Progress %': 'progress_pct',
        'Quality Score': 'quality_score',
        'Team Name': 'team_name'
    }

    sorted_df = filtered_df.sort_values(
        by=sort_map[sort_by],
        ascending=(sort_by not in ['Impact Score', 'Progress %', 'Quality Score'])
    )

    # Create display table
    display_df = sorted_df[[
        'team_name', 'system_name', 'phenotype', 'status',
        'quality_stars', 'impact_score', 'years_to_target'
    ]].copy()

    # Format columns
    display_df['years_to_target'] = display_df['years_to_target'].apply(
        lambda x: f"{x:.1f}" if np.isfinite(x) else "∞"
    )
    display_df['impact_score'] = display_df['impact_score'].apply(lambda x: f"{x:.1f}")

    # Rename for display
    display_df.columns = ['Team', 'System', 'Phenotype', 'Status', 'Quality', 'Impact', 'Years to Target']

    # Color code status
    def color_status(val):
        if val == 'On Track':
            return 'background-color: #d4edda'
        elif val == 'Behind Track':
            return 'background-color: #fff3cd'
        else:
            return 'background-color: #f8d7da'

    styled_df = display_df.style.applymap(color_status, subset=['Status'])

    st.dataframe(styled_df, use_container_width=True, hide_index=True)

    st.caption(f"Showing {len(sorted_df)} of {len(df)} projects")


def render_portfolio_analytics(df: pd.DataFrame, projects: list):
    """Render portfolio analytics visualizations."""
    st.markdown("## Portfolio Analytics")

    tab1, tab2, tab3 = st.tabs(["📈 Normalized Progress", "🎯 Risk Matrix", "📊 Distribution"])

    with tab1:
        render_normalized_progress(df, projects)

    with tab2:
        render_risk_matrix_view(df)

    with tab3:
        render_distributions(df)


def render_normalized_progress(df: pd.DataFrame, projects: list):
    """Plot all projects on normalized 0-100% scale."""
    st.markdown("### Normalized Progress to Target")
    st.caption("All projects shown as % progress from baseline to target")

    current_year = datetime.now().year

    # Prepare data for plotting
    plot_data = []
    for _, row in df.iterrows():
        project = next(p for p in projects if p.project_id == row['project_id'])

        # Get projection
        try:
            if project.model_type == 'additive':
                projection = compute_additive_projection(
                    project.W0, project.W_current, project.t_gen_elapsed,
                    project.gen_time_years, project.projection_generations,
                    0, 0.95  # No uncertainty for cleaner plot
                )
            elif project.model_type == 'multiplicative':
                projection = compute_multiplicative_projection(
                    project.W0, project.W_current, project.t_gen_elapsed,
                    project.gen_time_years, project.projection_generations,
                    0, 0.95
                )
            else:
                projection = compute_logistic_projection(
                    project.W0, project.W_current, project.plateau_performance,
                    project.t_gen_elapsed, project.gen_time_years,
                    project.projection_generations, 0, 0.95
                )

            # Normalize to percentage
            W_target = row['W_target']
            W0 = row['W0']
            if W_target > W0:
                W_norm = ((projection['W_projection'] - W0) / (W_target - W0)) * 100
            else:
                W_norm = projection['W_projection'] * 0

            years_actual = current_year + projection['years']

            # Color by status
            color_map = {'On Track': 'green', 'Behind Track': 'orange', 'At Risk': 'red'}
            color = color_map.get(row['status'], 'gray')

            plot_data.append({
                'name': f"{row['system_name']} ({row['team_name']})",
                'years': years_actual,
                'W': W_norm,
                'color': color,
                'W_target': 100,
                'W0': 0
            })
        except:
            continue

    if plot_data:
        fig = plot_multiple_trajectories(plot_data, normalize=True)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Could not generate comparison plot")


def render_risk_matrix_view(df: pd.DataFrame):
    """Render risk matrix: impact vs timeline."""
    st.markdown("### Risk Matrix: Impact vs Timeline")
    st.caption("Quadrant analysis for prioritization")

    # Prepare summary for risk matrix
    summary = []
    for _, row in df.iterrows():
        summary.append({
            'name': f"{row['system_name'][:20]}",
            'impact_score': row['impact_score'],
            'years_to_target': row['years_to_target'] if np.isfinite(row['years_to_target']) else 50,
            'status': row['status']
        })

    fig = plot_risk_matrix(summary)
    st.plotly_chart(fig, use_container_width=True)


def render_distributions(df: pd.DataFrame):
    """Render distribution plots for key metrics."""
    st.markdown("### Metric Distributions")

    col1, col2 = st.columns(2)

    with col1:
        # Impact score distribution
        fig = go.Figure(data=[go.Histogram(
            x=df['impact_score'],
            nbinsx=20,
            marker_color='#3498db'
        )])
        fig.update_layout(
            title="Impact Score Distribution",
            xaxis_title="Impact Score",
            yaxis_title="Number of Projects",
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Quality score distribution
        fig = go.Figure(data=[go.Histogram(
            x=df['quality_score'],
            nbinsx=6,
            marker_color='#2ecc71'
        )])
        fig.update_layout(
            title="Data Quality Distribution",
            xaxis_title="Quality Score (0-5)",
            yaxis_title="Number of Projects",
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Rate distribution
    finite_rates = df[np.isfinite(df['rate_per_year'])]['rate_per_year']
    if len(finite_rates) > 0:
        fig = go.Figure(data=[go.Histogram(
            x=finite_rates,
            nbinsx=20,
            marker_color='#e74c3c'
        )])
        fig.update_layout(
            title="Adaptation Rate Distribution (per year)",
            xaxis_title="Rate of Improvement",
            yaxis_title="Number of Projects",
            template='plotly_white'
        )
        st.plotly_chart(fig, use_container_width=True)
