

class Context_Free:
    def __init__(self, variables, terminals, productions, axiom):
        self.variables = variables
        self.terminals = terminals
        self.productions = productions
        self.axiom = axiom
        self.current_word = axiom


    def define_production(self, variable, equivalence):
        self.productions[variable] = self.productions[variable] + equivalence

