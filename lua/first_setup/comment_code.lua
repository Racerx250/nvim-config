vim.keymap.set("v", "<C-_>", function() 
	-- you have to do this since the locations only get updated when v mode is exited
	change_to_normal_mode()

	local end_row   = vim.fn.getpos("'>")[2]
 	local start_row = vim.fn.getpos("'<")[2]
	
	for line_num=start_row,end_row do
		toggle_comment(line_num)
 	end
end)

vim.keymap.set("n", "<C-_>", function() 
	local line_num, _ = unpack(vim.api.nvim_win_get_cursor(0))
	toggle_comment(line_num)
end)

function toggle_comment(line_num)
	if is_commented(line_num) then
		uncomment_line(line_num)
	else
		comment_line(line_num)
	end
end

function is_commented(line_num)
	--
	local line   = get_line(line_num)
	local file_path  = vim.api.nvim_buf_get_name(0)

	if file_path:endswith".py" and line:startswith('# ') then
		return true
	elseif file_path:endswith".py" then
		return false
	end

	if file_path:endswith".lua" and line:startswith('-- ') then
		return true
	elseif file_path:endswith".lua" then
		return false
	end

	error('FILE TYPE NOT HANDLED ' .. file_path)
	return false
end

function uncomment_line(line_num)
	--
	local old_line   = get_line(line_num)
	local file_path  = vim.api.nvim_buf_get_name(0)
	local new_line   = nil

	if file_path:endswith".py" then
		new_line = old_line:sub(3,-1)
	elseif file_path:endswith".lua" then
		new_line = old_line:sub(4,-1)
	else
		error('FILE TYPE NOT HANDLED ' .. file_path)
	end

	-- local new_line = '-- ' .. old_line
	set_line(line_num, new_line)
end

function comment_line(line_num)
	--
	local old_line   = get_line(line_num)
	local file_path  = vim.api.nvim_buf_get_name(0)
	local new_line   = nil

	if file_path:endswith".py" then
		new_line = '# '	.. old_line
	elseif file_path:endswith".lua" then
		new_line = '-- '	.. old_line
	else
		error('FILE TYPE NOT HANDLED ' .. file_path)
	end

	-- local new_line = '-- ' .. old_line
	set_line(line_num, new_line)
end


