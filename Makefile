
auswertung.pdf:
	pdflatex auswertung.tex

spellcheck:
	aspell -t -x -c -p .aspell.de.pws auswertung.tex
