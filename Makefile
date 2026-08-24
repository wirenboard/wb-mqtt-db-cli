.PHONY: all clean

PREFIX = /usr

all:
clean :

install:
	install -Dm0755 wb-mqtt-db-cli.py $(DESTDIR)$(PREFIX)/bin/wb-mqtt-db-cli
	install -Dm0644 completions/*.bash -t $(DESTDIR)$(PREFIX)/share/bash-completion/completions
