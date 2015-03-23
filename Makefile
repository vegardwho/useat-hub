.PHONY: serve
serve:
	python -m SimpleHTTPServer

.PHONY: sense
sense:
	python read_thermal.py
