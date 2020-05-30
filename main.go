package main

import (
	"flag"
	"log"
	"stellaris_tools/parser"

	"github.com/antlr/antlr4/runtime/Go/antlr"
)

func main() {
	infile := flag.String("infile", "", "")
	flag.Parse()

	is, err := antlr.NewFileStream(*infile)
	if err != nil {
		log.Fatal(err)
	}
	lexer := parser.NewGamestateLexer(is)
	stream := antlr.NewCommonTokenStream(lexer, antlr.TokenDefaultChannel)
	p := parser.NewGamestateParser(stream)
	parsed := p.Configfile()
	log.Print(parsed)
}
