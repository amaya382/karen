KAREN := Karen-Regular.ttf
KAREN_PATH := out/${KAREN}

.PHONY: all
all: prepare_src_font prepare_powerline_fontpatcher clean
	fontforge -lang=py -script create_karen.py
	cd fontmerger && bin/fontmerger -v --all -o ../out ../${KAREN_PATH}
	mv out/Karen.ttf ${KAREN_PATH}
	fontforge -lang=py -script fix_powerline.py

.PHONY: prepare_dirs
prepare_dirs:
	mkdir -p src out

.PHONY: prepare_src_font
prepare_src_font: prepare_dirs
	[ -f src/GenShinGothic-Monospace-Regular.ttf ] || ( \
		wget https://osdn.jp/downloads/users/8/8637/genshingothic-20150607.zip && \
		unzip -od src genshingothic-20150607.zip GenShinGothic-Monospace-Regular.ttf && \
		rm genshingothic-20150607.zip \
	)
	[ -f src/UbuntuMono-R.ttf ] || ( \
		wget https://assets.ubuntu.com/v1/fad7939b-ubuntu-font-family-0.83.zip \
			-O ubuntu-mono.zip && \
		unzip -od src ubuntu-mono.zip && \
		mv src/ubuntu-font-family-*/UbuntuMono-R.ttf src && \
		rm -r ubuntu-mono.zip src/ubuntu-font-family-* \
	)
	[ -f src/Hack-Regular.ttf ] || ( \
		wget https://github.com/source-foundry/Hack/releases/download/v3.003/Hack-v3.003-ttf.zip \
			-O Hack.zip && \
		unzip -od src Hack.zip && \
		mv src/ttf/Hack-Regular.ttf src && \
		rm -r Hack.zip src/ttf \
	)
	[ -f src/NotoEmoji-Regular.ttf ] || ( \
		wget https://github.com/googlei18n/noto-emoji/raw/master/fonts/NotoEmoji-Regular.ttf \
			-O src/NotoEmoji-Regular.ttf \
	)

.PHONY: prepare_powerline_fontpatcher
prepare_powerline_fontpatcher:
	git submodule init
	git submodule update

.PHONY: clean
clean:
	rm -rf out/*

.PHONY: clean-all
clean-all:
	rm -rf src out
