file.pdf: file.tex
	#python main.py
	pdflatex file.tex


.PHONY: clean
.clean:
	rm -f file.pdf
