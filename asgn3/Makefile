all:
	make clean
	make parser

parser: src/lexer.py src/parser.py
	mkdir -p bin
	cp src/*.py bin/
	cp bin/parser.py bin/parser
	chmod +x bin/parser

clean:
	rm -rf bin
