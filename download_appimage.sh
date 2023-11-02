#!/bin/bash
set -eu
nvim="$HOME/.local/bin/nvim"
nvimurl="https://github.com/neovim/neovim/releases/download/v0.9.0/nvim.appimage"
mkdir -p "$(dirname "$nvim")"
curl -fL "$nvimurl" -o "$nvim" -z "$nvim"
chmod u+x "$nvim"
