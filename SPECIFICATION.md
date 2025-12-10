# ARIA Adaptation Dashboard - Revised Specification

## Overview

A two-tiered dashboard system for tracking and comparing adaptation acceleration projects across multiple research teams.

**Two interfaces:**
1. **Contributor Interface**: Individual teams view and update their own project(s)
2. **ARIA Portfolio Interface**: Program managers view all projects, compare performance, make funding decisions

**Core principle**: Transparent, actionable, comparable metrics for adaptation progress.

---

## Architecture

### Data Model

Each **project** contains:

#### Core Identity
- `project_id`: Unique identifier
- `team_name`: Research team/institution
- `system_name`: Species/organism (e.g., "Coral (Acropora millepora)")
- `phenotype`: What's being adapted (e.g., "Heat tolerance (LT50)")
- `stress_scenario`: Future condition target (e.g., "RCP 8.5, 2050 ocean temps")
- `program_year`: Year project started
- `status`: Active / Paused / Completed / Discontinued

#### Performance Data
- `W0`: Baseline performance (float)
- `W0_units`: Units of measurement (e.g., "°C", "% survival", "yield kg/ha")
- `W_current`: Current performance (float)
- `dW`: Change from baseline (`W_current - W0`)
- `t_gen_elapsed`: Generations observed (float)
- `gen_time_years`: Years per generation (float)

#### Experimental Context (NEW)
- `observation_start_date`: When measurements began
- `observation_end_date`: Most recent measurement
- `sample_size`: Number of individuals/replicates
- `environment`: "Lab" / "Greenhouse" / "Field" / "Mixed"
- `selection_method`: "Artificial" / "Natural" / "Assisted gene flow" / "Other"
- `data_quality_score`: 0-5 rating (see scoring rubric below)

#### Targets
- `target_type`: "Fold increase" / "Absolute value" / "Scenario threshold"
- `target_value`: Numeric target
- `target_date`: Year by which target should be achieved
- `minimum_viable_performance`: Lowest acceptable W for success

#### Uncertainty
- `dW_se`: Standard error of performance change
- `confidence_level`: 0.8, 0.9, 0.95 (for CI calculations)

#### Impact Assessment (NEW - structured)
- `ecological_value`: 0-10 (biodiversity / ecosystem function importance)
- `economic_value`: 0-10 (agriculture / fisheries / forestry value)
- `urgency`: 0-10 (how soon is adaptation needed?)
- `technical_feasibility`: 0-10 (tractability of intervention)
- `scalability`: 0-10 (can solution be deployed widely?)

#### Model Parameters
- `model_type`: "additive" / "multiplicative" / "logistic" (NEW)
- `plateau_performance`: Optional max achievable W (for logistic)
- `projection_generations`: How far to project (int)

#### Metadata
- `last_updated`: Timestamp
- `contact_email`: Team lead
- `notes`: Free text

---

## Data Quality Scoring Rubric

**Automated score (0-5)** based on:

| Criterion | Points |
|-----------|--------|
| Sample size ≥ 100 individuals | +1 |
| Generations observed ≥ 5 | +1 |
| Field or mixed environment (vs lab only) | +1 |
| Standard error provided | +1 |
| Multiple independent measurements of W | +1 |

Display as stars (★★★★★) or traffic light thresholds:
- 4-5: Green (high confidence)
- 2-3: Yellow (moderate confidence)
- 0-1: Red (preliminary data)

---

## Contributor Interface

### Layout

