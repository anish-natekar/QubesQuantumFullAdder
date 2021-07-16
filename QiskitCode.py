from qiskit import *
from qiskit.tools.visualization import plot_histogram
from qiskit.tools.visualization import plot_bloch_multivector
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
def qxor(circ, in1, in2, meta1, meta2, qreg):
    #qnot
    circ.x(in1)
    #qand
    circ.ccx(qreg[in1], qreg[in2], qreg[meta1])
    #qnot
    circ.x(meta1)
    #qor
    circ.x(in1)
    circ.x(in2)
    circ.ccx(qreg[in1], qreg[in2], qreg[meta2])
    #qnot
    circ.x(meta2)
    #qand
    circ.cx(qreg[meta1], qreg[meta2])
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
    return list(counts.keys())[0]
def qhalfadder(circ, in1, in2, meta1, meta2, out1, c1, qreg):
    qand(circ, in1, in2, out1, qreg)
    #carry to c1
    c = output(circ, out1, c1)
    print("Carry bit ", c)
    qxor(circ, in1, in2, meta1, meta2, qreg)
    #sum to c2
    s = output(circ, meta2, c1)
    print("sum bit ", s)
    circ.draw(output='mpl')
    return (c, s)
def fulladder(a, b, c):
    # half adder 1
    qreg = QuantumRegister(5, 'q')
    creg = ClassicalRegister(1, 'c')
    circ = QuantumCircuit(qreg, creg)
    qinitialise(circ, 0, a)
    qinitialise(circ, 1, b)
    carry1, sum1 = qhalfadder(circ, 0, 1, 2, 3, 4, 0, qreg)
    circ.barrier()
    # half adder 2
    circ.reset(range(5))
    qinitialise(circ, 0, int(sum1))
    qinitialise(circ, 1, c)
    carry2, sum2 = qhalfadder(circ, 0, 1, 2, 3, 4, 0, qreg)
    circ.barrier()
    # or gate
    circ.reset(range(5))
    qinitialise(circ, 0, int(carry1))
    qinitialise(circ, 1, int(carry2))
    qor(circ, 0, 1, 2, qreg)
    carry = output(circ, 2, 0)
    return(carry, sum2, circ.draw(output='mpl'))
a = int(input("enter the first number to be added"))
b = int(input("enter the second number to be added"))
bina = bin(a)[2:]
binb = bin(b)[2:]
print(bina)
print(binb)
if(len(bina)!=len(binb)):
    if(a>b):
        diff=len(bina)-len(binb)
        binb=("0"*diff)+binb
    else:
        diff=len(binb)-len(bina)
        bina=("0"*diff)+bina
print(bina)
print(binb)
c = '0'
cir=""
num=""
ctr=len(bina)
for i in range(len(bina)-1,-1,-1):
    c, s, cir = fulladder(int(bina[i]), int(binb[i]), int(c))
    num = s + num
num = c + num
print("ans binary",num)
ans=0
for i in range(0,len(num)):
    ans+=int(num[i])*2**(len(num)-1-i)
print("ans decimal",ans)
cir
