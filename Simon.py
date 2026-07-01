'''
Simon's Algorithm

This algorithm sovles for a in the 2-to-1 function f(x) = f(x⊕a), where ⊕ is the bitwise-addition modulo 2 
'''

from qiskit import *
from qiskit_aer import AerSimulator
from Oracle import Simon_oracle as oracle
from collections import Counter
import numpy as np
import galois

n_qubits = 3
qc = QuantumCircuit(n_qubits*2,n_qubits*2) # Initialises a quantum circuit with an n_qubit input register, n_quibit ancilla qubits for the oracle output, and a register of classical bits corresponding to the input and output registers to measure into.
oracle = oracle(n_qubits)

qc.h(range(n_qubits + 1)) # Performs a Hadamard gate operation on all qubits (including ancilla). This initialises the circuit ready for the oracle.

#Apply the oracle function:
qc = oracle.f(qc)

qc.h(range(n_qubits)) # Apply Hadamard gate to all input register qubits
qc.measure(range(n_qubits*2), range(n_qubits*2)) #Measure all qubits

'''
We have now ensured that the measured input will be orthoganal to a. Thus by obtaining n different measurements, Gauss/Jordan elimination can be performed to obtain a.
'''

# Now simulate this circuit running 1024 times on a quantum computer:
simulator = AerSimulator()
job = simulator.run(qc, shots=1024)
result = job.result()
counts = result.get_counts()
rows = Counter(counts).most_common(n_qubits)

