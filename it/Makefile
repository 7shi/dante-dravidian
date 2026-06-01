URL = https://www.gutenberg.org/ebooks/1000
TARGET = pg1000.txt

all: $(TARGET)

$(TARGET):
	wget --trust-server-names $(URL).txt.utf-8

split: $(TARGET)
	python split.py < $(TARGET)

# Scene breakdowns (one .md per canticle, plus a per-canto NN.json next to each
# NN.txt source). Resumable: a full run skips cantos that already have a JSON.
# Override the model with e.g. `make scenes MODEL=google:gemini-3-pro-preview`.
MODEL ?=
SCENES = inferno.md purgatorio.md paradiso.md

scenes: $(SCENES)

$(SCENES): %.md: %
	uv run python scene.py $< $(if $(MODEL),-m $(MODEL)) -o $@

.PHONY: all split scenes
