function set_line(line_num, line)
	-- 
	local orig_row, orig_col = unpack(vim.api.nvim_win_get_cursor(0))

	--
	vim.api.nvim_win_set_cursor(0, {line_num, 0})
	vim.api.nvim_set_current_line(line)

	--
	vim.api.nvim_win_set_cursor(0, {orig_row, orig_col})
end

function get_line(line_num)
	-- 
	local orig_row, orig_col = unpack(vim.api.nvim_win_get_cursor(0))

	--
	vim.api.nvim_win_set_cursor(0, {line_num, 0})
	local line                 = vim.api.nvim_get_current_line()

	--
	vim.api.nvim_win_set_cursor(0, {orig_row, orig_col})

	return line
end

function change_to_normal_mode()
	vim.api.nvim_feedkeys(vim.api.nvim_replace_termcodes("<esc>", true, false, true), 'x', true)
end

function change_to_insert_mode()
	vim.api.nvim_feedkeys(vim.api.nvim_replace_termcodes("<esc>", true, false, true), 'x', true)
	vim.api.nvim_feedkeys(vim.api.nvim_replace_termcodes("i", true, false, true), 'x!', true)
end

-- 
function string:endswith(suffix)
	return self:sub(-#suffix) == suffix
end

function string:startswith(prefix)
	return self:sub(0, #prefix) == prefix
end

