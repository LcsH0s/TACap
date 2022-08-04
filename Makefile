all: conda exec

conda:
	conda create --name gt -c conda-forge graph-tool