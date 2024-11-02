import random
import math


class Region:
    def __init__(self, minimum_y,maximum_y,minimum_x,maximum_x):
        self.minimum_y=minimum_y
        self.maximum_y=maximum_y
        self.minimum_x=minimum_x
        self.maximum_x=maximum_x
    
    def update_params(self,new_gate):
        if self.maximum_y!=None and self.minimum_y!=None:
            if new_gate.x==self.maximum_x:
                self.maximum_x=new_gate.x+new_gate.width
            else:
                self.minimum_x=new_gate.x
            return 0
        elif self.maximum_y==None:
            self.maximum_y=new_gate.y+new_gate.height
            self.minimum_x=new_gate.x
            self.maximum_x=new_gate.x+new_gate.width
            return 1
        else:
            self.minimum_y=new_gate.y
            self.minimum_x=new_gate.x
            self.maximum_x=new_gate.x + new_gate.width
            return -1

class Gate:
    def __init__(self,id,width,height) -> None:
        self.id=id
        self.width=width
        self.height=height
        self.x=0
        self.y=0
        self.pinCoordinates={}
        self.connected_gates ={}
        self.added=False

    def pin(self,pin_id,x,y):
        self.pinCoordinates[pin_id]=(x,y)

    def wire(self,pin_id,other_gate,other_pin):
        if other_gate in self.connected_gates:
            self.connected_gates[other_gate].append((pin_id,other_pin))
        else:
            self.connected_gates[other_gate]=[(pin_id,other_pin)]

    def __repr__(self) -> str:
        return f'|{self.id} , {self.x,self.y} , h: {self.height} w:{self.width}  |'

class Part:
    def __init__(self,min_x,min_y,max_x,max_y,part_gates) -> None:
        self.min_x=min_x
        self.min_y=min_y
        self.max_x=max_x
        self.max_y=max_y
        self.part_gates=part_gates

def compare_wirelength(gate1,gate2,minimum):
    length=0
    for pin1,pin2 in gate1.connected_gates[gate2.id]:
        length += abs(gate1.x+gate1.pinCoordinates[pin1][0]-gate2.x-gate2.pinCoordinates[pin2][0]) + abs(gate1.y+gate1.pinCoordinates[pin1][1]- gate2.y -gate2.pinCoordinates[pin2][1])
    if minimum==None or length < minimum:
        return length
    return None

def gates_placer(pivot):
    global data,part_gates,boundaries
    part_gates.append(pivot)
    for gate_id in pivot.connected_gates:
        gate=None
        for it in data:
            if it.id==gate_id:
                gate=it
                break
        if not gate.added:
            # place_gate(gate, pivot, boundaries)
            minimum = None
            minWire_x = None
            minWire_y = None
            minRegion=None
            gate.added=True
            for region in boundaries:
                result=None
                if region.maximum_y==None:
                    gate.x=pivot.x + (pivot.width - gate.width)//2
                    gate.y=region.minimum_y
                    result=compare_wirelength(pivot,gate,minimum)

                elif region.minimum_y==None:
                    gate.x=pivot.x + (pivot.width - gate.width)//2
                    gate.y=region.maximum_y-gate.height
                    result=compare_wirelength(pivot,gate,minimum)

                elif region.maximum_y>= gate.height+region.minimum_y :
                    gate.x = region.maximum_x
                    gate.y = (region.minimum_y + region.maximum_y - gate.height)//2 
                    result=compare_wirelength(pivot,gate,minimum)

                    if result!=None:
                        minimum = result
                        minRegion=region
                        minWire_x = gate.x
                        minWire_y=gate.y

                    gate.x = region.minimum_x - gate.width
                    gate.y = (region.minimum_y + region.maximum_y - gate.height)//2 
                    result=compare_wirelength(pivot,gate,minimum)

                if result!=None:
                    minimum = result
                    minRegion=region
                    minWire_x = gate.x
                    minWire_y=gate.y
                
            gate.x=minWire_x 
            gate.y=minWire_y 
            placed=minRegion.update_params(new_gate=gate)
            if placed==1:   
                boundaries.append(Region(minRegion.maximum_y,None,None,None))
            elif placed==-1:
                boundaries.append(Region(None,minRegion.minimum_y,None,None))

            gates_placer(gate)
    return part_gates



def parse_gate(input_data, data):
    id = int(input_data[0][1:])
    w = int(input_data[1])
    h = int(input_data[2])
    gate = Gate(id, w, h)
    data.append(gate)

