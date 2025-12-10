"""
Create example projects for testing the dashboard.
"""

from storage import Project, save_project
from datetime import datetime

# Example 1: Coral heat tolerance (on track, high quality)
coral_project = Project(
    team_name="Oxford Marine Lab",
    system_name="Coral (Acropora millepora)",
    phenotype="Heat tolerance (LT50)",
    stress_scenario="RCP 8.5, 2050 ocean temps (+2°C)",
    program_year=2022,
    status="Active",
    W0=28.5,
    W0_units="°C",
    W_current=30.2,
    t_gen_elapsed=5.0,
    gen_time_years=0.5,
    observation_start_date="2022-06-01",
    observation_end_date="2024-12-01",
    sample_size=150,
    environment="Mixed",
    selection_method="Artificial",
    target_type="Absolute value",
    target_value=33.0,
    target_date=2030,
    dW_se=0.15,
    ecological_value=9.0,
    economic_value=7.5,
    urgency=9.0,
    technical_feasibility=6.5,
    scalability=7.0,
    model_type="additive",
    projection_generations=40,
    contact_email="coral.team@oxford.ac.uk",
    notes="Strong response to selection. Field trials showing promising heat tolerance transfer."
)

# Example 2: Wheat drought tolerance (behind track, moderate quality)
wheat_project = Project(
    team_name="Rothamsted Research",
    system_name="Winter Wheat (Triticum aestivum)",
    phenotype="Drought tolerance (yield under stress)",
    stress_scenario="30% reduction in growing season rainfall",
    program_year=2021,
    status="Active",
    W0=3.5,
    W0_units="tonnes/hectare",
    W_current=3.9,
    t_gen_elapsed=3.0,
    gen_time_years=1.0,
    observation_start_date="2021-09-01",
    observation_end_date="2024-09-01",
    sample_size=80,
    environment="Field",
    selection_method="Artificial",
    target_type="Fold increase",
    target_value=1.5,
    target_date=2032,
    dW_se=0.08,
    ecological_value=4.0,
    economic_value=10.0,
    urgency=8.0,
    technical_feasibility=7.5,
    scalability=9.5,
    model_type="additive",
    projection_generations=20,
    contact_email="wheat@rothamsted.ac.uk",
    notes="Slower progress than expected. May need to broaden genetic base."
)

# Example 3: Honeybee heat tolerance (early stage, low quality data)
bee_project = Project(
    team_name="UC Davis Pollinator Lab",
    system_name="Honeybee (Apis mellifera)",
    phenotype="Brood survival at high temperature",
    stress_scenario="+5°C summer peak temperatures",
    program_year=2023,
    status="Active",
    W0=65.0,
    W0_units="% survival",
    W_current=71.0,
    t_gen_elapsed=2.0,
    gen_time_years=0.25,
    observation_start_date="2023-04-01",
    observation_end_date="2024-10-01",
    sample_size=25,
    environment="Lab",
    selection_method="Artificial",
    target_type="Absolute value",
    target_value=85.0,
    target_date=2028,
    dW_se=0.0,
    ecological_value=8.5,
    economic_value=8.0,
    urgency=7.5,
    technical_feasibility=5.0,
    scalability=6.0,
    model_type="additive",
    projection_generations=30,
    contact_email="bees@ucdavis.edu",
    notes="Preliminary data. Need to increase colony replicates and add field validation."
)

# Example 4: Eucalyptus fire resistance (multiplicative model)
eucalypt_project = Project(
    team_name="CSIRO Forestry",
    system_name="Eucalyptus (E. grandis)",
    phenotype="Fire resistance (bark thickness)",
    stress_scenario="Increased wildfire frequency & intensity",
    program_year=2020,
    status="Active",
    W0=12.0,
    W0_units="mm",
    W_current=15.8,
    t_gen_elapsed=4.0,
    gen_time_years=2.5,
    observation_start_date="2020-01-01",
    observation_end_date="2024-06-01",
    sample_size=200,
    environment="Field",
    selection_method="Natural",
    target_type="Fold increase",
    target_value=2.0,
    target_date=2035,
    dW_se=0.4,
    ecological_value=8.0,
    economic_value=7.0,
    urgency=6.5,
    technical_feasibility=8.0,
    scalability=8.5,
    model_type="multiplicative",
    projection_generations=15,
    contact_email="eucalypt@csiro.au",
    notes="Natural selection in fire-prone areas showing strong response. Good heritability."
)

# Example 5: Rice salt tolerance (logistic model)
rice_project = Project(
    team_name="IRRI Philippines",
    system_name="Rice (Oryza sativa)",
    phenotype="Salt tolerance (yield at 8 dS/m)",
    stress_scenario="Coastal salinization (sea level rise)",
    program_year=2021,
    status="Active",
    W0=2.1,
    W0_units="tonnes/hectare",
    W_current=3.2,
    t_gen_elapsed=6.0,
    gen_time_years=0.5,
    observation_start_date="2021-01-15",
    observation_end_date="2024-11-01",
    sample_size=120,
    environment="Field",
    selection_method="Artificial",
    target_type="Absolute value",
    target_value=4.5,
    target_date=2029,
    dW_se=0.12,
    ecological_value=6.0,
    economic_value=9.5,
    urgency=9.5,
    technical_feasibility=7.0,
    scalability=9.0,
    model_type="logistic",
    plateau_performance=5.0,
    projection_generations=25,
    contact_email="rice@irri.org",
    notes="Approaching physiological limits. May need to incorporate new germplasm."
)

# Save all example projects
projects = [coral_project, wheat_project, bee_project, eucalypt_project, rice_project]

for project in projects:
    save_project(project)
    print(f"Created: {project.system_name} - {project.phenotype}")

print(f"\n✅ Created {len(projects)} example projects!")
print("Run 'streamlit run app.py' to view them in the dashboard.")
