# fdbk_ruuvi_reporter

![CI](https://github.com/kangasta/fdbk_ruuvi_reporter/workflows/CI/badge.svg)
![Release](https://github.com/kangasta/fdbk_ruuvi_reporter/workflows/Release/badge.svg)

## Getting started

_Originally published in [a Medium post](https://medium.com/@kangasta/indoor-weather-monitoring-transmitting-the-data-from-the-sensor-to-the-cloud-8c51f84f2abe?source=friends_link&sk=137ee2b0640f3c328efee64760191c73)._

Following steps assume that you have some RuuviTags transmitting data near the Raspberry Pi. The steps also require some Raspberry Pi, Unix, and AWS knowledge:

- Setup a Raspberry Pi with a fresh Rasbian, connect it to internet, change your password, and optionally enable SSH.
- Install required software dependencies on the Raspberry Pi:

```bash
sudo apt-get update
sudo apt-get install bluez-hcidump python3 python3-pip
sudo pip3 install fdbk_ruuvi_reporter fdbk_dynamodb_plugin
```

- Create AWS DynamoDB tables and a reporter user with [CloudFormation template](https://raw.githubusercontent.com/kangasta/fdbk_dynamodb_plugin/master/fdbk_tables.template.yaml).
- Create Access key for the reporter user in AWS. Configure the access keys and region to the `~/.aws` directory on the Raspberry Pi.
- On Raspberry Pi, create topics for your RuuviTags with `fdbk-ruuvi-reporter --create-topic ${name} ${mac} --db-connection fdbk_dynamodb_plugin` where `${name}` is the name for your sensor and `${mac}` is the MAC address of the RuuviTag.
- Try to run the reporter with `fdbk-ruuvi-reporter -v -i 10 --db-connection fdbk_dynamodb_plugin`, where `-v` is for verbose, `-i 10` sets data push interval to ten seconds, and `--db-connection fdbk_dynamodb_plugin` specifies database connection to be used, here DynamoDB. Check from the AWS console that data is being transmitted.
- Configure fdbk-ruuvi-reporter to start on reboot with `crontab -e`. For example, to transmit data every 15 minutes with output directed to file `/home/pi/.reporter-log.txt`, the crontab row would be:

```bash
@reboot /usr/local/bin/fdbk-ruuvi-reporter -v -i 900 --db-connection fdbk_dynamodb_plugin > /home/pi/.reporter-log.txt
```

- Reboot the Raspberry Pi and check from the AWS console that data is being transmitted.

To access the data via fdbk development server on your development computer: Install `fdbk` and `fdbk_dynamodb_plugin`. Configure AWS credentials with read access rights to both topics and data tables. Run `fdbk-server`, which is provided by `fdbk` package, with DynamoDB plugin as the DB connection: `fdbk-server --db-connection fdbk_dynamodb_plugin`. Navigate to [http://localhost:8080/overview](http://localhost:8080/overview) to access overview of the data.

## Development

### Installation

Run:

```bash
pip install fdbk_ruuvi_reporter
```

to install from [PyPI](https://pypi.org/project/fdbk_ruuvi_reporter/) or download this repository and run

```bash
python setup.py install
```

to install from sources.

### Testing

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
