from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.tools.visualization import plot_histogram
# remember quantum bit indexes start from 0
def qnot(circ, in1):
    circ.x(in1)
    circ.barrier()
    return circ.draw(output='mpl')
def qand(circ, in1, in2, out1, qreg):
    circ.ccx(qreg[in1], qreg[in2], qreg[out1])
    circ.barrier()
    return circ.draw(output='mpl')
def qor(circ, in1, in2, out1, qreg):
    #qnot
    circ.x(in1)
    #qnot
    circ.x(in2)
    #qand
    circ.ccx(qreg[in1], qreg[in2], qreg[out1])
    #qnot
    circ.x(out1)
    circ.barrier()
    return circ.draw(output='mpl')
def qxor(circ, in1, in2, meta1, meta2,...0.. out1, qreg):
    #qnot
    circ.x(in1)
    #qand
    circ.ccx(qreg[in1], qreg[in2], qreg[meta1])
    #qnot
    circ.x(in1)
    #qnot
    circ.x(in2)
    #qand
    circ.ccx(qreg[in1], qreg[in2], qreg[out1])
    #qor
    circ.x(meta1)
    circ.x(out1)
    circ.ccx(qreg[meta1], qreg[out1])
    circ.x(out1)
    circ.barrier()
    return circ.draw(output='mpl')
def qinitialise(circ, in1, value):
    if(value):
        circ.x(in1)
    circ.barrier()
    return circ.draw(output='mpl')
def output(circ, in1, c1):
    circ.measure(in1, c1)
    counts = execute(circ,Aer.get_backend('qasm_simulator')).result().get_counts()
    print(counts)
def halfadder(circ, in1, in2, meta1, out1, out2, c1, c2, qreg):
    qand(circ, in1, in2, out2, qreg)
    #carry to c1
    print("Carry bit\n")
    output(circ, out2, c1)
    
    qxor(circ, in1, in2, meta1, out1, qreg)
    #sum to c2
    print("sum bit\n")
    output(circ, out1, c2)
qreg = QuantumRegister(5, 'q')
creg = ClassicalRegister(2, 'c')
circ = QuantumCircuit(qreg, creg)
qinitialise(circ, 0, 1)
qinitialise(circ, 1, 1)
qxor(circ, 0, 1, 2, 3, qreg)
circ.measure(3,0)
counts = execute(circ,Aer.get_backend('qasm_simulator')).result().get_counts()
counts   
circ.draw(output='mpl')
