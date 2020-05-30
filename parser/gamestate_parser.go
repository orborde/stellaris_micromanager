// Code generated from Gamestate.g4 by ANTLR 4.8. DO NOT EDIT.

package parser // Gamestate

import (
	"fmt"
	"reflect"
	"strconv"

	"github.com/antlr/antlr4/runtime/Go/antlr"
)

// Suppress unused import errors
var _ = fmt.Printf
var _ = reflect.Copy
var _ = strconv.Itoa

var parserATN = []uint16{
	3, 24715, 42794, 33075, 47597, 16764, 15335, 30598, 22884, 3, 8, 35, 4,
	2, 9, 2, 4, 3, 9, 3, 4, 4, 9, 4, 3, 2, 7, 2, 10, 10, 2, 12, 2, 14, 2, 13,
	11, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 3, 4, 5, 4,
	25, 10, 4, 7, 4, 27, 10, 4, 12, 4, 14, 4, 30, 11, 4, 3, 4, 5, 4, 33, 10,
	4, 3, 4, 2, 2, 5, 2, 4, 6, 2, 2, 2, 36, 2, 11, 3, 2, 2, 2, 4, 14, 3, 2,
	2, 2, 6, 32, 3, 2, 2, 2, 8, 10, 5, 4, 3, 2, 9, 8, 3, 2, 2, 2, 10, 13, 3,
	2, 2, 2, 11, 9, 3, 2, 2, 2, 11, 12, 3, 2, 2, 2, 12, 3, 3, 2, 2, 2, 13,
	11, 3, 2, 2, 2, 14, 15, 5, 6, 4, 2, 15, 16, 7, 3, 2, 2, 16, 17, 5, 6, 4,
	2, 17, 5, 3, 2, 2, 2, 18, 33, 7, 6, 2, 2, 19, 33, 7, 7, 2, 2, 20, 28, 7,
	4, 2, 2, 21, 24, 5, 6, 4, 2, 22, 23, 7, 3, 2, 2, 23, 25, 5, 6, 4, 2, 24,
	22, 3, 2, 2, 2, 24, 25, 3, 2, 2, 2, 25, 27, 3, 2, 2, 2, 26, 21, 3, 2, 2,
	2, 27, 30, 3, 2, 2, 2, 28, 26, 3, 2, 2, 2, 28, 29, 3, 2, 2, 2, 29, 31,
	3, 2, 2, 2, 30, 28, 3, 2, 2, 2, 31, 33, 7, 5, 2, 2, 32, 18, 3, 2, 2, 2,
	32, 19, 3, 2, 2, 2, 32, 20, 3, 2, 2, 2, 33, 7, 3, 2, 2, 2, 6, 11, 24, 28,
	32,
}
var deserializer = antlr.NewATNDeserializer(nil)
var deserializedATN = deserializer.DeserializeFromUInt16(parserATN)

var literalNames = []string{
	"", "'='", "'{'", "'}'",
}
var symbolicNames = []string{
	"", "", "", "", "STRING", "ATOM", "WS",
}

var ruleNames = []string{
	"configfile", "assignment", "expression",
}
var decisionToDFA = make([]*antlr.DFA, len(deserializedATN.DecisionToState))

func init() {
	for index, ds := range deserializedATN.DecisionToState {
		decisionToDFA[index] = antlr.NewDFA(ds, index)
	}
}

type GamestateParser struct {
	*antlr.BaseParser
}

func NewGamestateParser(input antlr.TokenStream) *GamestateParser {
	this := new(GamestateParser)

	this.BaseParser = antlr.NewBaseParser(input)

	this.Interpreter = antlr.NewParserATNSimulator(this, deserializedATN, decisionToDFA, antlr.NewPredictionContextCache())
	this.RuleNames = ruleNames
	this.LiteralNames = literalNames
	this.SymbolicNames = symbolicNames
	this.GrammarFileName = "Gamestate.g4"

	return this
}

// GamestateParser tokens.
const (
	GamestateParserEOF    = antlr.TokenEOF
	GamestateParserT__0   = 1
	GamestateParserT__1   = 2
	GamestateParserT__2   = 3
	GamestateParserSTRING = 4
	GamestateParserATOM   = 5
	GamestateParserWS     = 6
)

// GamestateParser rules.
const (
	GamestateParserRULE_configfile = 0
	GamestateParserRULE_assignment = 1
	GamestateParserRULE_expression = 2
)

// IConfigfileContext is an interface to support dynamic dispatch.
type IConfigfileContext interface {
	antlr.ParserRuleContext

	// GetParser returns the parser.
	GetParser() antlr.Parser

	// IsConfigfileContext differentiates from other interfaces.
	IsConfigfileContext()
}

