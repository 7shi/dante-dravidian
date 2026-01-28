.PHONY: all clean test

all:

clean:
	rm -f test/*.txt test/*.xml

test:
	uv run test.py
