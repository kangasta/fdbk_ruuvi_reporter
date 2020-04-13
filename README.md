# fdbk_ruuvi_reporter

[![Build Status](https://travis-ci.org/kangasta/fdbk_ruuvi_reporter.svg?branch=master)](https://travis-ci.org/kangasta/fdbk_ruuvi_reporter)

## Installation

Run:

```bash
pip install fdbk_ruuvi_reporter
```

to install from [PyPI](https://pypi.org/project/fdbk_ruuvi_reporter/) or download this repository and run

```bash
python setup.py install
```

to install from sources.

## Testing

Check and automatically fix formatting with:

```bash
pycodestyle fdbk_ruuvi_reporter
autopep8 -aaar --in-place fdbk_ruuvi_reporter
```

Run static analysis with:

```bash
pylint -E --enable=invalid-name,unused-import,useless-object-inheritance fdbk_ruuvi_reporter
```

Run unit tests with command:

```bash
python3 -m unittest discover -s tst/
```

Get test coverage with commands:

```bash
coverage run --branch --source fdbk_ruuvi_reporter/ -m unittest discover -s tst/
coverage report -m
```
