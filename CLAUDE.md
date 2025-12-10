Here’s a ready-to-paste brief you can give to Claude Code to build the dashboard.

---

## Brief: Adaptation Projection Dashboard

### Goal

Build a small interactive **web dashboard** (preferably in **Streamlit** or similar Python framework) that:

1. Takes simple evolutionary / performance inputs for a species/system.
2. Projects future performance under a constant improvement rate.
3. Computes **time to reach specified targets**.
4. Optionally computes a simple **impact score** based on a weighting factor and population size.
5. Visualises all this cleanly for quick decision-making.

This is for comparing things like **bacteria, bees, trees**, etc., but the dashboard should work for any one system at a time.

---

## Tech Requirements

* Use **Python**.
* Prefer **Streamlit** (or FastAPI + simple frontend if you prefer, but Streamlit is fine).
* No external services required; everything local/in-memory.

---

## Inputs (user-editable)

Create a sidebar (or clear input section) with these controls:

### Core required inputs

1. **Baseline performance** `W0` (float)

   * Description: Performance / fitness proxy at baseline under focal stress.
   * Default: `1.0`

2. **Observed change in performance** `dW` (float)

   * Description: Change in performance over the observation window (W_current – W0).
   * Default: `0.2`

3. **Observation duration (generations)** `t_gen` (float > 0)

   * Description: Number of generations observed for `dW`.
   * Default: `5`

4. **Generation time (years per generation)** `gen_time` (float > 0)

   * Description: Used to convert generations to years.
   * Default: `0.5`

5. **Target definition**

   * Option A (default): **Fold increase target**

     * Input: `target_fold` (float ≥ 1; e.g. 2.0 = 2× W0)
     * Default: `2.0`
   * Option B: **Absolute target**

     * Input: `W_target_abs` (float > W0)
   * UI: radio/select to choose “Fold target” vs “Absolute target”.

6. **Projection horizon**

   * Input: `projection_generations` (int)
   * Description: How many generations into the future to simulate.
   * Default: `50`

### Optional inputs

7. **Weighting parameter** `weight` (0–1 slider)

   * Description: Represents downstream importance of this system (dependent organisms/functions).
   * Default: `0.5`

8. **Population size** `N` (optional, float)

   * Description: Used in a simple impact index.
   * Default: `1e5` (or blank allowed)

9. **Model type** (radio/select)

   * `"additive"` or `"multiplicative"`
   * Default: `"additive"`

10. **Uncertainty (optional but nice)**

    * Standard error (or SD) of `dW`: `dW_se` (float ≥ 0, default 0)
    * If provided, use it to show an approximate uncertainty band.

---

## Core Calculations

For both model types, first compute:

```python
W_current = W0 + dW        # performance at time t_gen
rate_per_gen_add = dW / t_gen
```

### 1. Additive model

* Performance trajectory (generations):

[
W(t) = W_{\text{current}} + r \cdot \tau_g
]

where:

* `r = dW / t_gen`

* `τ_g` = 0 … `projection_generations`

* Generations → years:

[
\text{years}(t) = (t_{\text{gen}} + \tau_g) \cdot gen_time
]

* Target:

  * If fold target: `W_target = target_fold * W0`
  * If absolute target: `W_target = W_target_abs`

* Time (generations) to target:

```python
if r > 0:
    tau_to_target = max((W_target - W_current) / r, 0)
else:
    tau_to_target = np.inf
years_to_target = tau_to_target * gen_time
```

### 2. Multiplicative model (relative rate per generation)

Estimate per-generation relative growth rate:

[
r_{\text{rel}} = \frac{1}{t_{\text{gen}}} \ln\left(\frac{W_{\text{current}}}{W_0}\right)
]

* Trajectory:

[
W(t) = W_{\text{current}} \cdot e^{r_{\text{rel}} \tau_g}
]

* Time to target:

[
\tau_g = \frac{1}{r_{\text{rel}}} \ln\left(\frac{W_{\text{target}}}{W_{\text{current}}}\right)
]

Clamp negative values to 0; if `r_rel <= 0` and `W_target > W_current` then time = ∞.

### 3. Impact score (simple)

Define:

[
\text{ImpactScore} = weight \times \left(\frac{W_{\text{current}}}{W_0}\right) \times \log_{10}(N + 1)
]

* If `N` is empty, drop the log term and just do:
  `ImpactScore = weight * (W_current / W0)`.

---

## Uncertainty (basic implementation)

If `dW_se > 0`:

* Draw upper and lower trajectories for `dW ± dW_se` and plot as a shaded band.
* You can ignore its contribution to time-to-target or show a simple min/max range using those bounds.

---

## Outputs / Layout

Use a simple, clean layout:

### Top: Summary metrics

Show a small metrics panel with:

* Current performance: `W_current`
* Rate per generation: `rate_per_gen` (or `r_rel` if multiplicative)
* Rate per year: `rate_per_gen / gen_time` (or `r_rel / gen_time`)
* Years to target:

  * If finite, show with 1 decimal place.
  * If infinite, show “Not reachable with current trend”.
* Impact score (if `N` and weight given).

### Middle: Main plot – Performance vs Time

* X-axis: **years from now** (0 at “now” or `t_gen * gen_time`)
* Y-axis: **performance W**
* Components:

  * Line: projected `W(t)` over the chosen horizon.
  * Point: current state `(t_gen * gen_time, W_current)`.
  * Horizontal line: `W_target`.
  * Optional shaded band: uncertainty region.

Nice to have: annotate the point where the trajectory crosses the target, if within the horizon.

### Side / bottom: Time-to-target table

If you want multiple targets:

* Let the user specify a list of fold targets (e.g. [1.5, 2, 3]) and compute:

| Target type | Target value | Generations to target | Years to target |
| ----------- | ------------ | --------------------- | --------------- |

If time is infinite, display “∞” or “> horizon”.

---

## Code organisation

Suggested structure:

* `app.py` (Streamlit or main entry)

  * Sidebar for inputs
  * Call helper functions
  * Render metrics + plots

* `model.py`

  * `compute_projection_additive(...)`
  * `compute_projection_multiplicative(...)`
  * `compute_time_to_target(...)`
  * `compute_impact_score(...)`

* `plots.py`

  * `plot_trajectory(...)`

Keep it simple; everything can also live in `app.py` if you prefer a single file.

---

## Nice-to-have extras (only if time)

* Allow saving a configuration to JSON and reloading.
* Allow comparing **two systems** side-by-side with duplicated inputs and two curves on the same plot.
* Switch for log-scale y-axis.

---

### Deliverable

A runnable Python app (ideally Streamlit) that I can start via something like:

```bash
streamlit run app.py
```

and then use the UI to:

* enter W0, dW, t_gen, gen_time, targets, weight, N
* see the projection plot
* read off years to target
* see an impact score.

---

That’s the full brief — please implement this dashboard end-to-end.