def parse_pins(input_data, data):
    id = int(input_data[1][1:])
    coordinates = input_data[2:]
    input_pin_id = 1
    for i in range(0, len(coordinates), 2):
        x, y = int(coordinates[i]), int(coordinates[i + 1])
        data[id - 1].pin(input_pin_id, x, y)
        input_pin_id += 1

def parse_wire(input_data, data):
    gate1, pin1 = input_data[1].split('.')
    gate2, pin2 = input_data[2].split('.')
    id1 = int(gate1[1:])
    id2 = int(gate2[1:])
    pID1 = int(pin1[1:])
    pID2 = int(pin2[1:])
    
    data[id1 - 1].wire(pID1, id2, pID2)
    data[id2 - 1].wire(pID2, id1, pID1)

data = []
parts=[]

file = open('input.txt', 'r')
lines = file.readlines()
file.close() 

for line in lines:
    input_data = line.split()
    if input_data[0][0] == 'g':
        parse_gate(input_data, data)
    elif input_data[0] == 'pins':
        parse_pins(input_data, data)
    elif input_data[0] == 'wire':
        parse_wire(input_data, data)

data.sort(key=lambda gate : len(gate.connected_gates),reverse=True)
    

for gate in data:
    gate.connected_gates=dict(sorted(gate.connected_gates.items(),key=lambda item: len(item[1]),reverse=True))  
    if not gate.added:
        gate.added=True
        min_x=None
        min_y=None
        max_x=None
        max_y=None
        boundaries=[Region(0,gate.height,0,gate.width),Region(None,0,None,None),Region(gate.height,None,None,None)]
        part_gates=[]
        gates_placer(gate)
        for gate in part_gates:
            if min_x==None or gate.x< min_x:
                min_x=gate.x
            if max_x==None or gate.x +gate.width> max_x:
                max_x=gate.x+gate.width
            if min_y==None or gate.y < min_y:
                min_y = gate.y
            if max_y==None or gate.y + gate.height> max_y:
                max_y = gate.y+gate.height

        parts.append(Part(min_x,min_y,max_x,max_y,part_gates))


max_x=None
max_y=0
for part in parts:
    for gate in part.part_gates:
        gate.x-=part.min_x
        gate.y=gate.y -part.min_y + max_y
    max_y=max_y+part.max_y - part.min_y 
    if max_x==None or part.max_x>max_x:
        max_x=part.max_x-part.min_x

total_wire_length=0
for i in range(len(data)):
    for j in range(i,len(data)):
        gate_1=data[i]
        gate_2=data[j]
        if gate_2.id not in gate_1.connected_gates:
            continue
        for pin1,pin2 in gate_1.connected_gates[gate_2.id]:
            total_wire_length += abs(gate_1.x+gate_1.pinCoordinates[pin1][0]-gate_2.x-gate_2.pinCoordinates[pin2][0]) + abs(gate_1.y+gate_1.pinCoordinates[pin1][1]- gate_2.y -gate_2.pinCoordinates[pin2][1])
        
data.sort(key=lambda x: x.id)

positions = {}
for gate in data:
    positions['g'+str(gate.id)] = (gate.x, gate.y)

file = open('input.txt', 'r')
lines = file.readlines()
file.close() 
gates = {}
wire_delay_per_unit = 0
wires = []
i = 0
while  i < len(lines):
    i1 = lines[i].rstrip().split()
    if i1[0] == 'wire_delay':
        wire_delay_per_unit = int(i1[1])
        i += 1
    if i1[0][0] == 'g':
        i2 = lines[i+1].rstrip().split()
        pins = []
        i2 = i2[2:]
        for j in range(0,len(i2),2):
            pins.append((int(i2[j]),int(i2[j+1])) )
        gates[i1[0]] = {'width': int(i1[1]), 'height': int(i1[2]), 'delay': int(i1[3]), 'pins': pins,'connected':[],'connected_pins':{},'primary_input':[],'primary_output': []}
        i  += 2
    if  i1[0] == 'wire':
        # print(i1)
        w1 = i1[1].split('.')
        w2 = i1[2].split('.')
        wires.append((w1[0],w1[1],w2[0],w2[1]))
        gates[w1[0]]['connected'].append(gates[w1[0]]['pins'][int(w1[1][1:])-1])
        gates[w2[0]]['connected'].append(gates[w2[0]]['pins'][int(w2[1][1:])-1])
        if w1[1] not in gates[w1[0]]['connected_pins']: 
            gates[w1[0]]['connected_pins'][w1[1]] = [i1[2]]
        else:
            gates[w1[0]]['connected_pins'][w1[1]].append(i1[2])
        gates[w2[0]]['connected_pins'][w2[1]] = None
        i  += 1

