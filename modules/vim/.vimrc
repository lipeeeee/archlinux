let mapleader = "\<Space>"

" Colorscheme
colorscheme default 

" fun stuff
set nowrap
set number
set noswapfile

" Netrw
nnoremap <Leader>e :Ex<CR>

" Navigation binds
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" Uppercase save & exits
command! -nargs=0 W w
command! -nargs=0 WA wa
command! -nargs=0 Wa wa
command! -nargs=0 WQA wqa
command! -nargs=0 WQa wqa
command! -nargs=0 Wqa wqa
command! -nargs=0 WQ wq
command! -nargs=0 Wq wq
command! -nargs=0 Qa qa
command! -nargs=0 QA qa

" Replace tabs with 2 spaces
set expandtab
set tabstop=2
set shiftwidth=2
