from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx 
from itertools import product 
import copy 

class node_DAG:

    def __init__(self, id, fn, string, args = []):
        self.id  = id   #id integer
        self.fn  = fn   #function symbol
        self.find  = id #rapresentative id
        self.args = args   #list of id (argoments)
        self.ccpar = set() #set id (parents)
        self.string = string # string rappresentation of a node
    
class CC_DAG: 

    def __init__(self): 
        self.graph = []
        self.equalities = []
        self.inequalities = []

    def add_node(self, node):
        self.graph.append(node)        

    def graph_to_string(self):
        s = ''
        for n in self.graph:
            s+= f"{n.id}: {n.string} "
            s+= f"{n.ccpar if n.ccpar else None} "
            s+='\n'
        return s

    def fix_find(self):
        """
        Update the find for all nodes
        """
        for n in self.graph:
            n.find = self.find(n.id)

    def add_fathers(self):
        """
        Set the ccpar of each node
        """
        for n in self.graph:
            for child_node in n.args:
                self.graph[child_node].ccpar.add(n.id)
                
    def print_find(self):
        for n in self.graph:
            print(f"{n.id}: {n.string}, {n.find}")

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
        if len(n1.ccpar) >len(n2.ccpar): 
            n2.find  = copy.copy(self.find(id1))
            n1.ccpar.update(n2.ccpar)
            n2.ccpar = set()
            if n1.id in n1.ccpar:
                n1.ccpar.remove(n1.id)
        else:
            n1.find  = copy.copy(self.find(id2))
            n2.ccpar.update(n1.ccpar)
            n1.ccpar = set()
            if n2.id in n2.ccpar:
                n2.ccpar.remove(n2.id)
    
    def congruent(self,id1,id2):
        n1 = self.NODE(id1)
        n2 = self.NODE(id2)
        if not (n1.fn == n2.fn): return False
        if not (len(n1.args) == len(n2.args)): return False
        for i in range(len(n1.args)):
            val1 = self.find(n1.args[i]) 
            val2 = self.find(n2.args[i]) 
            if val1 != val2: return False
        return True 
        
    def merge(self,id1,id2):
        a1 = self.find(id1)
        a2 = self.find(id2)
        if a1!=a2: 
            pi1 = self.ccpar(id1)
            pi2 = self.ccpar(id2)
            self.union(id1,id2)
            self.fix_find() #to correct the find 
            for t1,t2 in product(pi1,pi2):
                if (self.find(t1) != self.find(t2)) and self.congruent(t1,t2):
                    self.merge(t1,t2)
            return True
        else: 
            return False


    def solve(self):
        for eq in self.equalities:
            if eq in self.inequalities or eq[::-1] in self.inequalities: return 1,eq
            self.merge(eq[0],eq[1])
        for ineq in self.inequalities:
            find1,find2 =  self.find(ineq[0]),self.find(ineq[1])
            if find1 == find2:  
                return 1,ineq   # UNSAT if the 2 finds of an ineq are same 
        return 0, ""
    
    def create_dag_to_visualize(self):
        """
        Create a nx directed graph, just the ccpar edges, we use it for the plot
        """
        G = nx.DiGraph()
        # Add nodes to the graph
        for node in self.graph:
            G.add_node(node)
        # Add edges to the graph
        for node in self.graph:
            for child_id in node.ccpar:
                G.add_edge(self.graph[child_id], node)
        return G
    
    def visualize_dag(self, G, find = False):
        """
        Plot the dag with the find edges
        """
        # Create a dictionary to store node labels
        labels = {node: f"{node.string} (ID: {node.id})" for node in self.graph}
        # Draw the graph
        pos = nx.circular_layout(G)
        
        # Draw the dotted edges with curved lines
        if find:
            dotted_edges = []
            for node in self.graph:
                if not (node.find == node.id):
                    dotted_edges.append((node, self.graph[node.find]))
            nx.draw_networkx_edges(G, pos, edgelist=dotted_edges, style='dotted', connectionstyle='arc3,rad=0.3')
        
        title = 'DAG '
        title += "With find edge (dotted)" if find else "" 
        plt.title(title)
        handles = []
        handles.append(Line2D([0], [0], label='CCPAR Edge', color="black"))
        handles.append(Line2D([0], [0],  linestyle = "dashed", label='Find Edge', color="black"))
        nx.draw(G, pos, with_labels=True, labels=labels, node_color='green', node_size=500, font_size=10, arrows=True) #lightblue
        plt.legend(handles=handles)
        plt.savefig(f"DAG_{find}.png")
        plt.show()
        
        return G

    def print_formulas(self, eq= True, ineq = True):
        """
        Print all the equalities in the normal form and in the FIND versions and then inequalities 
        """
        s_eq  = ''
        s_ineq = ''
        if eq:
            s_eq = "Equalities:\n"
            for formula in self.equalities:
                s_eq += f"_{self.graph[formula[0]].string} = {self.graph[formula[1]].string}\n"
                s_eq += f"__Find version:\n"
                s_eq += f"__{self.graph[self.graph[formula[0]].find].string} = {self.graph[self.graph[formula[1]].find].string}"
                s_eq += "\n"
        if ineq:
            s_ineq = "Inequalities:\n"
            for formula in self.inequalities:
                s_ineq += f"_{self.graph[formula[0]].string} != {self.graph[formula[1]].string}\n"
                s_ineq += f"__Find version:\n"
                s_ineq += f"___{self.graph[self.graph[formula[0]].find].string} != {self.graph[self.graph[formula[1]].find].string}"
                s_ineq += "\n"
        return s_eq + s_ineq
