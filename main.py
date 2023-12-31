import sys
import formula_parser as gp
import congruence_closure as cc
import smt_parse as smtp
import time 

def main(file="",term=None):
    verbose = False
    # Checks args
    if len(sys.argv)>1: file = sys.argv[1]

    if len(sys.argv)>2:
        verbose = sys.argv[2] == "verbose"
   
    if file == "": 
        print("ERROR: no input file!")
        exit()

    # declarations:
    solver = cc.CC_DAG()
    smt_parser = smtp.smt_parser()
    atom_parser = gp.parse_atoms(solver) 

    
    # Parsing the file (split in tokens)
    tokens, ground_truth, or_presence = smt_parser.parse(file) 
    # running CC on all token till a SAT
    for token in tokens:
        start = time.time()
        token = token.strip()
        if or_presence:
            token = token[1:-1]
        equations,atoms = smt_parser.parse_and_clause(token) 
        # Parsing atoms to create the DAG
        atom_parser.parse(atoms) 
        #Fix all CCPAR
        solver.add_fathers()  
        
        # use class NetworkX to draw the dag, only in verbose setup
        if verbose:
            G = solver.create_dag_to_visualize()
            solver.visualize_dag(G)
            #saving status before the process to print it later
            status_before_process = solver.graph_to_string()
        
        # Parsing the formulas and transforming them in tuples for the CC algorithm 
        solver.equalities, solver.inequalities = gp.parse_equations(equations,atom_parser.atom_dict) 
        # Congruence Closure Step 
        result, ineq = solver.solve() 
        print((f"Formulas: {equations}"))
        if verbose:
            #some verbose prints
            print(f"Graph Nodes before the process:\nID\tAtom\tCCPAR\n{status_before_process}")
            print(f"Processed Graph Nodes:\nID\tAtom\tCCPAR\n{solver.graph_to_string()}")
            print(solver.print_formulas())
            if result:
                print(f"UNSAT, Inequality -> Find version: ({solver.graph[ineq[0]].string} = {solver.graph[ineq[1]].string}) -> ({solver.graph[solver.graph[ineq[0]].find].string} != {solver.graph[solver.graph[ineq[1]].find].string})\n")
            else:
                print("SAT")
        if not result: 
            print("Solver output: SAT")
            break
        print("Solver output: UNSAT")

        print(f"Ground Truth: {ground_truth}")
        if not verbose:
            print(f"Solved in: {round(time.time()-start,3)*1000} ms\n")
    if verbose:    
        solver.visualize_dag(G, find = True)
    return result 

if __name__ == "__main__": 
    main()
