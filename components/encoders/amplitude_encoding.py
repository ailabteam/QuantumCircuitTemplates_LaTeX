# components/encoders/amplitude_encoding.py

import cirq
import os
import sys
from sympy import Symbol 

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'utils')))
from plot_utility import generate_latex_file

def build_amplitude_encoding(n_qubits: int) -> cirq.Circuit:
    """
    Tạo một mạch minh họa Amplitude Encoding sử dụng cổng trừu tượng.
    Trong LaTeX, cổng này sẽ được hiển thị là 'P(x)' (Preparation).
    """
    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()
    
    # 1. Định nghĩa cổng Trừu tượng (Abstract Gate)
    # Chúng ta sử dụng một cổng tùy chỉnh (Custom Gate) để Cirq hiển thị nhãn mong muốn.
    
    # Sử dụng một cổng Unitary mà chúng ta định nghĩa nhãn
    class PreparationGate(cirq.Gate):
        def __init__(self, label):
            super().__init__()
            self.label = label
            
        def num_qubits(self):
            return n_qubits
            
        def __str__(self):
            # Tên sẽ được hiển thị trong LaTeX \gate{\text{...}}
            return self.label 

    # Tên nhãn: P(\vec{x}) hoặc Amplitude Encoding
    # Chúng ta dùng tên LaTeX thuần túy để tránh lỗi
    encoder_label = f"P(x)" 
    prep_gate = PreparationGate(encoder_label)
    
    # 2. Áp dụng cổng lên tất cả qubit
    circuit.append(prep_gate.on(*qubits))
    
    # 3. Thêm một số cổng cơ bản khác để minh họa việc sử dụng sau đó
    circuit.append(cirq.H.on(qubits[0]))
    
    return circuit

if __name__ == '__main__':
    N = 3 # 3 Qubits mã hóa vector 8 chiều
    
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
