"""
Contributor interface for individual teams to manage their projects.
"""

import streamlit as st
from datetime import datetime
import numpy as np

from storage import Project, save_project, load_project, get_projects_by_team, delete_project
from models import (
    compute_additive_projection,
    compute_multiplicative_projection,
    compute_logistic_projection,
    compute_time_to_target,
    get_target_value
)
from data_quality import (
    compute_data_quality_score,
    get_quality_label,
    get_quality_stars,
    get_warnings_and_recommendations
)
from impact import compute_impact_score, get_impact_interpretation
from plots import plot_trajectory, plot_progress_gauge, plot_impact_breakdown


def render_contributor_interface():
    """Render the main contributor interface."""
    st.title("🌱 ARIA Adaptation Tracker - Contributor Interface")

    # Team selection/identification
    if 'team_name' not in st.session_state:
        st.session_state.team_name = ""

    team_name = st.text_input(
        "Team/Institution Name",
        value=st.session_state.team_name,
        help="Enter your team or institution name"
    )

    if team_name:
        st.session_state.team_name = team_name
        render_team_dashboard(team_name)
    else:
        st.info("👆 Please enter your team name to get started.")


def render_team_dashboard(team_name: str):
    """Render dashboard for a specific team."""

    # Load team's projects
    projects = get_projects_by_team(team_name)

    # Project selection
    col1, col2 = st.columns([3, 1])

    with col1:
        if projects:
            project_options = {f"{p.system_name} - {p.phenotype}": p.project_id for p in projects}
            project_options["➕ Create New Project"] = "new"

            selected = st.selectbox(
                "Select Project",
                options=list(project_options.keys())
            )
            selected_id = project_options[selected]
        else:
            st.info("No projects yet. Create your first project below!")
            selected_id = "new"

    with col2:
        if st.button("🗑️ Delete Project", disabled=(not projects or selected_id == "new")):
            if selected_id != "new":
                delete_project(selected_id)
                st.success("Project deleted!")
                st.rerun()

    # Render appropriate view
    if selected_id == "new":
        render_project_form(team_name)
    else:
        project = load_project(selected_id)
        if project:
            render_project_dashboard(project)


