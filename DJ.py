'''
Deutsch-Josza Algorithm:

This algorithm determines whether some unitary function f is constant or balanced in a single queiry. 
'''

from qiskit import *
from qiskit_aer import AerSimulator
from Oracle import DJ_oracle as oracle

n_qubits = 2
qc = QuantumCircuit(n_qubits+1,n_qubits) # Initialises a quantum circuit with an n_qubit input register, an ancilla qubit for the oracle output and a register of classical bits corresponding to the input register to measure into.
oracle = oracle(n_qubits)

qc.x(n_qubits) # Initalises the ancilla qubit in the |1> state.
qc.h(range(n_qubits + 1)) # Performs a Hadamard gate operation on all qubits (including ancilla). This initialises the circuit ready for the oracle.

#Apply the oracle function:
qc = oracle.f(qc)

qc.h(range(n_qubits)) # Apply Hadamard gate to all register qubits
qc.measure(range(n_qubits), range(n_qubits))

# Now simulate this circuit running 1024 times on a quantum computer:
simulator = AerSimulator()
job = simulator.run(qc, shots=1024)
result = job.result()
counts = result.get_counts()

#Interpret Results:
if '0' * n_qubits in counts:
	print("The algorithm returned that the function is constant")
else:
	print("The algorithm returned that the function is balanced")

print("The oracle had a: " + oracle.type + " function")