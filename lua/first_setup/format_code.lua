vim.keymap.set("n", "<space>fc", function() 
	local file_path = vim.api.nvim_buf_get_name(0)

	if file_path:endswith".py" then
-- 		vim.cmd("!python ~/.config/nvim/python/format_code.py --file_path %") 
-- 		vim.cmd("!python ~/.config/nvim/python/format_py_func_signatures.py --file_path %") 
		vim.cmd("!python $MISC_UTILS_DIR/format_pyfpath_signatures.py --file_path %") 
		refresh_pane()
		return 
	end

	print('[file_formatter]: file format not recognized!')
end)
