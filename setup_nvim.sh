#!/bin/bash

help() {
	echo "run command as ./copy_model_performance.sh [ download_images BATCH_ID | upload_graphing_file | generate_bias_graphs BATCH_ID | generate_bias_graphs_cvpr BATCH_ID | generate_model_performance_graphs BATCH_ID | generate_graphs BATCH_ID | visualize_scatter BATCH_ID]"
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

# if [[ $1 == 'upload_graphing_file' ]]; then
#     upload_graphing_file
# fi

if [[ $# == 0 ]]; then
    help
    exit 0
fi

