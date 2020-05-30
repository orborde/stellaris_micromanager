// Code generated from Gamestate.g4 by ANTLR 4.8. DO NOT EDIT.

package parser

import (
	"fmt"
	"unicode"

	"github.com/antlr/antlr4/runtime/Go/antlr"
)

// Suppress unused import error
var _ = fmt.Printf
var _ = unicode.IsLetter

var serializedLexerAtn = []uint16{
	3, 24715, 42794, 33075, 47597, 16764, 15335, 30598, 22884, 2, 8, 50, 8,
	1, 4, 2, 9, 2, 4, 3, 9, 3, 4, 4, 9, 4, 4, 5, 9, 5, 4, 6, 9, 6, 4, 7, 9,
	7, 3, 2, 3, 2, 3, 3, 3, 3, 3, 4, 3, 4, 3, 5, 3, 5, 6, 5, 24, 10, 5, 13,
	5, 14, 5, 25, 3, 5, 3, 5, 5, 5, 30, 10, 5, 7, 5, 32, 10, 5, 12, 5, 14,
	5, 35, 11, 5, 3, 5, 3, 5, 3, 6, 6, 6, 40, 10, 6, 13, 6, 14, 6, 41, 3, 7,
	6, 7, 45, 10, 7, 13, 7, 14, 7, 46, 3, 7, 3, 7, 2, 2, 8, 3, 3, 5, 4, 7,
	5, 9, 6, 11, 7, 13, 8, 3, 2, 5, 4, 2, 36, 36, 94, 94, 7, 2, 47, 48, 50,
	60, 67, 92, 97, 97, 99, 124, 5, 2, 11, 12, 15, 15, 34, 34, 2, 54, 2, 3,
	3, 2, 2, 2, 2, 5, 3, 2, 2, 2, 2, 7, 3, 2, 2, 2, 2, 9, 3, 2, 2, 2, 2, 11,
	3, 2, 2, 2, 2, 13, 3, 2, 2, 2, 3, 15, 3, 2, 2, 2, 5, 17, 3, 2, 2, 2, 7,
	19, 3, 2, 2, 2, 9, 21, 3, 2, 2, 2, 11, 39, 3, 2, 2, 2, 13, 44, 3, 2, 2,
	2, 15, 16, 7, 63, 2, 2, 16, 4, 3, 2, 2, 2, 17, 18, 7, 125, 2, 2, 18, 6,
	3, 2, 2, 2, 19, 20, 7, 127, 2, 2, 20, 8, 3, 2, 2, 2, 21, 33, 7, 36, 2,
	2, 22, 24, 10, 2, 2, 2, 23, 22, 3, 2, 2, 2, 24, 25, 3, 2, 2, 2, 25, 23,
	3, 2, 2, 2, 25, 26, 3, 2, 2, 2, 26, 29, 3, 2, 2, 2, 27, 28, 7, 94, 2, 2,
	28, 30, 11, 2, 2, 2, 29, 27, 3, 2, 2, 2, 29, 30, 3, 2, 2, 2, 30, 32, 3,
	2, 2, 2, 31, 23, 3, 2, 2, 2, 32, 35, 3, 2, 2, 2, 33, 31, 3, 2, 2, 2, 33,
	34, 3, 2, 2, 2, 34, 36, 3, 2, 2, 2, 35, 33, 3, 2, 2, 2, 36, 37, 7, 36,
	2, 2, 37, 10, 3, 2, 2, 2, 38, 40, 9, 3, 2, 2, 39, 38, 3, 2, 2, 2, 40, 41,
	3, 2, 2, 2, 41, 39, 3, 2, 2, 2, 41, 42, 3, 2, 2, 2, 42, 12, 3, 2, 2, 2,
	43, 45, 9, 4, 2, 2, 44, 43, 3, 2, 2, 2, 45, 46, 3, 2, 2, 2, 46, 44, 3,
	2, 2, 2, 46, 47, 3, 2, 2, 2, 47, 48, 3, 2, 2, 2, 48, 49, 8, 7, 2, 2, 49,
	14, 3, 2, 2, 2, 8, 2, 25, 29, 33, 41, 46, 3, 8, 2, 2,
}

var lexerDeserializer = antlr.NewATNDeserializer(nil)
var lexerAtn = lexerDeserializer.DeserializeFromUInt16(serializedLexerAtn)

var lexerChannelNames = []string{
	"DEFAULT_TOKEN_CHANNEL", "HIDDEN",
}

var lexerModeNames = []string{
	"DEFAULT_MODE",
}

var lexerLiteralNames = []string{
	"", "'='", "'{'", "'}'",
}

var lexerSymbolicNames = []string{
	"", "", "", "", "STRING", "ATOM", "WS",
}

var lexerRuleNames = []string{
	"T__0", "T__1", "T__2", "STRING", "ATOM", "WS",
}

type GamestateLexer struct {
	*antlr.BaseLexer
	channelNames []string
	modeNames    []string
	// TODO: EOF string
}

var lexerDecisionToDFA = make([]*antlr.DFA, len(lexerAtn.DecisionToState))

func init() {
	for index, ds := range lexerAtn.DecisionToState {
		lexerDecisionToDFA[index] = antlr.NewDFA(ds, index)
	}
}

func NewGamestateLexer(input antlr.CharStream) *GamestateLexer {

	l := new(GamestateLexer)

	l.BaseLexer = antlr.NewBaseLexer(input)
	l.Interpreter = antlr.NewLexerATNSimulator(l, lexerAtn, lexerDecisionToDFA, antlr.NewPredictionContextCache())

	l.channelNames = lexerChannelNames
	l.modeNames = lexerModeNames
	l.RuleNames = lexerRuleNames
	l.LiteralNames = lexerLiteralNames
	l.SymbolicNames = lexerSymbolicNames
	l.GrammarFileName = "Gamestate.g4"
	// TODO: l.EOF = antlr.TokenEOF

	return l
}

// GamestateLexer tokens.
const (
	GamestateLexerT__0   = 1
	GamestateLexerT__1   = 2
	GamestateLexerT__2   = 3
	GamestateLexerSTRING = 4
	GamestateLexerATOM   = 5
	GamestateLexerWS     = 6
)
