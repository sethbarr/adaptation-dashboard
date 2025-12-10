"""
Core projection models for adaptation trajectories.
"""

import numpy as np
from scipy import stats
from typing import Dict, Tuple, Optional


def compute_additive_projection(
    W0: float,
    W_current: float,
    t_gen_elapsed: float,
    gen_time_years: float,
    projection_generations: int,
    dW_se: float = 0.0,
    confidence_level: float = 0.95
) -> Dict:
    """
    Compute additive (linear) projection.

    Args:
        W0: Baseline performance
        W_current: Current performance
        t_gen_elapsed: Generations observed
        gen_time_years: Years per generation
        projection_generations: How many generations to project
        dW_se: Standard error of performance change
        confidence_level: Confidence level for intervals (0.8, 0.9, 0.95)

    Returns:
        Dictionary with:
            - generations: array of generation points
            - years: array of year points (from present)
            - W_projection: array of projected performance
            - W_lower: lower CI bound (if dW_se > 0)
            - W_upper: upper CI bound (if dW_se > 0)
            - rate_per_gen: rate per generation
            - rate_per_year: rate per year
    """
    dW = W_current - W0

    if t_gen_elapsed > 0:
        rate_per_gen = dW / t_gen_elapsed
    else:
        rate_per_gen = 0.0

    rate_per_year = rate_per_gen / gen_time_years if gen_time_years > 0 else 0.0

    # Generate time points
    generations = np.arange(0, projection_generations + 1)
    years = generations * gen_time_years

    # Main projection
    W_projection = W_current + rate_per_gen * generations

    result = {
        'generations': generations,
        'years': years,
        'W_projection': W_projection,
        'rate_per_gen': rate_per_gen,
        'rate_per_year': rate_per_year,
        'W_current': W_current,
        'current_gen': 0  # Current is at generation 0 in projection
    }

    # Add uncertainty bounds if SE provided
    if dW_se > 0 and t_gen_elapsed > 0:
        z_score = stats.norm.ppf((1 + confidence_level) / 2)

        rate_lower = (dW - dW_se * z_score) / t_gen_elapsed
        rate_upper = (dW + dW_se * z_score) / t_gen_elapsed

        W_lower = W_current + rate_lower * generations
        W_upper = W_current + rate_upper * generations

        result['W_lower'] = W_lower
        result['W_upper'] = W_upper
        result['rate_lower'] = rate_lower
        result['rate_upper'] = rate_upper

    return result


def compute_multiplicative_projection(
    W0: float,
    W_current: float,
    t_gen_elapsed: float,
    gen_time_years: float,
    projection_generations: int,
    dW_se: float = 0.0,
    confidence_level: float = 0.95
) -> Dict:
    """
    Compute multiplicative (exponential) projection.

    Args:
        Same as compute_additive_projection

    Returns:
        Dictionary with same structure as additive model
    """
    if W0 <= 0 or W_current <= 0:
        raise ValueError("Multiplicative model requires positive W0 and W_current")

    if t_gen_elapsed > 0:
        r_rel = (1 / t_gen_elapsed) * np.log(W_current / W0)
    else:
        r_rel = 0.0

    rate_per_year = r_rel / gen_time_years if gen_time_years > 0 else 0.0

    # Generate time points
    generations = np.arange(0, projection_generations + 1)
    years = generations * gen_time_years

    # Main projection
    W_projection = W_current * np.exp(r_rel * generations)

    result = {
        'generations': generations,
        'years': years,
        'W_projection': W_projection,
        'rate_per_gen': r_rel,
        'rate_per_year': rate_per_year,
        'W_current': W_current,
        'current_gen': 0
    }

    # Add uncertainty bounds if SE provided
    if dW_se > 0 and t_gen_elapsed > 0:
        z_score = stats.norm.ppf((1 + confidence_level) / 2)

        # Approximate SE on log scale
        dW = W_current - W0
        # This is a rough approximation - could be improved with delta method
        log_se = dW_se / W0

        r_rel_lower = r_rel - (log_se * z_score / t_gen_elapsed)
        r_rel_upper = r_rel + (log_se * z_score / t_gen_elapsed)

        W_lower = W_current * np.exp(r_rel_lower * generations)
        W_upper = W_current * np.exp(r_rel_upper * generations)

        result['W_lower'] = W_lower
        result['W_upper'] = W_upper
        result['rate_lower'] = r_rel_lower
        result['rate_upper'] = r_rel_upper

    return result


