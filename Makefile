file.pdf: file.tex
	pdflatex file.tex 1>/dev/null
	rm file.log file.aux


.PHONY: clean
.clean:
	rm -f file.pdf
