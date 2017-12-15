all: talk-slides.pdf talk-handout.pdf talk-slides-heldback.pdf talk-handout-heldback.pdf

%.pdf: %.tex .FORCE
	mkdir -p build
	latexmk -f -pdflatex="lualatex -shell-escape -interaction=nonstopmode -file-line-error" -recorder -output-directory=build -pdf $<
	cp build/$@ $@

clean:
	latexmk -CA -output-directory=build

.FORCE:

.PHONY: all clean .FORCE

# vim: ft=make
