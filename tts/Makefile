LANGUAGES = Bengali Bulgarian Dutch Esperanto Estonian \
			French German Hindi Interlingua Japanese \
			Kannada Malayalam Polish Portuguese Serbian \
			Spanish Tamil Telugu Turkish

WAVDIR1 = 1split
WAVDIR2 = 2norm
TEXTDIR = ../fix/gpt-5.2/4split

.PHONY: all translate wav $(LANGUAGES)

WAV_FILES = $(patsubst %,%.wav,$(LANGUAGES))

all: $(WAV_FILES) Italian.wav English.wav Italian-English.wav

$(LANGUAGES): %: %.wav

$(WAV_FILES): %.wav: $(TEXTDIR)/%.txt
	uv run txt2wav.py $< -m gemini-2.5-pro-preview-tts --outdir $(WAVDIR1)
	uv run normalize_combine.py $(WAVDIR1)/$*-*.wav -o $@ --outdir $(WAVDIR2)

Italian English: %: %.wav

Italian.wav English.wav: %.wav: %.txt
	uv run txt2wav.py $< -m gemini-2.5-pro-preview-tts --outdir $(WAVDIR1)
	uv run normalize_combine.py $(WAVDIR1)/$*-*.wav -o $@ --outdir $(WAVDIR2)

Italian-English.wav: Italian.txt English.txt
	uv run txt2wav.py --multiple $^ -m gemini-2.5-pro-preview-tts --outdir $(WAVDIR1)
	uv run normalize_combine.py $(WAVDIR1)/Italian-English-*.wav -o $@ --outdir $(WAVDIR2)
