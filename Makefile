all: install run

install:
	conda env update -f cfg/environment.yml

run:
	conda run -n tacap-env python3 src/app.py