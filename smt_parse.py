from pysmt.smtlib.parser import SmtLibParser
from pysmt.rewritings import CNFizer 
cnf_parser = CNFizer()
# from cnf_converter import cnf_convert 

class smt_parser():
    def __init__(self):
        self.parser = SmtLibParser()

    def parse(self,filename):
        # NB: Should create an smtlib env here for script values 
        script = self.parser.get_script_fname(filename)

        # Get all the Assert's
        # f= script.get_last_formula() # No More only last assert
        f= script.get_strict_formula()

        # Checks on the File
        assert script.count_command_occurrences("assert") >= 1
        assert script.contains_command("check-sat")

        # Transform formulas to cnf 
        # converted = cnf_parser.convert(f)
        # formulas = cnf_parser.serialize(converted) 

        formulas = f.serialize() #list(map(lambda x: x.serialize(),list(f.args())))
        #create a list with all atoms (string version serialize)
        atoms    = list(map(lambda x: x.serialize(),list(f.get_atoms())))

        real_atoms,real_formulas = [],[]
        for atom in atoms:
            if atom.find("=") != -1:    #if equality we remove the paretesis and split in the 2 atoms
                equality = atom[1:-1].split("=")
                real_atoms.append(equality[0].strip())
                real_atoms.append(equality[1].strip())
            else:
                real_atoms.append(atom) #[1:-1])
        # Separate all Ands 
        if formulas.find("&") != -1:
            separated_formulas = formulas[1:-1].split("&")
            real_formulas.extend(list(map(lambda x: x.strip(),separated_formulas)))
        # Remove all non-equality formulas
        real_formulas = [x for x in real_formulas if x.find("=")!=-1 ]#check cosa fa

        # print(real_formulas)
        # real_formulas = cnf_convert(real_formulas)
        return real_formulas,list(set(real_atoms))
