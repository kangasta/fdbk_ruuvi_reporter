# fdbk_ruuvi_reporter

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
