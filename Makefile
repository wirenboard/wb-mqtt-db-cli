.PHONY: all clean

PREFIX = /usr

all:
clean :

install:
	install -Dm0755 wb-mqtt-db-cli.py $(DESTDIR)$(PREFIX)/bin/wb-mqtt-db-cli
	install -Dm0644 completions/*.bash -t $(DESTDIR)$(PREFIX)/share/bash-completion/completions
	install -Dm0644 completions/*.fish -t $(DESTDIR)$(PREFIX)/share/fish/completions
	install -Dm0644 completions/_* -t $(DESTDIR)$(PREFIX)/share/zsh/vendor-completions
