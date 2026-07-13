'''
Simon's Algorithm

This algorithm sovles for a in the 2-to-1 function f(x) = f(x⊕a), where ⊕ is the bitwise-addition modulo 2 
'''

from qiskit import *
from qiskit_aer import AerSimulator
from Oracle import Simon_oracle as oracle
from collections import Counter
import numpy as np

n_qubits = 3
qc = QuantumCircuit(n_qubits*2,n_qubits*2) # Initialises a quantum circuit with an n_qubit input register, n_quibit ancilla qubits for the oracle output, and a register of classical bits corresponding to the input and output registers to measure into.
oracle = oracle(n_qubits)

qc.h(range(n_qubits)) # Performs a Hadamard gate operation on all input qubits. This initialises the circuit ready for the oracle.

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
outputs = [item[0][-n_qubits:] for item in Counter(counts).most_common()]
outputs = [o for o in outputs if int(o, 2) != 0] # Filter out 0's
rows = list(dict.fromkeys(outputs))[:n_qubits-1]
rows = [int(bitstring[::-1], 2) for bitstring in rows]
def GJ_elimination(rows, pivot=0, c=n_qubits-1, free=None):
	pivot_row = rows[pivot] #Store the current state of the pivot row.
	if ((pivot_row >> c) & 1) == 1: #Check if there is a 1 in the pivot position, if not then find the next row with one and swap it into place.
		for idx, row in enumerate(rows):
			if ((row >> c) & 1) == 1:
				rows[idx] = (row ^ pivot_row)
		rows[pivot] = pivot_row
		pivot += 1 # Only after a successful XOR will it go to the next pivot. 
		#res.append((pivot_row, c))
	else:
		for idx, row in enumerate(rows[pivot+1:], start=pivot+1):
			if (row >> c)&1==1:
				rows[idx] = pivot_row
				rows[pivot] = row
				return GJ_elimination(rows, pivot, c, free)
		free = c # this is set if has checked them all and there are no 1's in this column, otherwise its going to be the last column.
	c -= 1 # Go to next column
	if pivot == n_qubits-1:
		return rows, free
	return GJ_elimination(rows, pivot, c, free)

RREF, free = GJ_elimination(rows)
if free is None: free = 0
free = n_qubits-free-1
s = (2**(n_qubits-1)>>free) # set the free variable.
for row in RREF:
	pivot = row.bit_length() #gives the bits position
	s+= ((row - 2**(pivot-1)).bit_count() % 2)*2**(pivot-1) #Gives the bits value (0 or 1) then multiplies it with the integer corresponding to the position.

actual_s = int(oracle.s, 2)
print("The algorithm found the value of s to be " + str(s))
print("The oracle used a value of " + str(actual_s))


