.PHONY: all clean

all:
clean :

install: all
	mkdir -p $(DESTDIR)/usr/bin
	install -m 0755 	wb-mqtt-db-cli.py $(DESTDIR)/usr/bin/wb-mqtt-db-cli






