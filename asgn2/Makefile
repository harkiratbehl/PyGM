all:
	make clean
	make lexer
	make codegen

codegen: src/codegen.py src/code.py src/lexer.py src/registers.py src/symbol_table.py
	mkdir -p bin
	cp src/*.py bin/
	cp bin/codegen.py bin/codegen
	chmod +x bin/codegen

lexer: src/lexer.py
	mkdir -p bin
	cp src/*.py bin/
	cp bin/lexer.py bin/lexer
	chmod +x bin/lexer

clean:
	rm -rf bin
