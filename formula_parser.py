import copy
from pyparsing import *
import formula_parser as gp
from congruence_closure import node_DAG
import smt_parse as smtp
#congruence_closure import node_DAG
def parse_equations(equations,atom_dict):
    equalities,inequalities = [],[]
    for eq in equations:
        if ("!" in eq) and ("=" in eq):
            ineq = eq[3:-1] #remove "! ("
           
            ineq = ineq.split("=")
            inequalities.append([atom_dict[ineq[0].strip()],atom_dict[ineq[1].strip()]])
        else:
            equality = eq.split("=")
            equalities.append([atom_dict[equality[0].strip()],atom_dict[equality[1].strip()]])
    

    return equalities,inequalities

class parse_atoms:

    def __init__(self,cc_dag):
        self.atom_dict = {}
        self.cc_dag = cc_dag
        self.id = -1

    def rec_build(self,fn,args): 
        """
        recursive func to go to inner most args and come back to process them all
        """
        real_args = []
        c_len,counter = len(args),0
        # processing args
        while counter < c_len:
            try:
                # Argument is a function with arguments
                if args[counter] == ",":
                    counter+=1
                elif isinstance(args[counter], str) and (not isinstance(args[counter +1], str)):
                    #if we got a fn and a list near we call the function passing the args (to go deeper) 
                    real_args.append(self.rec_build(args[counter],args[counter+1])) #recursive call
                    counter+=2
                # Argument is a literal with NO arguments
                elif isinstance(args[counter], str): # else: 
                    if "," in args[counter]:
                        args[counter] = args[counter].split(",")[0]
                    check_id =  self.atom_dict.get(args[counter],"aviable")
                    if check_id == "aviable":  # If the node do not exit we create it 
                        self.id+=1
                        self.atom_dict[args[counter]] = copy.copy(self.id) #updating the dict
                        self.cc_dag.add_node(node_DAG(id=copy.copy(self.id),fn=args[counter],string = args[counter],args=[]))   #updating the dag
                        real_args.append(copy.copy(self.id))    #saving args to give to the caller
                    else: real_args.append(check_id)    #saving args to give to the caller
                    counter+=1
                else:
                    pass
            # Last Element is a Literal and there are no more arguments to args 
            except: 
                
                check_id =  self.atom_dict.get(args[counter],"aviable")
                if check_id == "aviable":  # If the node do not exit we create it
                    self.id+=1
                    self.atom_dict[args[counter]] = copy.copy(self.id)  #updating the dict
                    real_args.append(copy.copy(self.id))    #saving args to give to the caller
                    self.cc_dag.add_node(node_DAG(id=copy.copy(self.id),fn=args[counter],string = args[counter],args=[]))    #updating the dag
                else: real_args.append(check_id)    #saving args to give to the caller
                counter+=1
            
        if fn != None:
            args_string = ""
            # recreate the original string to check it in the dict
            for instance in real_args:
                args_string= args_string + self.cc_dag.graph[instance].string +", "
            args_string = args_string[:-2]
            final_node = fn + "(" + args_string  + ")"
            check_id =  self.atom_dict.get(final_node,"aviable")
            if check_id == "aviable":  # If the node do not exit we create it
                self.id+=1
                self.atom_dict[final_node] = copy.copy(self.id) 
                self.cc_dag.add_node(node_DAG(id=copy.copy(self.id),fn=fn,string = final_node, args=real_args))  #updating the dag
                return copy.copy(self.id)
            return check_id
        else: return 

    def parse(self,atoms):
        for atom in atoms: 
            atom = "(" + atom + ")"
            if self.atom_dict.get(atom,"aviable") == "aviable": # If the node do not exit we process it 
                dissected_atom = nestedExpr('(',')').parseString(atom).asList()
                dissected_atom = dissected_atom[0]
                self.rec_build(None,dissected_atom)
             
