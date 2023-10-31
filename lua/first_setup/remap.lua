-- vim.g.mapleader = " "
-- vim.keymap.set("n", "<leader>pv", function() vim.cmd("Ex") end)
vim.keymap.set('n', '<space>ex', function()
	vim.cmd("tabnew")
	vim.cmd("Ex")
end)
