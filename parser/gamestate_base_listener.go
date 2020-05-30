// Code generated from Gamestate.g4 by ANTLR 4.8. DO NOT EDIT.

package parser // Gamestate

import "github.com/antlr/antlr4/runtime/Go/antlr"

// BaseGamestateListener is a complete listener for a parse tree produced by GamestateParser.
type BaseGamestateListener struct{}

var _ GamestateListener = &BaseGamestateListener{}

// VisitTerminal is called when a terminal node is visited.
func (s *BaseGamestateListener) VisitTerminal(node antlr.TerminalNode) {}

// VisitErrorNode is called when an error node is visited.
func (s *BaseGamestateListener) VisitErrorNode(node antlr.ErrorNode) {}

// EnterEveryRule is called when any rule is entered.
func (s *BaseGamestateListener) EnterEveryRule(ctx antlr.ParserRuleContext) {}

// ExitEveryRule is called when any rule is exited.
func (s *BaseGamestateListener) ExitEveryRule(ctx antlr.ParserRuleContext) {}

// EnterConfigfile is called when production configfile is entered.
func (s *BaseGamestateListener) EnterConfigfile(ctx *ConfigfileContext) {}

// ExitConfigfile is called when production configfile is exited.
func (s *BaseGamestateListener) ExitConfigfile(ctx *ConfigfileContext) {}

// EnterAssignment is called when production assignment is entered.
func (s *BaseGamestateListener) EnterAssignment(ctx *AssignmentContext) {}

// ExitAssignment is called when production assignment is exited.
func (s *BaseGamestateListener) ExitAssignment(ctx *AssignmentContext) {}

// EnterExpression is called when production expression is entered.
func (s *BaseGamestateListener) EnterExpression(ctx *ExpressionContext) {}

// ExitExpression is called when production expression is exited.
func (s *BaseGamestateListener) ExitExpression(ctx *ExpressionContext) {}