for gate in gates:
    not_connected = list(set(gates[gate]['pins'])-set(gates[gate]['connected']))
    for i in  not_connected:
        if i[0] == 0:
            gates[gate]['primary_input'].append('p'+str(gates[gate]['pins'].index(i)+1))
        elif  i[0] == gates[gate]['width']:
            gates[gate]['primary_output'].append('p'+str(gates[gate]['pins'].index(i)+1))

# print(gates)
def next(gate,pin,position):
    if pin in gates[gate]['connected_pins'].keys():
        if  gates[gate]['connected_pins'][pin] != None:
            mini = 0
            n = 0
            for i in gates[gate]['connected_pins'][pin]:
                pin2 = i.split('.')
                p1 = gates[gate]['pins'][int(pin[1:])-1]
                p2 = gates[pin2[0]]['pins'][int(pin2[1][1:])-1]
                g1_position = position[gate]
                g2_position = position[pin2[0]]

                # Get the pin coordinates relative to the gate's bottom-left corner
                pin1_coords = tuple(map(sum, zip(g1_position, p1)))
                pin2_coords = tuple(map(sum, zip(g2_position, p2)))
                if wire_length(pin1_coords,pin2_coords)>mini:
                    mini = wire_length(pin1_coords,pin2_coords)
                    n = i
            return [n,'wired']
        if  gates[gate]['connected_pins'][pin] == None:
            s = 0
            for i in gates[gate]['connected_pins'].keys():
                if gates[gate]['connected_pins'][i]  != None:
                    s = i
                    break
                else:
                    continue
            if s == 0:
                return [str(gate) +'.'+gates[gate]['primary_output'][0],'not wired']
            else:
                return [str(gate) +'.'+ s,'not wired']
    elif pin in gates[gate]['primary_input']:
        s = 0
        for i in gates[gate]['connected_pins'].keys():
            if gates[gate]['connected_pins'][i]  != None:
                s = i
                break
            else:
                continue
        if s == 0:
            return [str(gate) +'.'+gates[gate]['primary_output'][0],'not wired']
        else:
            return [str(gate) +'.'+ s,'not wired']
    elif  pin in gates[gate]['primary_output']:
        return
    
def wire_length(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return (abs(x1 - x2) + abs(y1 - y2))

def compute_wire_delay(gate1, pin1, gate2, pin2,position):
    g1_position = position[gate1]
    g2_position = position[gate2]
    pin1_coords = tuple(map(sum, zip(g1_position, gates[gate1]['pins'][int(pin1[1:])-1])))
    pin2_coords = tuple(map(sum, zip(g2_position, gates[gate2]['pins'][int(pin2[1:])-1])))
    length = wire_length(pin1_coords, pin2_coords)

    return wire_delay_per_unit * length
def bounding_box(position):
    min_x = float('inf')
    min_y = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')
    
    for gate, posi in position.items():
        x, y = posi
        width = gates[gate]['width']
        height = gates[gate]['height']
        
        # Update min/max x and y based on the gate's bottom-left corner and dimensions
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + width)
        max_y = max(max_y, y + height)

    # Return the width and height of the bounding box
    return (max_x - min_x, max_y - min_y)

def compute_critical_path_delay(position):
    def ccpd(pin, accumulated_delay, visited):
        # Mark the current gate as visited
        visited.add(pin)
        max_delay = accumulated_delay
        path = [pin]
        gate = pin.split('.')[0]
        # Explore connected gates\
        s = 0
        for p in gates[gate]['connected_pins']:
            if gates[gate]['connected_pins'][p] is not None:
                s = 1
                for connected_gate in gates[gate]['connected_pins'][p]:
                    next_gate = connected_gate.split('.')[0]
                    if connected_gate not in visited:
                        # Compute wire delay
                        wire_delay = compute_wire_delay(gate, p, next_gate, connected_gate.split('.')[1], position)
                        # Recursive DFS call
                        new_delay = accumulated_delay + wire_delay + gates[next_gate]['delay']
                        new_path, new_max_delay = ccpd(connected_gate, new_delay, visited)
                        if new_max_delay > max_delay:
                            max_delay = new_max_delay
                            path += [gate+'.'+p]+ new_path
        if s == 0:
            max_delay += gates[pin.split('.')[0]]['delay']
            path += [gate+'.'+gates[gate]['primary_output'][0]]
        return path, max_delay
     
    final_delay = 0
    final_path = []

    for gate in gates:
        if gates[gate]['primary_input']:
            visited = set()
            pin = gate+'.'+ gates[gate]['primary_input'][0]
            initial_delay = gates[gate]['delay']
            path, delay = ccpd(pin, initial_delay, visited)
            if delay > final_delay:
                final_delay = delay
                final_path = path
    return final_delay, final_path


