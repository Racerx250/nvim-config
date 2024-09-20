function compile_document()
	-- 
	local main_document = get_main_document()
		
	-- 
	pdf_cmd             = "pdflatex " .. main_document

	-- 
	full_cmd            = pdf_cmd
	
	-- for more: https://www.reddit.com/r/neovim/comments/y2by27/is_there_a_way_to_run_terminal_commands_with_lua/
	local job = vim.fn.jobstart(
		full_cmd, 
		{
			cwd       = nil,
			on_exit   = function() end,
			on_stdout = function() end,
			on_stderr = function() end
		}
	)
end

function compile_bibliography()
	-- 
	local main_fname    = get_main_fname()
		
	-- 
	bib_cmd             = "bibtex " .. main_fname

	-- 
	full_cmd            = bib_cmd
	
	-- for more: https://www.reddit.com/r/neovim/comments/y2by27/is_there_a_way_to_run_terminal_commands_with_lua/
	local job = vim.fn.jobstart(
		full_cmd, 
		{
			cwd       = nil,
			on_exit   = function() end,
			on_stdout = function() end,
			on_stderr = function() end
		}
	)
end

function get_main_document()
	local f_path = "document/main"
	return f_path:rstrip('.tex')
end

function get_main_fname()
	local main_document = get_main_document()
	local split_string  = main_document:split('/')
	return split_string[#split_string]
end

vim.keymap.set("n", "<space>ld", function()
	compile_document()
end)
vim.keymap.set("n", "<space>lb", function()
	compile_bibliography()
end)
