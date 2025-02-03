local cmp           = require('cmp')
local toggle_status = false

-- 
function setAutoCmp(mode)
  if mode then
    cmp.setup({
      completion = {
        autocomplete = { require('cmp.types').cmp.TriggerEvent.TextChanged }
      }
    })
  else
    cmp.setup({
      completion = {
        autocomplete = false
      }
    })
  end
end

-- 
function toggleAutoCmp()
	if toggle_status == true then
		setAutoCmp(false)
		toggle_status = false
		print("AutoCmp Status: OFF")
	else
		setAutoCmp(true)
		toggle_status = true
		print("AutoCmp Status: ON")
	end	
end

setAutoCmp(toggle_status)

-- enable automatic completion popup on typing
vim.cmd('command AutoCmpOn lua setAutoCmp(true)')

-- disable automatic competion popup on typing
vim.cmd('command AutoCmpOff lua setAutoCmp(false)')

-- 
vim.cmd('command ToggleAutoCmp lua toggleAutoCmp()')

--
vim.keymap.set("n", "<space>ac", function() 
	vim.cmd("ToggleAutoCmp")
end)
