'''
Oracle -- Set up to randomise and return the oracle operation to the required algorithm and number of qubits.
'''

from qiskit import *
from random import random, getrandbits
from qiskit.circuit.library import ZGate

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

class Simon_oracle:
	def __init__(self, n_qubits):
		while True:
		    self.s = format(getrandbits(n_qubits), f'0{n_qubits}b')
		    if int(self.s, 2) != 0:
		        break
		self.n_qubits = n_qubits
		a = int(self.s, 2)
		pos = len(self.s)
		j = None
		while j is None:
			if a&1 == 1:
				j = pos
			else:
				a = a>>1
				pos -= 1
		self.j = j-1 #This is the index for the leaset significant 1 in the bit string.
	def f(self, qc):
		i = 0
		while i < self.n_qubits:
			qc.cx(i, i+self.n_qubits) #Copies the input register into the ouput.
			if self.s[i] == "1":
				qc.cx(self.j, i+self.n_qubits)
			i+=1
		return qc

class Grover_oracle:
	def __init__(self, n_qubits):
		self.mark = format(getrandbits(n_qubits), f'0{n_qubits}b') #Choose a state to mark
		self.n_qubits = n_qubits
	def f(self, qc):
		for idx, bit in enumerate(self.mark):
			if bit == "0":
				qc.x(idx)
		multi_controlled_z = ZGate().control(self.n_qubits-1)
		qc.append(multi_controlled_z, range(self.n_qubits))
		for idx, bit in enumerate(self.mark):
			if bit == "0":
				qc.x(idx)
		return qc