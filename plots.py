"""
Visualization functions for adaptation trajectories.
"""

import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Dict, Optional


def plot_trajectory(
    projection: Dict,
    W_target: float,
    W0: float,
    W0_units: str,
    target_date: int,
    current_year: int,
    system_name: str = "",
    phenotype: str = "",
    show_uncertainty: bool = True
) -> go.Figure:
    """
    Create interactive trajectory plot.

    Args:
        projection: Output from models.compute_*_projection
        W_target: Target performance value
        W0: Baseline performance
        W0_units: Units of measurement
        target_date: Target year
        current_year: Current year
        system_name: Name of system for title
        phenotype: Phenotype being measured
        show_uncertainty: Whether to show CI bands

    Returns:
        Plotly figure object
    """
    years = projection['years']
    W_projection = projection['W_projection']
    W_current = projection['W_current']

    # Convert generations to actual years
    years_actual = current_year + years

    fig = go.Figure()

    # Main projection line
    fig.add_trace(go.Scatter(
        x=years_actual,
        y=W_projection,
        mode='lines',
        name='Projected trajectory',
        line=dict(color='#1f77b4', width=3),
        hovertemplate='<b>Year:</b> %{x}<br><b>Performance:</b> %{y:.2f}<extra></extra>'
    ))

    # Uncertainty band
    if show_uncertainty and 'W_lower' in projection and projection['W_lower'] is not None:
        W_lower = projection['W_lower']
        W_upper = projection['W_upper']

        # Upper bound
        fig.add_trace(go.Scatter(
            x=years_actual,
            y=W_upper,
            mode='lines',
            name='95% CI upper',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))

        # Lower bound with fill
        fig.add_trace(go.Scatter(
            x=years_actual,
            y=W_lower,
            mode='lines',
            name='95% CI',
            line=dict(width=0),
            fillcolor='rgba(31, 119, 180, 0.2)',
            fill='tonexty',
            hovertemplate='<b>95% CI:</b> %{y:.2f}<extra></extra>'
        ))

    # Current position marker
    fig.add_trace(go.Scatter(
        x=[current_year],
        y=[W_current],
        mode='markers',
        name='Current position',
        marker=dict(size=12, color='green', symbol='circle'),
        hovertemplate='<b>Current:</b> %{y:.2f}<br><b>Year:</b> %{x}<extra></extra>'
    ))

    # Baseline marker
    fig.add_trace(go.Scatter(
        x=[current_year - projection['current_gen'] * projection['years'][1]],
        y=[W0],
        mode='markers',
        name='Baseline',
        marker=dict(size=10, color='gray', symbol='diamond'),
        hovertemplate='<b>Baseline:</b> %{y:.2f}<extra></extra>'
    ))

    # Target line
    fig.add_trace(go.Scatter(
        x=[years_actual[0], years_actual[-1]],
        y=[W_target, W_target],
        mode='lines',
        name=f'Target ({W_target:.2f})',
        line=dict(color='red', width=2, dash='dash'),
        hovertemplate='<b>Target:</b> %{y:.2f}<extra></extra>'
    ))

    # Target date vertical line
    if target_date is not None:
        fig.add_trace(go.Scatter(
            x=[target_date, target_date],
            y=[min(W0, W_projection.min()), max(W_target * 1.1, W_projection.max())],
            mode='lines',
            name=f'Target date ({target_date})',
            line=dict(color='orange', width=2, dash='dot'),
            hovertemplate=f'<b>Target year:</b> {target_date}<extra></extra>'
        ))

    # Layout
    title = f"Adaptation Trajectory"
    if system_name:
        title += f" - {system_name}"
    if phenotype:
        title += f" ({phenotype})"

    fig.update_layout(
        title=title,
        xaxis_title="Year",
        yaxis_title=f"Performance ({W0_units})" if W0_units else "Performance",
        hovermode='closest',
        template='plotly_white',
        height=500,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    return fig


def plot_progress_gauge(
    W_current: float,
    W0: float,
    W_target: float,
    W0_units: str = ""
) -> go.Figure:
    """
    Create a gauge showing progress to target.

    Args:
        W_current: Current performance
        W0: Baseline performance
        W_target: Target performance
        W0_units: Units for display

    Returns:
        Plotly figure object
    """
    # Calculate progress percentage
    if W_target > W0:
        progress = ((W_current - W0) / (W_target - W0)) * 100
    else:
        progress = 0

    progress = np.clip(progress, 0, 100)

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=progress,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Progress to Target", 'font': {'size': 24}},
        delta={'reference': 100, 'suffix': '%'},
        gauge={
            'axis': {'range': [None, 100], 'ticksuffix': '%'},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 33], 'color': "lightgray"},
                {'range': [33, 66], 'color': "gray"},
                {'range': [66, 100], 'color': "darkgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 100
            }
        }
    ))

    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20)
    )

    return fig


