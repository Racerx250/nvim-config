config_name = "first_setup"

require(config_name)

-- taken from https://stackoverflow.com/questions/72412720/how-to-source-init-lua-without-restarting-neovim
function reload_config()
	for name,_ in pairs(package.loaded) do
		if name:match('^user') then
			package.loaded[name] = nil
		end
	end

	require(config_name)

	-- Reload after/ directory
	local glob = vim.fn.stdpath('config') .. '/after/**/*.lua'
	local after_lua_filepaths = vim.fn.glob(glob, true, true)

        for _, filepath in ipairs(after_lua_filepaths) do
		dofile(filepath)
	end

	vim.notify("Nvim configuration reloaded!", vim.log.levels.INFO)
end
-- vim.keymap.set('n', '<space><space>=', reload_config)
vim.keymap.set('n', '<space>=r', function()
	vim.cmd('so')
	reload_config()
end)
