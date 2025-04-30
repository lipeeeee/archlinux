# Tmux copy buffer to windows clipboard
cpt() {
	tmux show-buffer | clip.exe
}

# Fast compiler for simple c files
# gcc file.c && ./a.out
makec() {
  gcc $1 && ./a.out
  rm ./a.out
}
