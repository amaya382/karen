KAREN := 'Karen-Regular.ttf'
KAREN_PATH := 'out/'${KAREN}

all: prepare_src_font prepare_powerline_fontpatcher clean
	./create_karen.pe
	fontforge -lang=py -script overwrite_unicoderanges.py ${KAREN_PATH}
	fontforge -lang=py -script fontpatcher/scripts/powerline-fontpatcher \
		--no-rename ${KAREN_PATH}
	mv ${KAREN} ${KAREN_PATH}

.PHONY: prepare_dirs
prepare_dirs:
	mkdir -p src tmp out

.PHONY: prepare_src_font
prepare_src_font: prepare_dirs
	#wget

.PHONY: prepare_powerline_fontpatcher
prepare_powerline_fontpatcher:
	git submodule init
	git submodule update

.PHONY: clean
clean:
	rm -r tmp/* out/*

.PHONY: clean-all
clean-all:
	rm -r src tmp out fontpatcher
