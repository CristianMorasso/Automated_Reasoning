## Congruence Closure with DAG's Algorithm
TEST AVAILABLE:<br>
https://colab.research.google.com/drive/1rJMmnOFuNXOE60Z6-e-T_yU2XaX5j-jA?usp=sharing <br>
The code is complete with a guide to test it.

CODE AVAILABLE:<br>
https://github.com/CristianMorasso/Automated_Reasoning<br>
Here there is the repo with the source code of the project.

INPUT DIR AVAILABLE:<br>
https://github.com/CristianMorasso/SMT_inputs
<br>
Here you can find the inputs, some input was found online and some was translated by another student in the course (cited as author in the file).

### HOW IT WORKS  
This code can process some SMT input file and say if the given problem is *satisfiable* or not using the Congruence closure algorithm.

The input <u><b>must be in DNF form or do not have OR inside!!</b></u>
The code is not able to manage other types of input.

Taken an input it splits the formula on the *OR* operetor if is present, and then use CC algorithms on all *AND* clause till he reach a SAT.

## TEST THE CODE

As i said the code is testable at the link in the first rows, with its guide.
Anyway the software is able to test a single problem (input) and also a set of problems.

- ### Single problem
    To test an external input you can drag and drop it on the colab workspace, copy the path and paste it to the variable *path* and then run the cell, it will process the input and print back the response.

- ### Multiple problem
    To test multiple external inputs you they must be in the same directory, you can create it or drag and drop it on the workspace, copy the path on *directory_path* variable and run the next cells.
    It will print all outputs one after another.

## TYPES OF OUTPUT

- Verbose output:

    Need to add the the keyward "verbose" as second input parameter, the output will show:
    1. Formula.
    2. Table with ID ATOM and CCPAR before and after the processing.
    3. Trasformation of equalities and inequalities to the find version in order to see the representative class.
    4. And the solve output if *UNSAT* it would give the wrong inequality
    5. The ground truth from the SMT File



- Standard output: 

    Ouput in a slimmer version (removing verbose parameter in the input).
    This output shows:
    1. Formula
    2. Solver output
    3. Ground Truth
    4. Time needed

    Note: here we add the time because we don't create and display plots during the process, so we have a real read.


