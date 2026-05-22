# 3D Trajectory EDA Pipeline

> A systematic workflow for visualizing and analyzing mosquito flight paths.

---

## 1. Definition & Role
- **Visualization:** Generates 3D plots (`matplotlib` or `plotly`) of individual mosquito flight trajectories over time.
- **Statistical Analysis:** Extracts and plots distributions of velocity, acceleration, and movement bounding boxes to understand mosquito behavioral patterns.

## 2. Execution Pipeline
1. **Load Sample:** Select a random subset of `TRAIN_XXXXX.csv` files.
2. **Plot 3D Path:** 
   - X, Y, Z axes for physical space.
   - Use color gradients (e.g., light to dark) to represent time (`timestep_ms` from -400 to 0).
3. **Plot Time-Series:** 
   - 3 separate 2D line plots for X(t), Y(t), Z(t).
4. **Velocity Analysis:** 
   - Calculate Euclidean distance between timesteps and plot the velocity distribution.
5. **Output:** Save visualizations to `notebooks/` or display inline if in a Jupyter environment.

## 3. Constraints
- **Library Choice:** Prefer `matplotlib` for static reports, `plotly` for interactive Colab notebooks.
- **Performance:** Do not attempt to plot all 10,000+ trajectories at once. Always sample (n=10 ~ n=100) for visual clarity and memory safety.
