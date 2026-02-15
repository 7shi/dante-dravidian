LANGUAGES = Bengali Bulgarian Dutch Esperanto Estonian \
			French German Hindi Interlingua Japanese \
			Kannada Malayalam Polish Portuguese Serbian \
			Spanish Tamil Telugu Turkish

MODEL = openai:gpt-5.2

.PHONY: all $(LANGUAGES)

REVIEW_FILES = $(patsubst %,1review/%.txt,$(LANGUAGES))
FIX_FILES = $(patsubst %,2fix/%.txt,$(LANGUAGES))
QUOTE_FILES = $(patsubst %,3quote/%.txt,$(LANGUAGES))
SPLIT_FILES = $(patsubst %,4split/%.txt,$(LANGUAGES))

all: $(SPLIT_FILES)

$(LANGUAGES): %: 4split/%.txt

$(REVIEW_FILES): 1review/%.txt: ../gemini3pro/2fix/%.txt
	uv run ../dante.py -m $(MODEL) --outdir 1review/ review $<

$(FIX_FILES): 2fix/%.txt: 1review/%.txt
	uv run ../dante.py -m $(MODEL) --outdir 2fix/ fix $<

$(QUOTE_FILES): 3quote/%.txt: 2fix/%.txt
	uv run ../dante.py -m $(MODEL) --outdir 3quote/ quote $<

$(SPLIT_FILES): 4split/%.txt: 3quote/%.txt
	uv run ../dante.py -m $(MODEL) --outdir 4split/ split $<
