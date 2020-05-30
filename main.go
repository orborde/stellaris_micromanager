package main

import (
	"encoding/json"
	"flag"
	"log"
	"os"
	"stellaris_tools/parser"

	"github.com/antlr/antlr4/runtime/Go/antlr"
)

func translateConfigFile(configFile *parser.ConfigfileContext) map[string][]interface{} {
	result := make(map[string][]interface{})
	for _, assignment := range configFile.AllAssignment() {
		key := translateExpression(assignment.GetKey().(*parser.ExpressionContext)).(string)
		value := translateExpression(assignment.GetValue().(*parser.ExpressionContext))

		result[key] = append(result[key], value)
	}
	return result
}

func isMap(expr *parser.ExpressionContext) bool {
	if expr.GetChildCount() < 3 {
		return false
	}

	terminal, ok := expr.GetChild(2).(antlr.TerminalNode)
	if !ok {
		return false
	}

	return terminal.GetText() == "="
}

func translateExpression(expr *parser.ExpressionContext) interface{} {
	if expr.STRING() != nil {
		return expr.STRING().GetText()
	}

	if expr.ATOM() != nil {
		return expr.ATOM().GetText()
	}

	if isMap(expr) {
		result := make(map[string][]interface{})
		for keyInd := 1; keyInd < expr.GetChildCount()-1; keyInd += 3 {
			key := translateExpression(expr.GetChild(keyInd).(*parser.ExpressionContext)).(string)
			value := translateExpression(expr.GetChild(keyInd + 2).(*parser.ExpressionContext))
			result[key] = append(result[key], value)
		}
		return result
	}

	var result []interface{}
	for i := 1; i < expr.GetChildCount()-1; i++ {
		result = append(result, translateExpression(expr.GetChild(i).(*parser.ExpressionContext)))
	}
	return result
}
func main() {
	infile := flag.String("infile", "", "")
	flag.Parse()

	log.Println("load/parse")
	is, err := antlr.NewFileStream(*infile)
	if err != nil {
		log.Fatal(err)
	}
	lexer := parser.NewGamestateLexer(is)
	stream := antlr.NewCommonTokenStream(lexer, antlr.TokenDefaultChannel)
	p := parser.NewGamestateParser(stream)
	parsed := p.Configfile().(*parser.ConfigfileContext)
	log.Println("translate")
	mess := translateConfigFile(parsed)
	log.Println("encode")
	enc := json.NewEncoder(os.Stdout)
	if err := enc.Encode(mess); err != nil {
		log.Fatal(err)
	}
}
