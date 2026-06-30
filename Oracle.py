'''
Oracle -- Set up to randomise and return the oracle operation to the required algorithm and number of qubits.
'''

from qiskit import *
from random import random

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

