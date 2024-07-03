import sys

import clingo
from antlr4 import *
from AlpLexer import AlpLexer
from AlpParser import AlpParser
from AlpVisitor import AlpVisitor
from VisitorInterp import VisitorInterp
from AlpListener import AlpListener
from itertools import combinations
from collections import defaultdict

matched_model = None


def enumerate_combinations(elements, fact, neg_need):
    def backtrack(start, path):
        # Add current path to the result
        result.append(path[:])
        # Recursively construct combinations
        for i in range(start, len(elements)):
            # Add item
            # print(elements[i])
            path.append(elements[i])

            # Recursion
            backtrack(i + 1, path)
            # Backtracking

            path.pop()
    for atom in neg_need:
        elements.append(atom)
    result = []  # Store results for all combinations
    init = [f for f in fact]
    backtrack(0, init)

    return result


def all_contain(value, ass, type):
    if len(value) == 0:
        return True
    if type == 0:
        for v in value:
            if v not in ass:
                return False
    elif type == 1:
        for v in value:
            v = "-"+v
            if v not in ass:
                return False

    return True


def all_not_contain(value, ass, type):
    if len(value) == 0:
        return True
    if type == 0:
        for v in value:
            if v in ass:
                return False
    elif type == 1:
        for v in value:
            v = "-"+v
            if v in ass:
                return False

    return True


def check(ass_dict, ass):
    for key, value in ass_dict.items():
        if key == "literal" and not all_contain(value, ass, 0):
            return False
        if key == "neg_literal" and not all_contain(value, ass, 1):
            return False
        if key == "default" and not all_not_contain(value, ass, 0):
            return False
        if key == "neg_default" and not all_not_contain(value, ass, 1):
            return False

    return True


def preprocess(atoms_prog, fact_prog, constraint_prog, assump_dict_program):
    needed = set()
    neg_needed = set()
    for key, value in fact_prog.items():
        if key == "neg_literal":
            for v in value:
                atoms_prog.remove(v)
                needed.add("-"+v)
        if key == "literal":
            for v in value:
                needed.add(v)
                atoms_prog.remove(v)
    for key, dict in constraint_prog.items():
        for k, value in dict.items():
            if len(value) >= 2:
                continue
            if key == "literal":
                for v in value:
                    atoms_prog.remove(v)
            if key == "default":
                for v in value:
                    needed.add(v)
                    atoms_prog.remove(v)
    for key, dicts in assump_dict_program.items():
        for k, value in dicts.items():
            if k == 'neg_literal' or k =='neg_default':
                for v in value:
                    neg_needed.add("-"+v)
                    atoms_prog.remove(v)

    return needed, neg_needed


def generate_asp_rule(rule_number, head_dict_prog, precondition_dict_prog):

    asp_rules = set()
    if len(rule_number) != 0:
        for n in rule_number:
            rule = ""
            head = ""
            body = ""
            for key, value in head_dict_prog[n].items():
                value_list = list(value)
                if key == "literal":
                    for i in range(len(value_list)):
                        if i != len(value_list) - 1:
                            head += value_list[i] + "; "
                        else:
                            head += value_list[i]
                if key == "neg_literal":
                    if head != "":
                        head += "; "
                    for i in range(len(value_list)):
                        if i != len(value) - 1:
                            head += "-" + value_list[i] + "; "
                        else:
                            head += "-" + value_list[i]
            if not precondition_dict_prog[n]:
                rule += head + "."
            else:
                head += " :- "
                for key, value in precondition_dict_prog[n].items():
                    value_list = list(value)
                    if key == "literal":
                        for i in range(len(value_list)):
                            if i != len(value_list) - 1:
                                body += value_list[i] + ", "
                            else:
                                body += value_list[i]
                    if key == "neg_literal":
                        if body != "":
                            body += ", "
                        for i in range(len(value_list)):
                            if i != len(value) - 1:
                                body += "-" + value_list[i] + ", "
                            else:
                                body += "-" + value_list[i]
                    if key == "default":
                        if body != "":
                            body += ", "
                        for i in range(len(value_list)):
                            if i != len(value) - 1:
                                body += "not " + value_list[i] + ", "
                            else:
                                body += "not " + value_list[i]
                    if key == "neg_default":
                        if body != "":
                            body += ", "
                        for i in range(len(value_list)):
                            if i != len(value) - 1:
                                body += "not -" + value_list[i] + ", "
                            else:
                                body += "not -" + value_list[i]
                rule += head + body + "."
            asp_rules.add(rule)

    return asp_rules