type ConfigfileContext struct {
	*antlr.BaseParserRuleContext
	parser antlr.Parser
}

func NewEmptyConfigfileContext() *ConfigfileContext {
	var p = new(ConfigfileContext)
	p.BaseParserRuleContext = antlr.NewBaseParserRuleContext(nil, -1)
	p.RuleIndex = GamestateParserRULE_configfile
	return p
}

func (*ConfigfileContext) IsConfigfileContext() {}

func NewConfigfileContext(parser antlr.Parser, parent antlr.ParserRuleContext, invokingState int) *ConfigfileContext {
	var p = new(ConfigfileContext)

	p.BaseParserRuleContext = antlr.NewBaseParserRuleContext(parent, invokingState)

	p.parser = parser
	p.RuleIndex = GamestateParserRULE_configfile

	return p
}

func (s *ConfigfileContext) GetParser() antlr.Parser { return s.parser }

func (s *ConfigfileContext) AllAssignment() []IAssignmentContext {
	var ts = s.GetTypedRuleContexts(reflect.TypeOf((*IAssignmentContext)(nil)).Elem())
	var tst = make([]IAssignmentContext, len(ts))

	for i, t := range ts {
		if t != nil {
			tst[i] = t.(IAssignmentContext)
		}
	}

	return tst
}

func (s *ConfigfileContext) Assignment(i int) IAssignmentContext {
	var t = s.GetTypedRuleContext(reflect.TypeOf((*IAssignmentContext)(nil)).Elem(), i)

	if t == nil {
		return nil
	}

	return t.(IAssignmentContext)
}

func (s *ConfigfileContext) GetRuleContext() antlr.RuleContext {
	return s
}

func (s *ConfigfileContext) ToStringTree(ruleNames []string, recog antlr.Recognizer) string {
	return antlr.TreesStringTree(s, ruleNames, recog)
}

func (s *ConfigfileContext) EnterRule(listener antlr.ParseTreeListener) {
	if listenerT, ok := listener.(GamestateListener); ok {
		listenerT.EnterConfigfile(s)
	}
}

func (s *ConfigfileContext) ExitRule(listener antlr.ParseTreeListener) {
	if listenerT, ok := listener.(GamestateListener); ok {
		listenerT.ExitConfigfile(s)
	}
}

func (p *GamestateParser) Configfile() (localctx IConfigfileContext) {
	localctx = NewConfigfileContext(p, p.GetParserRuleContext(), p.GetState())
	p.EnterRule(localctx, 0, GamestateParserRULE_configfile)
	var _la int

	defer func() {
		p.ExitRule()
	}()

	defer func() {
		if err := recover(); err != nil {
			if v, ok := err.(antlr.RecognitionException); ok {
				localctx.SetException(v)
				p.GetErrorHandler().ReportError(p, v)
				p.GetErrorHandler().Recover(p, v)
			} else {
				panic(err)
			}
		}
	}()

	p.EnterOuterAlt(localctx, 1)
	p.SetState(9)
	p.GetErrorHandler().Sync(p)
	_la = p.GetTokenStream().LA(1)

	for ((_la)&-(0x1f+1)) == 0 && ((1<<uint(_la))&((1<<GamestateParserT__1)|(1<<GamestateParserSTRING)|(1<<GamestateParserATOM))) != 0 {
		{
			p.SetState(6)
			p.Assignment()
		}

		p.SetState(11)
		p.GetErrorHandler().Sync(p)
		_la = p.GetTokenStream().LA(1)
	}

	return localctx
}

// IAssignmentContext is an interface to support dynamic dispatch.
type IAssignmentContext interface {
	antlr.ParserRuleContext

	// GetParser returns the parser.
	GetParser() antlr.Parser

	// GetKey returns the key rule contexts.
	GetKey() IExpressionContext

	// GetValue returns the value rule contexts.
	GetValue() IExpressionContext

	// SetKey sets the key rule contexts.
	SetKey(IExpressionContext)

	// SetValue sets the value rule contexts.
	SetValue(IExpressionContext)

	// IsAssignmentContext differentiates from other interfaces.
	IsAssignmentContext()
}

type AssignmentContext struct {
	*antlr.BaseParserRuleContext
	parser antlr.Parser
	key    IExpressionContext
	value  IExpressionContext
}

func NewEmptyAssignmentContext() *AssignmentContext {
	var p = new(AssignmentContext)
	p.BaseParserRuleContext = antlr.NewBaseParserRuleContext(nil, -1)
	p.RuleIndex = GamestateParserRULE_assignment
	return p
}

