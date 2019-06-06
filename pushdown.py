import copy
import sys


class Stack:

    def __init__(self, init_stack: list):
        self.stack = init_stack

    def __str__(self):
        return str(self.stack)

    def __repr__(self):
        return str(self)

    def head(self):
        if self.stack:
            return self.stack[len(self.stack) - 1]

    def operation(self, opt: tuple):
        operation = opt[0]
        symbol = opt[1]
        if operation == "I":
            self.stack.append(symbol)
        elif operation == "P":
            self.stack.pop()

    def push(self, symbol):
        self.stack.append(symbol)

    def pop(self):
        if self.stack != ['z']:
            self.stack.pop();


class Pushdown:

    def __init__(self, states, transition, q0, z0, accept):
        self.states = states
        self.transition = transition
        self.configuration = [(q0, Stack([z0]))]
        self.accept = accept
        self.q0 = q0
        self.z0 = z0

    def refresh(self):
        self.configuration = [(self.q0, Stack([self.z0]))]

    def define_transition(self, pair: str, symbol: str, stack_action: str, new_state: str) -> None:
        action = ""

        if stack_action[0] == "I":
            action = stack_action[1]

        if pair_to_tuple(pair) in self.transition:
            if symbol in self.transition[pair_to_tuple(pair)]:
                self.transition[pair_to_tuple(pair)][symbol].append([(stack_action[0], action), new_state])
            else:
                self.transition[pair_to_tuple(pair)][symbol] = [[(stack_action[0], action), new_state]]

        else:
            self.transition[pair_to_tuple(pair)] = {symbol: [[(stack_action[0], action), new_state]]}

    def compute(self, string: str):
        string = list(string[::-1])
        self.configuration = set_epsilon_closure(self, self.configuration)

        while string:
            symbol = string[len(string) - 1]
            self.configuration = self.delta(symbol)

            string.pop()

    def interactive_compute(self):
        symbol = "-1"
        while symbol != "":
            symbol = input("Entrada: ")

            for t in self.configuration:
                sys.stdout.write("\033[K")

            self.p_print_config(symbol)
            self.delta(symbol)

    def p_print_config(self, symbol: str):
        for conf in self.configuration:
            print(conf)

    def delta(self, symbol) -> None:
        current_config = self.configuration
        new_conf = []

        for config_s in current_config:
            config = (config_s[0], config_s[1].head())

            if config in self.transition:
                if symbol in self.transition[config]:
                    for transition in self.transition[config][symbol]:
                        new_stack = copy.deepcopy(config_s[1])
                        new_stack.operation(transition[0])
                        new_conf.append((transition[1], new_stack))

        if not new_conf:
            return []
        else:
            return set_epsilon_closure(self, new_conf)

    def current_conf(self):
        current = []

        for t in self.configuration:
            current.append((t[0], t[1].head()))

        return current

    def is_accepting(self):
        accepted = False

        for state in self.current_conf():
            for accept in self.accept:
                if (accept, self.z0) == state:
                    accepted = True

        return accepted


def pair_to_tuple(pair: str) -> tuple:
    l = len(pair) - 1

    return (pair[0: l], pair[l])


def epsilon_closure(pda: Pushdown, configuration: tuple):
    stack = configuration[1]
    current_state = configuration[0]
    transition = {}

    if (current_state, stack.head()) in pda.transition:
        transition = pda.transition[(current_state, stack.head())]

    final = [configuration]

    if "`" in transition:
        for trans in transition["`"]:
            new_stack = copy.deepcopy(stack)
            new_stack.operation(trans[0])
            if not ((trans[1], new_stack) in final):
                final = final + epsilon_closure(pda, (trans[1], new_stack))

    return sorted(final)


def set_epsilon_closure(pda: Pushdown, conjunto: list):
    final = []
    temp = list(conjunto)

    for t in temp:
        final = final + epsilon_closure(pda, t)

    return final


def p_print(pda: Pushdown, strings: list, caption: str):
    print("")
    print(caption)
    for palabra in strings:
        pda.compute(palabra)
        string = 'Palabra: {:<10}  Aceptada: {:<10}'.format(palabra, pda.is_accepting())
        print(string)
        pda.refresh()


p1 = Pushdown(["q1", "q2", "q3", "q4"], dict(), "q1", "z", ["q4"])

p1.define_transition("q1z", "0", "I0", "q1")
p1.define_transition("q10", "0", "I0", "q1")
p1.define_transition("q1z", "3", "N", "q4")
p1.define_transition("q1z", "1", "I1", "q2")
p1.define_transition("q10", "1", "P", "q2")
p1.define_transition("q2z", "1", "I1", "q2")
p1.define_transition("q21", "1", "I1", "q2")
p1.define_transition("q20", "1", "P", "q2")
p1.define_transition("q2z", "3", "N", "q4")
p1.define_transition("q21", "2", "P", "q3")
p1.define_transition("q31", "2", "P", "q3")
p1.define_transition("q3z", "3", "N", "q4")
p1.define_transition("q4z", "3", "N", "q4")


