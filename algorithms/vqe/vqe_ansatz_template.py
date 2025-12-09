# algorithms/vqe/vqe_ansatz_template.py

import cirq
import os
import sys

# Thiết lập đường dẫn để import plot_utility và layer builder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'utils')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'components', 'layers')))

from plot_utility import generate_latex_file
from hardware_efficient_layer import build_hardware_efficient_layer # Import hàm xây dựng layer

def build_vqe_ansatz(n_qubits: int, n_layers: int) -> cirq.Circuit:
    """Xây dựng toàn bộ VQE ansatz sử dụng Hardware Efficient Layers."""
    
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()

    # 1. Chuẩn bị Trạng thái Ban đầu (Initial State Preparation)
    # Trong VQE, thường là trạng thái Hartree-Fock |0...0> hoặc |1...1>, 
    # nhưng nếu cần superposition, có thể thêm H.
    
    # Ở đây, chúng ta sẽ khởi tạo |0...0> (mặc định) và chỉ thêm các lớp biến phân.

    # 2. Xây dựng các lớp biến phân (P-layers)
    for layer_idx in range(n_layers):
        # Lớp layer_idx sẽ có các tham số Tz_idx_q, Tx_idx_q
        layer = build_hardware_efficient_layer(n_qubits, layer_index=layer_idx)
        
        # Thêm một thanh chắn (Barrier) để phân tách rõ các lớp trong biểu đồ LaTeX
        if layer_idx > 0:
             circuit.append(cirq.resolve_parameters(cirq.X, cirq.ParamResolver({})).on_each(qubits)) # Hack để tạo dòng rào ngang
             circuit.append(cirq.Moment([cirq.Z.on_each(qubits)])) # Thêm một Moment để đẩy các cổng vào các cột riêng
             
        circuit.append(layer)
        
    return circuit

if __name__ == '__main__':
    N = 4 # 4 Qubits
    P = 2 # 2 Layers
    
    vqe_ansatz = build_vqe_ansatz(n_qubits=N, n_layers=P)
    
    print(f"--- Generating VQE Ansatz (N={N}, P={P}) ---")
    
    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    
    generate_latex_file(
        circuit=vqe_ansatz, 
        filename=f"VQE_Ansatz_N{N}_P{P}", 
        output_dir=output_folder
    )
