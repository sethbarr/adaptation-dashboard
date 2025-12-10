"""
Data storage and retrieval for adaptation projects.
Uses JSON files for simplicity in Phase 1.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import uuid


DATA_DIR = Path(__file__).parent / "data" / "projects"


class Project:
    """Represents a single adaptation project."""

    def __init__(self, **kwargs):
        # Core Identity
        self.project_id = kwargs.get('project_id', str(uuid.uuid4()))
        self.team_name = kwargs.get('team_name', '')
        self.system_name = kwargs.get('system_name', '')
        self.phenotype = kwargs.get('phenotype', '')
        self.stress_scenario = kwargs.get('stress_scenario', '')
        self.program_year = kwargs.get('program_year', datetime.now().year)
        self.status = kwargs.get('status', 'Active')

        # Performance Data
        self.W0 = kwargs.get('W0', 1.0)
        self.W0_units = kwargs.get('W0_units', '')
        self.W_current = kwargs.get('W_current', 1.0)
        self.t_gen_elapsed = kwargs.get('t_gen_elapsed', 0.0)
        self.gen_time_years = kwargs.get('gen_time_years', 1.0)

        # Experimental Context
        self.observation_start_date = kwargs.get('observation_start_date', '')
        self.observation_end_date = kwargs.get('observation_end_date', '')
        self.sample_size = kwargs.get('sample_size', 0)
        self.environment = kwargs.get('environment', 'Lab')
        self.selection_method = kwargs.get('selection_method', 'Artificial')

        # Targets
        self.target_type = kwargs.get('target_type', 'Fold increase')
        self.target_value = kwargs.get('target_value', 2.0)
        self.target_date = kwargs.get('target_date', datetime.now().year + 10)
        self.minimum_viable_performance = kwargs.get('minimum_viable_performance', None)

        # Uncertainty
        self.dW_se = kwargs.get('dW_se', 0.0)
        self.confidence_level = kwargs.get('confidence_level', 0.95)

        # Impact Assessment
        self.ecological_value = kwargs.get('ecological_value', 5.0)
        self.economic_value = kwargs.get('economic_value', 5.0)
        self.urgency = kwargs.get('urgency', 5.0)
        self.technical_feasibility = kwargs.get('technical_feasibility', 5.0)
        self.scalability = kwargs.get('scalability', 5.0)

        # Model Parameters
        self.model_type = kwargs.get('model_type', 'additive')
        self.plateau_performance = kwargs.get('plateau_performance', None)
        self.projection_generations = kwargs.get('projection_generations', 50)

        # Metadata
        self.last_updated = kwargs.get('last_updated', datetime.now().isoformat())
        self.contact_email = kwargs.get('contact_email', '')
        self.notes = kwargs.get('notes', '')

    @property
    def dW(self):
        """Computed change in performance."""
        return self.W_current - self.W0

    def to_dict(self) -> Dict:
        """Convert project to dictionary for JSON serialization."""
        return {
            'project_id': self.project_id,
            'team_name': self.team_name,
            'system_name': self.system_name,
            'phenotype': self.phenotype,
            'stress_scenario': self.stress_scenario,
            'program_year': self.program_year,
            'status': self.status,
            'W0': self.W0,
            'W0_units': self.W0_units,
            'W_current': self.W_current,
            't_gen_elapsed': self.t_gen_elapsed,
            'gen_time_years': self.gen_time_years,
            'observation_start_date': self.observation_start_date,
            'observation_end_date': self.observation_end_date,
            'sample_size': self.sample_size,
            'environment': self.environment,
            'selection_method': self.selection_method,
            'target_type': self.target_type,
            'target_value': self.target_value,
            'target_date': self.target_date,
            'minimum_viable_performance': self.minimum_viable_performance,
            'dW_se': self.dW_se,
            'confidence_level': self.confidence_level,
            'ecological_value': self.ecological_value,
            'economic_value': self.economic_value,
            'urgency': self.urgency,
            'technical_feasibility': self.technical_feasibility,
            'scalability': self.scalability,
            'model_type': self.model_type,
            'plateau_performance': self.plateau_performance,
            'projection_generations': self.projection_generations,
            'last_updated': self.last_updated,
            'contact_email': self.contact_email,
            'notes': self.notes
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Project':
        """Create project from dictionary."""
        return cls(**data)


def save_project(project: Project) -> None:
    """Save a project to JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Update timestamp
    project.last_updated = datetime.now().isoformat()

    filepath = DATA_DIR / f"{project.project_id}.json"
    with open(filepath, 'w') as f:
        json.dump(project.to_dict(), f, indent=2)


def load_project(project_id: str) -> Optional[Project]:
    """Load a project from JSON file."""
    filepath = DATA_DIR / f"{project_id}.json"

    if not filepath.exists():
        return None

    with open(filepath, 'r') as f:
        data = json.load(f)

    return Project.from_dict(data)


def load_all_projects() -> List[Project]:
    """Load all projects from data directory."""
    if not DATA_DIR.exists():
        return []

    projects = []
    for filepath in DATA_DIR.glob("*.json"):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            projects.append(Project.from_dict(data))
        except Exception as e:
            print(f"Error loading {filepath}: {e}")

    return projects


def delete_project(project_id: str) -> bool:
    """Delete a project file."""
    filepath = DATA_DIR / f"{project_id}.json"

    if filepath.exists():
        filepath.unlink()
        return True

    return False


def get_projects_by_team(team_name: str) -> List[Project]:
    """Get all projects for a specific team."""
    all_projects = load_all_projects()
    return [p for p in all_projects if p.team_name == team_name]