aceptadas_1 = ["0011123", "1122333", "0001113", "3", "013", "123"]
no_aceptadas_1 = ["321", "0123", "2222", "00112223", "31"]

print("Automata 1:")
p_print(p1, aceptadas_1, "Palabras Aceptadas")
p_print(p1, no_aceptadas_1, "Palabras no aceptadas")

p3 = p2 = Pushdown(["q1", "q2", "q3", "q4", "q5"], dict(), "q1", "z", ["q5"])
p3.define_transition("q1z", "a", "Ik", "q1")
p3.define_transition("q1k", "a", "Ik", "q1")
p3.define_transition("q1k", "b", "Ik", "q2")

p3.define_transition("q2k", "b", "Ik", "q2")
p3.define_transition("q2k", "c", "P", "q3")

p3.define_transition("q3k", "c", "P", "q3")
p3.define_transition("q3k", "d", "P", "q4")

p3.define_transition("q4k", "d", "P", "q4")
p3.define_transition("q4z", "`", "N", "q5")

aceptadas_2 = ["abcd", "aaaabcdddd", "abbcdd", "aaabbccccd", "aabbccdd"]
no_aceptadas_2 = ["abbcd", "abcc", "bbbddd", "abbbddd", "abdd"]

print("\n\nAutomata 2:")
p_print(p3, aceptadas_2, "Palabras Aceptadas")
p_print(p3, no_aceptadas_2, "Palabras no aceptadas")


p2 = Pushdown(["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9"], dict(), "q5", "z", ["q4", "q9"])

p2.define_transition("q1z", "a", "Ia", "q1")
p2.define_transition("q1a", "a", "Ia", "q1")
p2.define_transition("q1a", "b", "P", "q2")
p2.define_transition("q2a", "b", "P", "q2")
p2.define_transition("q2a", "`", "P", "q3")
p2.define_transition("q3a", "b", "P", "q2")
p2.define_transition("q3z", "`", "N", "q4")

p2.define_transition("q5z", "`", "N", "q1")
p2.define_transition("q5z", "`", "N", "q6")

p2.define_transition("q6z", "a", "Ia", "q6")
p2.define_transition("q6a", "a", "Ia", "q6")
p2.define_transition("q6a", "b", "Ib", "q7")
p2.define_transition("q7b", "b", "Ib", "q7")
p2.define_transition("q7b", "c", "P", "q8")
p2.define_transition("q8b", "c", "P", "q8")
p2.define_transition("q8a", "c", "P", "q8")
p2.define_transition("q8z", "`", "N", "q9")


aceptadas_3 = ["aaaabb", "aab", "abcc", "aaabcccc", "abbccc"]
no_aceptadas_3 = ["abc", "acc", "abbcccc", "aaabc", "aaaaabbbccccccc"]

print("\n\nAutomata 3:")
p_print(p2, aceptadas_3, "Palabras Aceptadas")
p_print(p2, no_aceptadas_3, "Palabras no aceptadas")

p4 = Pushdown(["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8"], dict(), "q0", "z", ["q4", "q8"])

p4.define_transition("q0z", "`", "N", "q1")
p4.define_transition("q0z", "`", "N", "q5")

p4.define_transition("q1z", "a", "Ia", "q1")
p4.define_transition("q1a", "a", "Ia", "q2")

p4.define_transition("q2a", "b", "Ia", "q2")
p4.define_transition("q2a", "c", "P", "q3")

p4.define_transition("q3a", "c", "P", "q3")
p4.define_transition("q3z", "`", "N", "q4")

p4.define_transition("q5z", "a", "Ia", "q5")
p4.define_transition("q5a", "a", "Ia", "q5")
p4.define_transition("q5a", "b", "P", "q6")

p4.define_transition("q6z", "b", "N", "q7")
p4.define_transition("q6a", "b", "N", "q7")
p4.define_transition("q7a", "b", "P", "q6")
p4.define_transition("q7z", "`", "N", "q8")

aceptadas_4 = ["aabc", "aaabbc", "aaaabccc", "aaaaabbccc", "aaaabbbc"]
no_aceptadas_4 = ["abc", "aabcccc", "aaabcccc", "abbbbc", "aabbc"]

p4.compute(aceptadas_4[0])
print(p4.configuration)

#print("\n\nAutomata 4:")
#p_print(p4, aceptadas_4, "Palabras Aceptadas")
#p_print(p4, no_aceptadas_4, "Palabras no aceptadas")

