-- useful tool to see filetype
-- := vim.bo.filetype

require('lint').linters_by_ft = {
	markdown = {'vale'},
	python   = {'pylint'},
}
-- au BufWritePost * lua require('lint').try_lint()

-- local lint = require("lint")
-- local lint_augroup = vim.api.nvim_create_augroup("Lint", { clear = true })
-- 
-- vim.api.nvim_create_autocmd("BufWritePost", {
--   group    = lint_augroup,
--   pattern  = "*",
--   callback = function()
--     lint.try_lint()
--   end,
-- })
--
vim.api.nvim_create_autocmd({ "BufWritePost" }, {
  callback = function()

    -- try_lint without arguments runs the linters defined in `linters_by_ft`
    -- for the current filetype
    require("lint").try_lint()

    -- You can call `try_lint` with a linter name or a list of names to always
    -- run specific linters, independent of the `linters_by_ft` configuration
--     require("lint").try_lint("pylint")
-- 
--     if vim.fn.executable("cspell") == 1 then
--       require("lint").try_lint("cspell")
--     end
  end,
})

