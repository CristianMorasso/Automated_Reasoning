from matplotlib import pyplot as plt
import networkx as nx 
from itertools import product 
import copy 

# from matplotlib import pyplot as plt
class node_DAG:

    def __init__(self, id, fn, args = []):
        self.id  = id   #id integer
        self.fn  = fn   #string
        self.find  = id #rapresentative id
        self.args = args   #list of id
        self.ccpar = set() #set id 

    # def set_father(self, father_id):
    #     self.ccpar.add(father_id)

    # def __str__(self):
    #     if len(self.args) == 0:
    #         return f"{self.fn}"
    #     else:
    #         args_str = ""
    #         for arg in self.args:
    #             args_str = args_str + self.node_string(arg) + ", "
    #         args_str = args_str[:-2]
    #         return f"{self.fn}({args_str})"
    
class CC_DAG: 

    def __init__(self): 
        self.graph = []#nx.DiGraph()

        self.equalities = []
        self.inequalities = []
         
    # def __str__(self):  #DA FARE
    #     #nodes = list(self.g.nodes) 
    #     result = ""
    #     for node in self.graph:
    #         node_string = self.node_string(node)
    #         result += f"{node} {node_string}\n" 
    #     return result

    # def add_node(self,id,fn,args):
    #     mutable_ccpar = set()
    #     # mutable_ccpar.add(father)
    #     mutable_find = id
    #     self.g.add_node(id,fn=fn, args=args, mutable_find=mutable_find,mutable_ccpar=mutable_ccpar)
    def add_node(self, node):
        self.graph.append(node)        
    
    # PRINT NODE 
    #fatto nella classe nodo
    # def node_string(self,id): 
    #     return self.graph[id].__str__

    def node_string(self,id): 
        node = self.graph[id]
        if len(node.args) == 0:
            return f"{node.fn}"
        else:
            args_str = ""
            for arg in node.args:
                args_str = args_str + self.node_string(arg) + ", "
            args_str = args_str[:-2]
            return f"{node.fn}({args_str})"

    def graph_to_string(self):
        s = ''
        for n in self.graph:
            s+= f"{n.id}: {self.node_string(n.id)} "
            s+= f"{n.ccpar if not n.ccpar.is_empty() else None} "
            s+='\n'
        return s
    # def complete_ccpar(self):
    #     nodes_list = list(self.g.nodes)#(data=True)) 
    #     for id in nodes_list:
    #         self.add_father(id) 
    #         pass
    
    # def add_father(self,id):
    #     father_args = self.g.nodes[id]["args"]
    #     for arg in father_args:
    #         target = self.g.nodes[arg] 
    #         target["mutable_ccpar"].add(id)
    def add_fathers(self):
        for n in self.graph:
            for child_node in n.args:
                self.graph[child_node].ccpar.add(n.id)
    #defined in the pseudo code
    def NODE(self,id):
        return self.graph[id]
        
    def find(self,id): 
        node = self.NODE(id)
        if node.find == id: 
            return id
        else:
            new_id = self.find(node.find)
            return new_id 

    #wrapper ccpar
    def ccpar(self,id):
        return self.NODE(self.find(id)).ccpar
        
        
    def union(self,id1,id2):
        n1 = self.NODE(self.find(id1))
        n2 = self.NODE(self.find(id2))
        n1.find  = copy.copy(n2.find)
        n2.ccpar.update(n1.ccpar)
        n1.ccpar = set()
    
    def congruent(self,id1,id2):
        n1 = self.NODE(id1)
        n2 = self.NODE(id2)
        if (n1.fn is not n2.fn): return False
        if(len(n1.args) is not len(n2.args)): return False
        for i in range(len(n1.args)):
            val1= self.find(n1.args[i]) 
            val2= self.find(n2.args[i]) 
            if val1 != val2: return False
        return True 
        
    def merge(self,id1,id2):
        a1 = self.find(id1)
        a2 = self.find(id2)
        if a1!=a2: 
            pi1 = self.ccpar(id1)
            pi2 = self.ccpar(id2)
            self.union(id1,id2)
            for t1,t2 in product(pi1,pi2):
                if (self.find(t1) is not self.find(t2)) and self.congruent(t1,t2):
                    self.merge(t1,t2)
            return True
        else: 
            return False


    def solve(self):
        for eq in self.equalities:
            val1,val2 =  self.find(eq[0]),self.find(eq[1])
            # print(f"Eq: {eq}")
            self.merge(eq[0],eq[1])
        for ineq in self.inequalities:
            val1,val2 =  self.find(ineq[0]),self.find(ineq[1])
            # print(f"Ineq: {ineq} <-> Mutable_find: [{val1},{val2}] ")
            if val1 == val2: # If the inequality is not correct it's UNSAT 
                # print("UNSAT")
                return "UNSAT"
        # print("SAT")
        return "SAT"
    def visualize_dag(self):
        G = nx.DiGraph()

        # Add nodes to the graph
        for node in self.graph:
            G.add_node(node)

        # Add edges to the graph
        for node in self.graph:
            for child_id in node.ccpar:
                G.add_edge(self.graph[child_id], node)

        # Create a dictionary to store node labels
        labels = {node: f"{node.fn} (ID: {node.id})" for node in self.graph}

        # Draw the graph
        pos = nx.circular_layout(G)
        
        nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=500, font_size=10, arrows=True)
        plt.show()