function ColorMyPencils(color)
	-- color = color or "rose-pine"
	color = color or "gruvbox"
	vim.g.gruvbox_contrast_dark  = "medium"
	vim.g.gruvbox_contrast_light = "hard"
	vim.cmd.colorscheme(color)

	-- vim.api.nvim_set_hl(0, "Normal", { bg = "none"})
	-- vim.api.nvim_set_hl(0, "NormalNC", { bg = "none"})
	-- vim.api.nvim_set_hl(0, "NormalFloat", { bg = "none"})
end

ColorMyPencils()
