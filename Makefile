all:
	make clean
	make compiler

compiler:
	mkdir -p bin
	cp src/*.py bin/
	cp bin/parser.py bin/go-compiler
	chmod +x bin/go-compiler

clean:
	rm -rf bin
