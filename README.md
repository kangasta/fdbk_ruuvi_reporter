# fdbk_ruuvi_reporter

## Testing

Check and automatically fix formatting with:

```bash
pycodestyle fdbk
autopep8 -aaar --in-place fdbk
```

Run static analysis with:

```bash
pylint -E --enable=invalid-name,unused-import,useless-object-inheritance fdbk
```

Run unit tests with command:

```bash
python3 -m unittest discover -s tst/
```

Get test coverage with commands:

```bash
coverage run --branch --source fdbk/ -m unittest discover -s tst/
coverage report -m
```
