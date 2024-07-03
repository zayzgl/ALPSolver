import sys
from antlr4 import *
from AlpParser import AlpParser
from AlpVisitor import AlpVisitor
from collections import defaultdict
import copy
from collections import defaultdict


class VisitorInterp(AlpVisitor):

    def visitAtom(self, ctx: AlpParser.AtomContext):
        return ctx.getChild(0).getText()  # string

    def visitLiteral(self, ctx: AlpParser.LiteralContext):
        if ctx.getChildCount() == 1:
            return self.visitAtom(ctx.getChild(0))
        else:
            return self.visitAtom(ctx.getChild(1))

    def visitDefault_literal(self, ctx: AlpParser.Default_literalContext):
        return self.visitLiteral(ctx.getChild(1))

    def visitExtended_literal(self, ctx: AlpParser.Extended_literalContext):
        literal = None
        neg_literal = None
        default = None
        neg_default = None

        new_ctx = ctx.getChild(0)  # default_literal或literal
        if type(new_ctx).__name__ == "LiteralContext":
            if new_ctx.getChildCount() == 1:
                literal = self.visitLiteral(new_ctx)
            elif new_ctx.getChildCount() == 2:
                neg_literal = self.visitLiteral(new_ctx)
        elif type(new_ctx).__name__ == "Default_literalContext":
            new_ctx1 = new_ctx.getChild(1)  # Literal
            if new_ctx1.getChildCount() == 1:
                default = self.visitLiteral(new_ctx1)
            elif new_ctx1.getChildCount() == 2:
                neg_default = self.visitLiteral(new_ctx1)

        return literal, neg_literal, default, neg_default

    def visitHead(self, ctx: AlpParser.HeadContext):
        head_dict = defaultdict(set)

        for i in range(0, ctx.getChildCount(), 2):
            new_ctx = ctx.getChild(i)
            if new_ctx.getChildCount() == 1:
                head_dict["literal"].add(self.visitLiteral(new_ctx))
            else:
                head_dict["neg_literal"].add(self.visitLiteral(new_ctx))

        return head_dict

    def visitPrecondition(self, ctx: AlpParser.PreconditionContext):
        precondition_literal_dict = defaultdict(set)

        for i in range(0, ctx.getChildCount(), 2):
            new_ctx = ctx.getChild(i)
            literal, neg_literal, default, neg_default = self.visitExtended_literal(new_ctx)
            if literal is not None:
                precondition_literal_dict["literal"].add(literal)
            elif neg_literal is not None:
                precondition_literal_dict["neg_literal"].add(neg_literal)
            elif default is not None:
                precondition_literal_dict["default"].add(default)
            elif neg_default is not None:
                precondition_literal_dict["neg_default"].add(neg_default)

        return precondition_literal_dict

    def visitAssump(self, ctx: AlpParser.AssumpContext):
        assumption_literal_dict = defaultdict(set)

        for i in range(0, ctx.getChildCount(), 2):
            new_ctx = ctx.getChild(i)
            literal, neg_literal, default, neg_default = self.visitExtended_literal(new_ctx)
            if literal is not None:
                assumption_literal_dict["literal"].add(literal)
            elif neg_literal is not None:
                assumption_literal_dict["neg_literal"].add(neg_literal)
            elif default is not None:
                assumption_literal_dict["default"].add(default)
            elif neg_default is not None:
                assumption_literal_dict["neg_default"].add(neg_default)

        return assumption_literal_dict

    def visitBody(self, ctx: AlpParser.BodyContext):
        body_precondition_dict = defaultdict(set)
        body_assumption_dict = defaultdict(set)
        all_atom = set()

        if ctx.getChildCount() == 0:
            return 0
        else:
            precondition_literal_dict = self.visitPrecondition(ctx.getChild(0))
            for key, value in precondition_literal_dict.items():
                for v in value:
                    body_precondition_dict[key].add(v)
                    all_atom.add(v)
            if ctx.getChildCount() == 3:
                assumption_literal_dict = self.visitAssump(ctx.getChild(2))
                for key, value in assumption_literal_dict.items():
                    for v in value:
                        body_assumption_dict[key].add(v)
                        all_atom.add(v)

        return body_precondition_dict, body_assumption_dict, all_atom

    def visitFact(self, ctx: AlpParser.FactContext):
        new_ctx = ctx.getChild(0)
        head_dict= self.visitHead(new_ctx)

        return head_dict

    def visitConstraint(self, ctx: AlpParser.ConstraintContext):  # 返回每条约束规则先决条件部分的literal
        new_ctx = ctx.getChild(1)  # bodyContext
        body_precondition_dict_perRule, _, all_atom_perRule = self.visitBody(new_ctx)

        return body_precondition_dict_perRule, all_atom_perRule

    def visitFull_rule(self, ctx: AlpParser.Full_ruleContext):
        head_dict_perRule = self.visitHead(ctx.getChild(0))
        all_atom_perRule = set()
        for key, value in head_dict_perRule.items():
            for v in value:
                all_atom_perRule.add(v)
        body_precondition_dict_perRule, body_assumption_dict_perRule, body_atom_perRule = self.visitBody(ctx.getChild(2))
        for a in body_atom_perRule:
            all_atom_perRule.add(a)

        return head_dict_perRule, body_precondition_dict_perRule, body_assumption_dict_perRule, all_atom_perRule

    def visitAlp_rule(self, ctx: AlpParser.Alp_ruleContext):
        head_perRule = defaultdict(set)
        precondition_perRule = defaultdict(set)
        assump_perRule = defaultdict(set)
        atom_perRule = set()
        fact_perRule = defaultdict(set)
        constraint_perRule = defaultdict(set)

        new_ctx = ctx.getChild(0)
        if type(new_ctx).__name__ == "Full_ruleContext":
            head_dict_perRule, body_precondition_dict_perRule, body_assumption_dict_perRule, all_atom_perRule = self.visitFull_rule(new_ctx)
            head_perRule = copy.deepcopy(head_dict_perRule)
            precondition_perRule = copy.deepcopy(body_precondition_dict_perRule)
            assump_perRule = copy.deepcopy(body_assumption_dict_perRule)
            atom_perRule = copy.deepcopy(all_atom_perRule)
        elif type(new_ctx).__name__ == "FactContext":
            head_dict = self.visitFact(new_ctx)
            head_perRule = copy.deepcopy(head_dict)
            for key, value in head_dict.items():
                for v in value:
                    fact_perRule[key].add(v)
                    atom_perRule.add(v)
        elif type(new_ctx).__name__ == "ConstraintContext":
            body_precondition_dict_perRule, all_atom_perRule = self.visitConstraint(new_ctx)
            precondition_perRule = copy.deepcopy(body_precondition_dict_perRule)
            atom_perRule = copy.deepcopy(all_atom_perRule)
            constraint_perRule = copy.deepcopy(body_precondition_dict_perRule)

        return head_perRule, precondition_perRule, assump_perRule, atom_perRule, fact_perRule, constraint_perRule

    def visitAlp(self, ctx: AlpParser.AlpContext):
        head_dict = defaultdict(lambda: defaultdict(set))
        precondition_dict = defaultdict(set)
        assump_dict = defaultdict(set)
        atoms = set()
        fact = defaultdict(set)
        constraint = defaultdict(lambda: defaultdict(set))

        for i in range(0, ctx.getChildCount()):
            head_perRule, precondition_perRule, assump_perRule, atom_perRule, fact_perRule, constraint_perRule = self.visitAlp_rule(ctx.getChild(i))
            for a in atom_perRule:
                atoms.add(a)
            for key, value in fact_perRule.items():
                for v in value:
                    fact[key].add(v)

            constraint[i] = constraint_perRule
            head_dict[i] = head_perRule
            precondition_dict[i] = precondition_perRule
            assump_dict[i] = assump_perRule

        return head_dict, precondition_dict, assump_dict, atoms, fact, constraint