```
┌─────────────────────────────────────────────────────────┐
│  ARIA Adaptation Tracker - [Team Name]                 │
├─────────────────────────────────────────────────────────┤
│  Your Projects: [Project Dropdown ▼] [+ New Project]   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  PROJECT: Coral Heat Tolerance                          │
│  Status: ● Active    Data Quality: ★★★★☆               │
│                                                          │
│  ┌─────────────────┐  ┌──────────────────────────────┐ │
│  │ CURRENT STATUS  │  │ TRAJECTORY                    │ │
│  │                 │  │                               │ │
│  │ Baseline: 28.5°C│  │  [Performance vs Time Plot]  │ │
│  │ Current:  30.2°C│  │                               │ │
│  │ Target:   33.0°C│  │  Shows:                       │ │
│  │                 │  │  - Observed data points       │ │
│  │ Progress: 47%   │  │  - Projection with CI         │ │
│  │                 │  │  - Target line & date         │ │
│  │ Rate: 0.34°C/gen│  │  - Current position           │ │
│  │       0.68°C/yr │  │                               │ │
│  │                 │  │                               │ │
│  │ Est. arrival:   │  │                               │ │
│  │  2028 (4.5 yr)  │  │                               │ │
│  │  ±1.2 yr        │  │                               │ │
│  └─────────────────┘  └──────────────────────────────┘ │
│                                                          │
│  STATUS: ✓ On track                                     │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ UPDATE DATA                                        │ │
│  │ [Collapsible form for editing all parameters]     │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ DIAGNOSTICS & WARNINGS                             │ │
│  │                                                     │ │
│  │ ⚠ Small sample size (n=45) - consider increasing  │ │
│  │ ℹ Approaching 10 generations - time to reassess    │ │
│  │   rate assumptions                                 │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Features

1. **Simple data entry form** with:
   - Tooltips explaining each field
   - Validation (e.g., W_current > W0 for positive adaptation)
   - Auto-calculation of derived values (dW, rates)

2. **Visual feedback**:
   - Clear "on track / behind / ahead" status
   - Confidence intervals on all projections
   - Data quality score prominent

3. **Download options**:
   - Export project data as JSON
   - Generate report PDF

4. **Version history**:
   - Show past updates
   - Plot historical projections vs actual performance

---

## ARIA Portfolio Interface

### Layout

```
┌──────────────────────────────────────────────────────────────┐
│  ARIA Portfolio Dashboard                        [Filters ▼] │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  PORTFOLIO SUMMARY                                           │
│  ┌────────┬────────┬────────┬────────┐                      │
│  │ Total  │ On     │ Behind │ At     │                      │
│  │ Active │ Track  │ Track  │ Risk   │                      │
│  │   24   │   15   │   6    │   3    │                      │
│  └────────┴────────┴────────┴────────┘                      │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│  PROJECT COMPARISON TABLE                [Export CSV]        │
├──────────────────────────────────────────────────────────────┤
│Team    │System    │Phenotype  │Status│Quality│Impact│Years  │
│        │          │           │      │       │Score │to Tgt │
├────────┼──────────┼───────────┼──────┼───────┼──────┼───────┤
│Oxford  │Coral     │Heat tol   │ ✓    │★★★★☆ │ 8.2  │ 4.5   │
│Rotham  │Wheat     │Drought    │ ⚠    │★★★☆☆ │ 9.1  │ 7.2   │
│CSIRO   │Eucalypt  │Fire res   │ ✓    │★★★★★ │ 7.5  │ 3.1   │
│...     │...       │...        │...   │...    │...   │...    │
│                                                               │
│  [Sort by: Impact ▼] [Filter: Behind track] [Search...]     │
└──────────────────────────────────────────────────────────────┘
│                                                               │
│  SELECTED PROJECT DETAIL: [Project from table above]        │
│  [Same view as Contributor interface, read-only]            │
│                                                               │
├──────────────────────────────────────────────────────────────┤
│  PORTFOLIO ANALYTICS                                         │
│                                                               │
│  [Multi-project comparison plot]                             │
│   - All projects overlaid (normalized to % of target)        │
│   - Color-coded by status                                    │
│   - Size indicates impact score                              │
│                                                               │
│  [Risk matrix: Impact vs Timeline Risk]                      │
│   - Quadrant plot: high/low impact × on/off track           │
│   - Identify projects needing attention                      │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

