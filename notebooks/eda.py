import os
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def run_eda():
    data_dir = r"c:\dev\personal-project\dacon-mosquito-flight\data\train"
    out_dir = r"C:\Users\USER\.gemini\antigravity\brain\761d9594-0bf1-4265-9a1a-82e5ac9d0010"

    print("Loading data...")
    files = glob.glob(os.path.join(data_dir, "*.csv"))
    if not files:
        print("Error: No training data found.")
        return
        
    np.random.seed(42)
    sample_files = np.random.choice(files, size=5, replace=False)

    # 1. Plot 3D Path
    print("Generating 3D Path plot...")
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    for f in sample_files:
        df = pd.read_csv(f)
        sc = ax.scatter(df['x'], df['y'], df['z'], c=df['timestep_ms'], cmap='viridis', s=50, alpha=0.8)
        ax.plot(df['x'], df['y'], df['z'], alpha=0.5)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title("3D Mosquito Flight Trajectories")
    fig.colorbar(sc, label='Timestep (ms)')
    plt.savefig(os.path.join(out_dir, "eda_3d_path.png"))
    plt.close()

    # 2. Plot Time-Series
    print("Generating Time-Series plot...")
    df_single = pd.read_csv(sample_files[0])
    fig, axes = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
    axes[0].plot(df_single['timestep_ms'], df_single['x'], marker='o', color='r')
    axes[0].set_ylabel('X Coordinate')
    axes[1].plot(df_single['timestep_ms'], df_single['y'], marker='o', color='g')
    axes[1].set_ylabel('Y Coordinate')
    axes[2].plot(df_single['timestep_ms'], df_single['z'], marker='o', color='b')
    axes[2].set_ylabel('Z Coordinate')
    axes[2].set_xlabel('Timestep (ms)')
    plt.suptitle("Time-Series Coordinates (Single Sample)")
    plt.savefig(os.path.join(out_dir, "eda_time_series.png"))
    plt.close()

    # 3. Velocity Analysis
    print("Generating Velocity Distribution plot...")
    all_velocities = []
    # Sample 500 for velocity distribution
    for f in np.random.choice(files, size=min(500, len(files)), replace=False):
        df = pd.read_csv(f)
        coords = df[['x', 'y', 'z']].values
        dt = np.diff(df['timestep_ms'].values)
        dt = np.where(dt == 0, 1e-6, dt)
        dp = np.diff(coords, axis=0)
        dist = np.linalg.norm(dp, axis=1)
        vel = dist / np.abs(dt)
        all_velocities.extend(vel)

    plt.figure(figsize=(10, 6))
    sns.histplot(all_velocities, bins=50, kde=True, color='purple')
    plt.xlabel("Velocity (Distance / ms)")
    plt.ylabel("Frequency")
    plt.title("Velocity Distribution (500 Sampled Trajectories)")
    plt.savefig(os.path.join(out_dir, "eda_velocity.png"))
    plt.close()

    print("EDA plots generated successfully.")

if __name__ == "__main__":
    run_eda()
