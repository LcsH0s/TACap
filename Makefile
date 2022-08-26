all: setup

setup:
	brew install graphviz
	export GRAPHVIZ_DIR="/usr/local/Cellar/graphviz/5.0.1"
	python -m pip install pygraphviz --global-option=build_ext --global-option="-I$GRAPHVIZ_DIR/include" --global-option="-L$GRAPHVIZ_DIR/lib"
	python -m pip install -r ./requirements.txt
