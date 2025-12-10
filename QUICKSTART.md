# Quick Start Guide

## Installation

1. **Set up the virtual environment** (already done):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Load example data** (already done):
   ```bash
   python create_example_data.py
   ```

## Running the Dashboard

### Option 1: Using the startup script
```bash
./run_dashboard.sh
```

### Option 2: Manual activation
```bash
source venv/bin/activate
streamlit run app.py
```

The dashboard will open in your browser at `http://localhost:8501`

## Example Projects Included

We've created 5 example projects to demonstrate the dashboard:

1. **Oxford Marine Lab** - Coral heat tolerance
   - Status: On track
   - Quality: High (4★)
   - Shows strong adaptation trajectory

2. **Rothamsted Research** - Wheat drought tolerance
   - Status: Behind track
   - Quality: Moderate (3★)
   - Slower progress than expected

3. **UC Davis** - Honeybee heat tolerance
   - Status: Early stage
   - Quality: Preliminary (2★)
   - Needs more data

4. **CSIRO Forestry** - Eucalyptus fire resistance
   - Status: On track
   - Quality: High (5★)
   - Uses multiplicative model

5. **IRRI Philippines** - Rice salt tolerance
   - Status: On track
   - Quality: High (4★)
   - Uses logistic (plateau) model

## Testing the Dashboard

1. **Enter a team name**: Try "Oxford Marine Lab"
2. **Select a project**: Choose "Coral (Acropora millepora) - Heat tolerance (LT50)"
3. **Explore the dashboard**:
   - View current status and metrics
   - See the trajectory projection
   - Review data quality warnings
   - Check impact score breakdown
4. **Edit the project**: Try changing parameters in the "Edit Project Data" section
5. **Create a new project**: Select "➕ Create New Project" and add your own data

## Key Features to Test

- ✅ Traffic light status (green/yellow/red)
- ✅ Data quality stars (1-5)
- ✅ Interactive trajectory plot with uncertainty bands
- ✅ Time-to-target calculations
- ✅ Impact score breakdown
- ✅ Warnings and recommendations
- ✅ Multiple model types (additive, multiplicative, logistic)

## Troubleshooting

**Dashboard won't start?**
- Make sure you activated the virtual environment: `source venv/bin/activate`
- Check Python version: `python --version` (needs 3.8+)

**No projects showing up?**
- Run `python create_example_data.py` to generate example data
- Check that `data/projects/` contains JSON files

**Plot not displaying?**
- Check console for errors
- Ensure all required packages are installed
- Try refreshing the browser

## Next Steps

- Create your own projects with real data
- Experiment with different model types
- Compare how parameters affect projections
- Test the data quality scoring with different sample sizes

## Getting Help

For issues or questions:
1. Check the main README.md for detailed documentation
2. Review the SPECIFICATION.md for feature details
3. Contact your ARIA program manager
