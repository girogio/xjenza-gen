.SILENT:

SHELL := /bin/bash

clean:
	echo -n "Cleaning... "
	rm -rf __pycache__/
	cd outputs && \
	for file in *.aux *.log *.out *.toc *.bbl *.blg *.bcf *.xml *.run.xml *.fls *.fdb_latexmk *.synctex.gz; do \
		if [ -f "$$file" ]; then \
			rm "$$file"; \
		fi; \
	done
	echo "Done"


build: clean
	python3 main.py && \
	$(MAKE) --no-print-directory clean