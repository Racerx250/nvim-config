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
	local line               = vim.api.nvim_get_current_line()

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

-- things that should be in lua natively but lol
function print_table(my_table) 

	--
	if type(my_table) ~= 'table' then
		print('table given in print_table is of type:', type(my_table))
		return nil
	end
	
	--
	for index, data in ipairs(my_table) do
		print(index)

		for key, value in pairs(data) do
			print('\t', key, value)
		end
	end
end

function refresh_pane() 
	vim.cmd("edit") 
end

function print(message)
	vim.notify(message, vim.log.levels.INFO)
end

-- 
function string:endswith(suffix)
	return self:sub(-#suffix) == suffix
end

function string:startswith(prefix)
	return self:sub(0, #prefix) == prefix
end

function string:split(pat)
	-- holy shit lua is dumb, but I do appreicate its minimalistic approach
	local t = {}  -- NOTE: use {n = 0} in Lua-5.0
	local fpat = "(.-)" .. pat
	local last_end = 1
	local s, e, cap = self:find(fpat, 1)

	-- 
	while s do
		if s ~= 1 or cap ~= "" then
			table.insert(t, cap)
		end
		last_end = e+1
		s, e, cap = self:find(fpat, last_end)
	end

	-- 
	if last_end <= #self then
		cap = self:sub(last_end)
		table.insert(t, cap)
	end

	return t
end

function string:rstrip(sep)
	local split_str = self:split(sep)
	local final_str = split_str[1]

	for i = 2,#split_str-1 do
		final_str = final_str .. sep .. split_str[i]
	end

	return final_str
end

-- debug functions
function print_table(my_table)
	print('printing table')
	for i,v in ipairs(my_table) do
		print(i, v)
	end
end

