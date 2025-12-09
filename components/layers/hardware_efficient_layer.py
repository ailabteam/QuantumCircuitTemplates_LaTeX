# components/layers/hardware_efficient_layer.py

import cirq
import os
import sys
from sympy import Symbol 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'utils')))
from plot_utility import generate_latex_file

def build_hardware_efficient_layer(n_qubits: int, layer_index: int) -> cirq.Circuit:
    """
    Xây dựng một lớp Variational (Hardware Efficient Ansatz) cơ bản.
    Sử dụng tên tham số thuần túy (T_z_L_Q) để đảm bảo khả năng biên dịch LaTeX.
    """
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()

    # 1. Lớp Quay đơn Qubit (Rz và Rx)
    single_qubit_ops = []
    for i in range(n_qubits):
        
        # Tên tham số thuần túy, dễ đọc: T_z_Layer_Qubit
        rz_param_name = f"Tz_{layer_index}_{i}"
        rx_param_name = f"Tx_{layer_index}_{i}"
        
        rz_symbol = Symbol(rz_param_name)
        rx_symbol = Symbol(rx_param_name)
        
        single_qubit_ops.append(cirq.rz(rz_symbol).on(qubits[i]))
        single_qubit_ops.append(cirq.rx(rx_symbol).on(qubits[i]))
    
    circuit.append(single_qubit_ops, strategy=cirq.InsertStrategy.EARLIEST) 
    
    # 2. Lớp Vướng víu (Entangling Layer) - Liên kết tuyến tính
    entangling_ops = []
    for i in range(n_qubits - 1):
        entangling_ops.append(cirq.CNOT.on(qubits[i], qubits[i+1]))
        
    circuit.append(entangling_ops, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
    
    return circuit

if __name__ == '__main__':
    N = 4
    L = 0
    
    ansatz_layer = build_hardware_efficient_layer(n_qubits=N, layer_index=L)
    
    print(f"--- Generating Hardware Efficient Layer (N={N}, L={L}) ---")
    
    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    
    generate_latex_file(
        circuit=ansatz_layer, 
        filename=f"hardware_efficient_N{N}_L{L}", 
        output_dir=output_folder
    )
