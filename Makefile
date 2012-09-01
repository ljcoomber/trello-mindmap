.PHONY: check clean setup

setup: env
	. env/bin/activate && pip install trollop pystache

virtualenv.py:
	curl https://raw.github.com/pypa/virtualenv/master/virtualenv.py --output virtualenv.py

env: virtualenv.py
	python virtualenv.py env
	rm virtualenv.py*

clean:
	rm -rf env