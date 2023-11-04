vim.keymap.set({"n", "t"}, "<C-\\>", function()
	vim.cmd("FloatermToggle")
end)

vim.keymap.set("n", "<space><space>e", function()
	local file_path = vim.api.nvim_buf_get_name(0)
	local cmd       = "python " .. file_path
	run_then_exit(cmd)
end)

function run_then_exit(cmd)
	local final_cmd = "FloatermNew! --autoclose=0 " 
	final_cmd       = final_cmd .. cmd
	final_cmd       = final_cmd .. "; read -n 1 -s -r -p \"Press any key to continue\""
	final_cmd       = final_cmd .. "; exit"
	print(final_cmd)
	vim.cmd(final_cmd)
end

cmd_1 = nil
vim.keymap.set("n", "<space>e1", function()
	cmd_1 = vim.fn.input("cmd > ")
	print("Command 1 Set: \"" .. cmd_1 .. "\"")
end)
vim.keymap.set("n", "<space><space>1", function()
	if cmd_1 == nil then
		cmd_1 = vim.fn.input("cmd > ")
	end

	run_then_exit(cmd_1)
end)

cmd_2 = nil
vim.keymap.set("n", "<space>e2", function()
	cmd_2 = vim.fn.input("cmd > ")
	print("Command 2 Set: \"" .. cmd_2 .. "\"")
end)
vim.keymap.set("n", "<space><space>2", function()
	if cmd_2 == nil then
		cmd_2 = vim.fn.input("cmd > ")
	end

	run_then_exit(cmd_2)
end)
