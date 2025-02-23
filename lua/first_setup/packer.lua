-- This file can be loaded by calling `lua require('plugins')` from your init.vim
-- steps:
-- 1) :so
-- 2) PackerSync
print(os.date(), 'sourced packer.lua')

-- Only required if you have packer configured as `opt`
vim.cmd [[packadd packer.nvim]]

return require('packer').startup(function(use)
	-- Packer can manage itself
	use('wbthomason/packer.nvim')


	use {
		'nvim-telescope/telescope.nvim',
		tag = '0.1.1',
		requires = { {'nvim-lua/plenary.nvim'} }
	}

	
	-- primary theme, for desktop / other
	use('ellisonleao/gruvbox.nvim')

	-- theme for laptop
	use {
		'rose-pine/neovim',
		as = 'rose-pine',
		config = function()
			require("rose-pine").setup()
			vim.cmd('colorscheme rose-pine')
		end
	}

	-- secondary themes
	use {
		'nordtheme/vim',
		tag = 'v0.19.0'
	}
	use {
		'sainnhe/everforest',
		tag = 'v0.3.0'
	}
	
	--
	use {
		'nvim-treesitter/nvim-treesitter',
		tag = 'v0.9.0'
	}

	-- use('nvim-treesitter/playground')
	
	--
	use {
		'vim-airline/vim-airline',
		tag = 'v0.9'
	}
	use('vim-airline/vim-airline-themes')


-- 	use {
-- 		'edkolev/tmuxline.vim',
-- 		tag = 'v1.0'
-- 	}
	
	--
	use {
		'theprimeagen/harpoon',
		requires = {
			'nvim-lua/plenary.nvim'	
		}
	}
	
	-- 
	use('tpope/vim-fugitive')

	-- 
	use('preservim/nerdtree')

	-- 
	use('voldikss/vim-floaterm')

	use {
		'VonHeikemen/lsp-zero.nvim',
		branch = 'v1.x',
		requires = {
			-- LSP Support
			{'neovim/nvim-lspconfig'},             -- Required
			{'williamboman/mason.nvim'},           -- Optional
			{'williamboman/mason-lspconfig.nvim'}, -- Optional

			-- Autocompletion
			{'hrsh7th/nvim-cmp'},         -- Required
			{'hrsh7th/cmp-nvim-lsp'},     -- Required
			{'hrsh7th/cmp-buffer'},       -- Optional
			{'hrsh7th/cmp-path'},         -- Optional
			{'saadparwaiz1/cmp_luasnip'}, -- Optional
			{'hrsh7th/cmp-nvim-lua'},     -- Optional

			-- Snippets
			{'L3MON4D3/LuaSnip'},             -- Required
			{'rafamadriz/friendly-snippets'}, -- Optional
		}
	}

end)
