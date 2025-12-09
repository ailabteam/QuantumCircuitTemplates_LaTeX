import cirq
from cirq.contrib.qcircuit import circuit_to_latex_using_qcircuit
import inspect

# In ra các tham số mà hàm chấp nhận
print(inspect.signature(circuit_to_latex_using_qcircuit))

