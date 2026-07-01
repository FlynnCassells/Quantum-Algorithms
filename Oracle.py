'''
Oracle -- Set up to randomise and return the oracle operation to the required algorithm and number of qubits.
'''

from qiskit import *
from random import random, getrandbits

class DJ_oracle:
	def __init__(self, n_qubits):
		rnd = random()
		if rnd <= 0.5:
			self.type = "balanced"
		else: 
			self.type = "constant"
		self.n_qubits = n_qubits
	def f(self, qc):
		if self.type == "balanced":
			for i in range(self.n_qubits):
			    qc.cx(i, self.n_qubits) # Flips the output qubit once for each 1 in the input register. 
		elif self.type == "constant":
			qc.x(self.n_qubits) # Always flips the output/ancilla qubit.
		return qc

class BV_oracle:
	def __init__(self, n_qubits):
		self.s = format(getrandbits(n_qubits), f'0{n_qubits}b')
		self.n_qubits = n_qubits
	def f(self, qc):
		for idx, i in enumerate(self.s):
			if i == '1':
				qc.cx(idx, self.n_qubits) # This will apply the bitwise sum.
		return qc