#!/bin/bash

help() {
	echo "run command as ./setup_nvim.sh [ all ]"
}

download_appimage() {
	set -eu
	nvim="$HOME/.local/bin/nvim"
	nvimurl="https://github.com/neovim/neovim/releases/download/v0.9.0/nvim.appimage"
	mkdir -p "$(dirname "$nvim")"
	curl -fL "$nvimurl" -o "$nvim" -z "$nvim"
	chmod u+x "$nvim"
}

install_fuse() {
	sudo apt-get install fuse libfuse2
}

get_packer() {
	cd /tmp
	git clone --depth 1 https://github.com/wbthomason/packer.nvim ~/.local/share/nvim/site/pack/packer/start/packer.nvim/
}

if [[ $1 == 'all' ]]; then
	download_appimage
	install_fuse
	get_packer
fi

if [[ $# == 0 ]]; then
    help
    exit 0
fi

