all:
	make clean
	make irgen

irgen: src/lexer.py src/parser.py
	mkdir -p bin
	cp src/*.py bin/
	cp bin/parser.py bin/irgen
	chmod +x bin/irgen

clean:
	rm -rf bin
