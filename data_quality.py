"""
Data quality assessment for adaptation projects.
"""

from typing import Dict, List, Tuple


def compute_data_quality_score(
    sample_size: int,
    t_gen_elapsed: float,
    environment: str,
    dW_se: float,
    has_replicates: bool = True
) -> Tuple[int, List[str]]:
    """
    Compute data quality score (0-5) based on experimental rigor.

    Args:
        sample_size: Number of individuals/replicates
        t_gen_elapsed: Number of generations observed
        environment: 'Lab', 'Greenhouse', 'Field', or 'Mixed'
        dW_se: Standard error (0 if not provided)
        has_replicates: Whether multiple independent measurements exist

    Returns:
        Tuple of (score, reasons) where reasons explains the score
    """
    score = 0
    reasons = []

    # Sample size criterion
    if sample_size >= 100:
        score += 1
        reasons.append("✓ Large sample size (n≥100)")
    elif sample_size >= 30:
        reasons.append("• Moderate sample size (n≥30)")
    else:
        reasons.append("✗ Small sample size (n<30)")

    # Generations observed criterion
    if t_gen_elapsed >= 5:
        score += 1
        reasons.append("✓ Sufficient generations observed (≥5)")
    elif t_gen_elapsed >= 3:
        reasons.append("• Moderate observation period (3-4 gen)")
    else:
        reasons.append("✗ Few generations observed (<3)")

    # Environment criterion (field/mixed preferred over lab)
    if environment in ['Field', 'Mixed']:
        score += 1
        reasons.append(f"✓ Realistic environment ({environment})")
    else:
        reasons.append(f"• Lab environment (limited realism)")

    # Statistical rigor
    if dW_se > 0:
        score += 1
        reasons.append("✓ Uncertainty quantified (SE provided)")
    else:
        reasons.append("✗ No uncertainty estimate")

    # Replication
    if has_replicates:
        score += 1
        reasons.append("✓ Replicated measurements")
    else:
        reasons.append("✗ No replication")

    return score, reasons


def get_quality_label(score: int) -> str:
    """
    Convert numeric score to categorical label.

    Args:
        score: Quality score (0-5)

    Returns:
        String label: 'High', 'Moderate', or 'Preliminary'
    """
    if score >= 4:
        return "High"
    elif score >= 2:
        return "Moderate"
    else:
        return "Preliminary"


def get_quality_color(score: int) -> str:
    """
    Get color code for quality score.

    Args:
        score: Quality score (0-5)

    Returns:
        Color name for Streamlit styling
    """
    if score >= 4:
        return "green"
    elif score >= 2:
        return "orange"
    else:
        return "red"


def get_quality_stars(score: int) -> str:
    """
    Convert score to star rating.

    Args:
        score: Quality score (0-5)

    Returns:
        String with filled and empty stars
    """
    filled = "★" * score
    empty = "☆" * (5 - score)
    return filled + empty


def get_warnings_and_recommendations(
    score: int,
    sample_size: int,
    t_gen_elapsed: float,
    environment: str,
    dW_se: float
) -> List[Dict[str, str]]:
    """
    Generate actionable warnings and recommendations.

    Args:
        score: Quality score
        sample_size: Number of individuals
        t_gen_elapsed: Generations observed
        environment: Experimental environment
        dW_se: Standard error

    Returns:
        List of dictionaries with 'level' and 'message' keys
    """
    warnings = []

    # Critical warnings (red)
    if sample_size < 30:
        warnings.append({
            'level': 'error',
            'message': f"⚠️ Sample size is very small (n={sample_size}). Increase to at least 100 for reliable estimates."
        })

    if t_gen_elapsed < 3:
        warnings.append({
            'level': 'error',
            'message': f"⚠️ Only {t_gen_elapsed:.1f} generations observed. Early trends may not be reliable. Continue observations."
        })

    if dW_se == 0:
        warnings.append({
            'level': 'warning',
            'message': "⚠️ No uncertainty estimate provided. Calculate standard error for confidence intervals."
        })

    # Moderate warnings (yellow)
    if environment == 'Lab':
        warnings.append({
            'level': 'warning',
            'message': "ℹ️ Lab-only environment. Consider field validation to confirm adaptation transfers to natural conditions."
        })

    if 3 <= t_gen_elapsed < 5:
        warnings.append({
            'level': 'info',
            'message': f"ℹ️ {t_gen_elapsed:.1f} generations observed. Continue to 5+ generations for higher confidence."
        })

    # Informational (blue)
    if t_gen_elapsed >= 10:
        warnings.append({
            'level': 'info',
            'message': f"ℹ️ Long observation period ({t_gen_elapsed:.1f} gen). Consider re-assessing rate assumptions - adaptation may be slowing."
        })

    if score >= 4:
        warnings.append({
            'level': 'success',
            'message': "✓ Data quality is high. Projections are well-supported."
        })

    return warnings
