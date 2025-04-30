alias gg="lazygit"
alias ..="cd .."

# Git
alias ga="git add"
alias gs="git status"
alias gc="git commit"
alias gp="git push"
# Get all remote branches
# Commented because wsl randomly executes this command and results in an error on startup(xd)
# alias getbranches="for b in `git branch -r | grep -v -- '->'`; do git branch --track ${b##origin/} $b; done"

# ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Nvim
# We should put point nvim to /usr/bin but w.e, this causes a bit of confusion
# when refactoring things 
alias nvim="/squashfs-root/usr/bin/nvim"
alias nv=nvim
alias nvimcfg="cd ~/.config/nvim"

# vim
alias v=vim

# Goto aliases
alias dev="cd $DEV"
alias godev=dev
alias nvcfg="cd ~/.config/nvim"
alias nvimcfg=nvcfg

# tmux aliases
alias t="tmux"
alias ts="tmux-sessionizer"
alias tp="tmux-persistent"
