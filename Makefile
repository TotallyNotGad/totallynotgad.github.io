build:
	make generate
	hugo --gc --minify

serve:
	./hugo serve -p 8006

generate:
	python ./scripts/generate.py
