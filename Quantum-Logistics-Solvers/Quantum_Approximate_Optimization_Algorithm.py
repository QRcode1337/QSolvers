import networkx as nx
from qiskit import Aer, execute, QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.visualization import plot_histogram
from qiskit.aqua.algorithms import QAOA
from qiskit.optimization.algorithms import MinimumEigenOptimizer
from qiskit.optimization.applications.ising import tsp
from qiskit.optimization.applications.ising.common import sample_most_likely


class QAOASolver:
    def __init__(self, G, p, gamma, beta):
        self.G = G
        self.p = p
        self.gamma = gamma
        self.beta = beta

    def qaoa_circuit(self):
        q = QuantumRegister (self.G.number_of_nodes (), 'q')
        c = ClassicalRegister (self.G.number_of_nodes (), 'c')
        qc = QuantumCircuit (q, c)
        for i in range (self.G.number_of_nodes ()):
            qc.h (i)
            for j in range (i):
                if self.G.has_edge (i, j):
                    qc.cx (i, j)
                    qc.rz (self.gamma, j)
                    qc.cx (i, j)
            qc.rx (self.beta, i)
            qc.measure (i, i)
        return qc

    def run_qaoa(self):
        qc = self.qaoa_circuit ()
        backend = Aer.get_backend ('qasm_simulator')
        job = execute (qc, backend, shots=1000)
        result = job.result ()
        return result.get_counts (qc)

    def solve(self):
        qp = tsp.get_operator (self.G)
        qaoa = QAOA (optimizer=None, p=self.p, quantum_instance=Aer.get_backend ('qasm_simulator'))
        meo = MinimumEigenOptimizer (qaoa)
        result = meo.solve (qp)
        return result, sample_most_likely (result.eigenstate)


def main():
    G = nx.Graph ()
    G.add_edge (0, 1, weight=10)
    G.add_edge (0, 2, weight=15)
    G.add_edge (0, 3, weight=20)
    G.add_edge (1, 2, weight=35)
    G.add_edge (1, 3, weight=25)
    G.add_edge (2, 3, weight=30)

    solver = QAOASolver (G, p=1, gamma=0.5, beta=0.5)
    counts = solver.run_qaoa ()
    plot_histogram (counts)
    result, most_likely = solver.solve ()
    print (result)
    print (most_likely)


main ()
