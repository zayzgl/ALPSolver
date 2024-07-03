import sys
import clingo
import Prepare
from AlpLexer import AlpLexer
from AlpParser import AlpParser
from AlpVisitor import AlpVisitor
from VisitorInterp import VisitorInterp
from AlpListener import AlpListener
from itertools import combinations
from Prepare import *
from collections import defaultdict
import time


def show_view(final_ass, final_belief, ref, ref1, style):
    if len(final_ass.keys()) == 0:
        print("Unsatisfiable")
        return 0
    max_key = max(final_ass.keys())
    if ref == 0:
        print("Recording to Number of extended literals in assumption")
    else:
        print("Recording to Number of rules in reduced program")
    if ref1 == 0:
        print("In terms of inclusion")
    else:
        print("In terms of cardinality")
    if style == 0:
        print("Style : Cautious")
    else:
        print("Style : Brave")
    for i in range(max_key+1):
        print("Case :", i)
        print("Assumption set :", set(final_ass[i]))
        num = 0
        for v in final_belief[i]:
            print("View %s: <%s,%s>" % (num, set(final_ass[i]), v))
            num +=1

    return 0


def main():
    start_time = time.time()

    input_stream = FileStream("input.txt")
    lexer = AlpLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = AlpParser(stream)
    tree = parser.alp()
    if parser.getNumberOfSyntaxErrors() > 0:
        print("syntax errors")
    else:
        vinterp = VisitorInterp()
        head_dict_program, precondition_dict_program, assump_dict_program, atoms_program, fact_program, constraint_program = vinterp.visitAlp(
            tree)
        needed, neg_needed = preprocess(atoms_program, fact_program, constraint_program, assump_dict_program)
        all_possible_ass = Prepare.enumerate_combinations(list(atoms_program), needed, list(neg_needed))

        # Obtain the Assumption sets that meet the conditions and the corresponding reducted program
        satisfied_ass, asp_code_dict, reduct_code_dict = Prepare.checkAssumption(all_possible_ass, head_dict_program,
                                                                                 precondition_dict_program,
                                                                                 assump_dict_program)
        lit_in_assump = set()
        defalut_lit_in_assump = set()

        for key, value in assump_dict_program.items():
            for atom in value["literal"]:
                lit_in_assump.add(atom)
            for atom in value["default"]:
                defalut_lit_in_assump.add(atom)
            for atom in value["neg_literal"]:
                lit_in_assump.add("-"+atom)
            for atom in value["neg_default"]:
                defalut_lit_in_assump.add("-"+atom)
        Lit_Rule = 0
        Cau_Bra = 1
        Inc_Car = 1
        final_ass, final_belief = Prepare.getAnswer(Lit_Rule, Cau_Bra, Inc_Car, satisfied_ass, reduct_code_dict, lit_in_assump, defalut_lit_in_assump)

        show_view(final_ass, final_belief, Lit_Rule, Inc_Car, Cau_Bra)

        end_time = time.time()
        ued_time = end_time - start_time
        print("Time:%fs"%ued_time)


if __name__ == '__main__':
    main()