### Key Features

#### 1. **Sortable/Filterable Project Table**
- Click column headers to sort
- Filter by:
  - Status (on/behind/at risk)
  - System type
  - Data quality
  - Program year
  - Target date range

#### 2. **Impact Score Calculation**

Composite score (0-10):

```
Impact = 0.25 × ecological_value
       + 0.25 × economic_value
       + 0.20 × urgency
       + 0.15 × (1 / years_to_target)  # sooner = higher
       + 0.10 × scalability
       + 0.05 × technical_feasibility
```

Displayed with breakdown on hover/click.

#### 3. **Traffic Light Status Logic**

```
IF current_rate <= 0:
    status = "At Risk" (RED)
ELIF years_to_target_upper_CI > target_date - current_year:
    status = "Behind Track" (YELLOW)
ELIF data_quality_score < 2:
    status = "Needs Validation" (ORANGE)
ELSE:
    status = "On Track" (GREEN)
```

#### 4. **Portfolio Visualizations**

**A. Normalized Progress Chart**
- X-axis: Time (years from now)
- Y-axis: % progress to target (0-100%)
- Each project is a line
- Hover to see project name
- Vertical line at key policy dates (e.g., 2030, 2050)

**B. Impact vs Timeline Quadrant**
- X-axis: Years to target
- Y-axis: Impact score
- Quadrants:
  - **Top-left** (high impact, soon): "Strategic priorities"
  - **Top-right** (high impact, far): "Long-term investments"
  - **Bottom-left** (low impact, soon): "Quick wins"
  - **Bottom-right** (low impact, far): "Deprioritize?"

**C. Rate Distribution**
- Histogram of adaptation rates across all projects
- Identify outliers (very fast = suspicious? very slow = underfunded?)

#### 5. **Export & Reporting**
- Download full portfolio data as CSV/Excel
- Generate executive summary PDF
- API endpoint for programmatic access

---

## Model Enhancements

### 1. Logistic (Plateau) Model (NEW)

For systems with genetic constraints:

```
W(t) = W_max - (W_max - W_current) × exp(-r × τ)
```

Where:
- `W_max` = plateau performance (user-specified or estimated)
- `r` = growth rate
- `τ` = generations forward

**When to use**:
- Standing genetic variation is limited
- Trait has known physiological maximum
- Data shows decelerating improvement

### 2. Uncertainty Propagation

For **time-to-target**, compute confidence interval:

```
rate_lower = (dW - dW_se * z_score) / t_gen
rate_upper = (dW + dW_se * z_score) / t_gen

years_to_target_lower = (W_target - W_current) / rate_upper
years_to_target_upper = (W_target - W_current) / rate_lower
```

Where `z_score` = 1.645 (90% CI), 1.96 (95% CI), etc.

Display as: **"4.5 years (95% CI: 3.3 - 6.8)"**

### 3. Multi-Target Support

Allow projects to specify:
- `minimum_viable`: Lowest acceptable performance
- `target_sufficient`: Main program goal
- `target_stretch`: Aspirational goal

Show all three on trajectory plot.

---

## Data Storage

### Option A: SQLite (Recommended for MVP)

Simple local database:
- `projects` table with all fields above
- `history` table logging all updates (for audit trail)
- No authentication needed initially (file-based access control)

### Option B: JSON Files

For simplicity:
- Each project = 1 JSON file
- Directory structure:
  ```
  data/
    projects/
      project_001.json
      project_002.json
      ...
    portfolio_config.json
  ```

---

## Implementation Phases

### Phase 1: Core Contributor Interface (MVP)
- Single-project data entry form
- Additive & multiplicative models
- Basic trajectory plot
- Time-to-target calculation
- Data quality scoring
- Local JSON storage

**Deliverable**: Teams can track their own project

