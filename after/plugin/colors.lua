function set_default_theme()
	vim.g.gruvbox_contrast_dark  = "medium"
	vim.g.gruvbox_contrast_light = "hard"
	vim.cmd.colorscheme('gruvbox')
	vim.cmd.AirlineTheme('night_owl')

-- airline themes which arent too bad 
-- seagull 
-- night_owl
-- transparent
end

function set_everforest_theme_1()
	vim.g.everforest_background = "hard"
	vim.g.everforest_diagnostic_text_highlight = "0"
	vim.g.everforest_transparent_background = "0"
	vim.g.everforest_ui_contrast = "low"
	vim.g.everforest_float_style = "bright"
	vim.cmd.colorscheme('everforest')

-- 	print_table(vim.cmd)
end

function set_devone_theme()
	color = 'rose-pine'
	vim.api.nvim_set_hl(0, "Normal", { bg = "none"})
	vim.api.nvim_set_hl(0, "NormalNC", { bg = "none"})
	vim.api.nvim_set_hl(0, "NormalFloat", { bg = "none"})
end

function SetTheme()
	local hostname = vim.fn.hostname()

	if hostname == 'pop-os' then
		set_devone_theme()
	elseif hostname == 'DESKTOP-JOGS6KI' then
		set_default_theme()
-- 		set_everforest_theme_1()
	else
		set_default_theme()
	end



end

SetTheme()
