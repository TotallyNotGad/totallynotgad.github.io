build:
	- clear
	make generate
	- clear
	hugo --gc --minify

serve:
	- clear
	./hugo serve -p 8006

generate:
		- clear
		- make clear
		python ./scripts/generate.py

clear:
	- find . -wholename "./content/*/*" ! -name "_index.md" -exec rm -rf {} \;
	- rm -rf temp
