all:
	make clean
	make lexer
	make codegen

codegen:
	mkdir -p bin
	cp src/*.py bin/
	cp bin/codegen.py bin/codegen
	chmod +x bin/codegen

lexer:
	mkdir -p bin
	cp src/lexer.py bin/lexer
	chmod +x bin/lexer

clean:
	rm -rf bin
