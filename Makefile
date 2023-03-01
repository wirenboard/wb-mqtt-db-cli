.PHONY: all clean

PREFIX = /usr

all:
clean :

install: all
	install -Dm0755 wb-mqtt-db-cli.py $(DESTDIR)$(PREFIX)/bin/wb-mqtt-db-cli
