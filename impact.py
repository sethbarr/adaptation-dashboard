"""
Impact scoring for adaptation projects.
"""

from datetime import datetime
from typing import Dict
import numpy as np


def compute_impact_score(
    ecological_value: float,
    economic_value: float,
    urgency: float,
    technical_feasibility: float,
    scalability: float,
    years_to_target: float = None,
    target_date: int = None
) -> Dict[str, float]:
    """
    Compute composite impact score for a project.

    Args:
        ecological_value: 0-10 score for biodiversity/ecosystem importance
        economic_value: 0-10 score for economic value
        urgency: 0-10 score for time-sensitivity
        technical_feasibility: 0-10 score for tractability
        scalability: 0-10 score for deployment potential
        years_to_target: Years until target achieved (optional, for time penalty)
        target_date: Target year (optional, for urgency calculation)

    Returns:
        Dictionary with:
            - total_score: Composite score (0-10)
            - components: Breakdown of weighted components
            - time_factor: Multiplier based on timeline (1.0 if not applicable)
    """
    # Weights for each component
    weights = {
        'ecological': 0.25,
        'economic': 0.25,
        'urgency': 0.20,
        'timeline': 0.15,
        'scalability': 0.10,
        'feasibility': 0.05
    }

    # Normalize inputs to 0-10 scale (in case they're outside)
    ecological_value = np.clip(ecological_value, 0, 10)
    economic_value = np.clip(economic_value, 0, 10)
    urgency = np.clip(urgency, 0, 10)
    technical_feasibility = np.clip(technical_feasibility, 0, 10)
    scalability = np.clip(scalability, 0, 10)

    # Calculate timeline component
    if years_to_target is not None and years_to_target > 0 and np.isfinite(years_to_target):
        # Sooner is better: 10 points for 1 year, declining to 0 at 20+ years
        timeline_score = 10 * np.exp(-years_to_target / 5)
        timeline_score = np.clip(timeline_score, 0, 10)
    else:
        # If not reachable or no timeline, give minimal points
        timeline_score = 0.0

    # Calculate weighted components
    components = {
        'ecological': ecological_value * weights['ecological'],
        'economic': economic_value * weights['economic'],
        'urgency': urgency * weights['urgency'],
        'timeline': timeline_score * weights['timeline'],
        'scalability': scalability * weights['scalability'],
        'feasibility': technical_feasibility * weights['feasibility']
    }

    total_score = sum(components.values())

    # Additional time pressure factor if target_date provided
    time_factor = 1.0
    if target_date is not None:
        current_year = datetime.now().year
        years_remaining = target_date - current_year

        if years_remaining <= 0:
            # Past deadline - critical
            time_factor = 1.5
        elif years_remaining <= 5:
            # Very urgent
            time_factor = 1.3
        elif years_remaining <= 10:
            # Moderately urgent
            time_factor = 1.1

    # Apply time pressure to urgency component
    if time_factor > 1.0:
        components['urgency'] *= time_factor
        total_score = sum(components.values())

    # Ensure score stays in 0-10 range
    total_score = np.clip(total_score, 0, 10)

    return {
        'total_score': round(total_score, 2),
        'components': {k: round(v, 2) for k, v in components.items()},
        'component_unweighted': {
            'ecological': ecological_value,
            'economic': economic_value,
            'urgency': urgency,
            'timeline': round(timeline_score, 2),
            'scalability': scalability,
            'feasibility': technical_feasibility
        },
        'time_factor': round(time_factor, 2)
    }


def get_impact_interpretation(score: float) -> str:
    """
    Get qualitative interpretation of impact score.

    Args:
        score: Impact score (0-10)

    Returns:
        String interpretation
    """
    if score >= 8.0:
        return "Critical Priority"
    elif score >= 6.0:
        return "High Priority"
    elif score >= 4.0:
        return "Moderate Priority"
    else:
        return "Lower Priority"


def get_impact_color(score: float) -> str:
    """
    Get color for impact score visualization.

    Args:
        score: Impact score (0-10)

    Returns:
        Color name
    """
    if score >= 8.0:
        return "red"  # Critical
    elif score >= 6.0:
        return "orange"  # High
    elif score >= 4.0:
        return "blue"  # Moderate
    else:
        return "gray"  # Lower


def compare_projects_by_impact(projects_impacts: Dict[str, float]) -> Dict:
    """
    Rank projects by impact score.

    Args:
        projects_impacts: Dictionary mapping project_id to impact score

    Returns:
        Dictionary with ranking information
    """
    if not projects_impacts:
        return {}

    sorted_projects = sorted(
        projects_impacts.items(),
        key=lambda x: x[1],
        reverse=True
    )

    rankings = {}
    for rank, (project_id, score) in enumerate(sorted_projects, 1):
        rankings[project_id] = {
            'rank': rank,
            'score': score,
            'percentile': (1 - (rank - 1) / len(sorted_projects)) * 100
        }

    return rankings
