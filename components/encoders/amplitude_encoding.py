# components/encoders/amplitude_encoding.py

import cirq
import os
import sys

# Thiết lập đường dẫn để import plot_utility
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'utils')))
from plot_utility import generate_latex_file

def build_amplitude_encoding(n_qubits: int) -> cirq.Circuit:
    """
    Tạo một mạch minh họa Amplitude Encoding sử dụng cổng Unitary trống.
    Phiên bản này sử dụng cách định nghĩa cổng tùy chỉnh đơn giản nhất.
    """
    qubits = cirq.LineQubit.range(n_qubits)
    
    # Định nghĩa cổng đa qubit tùy chỉnh (chỉ cần __str__ để đặt tên)
    class PreparationGate(cirq.Gate):
        def num_qubits(self): 
            return n_qubits
        
        # Chuỗi này sẽ được hiển thị trong LaTeX \gate{\text{...}}
        def __str__(self): 
            return "P(x)" 

    circuit = cirq.Circuit(
        PreparationGate().on(*qubits),
        cirq.H.on(qubits[0])
    )
    
    return circuit

if __name__ == '__main__':
    N = 3 # 3 Qubits 
    
    encoder_circuit = build_amplitude_encoding(n_qubits=N)
    
    print(f"--- Generating Amplitude Encoding Circuit (N={N}) ---")
    
    # Đảm bảo thư mục output tồn tại
    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(output_folder, exist_ok=True)
    
    generate_latex_file(
        circuit=encoder_circuit, 
        filename=f"Amplitude_Encoding_N{N}", 
        output_dir=output_folder
    )