def compute_logistic_projection(
    W0: float,
    W_current: float,
    W_max: float,
    t_gen_elapsed: float,
    gen_time_years: float,
    projection_generations: int,
    dW_se: float = 0.0,
    confidence_level: float = 0.95
) -> Dict:
    """
    Compute logistic (plateau) projection.

    Args:
        W0: Baseline performance
        W_current: Current performance
        W_max: Maximum achievable performance (plateau)
        t_gen_elapsed: Generations observed
        gen_time_years: Years per generation
        projection_generations: How many generations to project
        dW_se: Standard error of performance change
        confidence_level: Confidence level for intervals

    Returns:
        Dictionary with same structure as additive model
    """
    if W_max <= W_current:
        raise ValueError("W_max must be greater than W_current for logistic model")

    if t_gen_elapsed > 0 and W_current > W0:
        # Estimate growth rate from observed change
        # W(t) = W_max - (W_max - W0) * exp(-r * t)
        # Solve for r given W_current at t_gen_elapsed
        r = -np.log((W_max - W_current) / (W_max - W0)) / t_gen_elapsed
    else:
        r = 0.0

    rate_per_year = r / gen_time_years if gen_time_years > 0 else 0.0

    # Generate time points
    generations = np.arange(0, projection_generations + 1)
    years = generations * gen_time_years

    # Main projection
    W_projection = W_max - (W_max - W_current) * np.exp(-r * generations)

    result = {
        'generations': generations,
        'years': years,
        'W_projection': W_projection,
        'rate_per_gen': r,
        'rate_per_year': rate_per_year,
        'W_current': W_current,
        'current_gen': 0,
        'W_max': W_max
    }

    # Uncertainty bounds for logistic are complex - skip for Phase 1
    if dW_se > 0:
        result['W_lower'] = None
        result['W_upper'] = None

    return result


def compute_time_to_target(
    W_current: float,
    W_target: float,
    rate_per_gen: float,
    gen_time_years: float,
    model_type: str = 'additive',
    rate_lower: Optional[float] = None,
    rate_upper: Optional[float] = None,
    W_max: Optional[float] = None
) -> Dict:
    """
    Calculate time to reach target performance.

    Args:
        W_current: Current performance
        W_target: Target performance
        rate_per_gen: Rate of improvement per generation
        gen_time_years: Years per generation
        model_type: 'additive', 'multiplicative', or 'logistic'
        rate_lower: Lower bound on rate (for CI)
        rate_upper: Upper bound on rate (for CI)
        W_max: Maximum performance (for logistic only)

    Returns:
        Dictionary with:
            - generations_to_target: generations needed
            - years_to_target: years needed
            - generations_lower: lower CI bound (if rates provided)
            - generations_upper: upper CI bound (if rates provided)
            - years_lower: lower CI bound in years
            - years_upper: upper CI bound in years
            - reachable: boolean, whether target is achievable
    """
    if W_target <= W_current:
        # Already at or past target
        return {
            'generations_to_target': 0.0,
            'years_to_target': 0.0,
            'reachable': True
        }

    if model_type == 'additive':
        if rate_per_gen > 0:
            gen_to_target = (W_target - W_current) / rate_per_gen
            reachable = True
        else:
            gen_to_target = np.inf
            reachable = False

        result = {
            'generations_to_target': gen_to_target,
            'years_to_target': gen_to_target * gen_time_years,
            'reachable': reachable
        }

        # Add CI if bounds provided
        if rate_lower is not None and rate_upper is not None:
            if rate_upper > 0:
                gen_lower = (W_target - W_current) / rate_upper
            else:
                gen_lower = np.inf

            if rate_lower > 0:
                gen_upper = (W_target - W_current) / rate_lower
            else:
                gen_upper = np.inf

            result['generations_lower'] = gen_lower
            result['generations_upper'] = gen_upper
            result['years_lower'] = gen_lower * gen_time_years
            result['years_upper'] = gen_upper * gen_time_years

    elif model_type == 'multiplicative':
        if rate_per_gen > 0 and W_current > 0:
            gen_to_target = (1 / rate_per_gen) * np.log(W_target / W_current)
            reachable = True
        else:
            gen_to_target = np.inf
            reachable = False

        result = {
            'generations_to_target': gen_to_target,
            'years_to_target': gen_to_target * gen_time_years,
            'reachable': reachable
        }

        if rate_lower is not None and rate_upper is not None:
            if rate_upper > 0:
                gen_lower = (1 / rate_upper) * np.log(W_target / W_current)
            else:
                gen_lower = np.inf

            if rate_lower > 0:
                gen_upper = (1 / rate_lower) * np.log(W_target / W_current)
            else:
                gen_upper = np.inf

            result['generations_lower'] = gen_lower
            result['generations_upper'] = gen_upper
            result['years_lower'] = gen_lower * gen_time_years
            result['years_upper'] = gen_upper * gen_time_years

    elif model_type == 'logistic':
        if W_max is None:
            raise ValueError("W_max required for logistic model")

        if W_target >= W_max:
            # Target exceeds plateau
            reachable = False
            gen_to_target = np.inf
        elif rate_per_gen > 0:
            # W(t) = W_max - (W_max - W_current) * exp(-r * t)
            # Solve for t when W(t) = W_target
            gen_to_target = -(1 / rate_per_gen) * np.log((W_max - W_target) / (W_max - W_current))
            reachable = True
        else:
            gen_to_target = np.inf
            reachable = False

        result = {
            'generations_to_target': gen_to_target,
            'years_to_target': gen_to_target * gen_time_years,
            'reachable': reachable
        }

    else:
        raise ValueError(f"Unknown model_type: {model_type}")

    return result


def get_target_value(
    W0: float,
    target_type: str,
    target_value: float
) -> float:
    """
    Convert target specification to absolute performance value.

    Args:
        W0: Baseline performance
        target_type: 'Fold increase' or 'Absolute value'
        target_value: The target (fold or absolute)

    Returns:
        Absolute target performance value
    """
    if target_type == 'Fold increase':
        return W0 * target_value
    else:  # Absolute value
        return target_value
