import sys
import formula_parser as gp
import congruence_closure as cc
import smt_parse as smtp

def main(file="",term=None):
    # Checks
    if len(sys.argv)>1: file = sys.argv[1]
    # if file == "": 
    #     print("ERROR: no input file!")
    #     exit()
    #file = 'inputs\input_smt2\input.smt2'
    file = '.\inputs\input2.smt2'

    # DECLARATIONS:
    solver = cc.CC_DAG()
    smt_parser = smtp.smt_parser()
    atom_parser = gp.parse_atoms(solver) 

    # IMPLEMENTATION:
    # Parsing the file
    tokens, ground_truth, or_presence = smt_parser.parse(file) 
    #tokens.sort()
    for token in tokens:
        token = token.strip()
        if or_presence:
            token = token[1:-1]
        equations,atoms = smt_parser.parse_and_clause(token) 
        print(equations)
        # Drawing the graph in the CC_DAG object instance
        atom_parser.parse(atoms) 
        solver.add_fathers()  
        
        G = solver.create_dag_to_visualize()
        solver.visualize_dag(G)
        status_before_process = solver.graph_to_string()
        
        # Parsing the formulas and transforming them in tuples for the CC algorithm 
        solver.equalities, solver.inequalities = gp.parse_equations(equations,atom_parser.atom_dict) 
        # Running Congruence Closure 
        result, ineq = solver.solve() 
        print((f"Problem: "))
        print((f"Formulas:\n{equations}"))
        print(f"Graph Nodes before the process:\nID\tAtom\tCCPAR\n{status_before_process}")
        print(f"Processed Graph Nodes:\nID\tAtom\tCCPAR\n{solver.graph_to_string()}")
        print(solver.print_formulas())
        if result:
            print(f"UNSAT, Inequality -> Find version: ({solver.graph[ineq[0]].string} = {solver.graph[ineq[1]].string}) -> ({solver.graph[solver.graph[ineq[0]].find].string} != {solver.graph[solver.graph[ineq[1]].find].string})\n")
        else:
            print("SAT")
        if not result: 
            print("SAT")
            break
        print(f"Unsat: {token}\n\n\n")

    print(f"Ground Truth: {ground_truth}")
    solver.visualize_dag(G, find = True)
    return result 

if __name__ == "__main__": 
    main()
