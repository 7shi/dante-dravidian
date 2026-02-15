LANGUAGES = Bengali Bulgarian Dutch Esperanto Estonian \
			French German Hindi Interlingua Japanese \
			Kannada Malayalam Polish Portuguese Serbian \
			Spanish Tamil Telugu Turkish

MODEL = google:gemini-3-pro-preview

.PHONY: all $(LANGUAGES)

REVIEW_FILES = $(patsubst %,1review/%.txt,$(LANGUAGES))
FIX_FILES = $(patsubst %,2fix/%.txt,$(LANGUAGES))

all: $(FIX_FILES)

$(LANGUAGES): %: 2fix/%.txt

$(REVIEW_FILES): 1review/%.txt: ../../test/%.txt
	uv run ../dante.py -m $(MODEL) --outdir 1review/ review $<

$(FIX_FILES): 2fix/%.txt: 1review/%.txt
	uv run ../dante.py -m $(MODEL) --outdir 2fix/ fix $<
