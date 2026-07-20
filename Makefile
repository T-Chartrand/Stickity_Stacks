VERSION=$(shell cat VERSION)

linux:
	./scripts/build-linux.sh

arch:
	cd packaging/arch && makepkg -si

clean:
	rm -rf build releases/linux/*

release:
	./scripts/release.sh
