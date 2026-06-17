import pandas as pd
import numpy as np
import os
from scipy.interpolate import griddata

# ==============================================================================
# 1. USER INPUTS & PARAMETERS
# ==============================================================================
file_dir = r"D:\PhD\Phase 01\Manuscripts\1st\Rev00_2nd proposal\Python trail\D=0.9_L=22.5"
file_name = "D0.9_22.5.csv"  # Assuming the export is a CSV
full_path = os.path.join(file_dir, file_name)

# Grid parameters from your methodology documents:
M = 51   # User Input: Total number of regular vertical points along the pile length
N = 180  # User Input: Total number of points along the half-circumference (0 to pi)

# Physical Dimensions
D = 0.91  # Pile diameter (m)
R = D / 2
L = 22.5  # Pile Length (m)

# ==============================================================================
# 2. DATA LOADING & CLEANING
# ==============================================================================
df = pd.read_csv(full_path)

# Remove identical points based on coordinates
df = df.drop_duplicates(subset=['X', 'Y', 'Z'], keep='first')

# Physical Filtering: Remove positive normal stress (Tension/Suction)
df = df[df['sigma_N'] <= 0]

# Coordinate Transformation (Calculate angle around the pile)
df['theta_rad'] = np.arctan2(df['Y'], df['X'])

# ==============================================================================
# 3. GRID GENERATION & MATHEMATICAL INTEGRATION
# ==============================================================================
# Calculate regular vertical spacing based on Image 3: delta_z = L / (M - 1)
delta_z = L / (M - 1)

# Define the regular circumferential grid from 0 to pi with N points
theta_grid = np.linspace(0, np.pi, N)

# Identify unique depth slices present in your raw data
unique_depths = sorted(df['Z'].unique())

results = []

for depth in unique_depths:
    group = df[df['Z'] == depth]
    
    # Ensure there is enough data at this specific depth slice to interpolate
    if len(group) < 4: 
        continue
        
    # Perform linear interpolation using Scipy's griddata (Image 4)
    # This maps the irregular FEM nodes onto your predefined regular theta_grid
    sigma_N_interp = griddata(group['theta_rad'].values, group['sigma_N'].values, theta_grid, method='linear', fill_value=0)
    tau_2_interp = griddata(group['theta_rad'].values, group['tau_2'].values, theta_grid, method='linear', fill_value=0)
    
    # Evaluate the core functional equation inside the summation (Image 2)
    # Note: Using the corrected (+) sign to match your formulas exactly
    functional_values = (sigma_N_interp * np.cos(theta_grid)) + (tau_2_interp * np.sin(theta_grid))
    
    # Apply Equation 7.11: 
    # p = 2 * sum( (sigma_n*cos(psi) + tau_2*sin(psi)) * delta_z * (pi / n) )
    summation = np.sum(functional_values)
    p_total = 2 * summation * delta_z * (np.pi / N)
    
    results.append({
        'Depth': depth, 
        'P_total_kN_m': p_total
    })

# ==============================================================================
# 4. EXPORT RESULTS
# ==============================================================================
integrated_output = os.path.join(file_dir, "Integrated_Depth_Results_P.csv")
final_df = pd.DataFrame(results).sort_values('Depth', ascending=False)
final_df.to_csv(integrated_output, index=False)

print(f"Analysis complete using M={M} and N={N} grid configurations.")
print(f"Results successfully saved in: {file_dir}")