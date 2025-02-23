local toggle_paste = false

-- 
function togglePasteMode()
	if toggle_paste == true then
		vim.cmd('set nopaste')
		toggle_paste = false
		print("PasteMode Status: OFF")
	else
		vim.cmd('set paste')
		toggle_paste = true
		print("PasteMode Status: ON")
	end	
end

-- 
vim.cmd('command TogglePasteMode lua togglePasteMode()')

--
vim.keymap.set("n", "<space>tp", function() 
	vim.cmd("TogglePasteMode")
end)