func (*AssignmentContext) IsAssignmentContext() {}

func NewAssignmentContext(parser antlr.Parser, parent antlr.ParserRuleContext, invokingState int) *AssignmentContext {
	var p = new(AssignmentContext)

	p.BaseParserRuleContext = antlr.NewBaseParserRuleContext(parent, invokingState)

	p.parser = parser
	p.RuleIndex = GamestateParserRULE_assignment

	return p
}

func (s *AssignmentContext) GetParser() antlr.Parser { return s.parser }

func (s *AssignmentContext) GetKey() IExpressionContext { return s.key }

func (s *AssignmentContext) GetValue() IExpressionContext { return s.value }

func (s *AssignmentContext) SetKey(v IExpressionContext) { s.key = v }

func (s *AssignmentContext) SetValue(v IExpressionContext) { s.value = v }

func (s *AssignmentContext) AllExpression() []IExpressionContext {
	var ts = s.GetTypedRuleContexts(reflect.TypeOf((*IExpressionContext)(nil)).Elem())
	var tst = make([]IExpressionContext, len(ts))

	for i, t := range ts {
		if t != nil {
			tst[i] = t.(IExpressionContext)
		}
	}

	return tst
}

func (s *AssignmentContext) Expression(i int) IExpressionContext {
	var t = s.GetTypedRuleContext(reflect.TypeOf((*IExpressionContext)(nil)).Elem(), i)

	if t == nil {
		return nil
	}

	return t.(IExpressionContext)
}

func (s *AssignmentContext) GetRuleContext() antlr.RuleContext {
	return s
}

func (s *AssignmentContext) ToStringTree(ruleNames []string, recog antlr.Recognizer) string {
	return antlr.TreesStringTree(s, ruleNames, recog)
}

func (s *AssignmentContext) EnterRule(listener antlr.ParseTreeListener) {
	if listenerT, ok := listener.(GamestateListener); ok {
		listenerT.EnterAssignment(s)
	}
}

func (s *AssignmentContext) ExitRule(listener antlr.ParseTreeListener) {
	if listenerT, ok := listener.(GamestateListener); ok {
		listenerT.ExitAssignment(s)
	}
}

func (p *GamestateParser) Assignment() (localctx IAssignmentContext) {
	localctx = NewAssignmentContext(p, p.GetParserRuleContext(), p.GetState())
	p.EnterRule(localctx, 2, GamestateParserRULE_assignment)

	defer func() {
		p.ExitRule()
	}()

	defer func() {
		if err := recover(); err != nil {
			if v, ok := err.(antlr.RecognitionException); ok {
				localctx.SetException(v)
				p.GetErrorHandler().ReportError(p, v)
				p.GetErrorHandler().Recover(p, v)
			} else {
				panic(err)
			}
		}
	}()

	p.EnterOuterAlt(localctx, 1)
	{
		p.SetState(12)

		var _x = p.Expression()

		localctx.(*AssignmentContext).key = _x
	}
	{
		p.SetState(13)
		p.Match(GamestateParserT__0)
	}
	{
		p.SetState(14)

		var _x = p.Expression()

		localctx.(*AssignmentContext).value = _x
	}

	return localctx
}

// IExpressionContext is an interface to support dynamic dispatch.
type IExpressionContext interface {
	antlr.ParserRuleContext

	// GetParser returns the parser.
	GetParser() antlr.Parser

	// GetKey returns the key rule contexts.
	GetKey() IExpressionContext

	// GetValue returns the value rule contexts.
	GetValue() IExpressionContext

	// SetKey sets the key rule contexts.
	SetKey(IExpressionContext)

	// SetValue sets the value rule contexts.
	SetValue(IExpressionContext)

	// IsExpressionContext differentiates from other interfaces.
	IsExpressionContext()
}

type ExpressionContext struct {
	*antlr.BaseParserRuleContext
	parser antlr.Parser
	key    IExpressionContext
	value  IExpressionContext
}

func NewEmptyExpressionContext() *ExpressionContext {
	var p = new(ExpressionContext)
	p.BaseParserRuleContext = antlr.NewBaseParserRuleContext(nil, -1)
	p.RuleIndex = GamestateParserRULE_expression
	return p
}

func (*ExpressionContext) IsExpressionContext() {}

func NewExpressionContext(parser antlr.Parser, parent antlr.ParserRuleContext, invokingState int) *ExpressionContext {
	var p = new(ExpressionContext)

	p.BaseParserRuleContext = antlr.NewBaseParserRuleContext(parent, invokingState)

	p.parser = parser
	p.RuleIndex = GamestateParserRULE_expression

	return p
}

