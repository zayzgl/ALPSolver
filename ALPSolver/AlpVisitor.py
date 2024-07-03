# Generated from Alp.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .AlpParser import AlpParser
else:
    from AlpParser import AlpParser

# This class defines a complete generic visitor for a parse tree produced by AlpParser.

class AlpVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by AlpParser#negative_int.
    def visitNegative_int(self, ctx:AlpParser.Negative_intContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#integer.
    def visitInteger(self, ctx:AlpParser.IntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#natural_number.
    def visitNatural_number(self, ctx:AlpParser.Natural_numberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#arithmetic_op.
    def visitArithmetic_op(self, ctx:AlpParser.Arithmetic_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#simple_arithmetic_expr.
    def visitSimple_arithmetic_expr(self, ctx:AlpParser.Simple_arithmetic_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#simple_arithmetic_expr2.
    def visitSimple_arithmetic_expr2(self, ctx:AlpParser.Simple_arithmetic_expr2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#arithmetic_expr.
    def visitArithmetic_expr(self, ctx:AlpParser.Arithmetic_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#term.
    def visitTerm(self, ctx:AlpParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#atom.
    def visitAtom(self, ctx:AlpParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#range_atom.
    def visitRange_atom(self, ctx:AlpParser.Range_atomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#literal.
    def visitLiteral(self, ctx:AlpParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#default_literal.
    def visitDefault_literal(self, ctx:AlpParser.Default_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#extended_literal.
    def visitExtended_literal(self, ctx:AlpParser.Extended_literalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#relation_expr.
    def visitRelation_expr(self, ctx:AlpParser.Relation_exprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#head.
    def visitHead(self, ctx:AlpParser.HeadContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#precondition.
    def visitPrecondition(self, ctx:AlpParser.PreconditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#assump.
    def visitAssump(self, ctx:AlpParser.AssumpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#body.
    def visitBody(self, ctx:AlpParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#fact.
    def visitFact(self, ctx:AlpParser.FactContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#constraint.
    def visitConstraint(self, ctx:AlpParser.ConstraintContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#full_rule.
    def visitFull_rule(self, ctx:AlpParser.Full_ruleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#alp_rule.
    def visitAlp_rule(self, ctx:AlpParser.Alp_ruleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#meta_rule.
    def visitMeta_rule(self, ctx:AlpParser.Meta_ruleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by AlpParser#alp.
    def visitAlp(self, ctx:AlpParser.AlpContext):
        return self.visitChildren(ctx)



del AlpParser