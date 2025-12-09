# components/layers/qaoa_cost_layer.py

import cirq
import os
import sys
from sympy import Symbol 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'utils')))
from plot_utility import generate_latex_file

def build_zz_cost_layer(n_qubits: int, angle_symbol_name: str) -> cirq.Circuit:
    """
    Xây dựng lớp Cost Hamiltonian (ZZ-mixer) cho QAOA với liên kết tuyến tính (0-1, 1-2, ...).
    Cổng ZZ được thực hiện bằng Rz(gamma) giữa hai cổng CNOT.
    (ZZ(\gamma) on q0, q1) = CNOT(q0, q1) * Rz(2*gamma).on(q1) * CNOT(q0, q1)
    
    Chúng ta sẽ sử dụng cổng CZPowGate hoặc CNOT * RZ * CNOT.
    Để mạch đơn giản cho paper, chúng ta dùng cổng CZ (hoặc CZPowGate).
    Cổng Z-rotation (ZZ) được tạo bằng CZPowGate(exponent=angle)
    """
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()
    
    # Góc quay tham số (gamma)
    gamma = Symbol(angle_symbol_name)
    
    # 1. Áp dụng CZPowGate (hoặc Cirq gọi là CNOT**angle nếu dùng luỹ thừa Z)
    # Chúng ta sử dụng CZPowGate(exponent=gamma)
    cost_ops = []
    
    # Liên kết tuyến tính (Linear connection)
    for i in range(n_qubits - 1):
        # CZPowGate(exponent=gamma) tạo ra cổng ZZ^gamma
        cost_ops.append(cirq.CZPowGate(exponent=gamma).on(qubits[i], qubits[i+1]))
        
    circuit.append(cost_ops, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
    
    return circuit

if __name__ == '__main__':
    N = 4 
    GAMMA_SYM = "gamma_0"
    
    cost_layer = build_zz_cost_layer(N, GAMMA_SYM)
    
    print(f"--- Generating QAOA Cost Layer (N={N}) ---")
    
    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    
    generate_latex_file(
        circuit=cost_layer, 
        filename=f"QAOA_Cost_Layer_N{N}", 
        output_dir=output_folder
    )
