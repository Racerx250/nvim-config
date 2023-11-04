function set_default_theme()
	vim.g.gruvbox_contrast_dark  = "medium"
	vim.g.gruvbox_contrast_light = "hard"
	vim.cmd.colorscheme('gruvbox')
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
	else
		set_default_theme()
	end
end

SetTheme()
