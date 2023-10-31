local builtin = require('telescope.builtin')
vim.keymap.set('n', '<space>ff', builtin.find_files, {})
vim.keymap.set('n', '<space>gf', builtin.git_files, {})
vim.keymap.set('n', '<space>ps', function()
	builtin.grep_string({ search = vim.fn.input("Grep > ") });
end)