func (s *ExpressionContext) GetParser() antlr.Parser { return s.parser }

func (s *ExpressionContext) GetKey() IExpressionContext { return s.key }

func (s *ExpressionContext) GetValue() IExpressionContext { return s.value }

func (s *ExpressionContext) SetKey(v IExpressionContext) { s.key = v }

func (s *ExpressionContext) SetValue(v IExpressionContext) { s.value = v }

func (s *ExpressionContext) STRING() antlr.TerminalNode {
	return s.GetToken(GamestateParserSTRING, 0)
}

func (s *ExpressionContext) ATOM() antlr.TerminalNode {
	return s.GetToken(GamestateParserATOM, 0)
}

func (s *ExpressionContext) AllExpression() []IExpressionContext {
	var ts = s.GetTypedRuleContexts(reflect.TypeOf((*IExpressionContext)(nil)).Elem())
	var tst = make([]IExpressionContext, len(ts))

	for i, t := range ts {
		if t != nil {
			tst[i] = t.(IExpressionContext)
		}
	}

	return tst
}

func (s *ExpressionContext) Expression(i int) IExpressionContext {
	var t = s.GetTypedRuleContext(reflect.TypeOf((*IExpressionContext)(nil)).Elem(), i)

	if t == nil {
		return nil
	}

	return t.(IExpressionContext)
}

func (s *ExpressionContext) GetRuleContext() antlr.RuleContext {
	return s
}

func (s *ExpressionContext) ToStringTree(ruleNames []string, recog antlr.Recognizer) string {
	return antlr.TreesStringTree(s, ruleNames, recog)
}

func (s *ExpressionContext) EnterRule(listener antlr.ParseTreeListener) {
	if listenerT, ok := listener.(GamestateListener); ok {
		listenerT.EnterExpression(s)
	}
}

func (s *ExpressionContext) ExitRule(listener antlr.ParseTreeListener) {
	if listenerT, ok := listener.(GamestateListener); ok {
		listenerT.ExitExpression(s)
	}
}

func (p *GamestateParser) Expression() (localctx IExpressionContext) {
	localctx = NewExpressionContext(p, p.GetParserRuleContext(), p.GetState())
	p.EnterRule(localctx, 4, GamestateParserRULE_expression)
	var _la int

	defer func() {
		p.ExitRule()
	}()

	defer func() {
		if err := recover(); err != nil {
			if v, ok := err.(antlr.RecognitionException); ok {
				localctx.SetException(v)
				p.GetErrorHandler().ReportError(p, v)
				p.GetErrorHandler().Recover(p, v)
			} else {
				panic(err)
			}
		}
	}()

	p.SetState(30)
	p.GetErrorHandler().Sync(p)

	switch p.GetTokenStream().LA(1) {
	case GamestateParserSTRING:
		p.EnterOuterAlt(localctx, 1)
		{
			p.SetState(16)
			p.Match(GamestateParserSTRING)
		}

	case GamestateParserATOM:
		p.EnterOuterAlt(localctx, 2)
		{
			p.SetState(17)
			p.Match(GamestateParserATOM)
		}

	case GamestateParserT__1:
		p.EnterOuterAlt(localctx, 3)
		{
			p.SetState(18)
			p.Match(GamestateParserT__1)
		}
		p.SetState(26)
		p.GetErrorHandler().Sync(p)
		_la = p.GetTokenStream().LA(1)

		for ((_la)&-(0x1f+1)) == 0 && ((1<<uint(_la))&((1<<GamestateParserT__1)|(1<<GamestateParserSTRING)|(1<<GamestateParserATOM))) != 0 {
			{
				p.SetState(19)

				var _x = p.Expression()

				localctx.(*ExpressionContext).key = _x
			}
			p.SetState(22)
			p.GetErrorHandler().Sync(p)
			_la = p.GetTokenStream().LA(1)

			if _la == GamestateParserT__0 {
				{
					p.SetState(20)
					p.Match(GamestateParserT__0)
				}
				{
					p.SetState(21)

					var _x = p.Expression()

					localctx.(*ExpressionContext).value = _x
				}

			}

			p.SetState(28)
			p.GetErrorHandler().Sync(p)
			_la = p.GetTokenStream().LA(1)
		}
		{
			p.SetState(29)
			p.Match(GamestateParserT__2)
		}

	default:
		panic(antlr.NewNoViableAltException(p, nil, nil, nil, nil, nil))
	}

	return localctx
}