def plot_impact_breakdown(impact_result: Dict) -> go.Figure:
    """
    Create bar chart showing impact score components.

    Args:
        impact_result: Output from impact.compute_impact_score

    Returns:
        Plotly figure object
    """
    components = impact_result['component_unweighted']

    # Order components for display
    component_order = ['ecological', 'economic', 'urgency', 'timeline', 'scalability', 'feasibility']
    labels = ['Ecological\nValue', 'Economic\nValue', 'Urgency', 'Timeline', 'Scalability', 'Feasibility']
    values = [components.get(c, 0) for c in component_order]

    fig = go.Figure(go.Bar(
        x=labels,
        y=values,
        marker_color=['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6', '#95a5a6'],
        text=[f"{v:.1f}" for v in values],
        textposition='outside'
    ))

    fig.update_layout(
        title="Impact Score Components (0-10 scale)",
        yaxis_title="Score",
        yaxis_range=[0, 10.5],
        template='plotly_white',
        height=400,
        showlegend=False
    )

    return fig


def plot_multiple_trajectories(
    projects_data: list,
    normalize: bool = False
) -> go.Figure:
    """
    Plot multiple project trajectories on same axes.

    Args:
        projects_data: List of dicts, each containing:
            - 'name': project name
            - 'years': year array
            - 'W': performance array
            - 'color': optional color
        normalize: If True, show as % of target instead of raw values

    Returns:
        Plotly figure object
    """
    fig = go.Figure()

    for project in projects_data:
        name = project.get('name', 'Unknown')
        years = project.get('years', [])
        W = project.get('W', [])
        color = project.get('color', None)

        if normalize:
            W_target = project.get('W_target', 1)
            W0 = project.get('W0', 0)
            if W_target > W0:
                W_norm = ((np.array(W) - W0) / (W_target - W0)) * 100
            else:
                W_norm = np.array(W) * 0
        else:
            W_norm = W

        fig.add_trace(go.Scatter(
            x=years,
            y=W_norm,
            mode='lines',
            name=name,
            line=dict(color=color) if color else {},
            hovertemplate=f'<b>{name}</b><br>Year: %{{x}}<br>Value: %{{y:.1f}}<extra></extra>'
        ))

    ylabel = "Progress (%)" if normalize else "Performance"

    fig.update_layout(
        title="Project Comparison",
        xaxis_title="Year",
        yaxis_title=ylabel,
        hovermode='closest',
        template='plotly_white',
        height=500,
        showlegend=True
    )

    if normalize:
        fig.add_hline(y=100, line_dash="dash", line_color="red",
                     annotation_text="Target", annotation_position="right")

    return fig


def plot_risk_matrix(projects_summary: list) -> go.Figure:
    """
    Create impact vs timeline risk matrix.

    Args:
        projects_summary: List of dicts with:
            - 'name': project name
            - 'impact_score': impact score
            - 'years_to_target': years to reach target
            - 'status': status string

    Returns:
        Plotly figure object
    """
    names = [p['name'] for p in projects_summary]
    impact_scores = [p.get('impact_score', 0) for p in projects_summary]
    years_to_target = [p.get('years_to_target', np.inf) for p in projects_summary]
    statuses = [p.get('status', 'Unknown') for p in projects_summary]

    # Handle infinite values
    years_to_target = [y if np.isfinite(y) else 50 for y in years_to_target]

    # Color by status
    color_map = {
        'On Track': 'green',
        'Behind Track': 'orange',
        'At Risk': 'red',
        'Needs Validation': 'yellow'
    }
    colors = [color_map.get(s, 'gray') for s in statuses]

    fig = go.Figure(go.Scatter(
        x=years_to_target,
        y=impact_scores,
        mode='markers+text',
        marker=dict(size=15, color=colors, line=dict(width=2, color='white')),
        text=names,
        textposition='top center',
        textfont=dict(size=10),
        hovertemplate='<b>%{text}</b><br>Impact: %{y:.1f}<br>Years to target: %{x:.1f}<extra></extra>'
    ))

    # Add quadrant lines
    median_impact = np.median(impact_scores)
    median_years = np.median(years_to_target)

    fig.add_hline(y=median_impact, line_dash="dot", line_color="gray", opacity=0.5)
    fig.add_vline(x=median_years, line_dash="dot", line_color="gray", opacity=0.5)

    # Add quadrant labels
    max_years = max(years_to_target) if years_to_target else 20
    max_impact = max(impact_scores) if impact_scores else 10

    annotations = [
        dict(x=max_years * 0.25, y=max_impact * 0.75, text="High Priority<br>(High Impact, Soon)",
             showarrow=False, font=dict(size=10, color='darkgreen')),
        dict(x=max_years * 0.75, y=max_impact * 0.75, text="Strategic<br>(High Impact, Far)",
             showarrow=False, font=dict(size=10, color='darkblue')),
        dict(x=max_years * 0.25, y=max_impact * 0.25, text="Quick Wins<br>(Low Impact, Soon)",
             showarrow=False, font=dict(size=10, color='orange')),
        dict(x=max_years * 0.75, y=max_impact * 0.25, text="Deprioritize?<br>(Low Impact, Far)",
             showarrow=False, font=dict(size=10, color='gray'))
    ]

    fig.update_layout(
        title="Portfolio Risk Matrix: Impact vs Timeline",
        xaxis_title="Years to Target",
        yaxis_title="Impact Score",
        template='plotly_white',
        height=600,
        showlegend=False,
        annotations=annotations
    )

    return fig
