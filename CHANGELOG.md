# Changelog

## Version 2.0.0 - Phase 2 Complete (December 2024)

### New Features

#### Portfolio Interface for ARIA Managers
- **Multi-project dashboard** with summary metrics (total, on track, behind, at risk)
- **Sortable comparison table** with filtering by status, quality, and team
- **Normalized progress visualization** showing all projects on same 0-100% scale
- **Risk matrix** plotting impact vs timeline for prioritization
- **Distribution plots** for impact scores, quality, and adaptation rates
- **CSV export** functionality for portfolio data
- **Color-coded status indicators** throughout interface

#### UI/UX Improvements
- ✅ **Fixed:** Removed broken placeholder image in sidebar (replaced with emoji)
- ✅ **Fixed:** White text on white background in metrics (added CSS overrides)
- ✅ **Added:** Comprehensive FAQ section in sidebar with:
  - Model selection guide (when to use additive/multiplicative/logistic)
  - Data quality criteria explanation
  - Status indicator meanings
  - Impact score component breakdown

#### Interface Selection
- Radio button in sidebar to switch between Contributor and Portfolio views
- Context-appropriate descriptions for each interface
- Single app supporting both user types

### Technical Improvements
- Created `portfolio_view.py` with full analytics suite
- Enhanced CSS for better text visibility
- Improved sidebar organization and help system
- Updated all documentation to reflect Phase 2 features

---

## Version 1.0.0 - Phase 1 (December 2024)

### Initial Release - Contributor Interface

#### Core Features
- Project data entry and management
- Three projection models (additive, multiplicative, logistic)
- Time-to-target calculations with uncertainty
- Data quality scoring (0-5 stars)
- Impact assessment (0-10 scale)
- Interactive trajectory plots with confidence intervals
- Automated warnings and recommendations

#### Data Model
- JSON-based storage system
- Comprehensive project metadata
- Experimental context tracking
- Impact assessment dimensions

#### Visualizations
- Performance trajectory plots
- Progress gauges
- Impact score breakdowns
- Uncertainty bands

---

## Features Summary

### For Research Teams (Contributor Interface)
✅ Create and manage projects
✅ Track baseline → current → target performance
✅ Three projection models with model selection guidance
✅ Uncertainty quantification
✅ Data quality feedback
✅ Impact scoring
✅ Actionable warnings

### For ARIA Managers (Portfolio Interface)
✅ View all projects across teams
✅ Compare project performance
✅ Filter and sort by multiple criteria
✅ Risk-based prioritization
✅ Analytics and reporting
✅ Export capabilities

---

## Bug Fixes

### Version 2.0.0
- Fixed broken image link in sidebar
- Fixed metric text visibility (white on white)
- Added missing model selection guidance

---

## Known Limitations

- No user authentication (file-based access control)
- Single-user concurrent editing may cause conflicts
- No historical tracking of predictions vs actuals yet
- No automated alerts system yet

See SPECIFICATION.md Phase 3 for planned future enhancements.
