.SILENT:

SHELL := /bin/bash

clean:
	source run.sh && \
	clean

build: clean
	source run.sh && \
	run main