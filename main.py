import sys
import general_parsing as gp
import congruence_closure as cc
import smt_parse as smtp

def main(file="",term=None):
    # Checks
    if len(sys.argv)>1: file = sys.argv[1]
    # if file == "": 
    #     print("ERROR: no input file!")
    #     exit()
    file = 'inputs\input2.smt2'

    # DECLARATIONS:
    solver = cc.CC_DAG()
    smt_parser = smtp.smt_parser()
    atom_parser = gp.parse_atoms(solver) 

    # IMPLEMENTATION:
    # Parsing the file
    equations,atoms = smt_parser.parse(file) 
    # Drawing the graph in the CC_DAG object instance
    atom_parser.parse(atoms) 
    solver.add_fathers()
    # Parsing the formulas and transforming them in tuples for the CC algorithm 
    solver.equalities, solver.inequalities = gp.parse_equations(equations,atom_parser.atom_dict) 
    # Running Congruence Closure 
    result = solver.solve() 
    # Prints
    
    print((f"Problem: "))
    print((f"Atoms:\n{atoms}\nFormulas:\n{equations}"))
    #print(solver.g.nodes(data=True))
    #print(solver.graph_to_string())# fare to string
    print(f"Graph Nodes:\n{solver.graph_to_string()}")
    print(f"Atom Dictionary:\n{atom_parser.atom_dict}\n")
    print(solver.equalities)
    print(solver.inequalities)
    print(result)
    solver.visualize_dag()
    return result 

if __name__ == "__main__": 
    main()
