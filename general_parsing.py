import copy
from pyparsing import *
import general_parsing as gp
from congruence_closure import node_DAG
import smt_parse as smtp
#congruence_closure import node_DAG
def parse_equations(equations,atom_dict):
    equalities,inequalities = [],[]
    for eq in equations:
        if ("!" in eq) and ("=" in eq):
            inequality = eq[1:-1].split("!")[1].strip()[1:-1]
            inequality = inequality.split("=")
            transformed = [atom_dict[inequality[0].strip()],atom_dict[inequality[1].strip()]]
            inequalities.append(transformed)
        else:
            equality = eq[1:-1].split("=")
            transformed = [atom_dict[equality[0].strip()],atom_dict[equality[1].strip()]]
            equalities.append(transformed)

    return equalities,inequalities

class parse_atoms:

    def __init__(self,cc_dag):
        self.atom_dict = {}
        self.cc_dag = cc_dag
        self.id = -1

    def rec_build(self,fn,args): 
        real_args = []
        c_len,counter = len(args),0
        # Cycle through args
        while counter < c_len:
            try:
                # Argument is a function with arguments
                if args[counter] == ",":
                    counter+=1
                elif isinstance(args[counter], str) and (not isinstance(args[counter +1], str)):
                    #args[counter] contiene una stringa e args[counter+1] è una lista di args -> livello interno
                    real_args.append(self.rec_build(args[counter],args[counter+1])) #recursive call
                    counter+=2
                # Argument is a literal with NO arguments
                elif isinstance(args[counter], str): # else: 
                    if "," in args[counter]:
                        args[counter] = args[counter][:args[counter].find(",")]
                    check_id =  self.atom_dict.get(args[counter],"default")
                    if check_id == "default":  # CREATE SINGLE LITERAL ELEMENT
                        self.id+=1
                        self.atom_dict[args[counter]] = copy.copy(self.id)
                        self.cc_dag.add_node(node_DAG(id=copy.copy(self.id),fn=args[counter],args=[]))
                        real_args.append(copy.copy(self.id))
                    else: real_args.append(check_id)
                    counter+=1
                else:
                    pass
            # Last Element is a Literal and there are no more arguments to args 
            except: 
                check_id =  self.atom_dict.get(args[counter],"default")
                if check_id == "default":  # CREATE SINGLE LITERAL ELEMENT
                    self.id+=1
                    self.atom_dict[args[counter]] = copy.copy(self.id)
                    real_args.append(copy.copy(self.id))
                    self.cc_dag.add_node(node_DAG(id=copy.copy(self.id),fn=args[counter],args=[]))
                else: real_args.append(check_id)
                counter+=1
            
        if fn != None:
            iter_string = ""
            for instance in real_args:
                iter_string= iter_string + self.cc_dag.node_string(instance) +", "
            iter_string = iter_string[:-2]
            real_node = fn + "(" + iter_string  + ")"
            check_id =  self.atom_dict.get(real_node,"default")
            if check_id == "default":  # CREATE SINGLE LITERAL ELEMENT
                self.id+=1
                self.atom_dict[real_node] = copy.copy(self.id)
                self.cc_dag.add_node(node_DAG(id=copy.copy(self.id),fn=fn,args=real_args))
                return copy.copy(self.id)
            return check_id
        else: return 

    def parse(self,atoms):
        for atom in atoms: 
            atom = "(" + atom + ")"
            if self.atom_dict.get(atom,"default") == "default": # dissect the atom if is not already in the dict
                dissected_atom = nestedExpr('(',')').parseString(atom).asList()
                dissected_atom = dissected_atom[0]
                self.rec_build(None,dissected_atom)
             
