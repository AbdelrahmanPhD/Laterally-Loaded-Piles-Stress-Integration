# Pile Soil-Structure Interaction: Lateral Pressure Integrator

This repository contains a specialized Python utility developed for geotechnical engineering research (Pile-Soil-Structure Interaction). The script automates the transformation, filtering, interpolation, and integration of unstructured Finite Element Method (FEM) nodal data extracted around a pile boundary to compute the net lateral line load distribution ($p$) along the pile depth.

The methodology strictly implements the continuous and discrete integration formulations typically used in advanced soil-structure interaction analysis to simulate **gapping and structural line loads**.

---

## 🛠️ Mathematical Formulation

The script evaluates the net horizontal force components by integrating normal boundary stresses (\sigma_n) and tangential shear stresses (\tau_2) around the pile circumference.

### 1. Continuous Line Load Equation
The continuous total lateral load per unit depth (p) considering pile symmetry (0 \to \pi) is given by:

p = 2 *int_{\psi=0}^{\pi} (\sigma_n \cos\psi + \tau_2 \sin\psi) \, r \, d\psi

### 2. Discrete Grid Approximation
To process irregular boundary meshes from numerical models, the script maps the unstructured node coordinates onto a structured, regular curvilinear grid using a linear bivariate interpolation algorithm (`scipy.interpolate.griddata`). 

The line load p at each distinct vertical grid level is computed via a discrete Riemann summation:

 p = 2 \sum_{i=0}^{N} (\sigma_{n,i} \cos\psi + \tau_{2,i} \sin\psi) \, \Delta z \, \frac{\pi}{n}

Where the regular vertical grid spacing $\Delta z for a model consisting of M total vertical extraction layers over a total pile embedment length L is defined as:

\quad \Delta z = \frac{L}{M - 1}

---

## 🚀 Key Features

* **Gapping Simulation (Physical Filtering):** Automatically filters out positive normal stress regions (\sigma_N > 0) to eliminate tension/suction capacity, realistically capturing soil-pile detachment/gapping.
* **Coordinate Mapping:** Transforms spatial cartesian coordinates (X, Y) to polar angles (\theta_{\text{rad}}) around the pile center.
* **Regular Grid Interpolation:** Utilizes `SciPy` to map unstructured mesh nodes to a regular grid to allow robust, user-controlled sensitivity analyses on variables M and N.
* **Robust Integration:** Implements deterministic summation scaled perfectly to user mesh parameters, ensuring mathematical convergence independent of raw FE slice densities.

---

## 📦 Dependencies

Ensure you have the following packages installed before executing the script:

```bash
pip install numpy pandas scipy
