# algorithms/qaoa/qaoa_p1_template.py

import cirq
import os
import sys
from sympy import Symbol 

# Thiết lập đường dẫn để import plot_utility và layer builder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'utils')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'components', 'layers')))

# Hàm xây dựng Cost Layer (CZPow)
from qaoa_cost_layer import build_zz_cost_layer 
from plot_utility import generate_latex_file

def build_qaoa_mixer_layer(n_qubits: int, angle_symbol_name: str) -> cirq.Circuit:
    """Xây dựng lớp Mixer Hamiltonian (H_X), sử dụng Rx(2*beta) trên tất cả các qubit."""
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()
    
    # Góc quay tham số (beta)
    beta = Symbol(angle_symbol_name)
    
    # Áp dụng cổng Rx(2*beta) lên tất cả các qubit
    mixer_ops = []
    # Lưu ý: Cổng Rx(angle) trong Cirq sử dụng Radian. 
    # Công thức QAOA là Rx(2*beta), nên chúng ta truyền tham số là 2*beta.
    # Tuy nhiên, để đơn giản hóa ký hiệu trong LaTeX, chúng ta chỉ cần hiển thị beta.
    # Chúng ta dùng cirq.rx(2 * beta).on(q)
    
    for q in qubits:
        # Nếu chúng ta muốn hiển thị R_X(beta), chỉ cần đặt Symbol là beta
        mixer_ops.append(cirq.rx(2 * beta).on(q))
        
    circuit.append(mixer_ops, strategy=cirq.InsertStrategy.NEW_THEN_INLINE)
    
    return circuit

def build_qaoa_ansatz(n_qubits: int, p: int) -> cirq.Circuit:
    """Xây dựng QAOA Ansatz cho p lớp."""
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()

    # 1. Chuẩn bị trạng thái ban đầu: Hadamard trên tất cả qubit
    circuit.append(cirq.H.on_each(qubits))
    
    # 2. Lặp lại p lớp (Cost + Mixer)
    for layer_idx in range(p):
        gamma_sym_name = f"gamma_{layer_idx}"
        beta_sym_name = f"beta_{layer_idx}"
        
        # Lớp Cost (U_C(gamma))
        cost_layer = build_zz_cost_layer(n_qubits, gamma_sym_name)
        circuit.append(cost_layer)
        
        # Thêm Barrier để phân tách rõ ràng
        circuit.append(cirq.Moment(cirq.resolve_parameters(cirq.X, cirq.ParamResolver({})).on_each(qubits)))
        
        # Lớp Mixer (U_M(beta))
        mixer_layer = build_qaoa_mixer_layer(n_qubits, beta_sym_name)
        circuit.append(mixer_layer)
        
    # Thêm đo lường ở cuối (tùy chọn)
    circuit.append(cirq.measure(*qubits, key='m'))
        
    return circuit

if __name__ == '__main__':
    N = 4 # 4 Qubits
    P = 1 # QAOA p=1
    
    qaoa_ansatz = build_qaoa_ansatz(n_qubits=N, p=P)
    
    print(f"--- Generating QAOA Ansatz (N={N}, P={P}) ---")
    
    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    
    generate_latex_file(
        circuit=qaoa_ansatz, 
        filename=f"QAOA_Ansatz_N{N}_P{P}", 
        output_dir=output_folder
    )