def render_project_form(team_name: str, project: Project = None):
    """Render project data entry/edit form."""

    is_new = project is None
    st.subheader("➕ New Project" if is_new else "✏️ Edit Project")

    if project is None:
        project = Project(team_name=team_name)

    with st.form("project_form"):
        st.markdown("### 📋 Project Identity")

        col1, col2 = st.columns(2)
        with col1:
            system_name = st.text_input(
                "System/Species",
                value=project.system_name,
                help="e.g., 'Coral (Acropora millepora)', 'Winter Wheat', 'Honeybee'"
            )
            phenotype = st.text_input(
                "Phenotype/Trait",
                value=project.phenotype,
                help="e.g., 'Heat tolerance (LT50)', 'Drought survival', 'Disease resistance'"
            )
        with col2:
            stress_scenario = st.text_input(
                "Stress Scenario",
                value=project.stress_scenario,
                help="e.g., 'RCP 8.5, 2050 ocean temps', '+2°C air temperature'"
            )
            contact_email = st.text_input(
                "Contact Email",
                value=project.contact_email
            )

        st.markdown("### 📊 Performance Data")

        col1, col2, col3 = st.columns(3)
        with col1:
            W0 = st.number_input(
                "Baseline Performance (W₀)",
                value=float(project.W0),
                help="Performance at start of experiment"
            )
            W0_units = st.text_input(
                "Units",
                value=project.W0_units,
                help="e.g., '°C', '% survival', 'kg/ha'"
            )
        with col2:
            W_current = st.number_input(
                "Current Performance",
                value=float(project.W_current),
                help="Most recent measurement"
            )
            t_gen_elapsed = st.number_input(
                "Generations Observed",
                value=float(project.t_gen_elapsed),
                min_value=0.0,
                help="Number of generations between baseline and current"
            )
        with col3:
            gen_time_years = st.number_input(
                "Generation Time (years)",
                value=float(project.gen_time_years),
                min_value=0.01,
                help="Years per generation"
            )
            dW_se = st.number_input(
                "Standard Error (optional)",
                value=float(project.dW_se),
                min_value=0.0,
                help="Standard error of performance change"
            )

        st.markdown("### 🔬 Experimental Context")

        col1, col2, col3 = st.columns(3)
        with col1:
            sample_size = st.number_input(
                "Sample Size",
                value=int(project.sample_size) if project.sample_size else 0,
                min_value=0,
                help="Number of individuals/replicates"
            )
            environment = st.selectbox(
                "Environment",
                options=['Lab', 'Greenhouse', 'Field', 'Mixed'],
                index=['Lab', 'Greenhouse', 'Field', 'Mixed'].index(project.environment)
            )
        with col2:
            selection_method = st.selectbox(
                "Selection Method",
                options=['Artificial', 'Natural', 'Assisted gene flow', 'Other'],
                index=['Artificial', 'Natural', 'Assisted gene flow', 'Other'].index(project.selection_method)
            )
        with col3:
            observation_start = st.text_input(
                "Observation Start (YYYY-MM-DD)",
                value=project.observation_start_date,
                help="Optional: when measurements began"
            )
            observation_end = st.text_input(
                "Observation End (YYYY-MM-DD)",
                value=project.observation_end_date,
                help="Optional: most recent measurement date"
            )

        st.markdown("### 🎯 Targets")

        col1, col2, col3 = st.columns(3)
        with col1:
            target_type = st.radio(
                "Target Type",
                options=['Fold increase', 'Absolute value'],
                index=0 if project.target_type == 'Fold increase' else 1
            )
        with col2:
            target_value = st.number_input(
                "Target Value",
                value=float(project.target_value),
                help="Fold (e.g., 2.0 = 2× baseline) or absolute value"
            )
        with col3:
            target_date = st.number_input(
                "Target Year",
                value=int(project.target_date),
                min_value=datetime.now().year,
                max_value=2100,
                help="Year by which target should be achieved"
            )

        st.markdown("### 🌍 Impact Assessment")

        col1, col2 = st.columns(2)
        with col1:
            ecological_value = st.slider(
                "Ecological Value",
                min_value=0.0, max_value=10.0, value=float(project.ecological_value), step=0.5,
                help="Biodiversity/ecosystem function importance (0-10)"
            )
            economic_value = st.slider(
                "Economic Value",
                min_value=0.0, max_value=10.0, value=float(project.economic_value), step=0.5,
                help="Agriculture/fisheries/forestry value (0-10)"
            )
            urgency = st.slider(
                "Urgency",
                min_value=0.0, max_value=10.0, value=float(project.urgency), step=0.5,
                help="How soon is adaptation needed? (0-10)"
            )
        with col2:
            technical_feasibility = st.slider(
                "Technical Feasibility",
                min_value=0.0, max_value=10.0, value=float(project.technical_feasibility), step=0.5,
                help="Tractability of intervention (0-10)"
            )
            scalability = st.slider(
                "Scalability",
                min_value=0.0, max_value=10.0, value=float(project.scalability), step=0.5,
                help="Potential for wide deployment (0-10)"
            )

        st.markdown("### ⚙️ Model Settings")

        col1, col2 = st.columns(2)
        with col1:
            model_type = st.selectbox(
                "Model Type",
                options=['additive', 'multiplicative', 'logistic'],
                index=['additive', 'multiplicative', 'logistic'].index(project.model_type),
                help="Linear (additive), exponential (multiplicative), or plateau (logistic)"
            )
        with col2:
            projection_generations = st.number_input(
                "Projection Horizon (generations)",
                value=int(project.projection_generations),
                min_value=1,
                max_value=200,
                help="How many generations to project forward"
            )

        if model_type == 'logistic':
            plateau_performance = st.number_input(
                "Plateau Performance (W_max)",
                value=float(project.plateau_performance) if project.plateau_performance else W_current * 3,
                help="Maximum achievable performance (genetic constraint)"
            )
        else:
            plateau_performance = None

        notes = st.text_area(
            "Notes (optional)",
            value=project.notes,
            help="Any additional context or observations"
        )

        submitted = st.form_submit_button("💾 Save Project")

        if submitted:
            # Update project
            project.system_name = system_name
            project.phenotype = phenotype
            project.stress_scenario = stress_scenario
            project.contact_email = contact_email
            project.W0 = W0
            project.W0_units = W0_units
            project.W_current = W_current
            project.t_gen_elapsed = t_gen_elapsed
            project.gen_time_years = gen_time_years
            project.dW_se = dW_se
            project.sample_size = sample_size
            project.environment = environment
            project.selection_method = selection_method
            project.observation_start_date = observation_start
            project.observation_end_date = observation_end
            project.target_type = target_type
            project.target_value = target_value
            project.target_date = target_date
            project.ecological_value = ecological_value
            project.economic_value = economic_value
            project.urgency = urgency
            project.technical_feasibility = technical_feasibility
            project.scalability = scalability
            project.model_type = model_type
            project.plateau_performance = plateau_performance
            project.projection_generations = projection_generations
            project.notes = notes

            save_project(project)
            st.success("✅ Project saved successfully!")
            st.rerun()


