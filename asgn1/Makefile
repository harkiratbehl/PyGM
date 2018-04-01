all:
	make clean
	make lexer

lexer: src/lexer.py
	mkdir -p bin
	cp src/*.py bin/
	cp bin/lexer.py bin/lexer
	chmod +x bin/lexer

clean:
	rm -rf bin
