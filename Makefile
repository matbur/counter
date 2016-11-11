file.pdf: file.tex latex.py
	#python main.py
	pdflatex file.tex


.PHONY: clean
.clean:
	rm -f file.pdf
