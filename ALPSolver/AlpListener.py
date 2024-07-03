# Generated from Alp.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .AlpParser import AlpParser
else:
    from AlpParser import AlpParser

# This class defines a complete listener for a parse tree produced by AlpParser.
class AlpListener(ParseTreeListener):

    # Enter a parse tree produced by AlpParser#negative_int.
    def enterNegative_int(self, ctx:AlpParser.Negative_intContext):
        pass

    # Exit a parse tree produced by AlpParser#negative_int.
    def exitNegative_int(self, ctx:AlpParser.Negative_intContext):
        pass


    # Enter a parse tree produced by AlpParser#integer.
    def enterInteger(self, ctx:AlpParser.IntegerContext):
        pass

    # Exit a parse tree produced by AlpParser#integer.
    def exitInteger(self, ctx:AlpParser.IntegerContext):
        pass


    # Enter a parse tree produced by AlpParser#natural_number.
    def enterNatural_number(self, ctx:AlpParser.Natural_numberContext):
        pass

    # Exit a parse tree produced by AlpParser#natural_number.
    def exitNatural_number(self, ctx:AlpParser.Natural_numberContext):
        pass


    # Enter a parse tree produced by AlpParser#arithmetic_op.
    def enterArithmetic_op(self, ctx:AlpParser.Arithmetic_opContext):
        pass

    # Exit a parse tree produced by AlpParser#arithmetic_op.
    def exitArithmetic_op(self, ctx:AlpParser.Arithmetic_opContext):
        pass


    # Enter a parse tree produced by AlpParser#simple_arithmetic_expr.
    def enterSimple_arithmetic_expr(self, ctx:AlpParser.Simple_arithmetic_exprContext):
        pass

    # Exit a parse tree produced by AlpParser#simple_arithmetic_expr.
    def exitSimple_arithmetic_expr(self, ctx:AlpParser.Simple_arithmetic_exprContext):
        pass


    # Enter a parse tree produced by AlpParser#simple_arithmetic_expr2.
    def enterSimple_arithmetic_expr2(self, ctx:AlpParser.Simple_arithmetic_expr2Context):
        pass

    # Exit a parse tree produced by AlpParser#simple_arithmetic_expr2.
    def exitSimple_arithmetic_expr2(self, ctx:AlpParser.Simple_arithmetic_expr2Context):
        pass


    # Enter a parse tree produced by AlpParser#arithmetic_expr.
    def enterArithmetic_expr(self, ctx:AlpParser.Arithmetic_exprContext):
        pass

    # Exit a parse tree produced by AlpParser#arithmetic_expr.
    def exitArithmetic_expr(self, ctx:AlpParser.Arithmetic_exprContext):
        pass


    # Enter a parse tree produced by AlpParser#term.
    def enterTerm(self, ctx:AlpParser.TermContext):
        pass

    # Exit a parse tree produced by AlpParser#term.
    def exitTerm(self, ctx:AlpParser.TermContext):
        pass


    # Enter a parse tree produced by AlpParser#atom.
    def enterAtom(self, ctx:AlpParser.AtomContext):
        pass

    # Exit a parse tree produced by AlpParser#atom.
    def exitAtom(self, ctx:AlpParser.AtomContext):
        pass


    # Enter a parse tree produced by AlpParser#range_atom.
    def enterRange_atom(self, ctx:AlpParser.Range_atomContext):
        pass

    # Exit a parse tree produced by AlpParser#range_atom.
    def exitRange_atom(self, ctx:AlpParser.Range_atomContext):
        pass


    # Enter a parse tree produced by AlpParser#literal.
    def enterLiteral(self, ctx:AlpParser.LiteralContext):
        pass

    # Exit a parse tree produced by AlpParser#literal.
    def exitLiteral(self, ctx:AlpParser.LiteralContext):
        pass


    # Enter a parse tree produced by AlpParser#default_literal.
    def enterDefault_literal(self, ctx:AlpParser.Default_literalContext):
        pass

    # Exit a parse tree produced by AlpParser#default_literal.
    def exitDefault_literal(self, ctx:AlpParser.Default_literalContext):
        pass


    # Enter a parse tree produced by AlpParser#extended_literal.
    def enterExtended_literal(self, ctx:AlpParser.Extended_literalContext):
        pass

    # Exit a parse tree produced by AlpParser#extended_literal.
    def exitExtended_literal(self, ctx:AlpParser.Extended_literalContext):
        pass


    # Enter a parse tree produced by AlpParser#relation_expr.
    def enterRelation_expr(self, ctx:AlpParser.Relation_exprContext):
        pass

    # Exit a parse tree produced by AlpParser#relation_expr.
    def exitRelation_expr(self, ctx:AlpParser.Relation_exprContext):
        pass


    # Enter a parse tree produced by AlpParser#head.
    def enterHead(self, ctx:AlpParser.HeadContext):
        pass

    # Exit a parse tree produced by AlpParser#head.
    def exitHead(self, ctx:AlpParser.HeadContext):
        pass


    # Enter a parse tree produced by AlpParser#precondition.
    def enterPrecondition(self, ctx:AlpParser.PreconditionContext):
        pass

    # Exit a parse tree produced by AlpParser#precondition.
    def exitPrecondition(self, ctx:AlpParser.PreconditionContext):
        pass


    # Enter a parse tree produced by AlpParser#assump.
    def enterAssump(self, ctx:AlpParser.AssumpContext):
        pass

    # Exit a parse tree produced by AlpParser#assump.
    def exitAssump(self, ctx:AlpParser.AssumpContext):
        pass


    # Enter a parse tree produced by AlpParser#body.
    def enterBody(self, ctx:AlpParser.BodyContext):
        pass

    # Exit a parse tree produced by AlpParser#body.
    def exitBody(self, ctx:AlpParser.BodyContext):
        pass


    # Enter a parse tree produced by AlpParser#fact.
    def enterFact(self, ctx:AlpParser.FactContext):
        pass

    # Exit a parse tree produced by AlpParser#fact.
    def exitFact(self, ctx:AlpParser.FactContext):
        pass


    # Enter a parse tree produced by AlpParser#constraint.
    def enterConstraint(self, ctx:AlpParser.ConstraintContext):
        pass

    # Exit a parse tree produced by AlpParser#constraint.
    def exitConstraint(self, ctx:AlpParser.ConstraintContext):
        pass


    # Enter a parse tree produced by AlpParser#full_rule.
    def enterFull_rule(self, ctx:AlpParser.Full_ruleContext):
        pass

    # Exit a parse tree produced by AlpParser#full_rule.
    def exitFull_rule(self, ctx:AlpParser.Full_ruleContext):
        pass


    # Enter a parse tree produced by AlpParser#alp_rule.
    def enterAlp_rule(self, ctx:AlpParser.Alp_ruleContext):
        pass

    # Exit a parse tree produced by AlpParser#alp_rule.
    def exitAlp_rule(self, ctx:AlpParser.Alp_ruleContext):
        pass


    # Enter a parse tree produced by AlpParser#meta_rule.
    def enterMeta_rule(self, ctx:AlpParser.Meta_ruleContext):
        pass

    # Exit a parse tree produced by AlpParser#meta_rule.
    def exitMeta_rule(self, ctx:AlpParser.Meta_ruleContext):
        pass


    # Enter a parse tree produced by AlpParser#alp.
    def enterAlp(self, ctx:AlpParser.AlpContext):
        pass

    # Exit a parse tree produced by AlpParser#alp.
    def exitAlp(self, ctx:AlpParser.AlpContext):
        pass



del AlpParser