def resetGlobal():
    global matched_model
    matched_model = None


def checkAssumption(all_possible_ass, head_dict_program, precondition_dict_program, assump_dict_program):
    satisfied_ass = defaultdict(list)
    asp_code_dict = defaultdict(list)
    reduct_code_dict = defaultdict(list)
    print("All possible assumption sets: %s"%all_possible_ass+"\n")

    i = 0
    for ass in all_possible_ass:
        rule_number = list()
        # print("the assumption set: ", ass)
        for number, ass_dict in assump_dict_program.items():
            if check(ass_dict, ass):
                rule_number.append(number)
        asp_rules = generate_asp_rule(rule_number, head_dict_program, precondition_dict_program)
        asp_code = '\n'.join(f"{rule}" for rule in asp_rules)
        asp_code += '\n'
        asp_code += '\n'.join(f"{rule}." for rule in ass)
        reduct_code = '\n'.join(f"{rule}" for rule in asp_rules)

        # Create clingo
        ctl = clingo.Control(["--warn=none"])
        # Add ASP program
        ctl.add("base", [], asp_code)
        # Solver
        ctl.ground([("base", [])])

        # Print results
        def on_model(model):
            global matched_model
            model_atoms = set(str(atom) for atom in model.symbols(shown=True))
            if model_atoms == set(ass):
                matched_model = model_atoms
                return True
            else:
                print("%s is not an assumption set."%ass+"\n")

        with ctl.solve(yield_=True) as handle:
            for model in handle:
                on_model(model)
        # result = ctl.solve(on_model=on_model)
        if matched_model:
            # print("Found a matching model:", matched_model)
            satisfied_ass[i].append(matched_model)
            asp_code_dict[i].append(asp_code)
            reduct_code_dict[i].append(asp_rules)
            i = i + 1
        resetGlobal()

    return satisfied_ass, asp_code_dict, reduct_code_dict


