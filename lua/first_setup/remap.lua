vim.g.mapleader = " "

-- 
vim.keymap.set("n", "<space>pv", function() 
	vim.cmd("Ex") 
end)
vim.keymap.set("n", "<space>ex", function() 
	vim.cmd("tabnew") 
	vim.cmd("Ex") 
end)
vim.keymap.set("n", "<space>tb", function() 
	vim.cmd("tabnew") 
end)

-- 
vim.keymap.set('v', 'J', ":m '>+1<CR>gv=gv")
vim.keymap.set('v', 'K', ":m '<-2<CR>gv=gv")



