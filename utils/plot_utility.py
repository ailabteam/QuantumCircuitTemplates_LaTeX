# utils/plot_utility.py

import cirq
from cirq.contrib.qcircuit import circuit_to_latex_using_qcircuit 
import os
from sympy import Symbol 
# Đã loại bỏ import re

# Template LaTeX cơ bản (giữ nguyên)
LATEX_TEMPLATE = r"""
\documentclass[border=10pt]{standalone}
\usepackage{qcircuit}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{xfrac}
\begin{document}
%s 
\end{document}
"""

def generate_latex_file(circuit: cirq.Circuit, filename: str, output_dir: str):
    """
    Chuyển đổi cirq.Circuit thành mã LaTeX QCircuit và lưu vào file .tex.
    """
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Tạo mã QCircuit LaTeX thô
    
    # Sử dụng circuit.all_qubits() để đảm bảo thứ tự
    latex_code = circuit_to_latex_using_qcircuit(circuit, qubit_order=list(circuit.all_qubits()))
    
    # 2. Bọc mã QCircuit vào template tài liệu
    full_latex = LATEX_TEMPLATE % latex_code
    
    tex_path = os.path.join(output_dir, f"{filename}.tex")

    # 3. Lưu file .tex
    try:
        with open(tex_path, "w") as f:
            f.write(full_latex)
        print(f"[SUCCESS] LaTeX template saved to: {tex_path}")
    except Exception as e:
        print(f"[ERROR] Could not save file {tex_path}: {e}")

# ... (phần __main__ giữ nguyên, chỉ đảm bảo sử dụng Symbol đã import)
if __name__ == '__main__':
    q0, q1 = cirq.LineQubit.range(2)
    # Dùng tên thuần túy
    phi = Symbol('phi') 
    
    test_circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.rx(phi).on(q1), 
        cirq.CNOT.on(q0, q1),
        cirq.measure(q0, key='m')
    )
    
    current_dir = os.path.dirname(__file__)
    test_output_dir = os.path.join(current_dir, "test_output")

    print(f"Testing utility in directory: {current_dir}")
    generate_latex_file(test_circuit, "test_basic_circuit", test_output_dir)
