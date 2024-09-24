vim.keymap.set("n", "<space>sc", function() 
	local file_path = vim.api.nvim_buf_get_name(0)

	vim.cmd("!python ~/.config/nvim/python/spellcheck.py --file_path %") 
	refresh_pane()
end)
