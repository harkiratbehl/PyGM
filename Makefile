all:
	make clean
	make codegen
	make lexer
	make parser

codegen:
	mkdir -p bin
	cp src/*.py bin/
	cp bin/codegen.py bin/codegen
	chmod +x bin/codegen

lexer:
	mkdir -p bin
	cp src/*.py bin/
	cp bin/lexer.py bin/lexer
	chmod +x bin/lexer

parser:
	mkdir -p bin
	cp src/*.py bin/
	cp bin/parser.py bin/parser
	chmod +x bin/parser

clean:
	rm -rf bin
