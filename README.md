# QuantumCircuitTemplates_LaTeX

This repository provides standardized quantum circuit templates automatically generated using Google's `Cirq` library and converted into QCircuit LaTeX code. These templates are optimized for direct use in scientific papers, particularly for topics involving Variational Quantum Algorithms (VQE, QAOA) and Quantum Machine Learning.

---

## Table of Contents

1.  [Repository Structure](#1-repository-structure)
2.  [Environment Setup](#2-environment-setup)
3.  [Usage Guide](#3-usage-guide)
4.  [Available Circuit Templates](#4-available-circuit-templates)
5.  [Limitations and LaTeX Notes](#5-limitations-and-latex-notes)

---

## 1. Repository Structure

The project follows a clear structure to separate complete algorithms from reusable components:

```
.
├── algorithms/                 # Complete algorithms (VQE, QAOA, etc.)
├── components/                 # Reusable building blocks (Layers, Encoders)
├── utils/                      # Plotting utilities (converting Cirq to .tex)
├── README.md
└── requirements.txt
```

## 2. Environment Setup

This repository requires Python 3.10+ and the libraries listed in `requirements.txt`.

### Step 1: Create and Activate Conda Environment

```bash
conda create -n qctemplates python=3.10
conda activate qctemplates
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```
*(Key dependencies: `cirq` and `sympy`)*

## 3. Usage Guide

### A. Generating LaTeX Files

To generate the LaTeX code for any template, simply run the corresponding Python file:

```bash
# Example 1: Generate VQE Ansatz (4 Qubits, 2 Layers)
python algorithms/vqe/vqe_ansatz_template.py

# Example 2: Generate QAOA Cost Layer
python components/layers/qaoa_cost_layer.py
```

### B. Output Files

The `.tex` files are generated within the `output/` directory corresponding to the Python file executed.

Example: Running the VQE template creates `algorithms/vqe/output/VQE_Ansatz_N4_P2.tex`.

### C. Compiling on Overleaf

The generated `.tex` files are in `\documentclass[border=10pt]{standalone}` format and use the `qcircuit` package.

1.  Upload the `.tex` file to your Overleaf project.
2.  Ensure your main LaTeX document includes `\usepackage{qcircuit}`.
3.  You can then embed the circuit using `\input{filename.tex}` or copy the content directly.

## 4. Available Circuit Templates

### 4.1. Components (Building Blocks)

| File | Description | Example Output |
| :--- | :--- | :--- |
| `components/layers/hardware_efficient_layer.py` | Basic Variational Layer (Rz-Rx-CNOT linear entanglement). | `hardware_efficient_N4_L0.tex` |
| `components/layers/qaoa_cost_layer.py` | QAOA Cost Hamiltonian $U_C(\gamma)$ (uses $CZ^{\gamma}$ gates). | `QAOA_Cost_Layer_N4.tex` |
| `components/encoders/amplitude_encoding.py` | Abstract $P(x)$ gate for amplitude encoding (requires manual fix). | `Amplitude_Encoding_N3.tex` |

### 4.2. Algorithms

| File | Description | Example Output |
| :--- | :--- | :--- |
| `algorithms/vqe/vqe_ansatz_template.py` | VQE Ansatz using $P$ layers of the Hardware-Efficient structure. | `VQE_Ansatz_N4_P2.tex` |
| `algorithms/qaoa/qaoa_p1_template.py` | QAOA Ansatz for $p=1$ (Hadamard initialization, Cost $U_C$, Mixer $U_M$). | `QAOA_Ansatz_N4_P1.tex` |

## 5. Limitations and LaTeX Notes

Due to the constraints of `cirq.contrib.qcircuit` (version 1.5.0), the following aesthetic points require attention:

### A. Parameter Naming

*   **Output:** Parameters are displayed as plain variable names (e.g., `Rz(Tz_0_0)` or `Rx(2*beta_0)`).
*   **Recommendation:** If you require aesthetically superior mathematical notation (e.g., $\theta_{z,0}^{(0)}$), you must **manually edit** the `.tex` file content on Overleaf.
    *   *Example fix:* Replace `\text{Rz(Tz\_0\_0)}` with `\gate{R_z(\theta_{z,0}^{(0)})}`.

### B. Custom Multi-Qubit Gates

*   **Amplitude Encoding (`P(x)`):** The current Cirq version renders this custom multigate poorly (`P(x), #2, #3`).
*   **Recommendation:** For abstract multiqubit gates, manually edit the `.tex` file to replace the individual gates with the QCircuit commands `\multigate{N-1}{LABEL}` and `\ghost{LABEL}` for proper rendering.

---

**Current configuration has been tested and stabilized for Cirq 1.5.0 on your environment.**

Happy quantum coding and publishing!
