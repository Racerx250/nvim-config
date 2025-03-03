-- 
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
vim.keymap.set("n", "<space><space>n", function() 
	vim.wo.relativenumber = not vim.wo.relativenumber
end)
vim.keymap.set("n", "<space>tr", function() 
	vim.cmd("tabm +1")
end)
vim.keymap.set("n", "<space>tl", function() 
	vim.cmd("tabm -1")
end)
vim.keymap.set("n", "<space>wr", function() 
	vim.cmd("windo e")
end)
vim.keymap.set("n", "<space>qr", function() 
	vim.cmd(".+1,$tabdo :tabc")
end)
-- vim.keymap.set("n", "<space>=r", function() 
-- 	local nvim_config_dir = '~/.config/nvim'
-- 	local init_lua_path   = nvim_config_dir .. '/init.lua'
-- 	vim.cmd('luafile ' .. init_lua_path)
-- 	print('Refreshed a:', init_lua_path)
-- end)


-- 
vim.keymap.set('v', 'J', ":m '>+1<CR>gv=gv")
vim.keymap.set('v', 'K', ":m '<-2<CR>gv=gv")

-- NOTES
-- cw is a great way to quickly change a word, dw deletes a word
-- visual mode then command "left" automatically left aligns everything highlighted
-- check TODOs in the README.md
