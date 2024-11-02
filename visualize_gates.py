from visualize_gate import draw_gate_packing
"""
Create dictionary for the gate dimensions (gate_dimensions) and
gates coordinates (gates)
"""
a = open('m.txt','r')
s = a.readlines()
gate_dimensions = {}
for i in s:
    g = i.split()
    if g[0][0] == 'g':
        gate_dimensions[g[0]] = (int(g[1]),int(g[2]))
gates = {}
# gates  = {'g2': (0, 0), 'g5': (0, 2), 'g1': (6, 0), 'g4': (10, 0), 'g3': (13, 0)}
# gates = {'bounding_box':(15,6),'g1':(6,0),'g2':(0,0),'g3':(13,0),'g4':'10,0','g5':(0,2)}
# gates = {'g10': (0, 0), 'g8': (0, 5), 'g6': (0, 15), 'g2': (0, 20), 'g4': (0, 25), 'g1': (0, 35), 'g5': (35, 0), 'g9': (45, 0), 'g3': (30, 0), 'g7': (35, 0)}
b = open('output.txt','r')
f = b.readlines()
for j in f:
    h = j.split()   
    gates[h[0]] = (int(h[1]),int(h[2]))
# Invoke the GUI for visualization
root = draw_gate_packing(gate_dimensions, gates, (100,100))
root.mainloop()
# print(gates)
# print(gate_dimensions)