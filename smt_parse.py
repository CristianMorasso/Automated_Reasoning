from pysmt.smtlib.parser import SmtLibParser

class smt_parser():
    def __init__(self):
        self.parser = SmtLibParser()

    def parse(self,filename):
        script = self.parser.get_script_fname(filename)
        # Get all the Assert's
        f= script.get_strict_formula()
        #get ground_truth
        try:
            result = [cmd for cmd in script.commands if ((cmd.name == "set-info") and (":status" in cmd.args))]
            ground_truth = result[0].args[1].upper()
        except:
            ground_truth = "UNKNOWN"
        # Checks on the File
        assert script.count_command_occurrences("assert") >= 1
        assert script.contains_command("check-sat")

        formulas = f.serialize()[1:-1] 
        
        return formulas.split('|'),ground_truth, '|' in formulas
    

    def parse_and_clause(self, and_clause):

        atoms,formulas = [],[]
        # Separate all Ands 
        if "&" in and_clause:
            splitted_clause = and_clause.strip().split("&") #split on &
            for atom in splitted_clause:
                formulas.append(atom.strip()[1:-1]) #remove parentesis of &
        else:
            formulas.append(and_clause) #mono clause
        for atom in formulas:
            if "!" in atom:
                atom = atom[3:-1]   #remove "! (" and the last parentesis
            if "=" in atom:    #if equality we remove the paretesis and split in the 2 atoms
                equality = atom.split("=")
                atoms.append(equality[0].strip())
                atoms.append(equality[1].strip())
            else:
                atoms.append(atom) #[1:-1])
        # Remove all non-equality formulas
        formulas = [x for x in formulas if "=" in x]

        return formulas,list(set(atoms))

