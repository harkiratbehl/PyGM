all:
	make clean
	mkdir bin
	cp src/lexer.py bin/lexer
	chmod +x bin/lexer

clean:
	rm -rf bin