def getAnswer(ref, style, ref1, satisfied_ass, reduct_code_dict, lit_in_assump, defalut_lit_in_assump):

    final_ass = dict()
    final_belief = defaultdict(list)

    # mode selection
    if ref == 0:
        default_ass_dict = defaultdict(set)
        for k, value in satisfied_ass.items():
            default_ass_dict[k] = set()
        for lit in lit_in_assump:
            for k, value in satisfied_ass.items():
                if lit in value[0]:
                    default_ass_dict[k].add(lit)
        for dlit in defalut_lit_in_assump:
            for k, value in satisfied_ass.items():
                if dlit not in value[0]:
                    default_ass_dict[k].add("not "+dlit)
        alits_list = list()
        for k, value in default_ass_dict.items():
            alits_list.append(value)
        if ref1 == 0:  # inclusion
            brave_index = find_superset(alits_list)
            cautious_index = find_subset(alits_list)
            refs = {0: cautious_index, 1: brave_index}
            i = 0
            for value in refs[style]:
                current_ass = satisfied_ass[value][0]
                asp_code = '\n'.join(f"{rule}" for rule in reduct_code_dict[value][0])
                ctl = clingo.Control(["--warn=none"])
                ctl.add("base", [], asp_code)
                ctl.ground([("base", [])])
                with ctl.solve(yield_=True) as handle:
                    for model in handle:
                        model_atoms = set(str(atom) for atom in model.symbols(shown=True))
                        if model_atoms.issubset(set(current_ass)):
                            final_ass[i] = current_ass
                            final_belief[i].append(model_atoms)
                i += 1
        elif ref1 == 1:  # cardinality
            alit_len = [len(v) for v in alits_list]
            cautious_index = [i for i in range(len(alit_len)) if alit_len[i] == min(alit_len)]
            brave_index = [i for i in range(len(alit_len)) if alit_len[i] == max(alit_len)]
            refs = {0: cautious_index, 1: brave_index}
            i = 0
            for value in refs[style]:
                current_ass = satisfied_ass[value][0]
                asp_code = '\n'.join(f"{rule}" for rule in reduct_code_dict[value][0])
                ctl = clingo.Control(["--warn=none"])
                ctl.add("base", [], asp_code)
                ctl.ground([("base", [])])
                with ctl.solve(yield_=True) as handle:
                    for model in handle:
                        model_atoms = set(str(atom) for atom in model.symbols(shown=True))
                        if model_atoms.issubset(set(current_ass)):
                            final_ass[i] = current_ass
                            final_belief[i].append(model_atoms)
                i += 1
    # reduced program
    elif ref == 1:
        if ref1 == 1:
            reduct_code_dict_len = {key: len(value[0]) for key, value in reduct_code_dict.items()}
            min_keys = [key for key, value in reduct_code_dict_len.items() if value == min(reduct_code_dict_len.values())]
            max_keys = [key for key, value in reduct_code_dict_len.items() if value == max(reduct_code_dict_len.values())]
            refs = {0: min_keys, 1: max_keys}
            i = 0
            for value in refs[style]:
                current_reduct_rule = reduct_code_dict[value][0]
                asp_code = '\n'.join(f"{rule}" for rule in current_reduct_rule)
                ass = satisfied_ass[value][0]
                ctl = clingo.Control(["--warn=none"])
                ctl.add("base", [], asp_code)
                ctl.ground([("base", [])])
                with ctl.solve(yield_=True) as handle:
                    for model in handle:
                        model_atoms = set(str(atom) for atom in model.symbols(shown=True))
                        if model_atoms.issubset(set(ass)):
                            final_belief[i].append(model_atoms)
                            final_ass[i] = ass
                i += 1
        elif ref1 == 0:
            code_list = list()
            for key, value in reduct_code_dict.items():
                code_list.append(value[0])
            brave_index = find_superset(code_list)
            cautious_index = find_subset(code_list)
            refs = {0: cautious_index, 1: brave_index}
            i = 0
            for value in refs[style]:
                current_reduct_rule = reduct_code_dict[value][0]
                asp_code = '\n'.join(f"{rule}" for rule in current_reduct_rule)
                ass = satisfied_ass[value][0]
                ctl = clingo.Control(["--warn=none"])
                ctl.add("base", [], asp_code)
                ctl.ground([("base", [])])
                with ctl.solve(yield_=True) as handle:
                    for model in handle:
                        model_atoms = set(str(atom) for atom in model.symbols(shown=True))
                        if model_atoms.issubset(set(ass)):
                            final_belief[i].append(model_atoms)
                            final_ass[i] = ass
                i += 1
    else:
        print("The chosen mode is wrong！")
        # print(final_belief)
        # print(final_ass)

    return final_ass, final_belief


def find_superset(sets_list):
    index_list = list()
    for i in range(len(sets_list)):
        # Check
        candidate = sets_list[i]
        if not any(other.issuperset(candidate) for other in sets_list if other != candidate):
            index_list.append(i)
    # If not find, return None
    return index_list


def find_subset(sets_list):
    index_list = list()
    for i in range(len(sets_list)):
        # Check
        candidate = sets_list[i]
        if not any(other.issubset(candidate) for other in sets_list if other != candidate):
            index_list.append(i)
    # If not find, return None
    return index_list