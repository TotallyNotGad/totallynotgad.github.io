build:
	make generate
	hugo --gc --minify

serve:
	hugo serve -p 8006

generate:
	pipenv run python ./scripts/generate.py