def render_project_dashboard(project: Project):
    """Render dashboard for a specific project."""

    st.subheader(f"📊 {project.system_name} - {project.phenotype}")

    # Compute all metrics
    try:
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

        # Get target value
        W_target = get_target_value(project.W0, project.target_type, project.target_value)

        # Time to target
        time_result = compute_time_to_target(
            project.W_current, W_target, projection['rate_per_gen'],
            project.gen_time_years, project.model_type,
            projection.get('rate_lower'), projection.get('rate_upper'),
            project.plateau_performance
        )

        # Data quality
        quality_score, quality_reasons = compute_data_quality_score(
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

        # Status determination
        current_year = datetime.now().year
        if projection['rate_per_gen'] <= 0:
            status = "At Risk"
            status_color = "red"
        elif not time_result['reachable']:
            status = "At Risk"
            status_color = "red"
        elif 'years_upper' in time_result and np.isfinite(time_result['years_upper']):
            if current_year + time_result['years_upper'] > project.target_date:
                status = "Behind Track"
                status_color = "orange"
            else:
                status = "On Track"
                status_color = "green"
        elif np.isfinite(time_result['years_to_target']):
            if current_year + time_result['years_to_target'] > project.target_date:
                status = "Behind Track"
                status_color = "orange"
            else:
                status = "On Track"
                status_color = "green"
        else:
            status = "At Risk"
            status_color = "red"

        # Display status and quality
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"### Status: :{status_color}[{status}]")
        with col2:
            st.markdown(f"### Quality: {get_quality_stars(quality_score)}")
            st.caption(f"{get_quality_label(quality_score)} confidence")
        with col3:
            st.markdown(f"### Impact: {impact_result['total_score']:.1f}/10")
            st.caption(get_impact_interpretation(impact_result['total_score']))

        # Summary metrics
        st.markdown("---")
        st.markdown("### 📈 Current Status")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                "Baseline",
                f"{project.W0:.2f} {project.W0_units}"
            )
        with col2:
            st.metric(
                "Current",
                f"{project.W_current:.2f} {project.W0_units}",
                delta=f"{project.dW:+.2f}"
            )
        with col3:
            st.metric(
                "Target",
                f"{W_target:.2f} {project.W0_units}"
            )
        with col4:
            progress_pct = ((project.W_current - project.W0) / (W_target - project.W0)) * 100
            st.metric(
                "Progress",
                f"{progress_pct:.1f}%"
            )

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Rate per Generation",
                f"{projection['rate_per_gen']:.4f} {project.W0_units}/gen"
            )
        with col2:
            st.metric(
                "Rate per Year",
                f"{projection['rate_per_year']:.4f} {project.W0_units}/yr"
            )
        with col3:
            if time_result['reachable'] and np.isfinite(time_result['years_to_target']):
                if 'years_lower' in time_result and 'years_upper' in time_result:
                    st.metric(
                        "Years to Target",
                        f"{time_result['years_to_target']:.1f}",
                        delta=f"±{(time_result['years_upper'] - time_result['years_lower'])/2:.1f}"
                    )
                else:
                    st.metric(
                        "Years to Target",
                        f"{time_result['years_to_target']:.1f}"
                    )
            else:
                st.metric(
                    "Years to Target",
                    "∞ (Not reachable)"
                )

        # Main trajectory plot
        st.markdown("---")
        st.markdown("### 🎯 Trajectory Projection")

        fig = plot_trajectory(
            projection, W_target, project.W0, project.W0_units,
            project.target_date, current_year,
            project.system_name, project.phenotype,
            show_uncertainty=(project.dW_se > 0)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Warnings and recommendations
        st.markdown("---")
        st.markdown("### ⚠️ Diagnostics & Recommendations")

        warnings = get_warnings_and_recommendations(
            quality_score, project.sample_size, project.t_gen_elapsed,
            project.environment, project.dW_se
        )

        for warning in warnings:
            if warning['level'] == 'error':
                st.error(warning['message'])
            elif warning['level'] == 'warning':
                st.warning(warning['message'])
            elif warning['level'] == 'success':
                st.success(warning['message'])
            else:
                st.info(warning['message'])

        # Collapsible sections
        with st.expander("📊 Impact Score Breakdown"):
            fig_impact = plot_impact_breakdown(impact_result)
            st.plotly_chart(fig_impact, use_container_width=True)

            st.markdown("**Weighted Components:**")
            for component, value in impact_result['components'].items():
                st.write(f"- {component.capitalize()}: {value:.2f}")

        with st.expander("📋 Data Quality Details"):
            st.markdown("**Quality Criteria:**")
            for reason in quality_reasons:
                st.write(reason)

        with st.expander("✏️ Edit Project Data"):
            render_project_form(project.team_name, project)

    except Exception as e:
        st.error(f"Error computing projections: {str(e)}")
        st.info("Please check your input data and try again.")

        with st.expander("✏️ Edit Project Data"):
            render_project_form(project.team_name, project)