def move_gate_randomly(gate,position):

    current_x, current_y = position[gate]
    gate_width = gates[gate]['width']
    gate_height = gates[gate]['height']
 
    for _ in range(100): 
        new_x = current_x + random.choice([-1, 1]) * random.randint(1, 2)
        new_y = current_y + random.choice([-1, 1]) * random.randint(1, 2)
        
        no_overlap = True
        for other_gate, other_position in position.items():
            if other_gate == gate:
                continue  # Skip checking against itself
            
            other_x, other_y = other_position
            other_width = gates[other_gate]['width']
            other_height = gates[other_gate]['height']
            
            if not (new_x + gate_width <= other_x or  
                    new_x >= other_x + other_width or 
                    new_y + gate_height <= other_y or 
                    new_y >= other_y + other_height): 
                no_overlap = False
                break  
        
        if no_overlap:
            return (new_x, new_y)
    
    return (current_x, current_y)

def simulated_annealing(position):
    current_temp = 100.0
    min_temp = 0.001
    alpha = 0.99
    max_iter = 100000

    current_critical_path_delay, current_critical_path = compute_critical_path_delay(position)
    for i in range(max_iter):
        if current_temp < min_temp:
            break

        gate_to_move = random.choice(list(gates.keys()))
        old_position = position[gate_to_move]
        new_position = move_gate_randomly(gate_to_move,position)

        posit = position.copy()
        posit[gate_to_move] = new_position
        
        new_critical_path_delay, new_critical_path = compute_critical_path_delay(posit)

        if new_critical_path_delay < current_critical_path_delay:
            current_critical_path_delay = new_critical_path_delay
            current_critical_path = new_critical_path
            position = posit.copy()
        else:

            delta = new_critical_path_delay - current_critical_path_delay
            accept_prob = math.exp(-delta / current_temp)
            if random.random() > accept_prob:
                
                pass
            else:
                
                current_critical_path_delay = new_critical_path_delay
                current_critical_path = new_critical_path
                position = posit.copy()

        
        current_temp *= alpha
    return position, current_critical_path_delay, current_critical_path, bounding_box(position)
def check_cyclic_graph(gates):
    adjacency_list = {}
    in_degree = {}

    for gate in gates:
        adjacency_list[gate] = []
        in_degree[gate] = 0

    for gate in gates:
        for pin1, connections in gates[gate]['connected_pins'].items():
            if connections is not None:
                for connected_pin in connections:
                    connected_gate = connected_pin.split('.')[0]
                    adjacency_list[gate].append(connected_gate)
                    in_degree[connected_gate] += 1

    zero_in_degree_queue = [gate for gate in gates if in_degree[gate] == 0]
    topological_order = []

    while zero_in_degree_queue:
        current_gate = zero_in_degree_queue.pop(0)
        topological_order.append(current_gate)

        for neighbor in adjacency_list[current_gate]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                zero_in_degree_queue.append(neighbor)

    if len(topological_order) != len(gates):
        raise Exception("Cycle found in the graph")

check_cyclic_graph(gates)

# Run Simulated Annealing and print the result
final_positions, final_critical_path_delay,final_critical_path, final_bounding_box = simulated_annealing(positions)
print(f"\nBounding Box Dimensions (width x height): {final_bounding_box[0]} x {final_bounding_box[1]}")
print("Final Gate Positions:")
mini_x,mini_y=float('inf'),float('inf')
for gate, pos in final_positions.items():
    mini_x=min(mini_x,pos[0])
    mini_y=min(mini_y,pos[1])
for gate, pos in final_positions.items():
    print(f"{gate}: {pos[0]-mini_x} {pos[1]-mini_y}")
print(f"\nFinal Critical Path Delay: {final_critical_path_delay} ns")
print("\nCritical Path:")
print(final_critical_path)