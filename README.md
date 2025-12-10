# Adaptation Dashboard

A web-based dashboard for tracking and comparing adaptation acceleration projects across multiple research teams.

## Overview

This dashboard helps program managers and research teams monitor progress in accelerating species/system adaptation to future environmental conditions. It provides:

- **Transparent projections** of adaptation trajectories
- **Data quality assessment** to build confidence in estimates
- **Actionable metrics** including time-to-target and impact scores
- **Species/system agnostic** framework - works for any organism or phenotype

## Features

### Phase 2 - Two Interfaces

#### Contributor Interface (For Research Teams)

- ✅ Track adaptation progress for your projects
- ✅ Input baseline and current performance data
- ✅ View projections with uncertainty bands
- ✅ Get data quality feedback and recommendations
- ✅ Multiple projection models (additive, multiplicative, logistic)
- ✅ Automated warnings for small sample sizes, short observation periods, etc.
- ✅ Impact score calculation based on ecological, economic, and urgency factors
- ✅ Built-in FAQ and model selection guide

#### Portfolio Interface (For Program Managers)

- ✅ View all projects across teams in one dashboard
- ✅ Portfolio summary metrics (total, on track, behind, at risk)
- ✅ Sortable and filterable project comparison table
- ✅ Multi-project visualization on normalized progress scale
- ✅ Risk matrix: Impact vs Timeline quadrant analysis
- ✅ Distribution plots for key metrics
- ✅ Export portfolio data to CSV
- ✅ Color-coded status indicators

## Installation

### Requirements

- Python 3.8 or higher
- pip

### Setup

1. Clone or download this repository

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the Dashboard

Start the Streamlit app:

```bash
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Quick Start Guide

### For Contributors (Research Teams)

1. **Enter your team name** when prompted
2. **Create a new project**:
   - System/species (e.g., "Coral - Acropora millepora")
   - Phenotype being measured (e.g., "Heat tolerance LT50")
   - Baseline performance (W₀)
   - Current performance after selection
   - Generations observed
   - Target performance and target year
3. **Review your dashboard**:
   - Current status (on track / behind / at risk)
   - Data quality score
   - Projected trajectory
   - Warnings and recommendations
4. **Update data** as your experiment progresses

## Data Storage

Projects are stored as JSON files in `data/projects/`. Each project has a unique ID and contains all metadata, performance data, and settings.

To backup your data, simply copy the `data/projects/` directory.

## Project Structure

```
adaptation_dash/
├── app.py                    # Main Streamlit app with routing
├── contributor_view.py       # Contributor interface (teams)
├── portfolio_view.py         # Portfolio interface (program managers)
├── models.py                 # Projection calculations (3 model types)
├── impact.py                 # Impact scoring system
├── data_quality.py           # Data quality assessment
├── plots.py                  # Visualization functions
├── storage.py                # Data persistence (JSON)
├── create_example_data.py    # Generate test projects
├── run_dashboard.sh          # Startup script
├── requirements.txt          # Python dependencies
├── QUICKSTART.md             # Quick start guide
├── SPECIFICATION.md          # Detailed specification
├── data/
│   └── projects/            # JSON project files
└── README.md                # This file
```

## Model Types

### Additive (Linear)
- Assumes constant rate of improvement per generation
- Best for: Early-stage experiments, simple linear trends
- Formula: `W(t) = W_current + r × generations`

### Multiplicative (Exponential)
- Assumes constant relative growth rate
- Best for: Exponential improvement patterns
- Formula: `W(t) = W_current × exp(r × generations)`

### Logistic (Plateau)
- Assumes improvement approaches a genetic limit
- Best for: Systems with known constraints
- Formula: `W(t) = W_max - (W_max - W_current) × exp(-r × generations)`

## Data Quality Scoring

Projects receive a quality score (0-5 stars) based on:

- ✓ Sample size ≥ 100 individuals (+1)
- ✓ Generations observed ≥ 5 (+1)
- ✓ Field or mixed environment (+1)
- ✓ Standard error provided (+1)
- ✓ Replicated measurements (+1)

## Impact Scoring

Impact scores (0-10) are calculated from:

- Ecological value (25%)
- Economic value (25%)
- Urgency (20%)
- Timeline (15% - sooner is higher)
- Scalability (10%)
- Technical feasibility (5%)

## Quick Start

### Using the Dashboard

1. **Start the app**: Run `./run_dashboard.sh` or `streamlit run app.py`
2. **Select interface** in the sidebar:
   - **👥 Contributor View**: For research teams
   - **📊 Portfolio View**: For program managers
3. **Explore example data**: 5 example projects are pre-loaded

### Contributor Workflow

1. Enter your team name
2. Select an existing project or create new
3. Fill in performance data
4. Review trajectory and recommendations
5. Update as your experiment progresses

### Portfolio Workflow

1. View summary dashboard
2. Filter/sort projects by status, quality, team
3. Analyze risk matrix for prioritization
4. Export data for reporting

## Roadmap

### ✅ Phase 1: Contributor Interface (Complete)
- Single-project tracking and data entry
- Three projection models
- Data quality scoring
- Impact assessment

### ✅ Phase 2: Portfolio Interface (Complete)
- Multi-project comparison table
- Portfolio analytics and visualizations
- Risk matrix (impact vs timeline)
- Filtering and sorting
- CSV export for all projects

### Phase 3: Advanced Features (Future)
- Historical tracking (predictions vs actuals)
- Automated alerts when projects fall behind
- User authentication and permissions
- Advanced uncertainty quantification
- API for programmatic access

## Contributing

This is an open-source tool. For questions or feature requests, please open an issue on GitHub.

## License

MIT License - See LICENSE file for details

## Support

For technical support or questions about using the dashboard, please open an issue on GitHub or contact your program manager.

---

**Version:** 2.0.0 (Phase 2)
**Last Updated:** December 2024
