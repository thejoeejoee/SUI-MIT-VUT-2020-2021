PYTHON=.venv/bin/python
PIP=.venv/bin/pip

install-venv:
	python3 -m venv .venv && $(PIP) install -r requirements.txt

evaluate-tournament:
	PYTHONPATH=./:scripts/ $(PYTHON) ./scripts/dicewars-tournament.py --report --game-size 4 --nb-boards 14 --debug --logdir logs