### Phase 2: Portfolio Interface
- Multi-project table
- Impact scoring
- Comparison visualizations
- CSV import/export
- SQLite backend

**Deliverable**: ARIA can view all projects

### Phase 3: Advanced Features
- Logistic model
- Proper uncertainty quantification
- Historical tracking (predictions vs actuals)
- Automated alerts/warnings
- User authentication (if needed)

---

## User Workflows

### Workflow 1: Team Updates Progress

1. Open dashboard, select their project
2. Enter new performance measurement (`W_current`, `t_gen`)
3. Dashboard auto-updates:
   - Rate calculation
   - Projection
   - Time-to-target
   - Status (on/behind track)
4. Team reviews warnings (e.g., "sample size low")
5. Submit update
6. Download report for their records

### Workflow 2: ARIA Quarterly Review

1. Open portfolio interface
2. Filter for projects with `target_date <= 2030`
3. Sort by Impact score (descending)
4. Review "Behind Track" projects:
   - Check data quality - is delay real or measurement issue?
   - Review experimental design
   - Note for follow-up call
5. Generate executive summary PDF for stakeholders
6. Export data for further analysis in R/Python

### Workflow 3: New Project Onboarding

1. Team clicks "+ New Project"
2. Fills baseline form:
   - System, phenotype, target, etc.
   - Initial `W0` measurement
3. Dashboard flags if similar projects exist (avoid duplication)
4. Project created with status "Pending first update"
5. ARIA admin reviews and approves (optional gate)

---

## Technical Stack (Streamlit Implementation)

### Structure

```
adaptation_dash/
  app.py                 # Main entry - route to contributor/portfolio view
  contributor_view.py    # Single-project interface
  portfolio_view.py      # Multi-project interface
  models.py              # Projection calculations
  impact.py              # Impact score logic
  data_quality.py        # Scoring & validation
  plots.py               # Visualization functions
  storage.py             # Load/save projects (JSON or SQLite)
  utils.py               # Shared utilities
  data/
    projects/            # JSON files or SQLite DB
  tests/                 # Unit tests
  requirements.txt
  README.md
```

### Key Libraries

- `streamlit` - UI framework
- `pandas` - Data handling
- `numpy` - Calculations
- `plotly` or `altair` - Interactive plots
- `scipy` - Statistics (confidence intervals)
- `sqlite3` (stdlib) - Database (if not using JSON)

---

## UI/UX Principles

1. **Progressive disclosure**: Don't overwhelm with all fields at once - collapsible sections
2. **Validation & guidance**: Red/yellow/green indicators, helpful error messages
3. **Consistency**: Same metrics displayed identically in both interfaces
4. **Accessibility**: Color-blind safe palette, text alternatives for visual indicators
5. **Export-first**: Every view can be downloaded/shared

---

## Open Questions for Discussion

1. **Authentication**: Should teams log in, or is file-based access control sufficient?
2. **Impact weights**: Should ARIA be able to adjust the impact formula weights?
3. **Targets**: Should ARIA set standardized targets, or do teams define their own?
4. **Update frequency**: How often should teams update data? Should there be reminders?
5. **Confidence intervals**: 90% or 95% as default?
6. **Model selection**: Should dashboard recommend which model to use based on data, or leave to users?

---

## Success Metrics

Dashboard is successful if:

1. **Adoption**: ≥80% of funded teams use it quarterly
2. **Decision support**: ARIA references it in ≥50% of funding review meetings
3. **Transparency**: External reviewers rate data quality/auditability ≥4/5
4. **Time savings**: Reduces reporting overhead by ≥30% vs manual Excel tracking

---

## Next Steps

1. Review & refine this spec with ARIA stakeholders
2. Prioritize Phase 1 features
3. Create mockups for both interfaces
4. Build MVP contributor interface
5. Pilot with 3-5 teams
6. Iterate based on feedback
7. Roll out portfolio interface

---

**END OF SPECIFICATION**
