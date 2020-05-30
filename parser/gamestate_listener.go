// Code generated from Gamestate.g4 by ANTLR 4.8. DO NOT EDIT.

package parser // Gamestate

import "github.com/antlr/antlr4/runtime/Go/antlr"

// GamestateListener is a complete listener for a parse tree produced by GamestateParser.
type GamestateListener interface {
	antlr.ParseTreeListener

	// EnterConfigfile is called when entering the configfile production.
	EnterConfigfile(c *ConfigfileContext)

	// EnterAssignment is called when entering the assignment production.
	EnterAssignment(c *AssignmentContext)

	// EnterExpression is called when entering the expression production.
	EnterExpression(c *ExpressionContext)

	// ExitConfigfile is called when exiting the configfile production.
	ExitConfigfile(c *ConfigfileContext)

	// ExitAssignment is called when exiting the assignment production.
	ExitAssignment(c *AssignmentContext)

	// ExitExpression is called when exiting the expression production.
	ExitExpression(c *ExpressionContext)
}
