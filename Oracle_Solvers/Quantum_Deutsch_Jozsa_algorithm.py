# hard code the quantum Deutsch-Jozsa algorithm for 3 qubits

# Importing standard Qiskit libraries
from qiskit import QuantumCircuit, execute, Aer, IBMQ
from qiskit.providers.ibmq import least_busy
from qiskit.visualization import plot_histogram

# Load IBM Q account and get the least busy backend device
provider = IBMQ.load_account()
backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= 3 and
                                       not x.configuration().simulator and x.status().operational))

# Create a Quantum Circuit acting on the q register
qc = QuantumCircuit(3, 3)

# Apply Hadamard gate to all qubits
qc.h(range(3))

# Apply Oracle
qc.x(range(3))
qc.h(2)
qc.ccx(0, 1, 2)
qc.h(2)
qc.x(range(3))

# Measure qubits
qc.measure(range(3), range(3))

# Execute the circuit on the least busy backend
job = execute(qc, backend, shots=1024)
result = job.result()

# Get the results from the computation
counts = result.get_counts(qc)

# Plot the results
plot_histogram(counts)

# print the circuit
print(qc)
