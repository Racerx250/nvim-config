local builtin = require('telescope.builtin')

vim.keymap.set("n", "<space>of", function() 
	vim.cmd("tabnew");
	builtin.find_files({})
end)
