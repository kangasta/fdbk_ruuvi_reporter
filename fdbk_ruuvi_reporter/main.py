import json
from os.path import expanduser
from signal import signal, SIGINT

from ruuvitag_sensor.ruuvi import RuuviTagSensor, RunFlag

from fdbk.utils import create_db_connection
from fdbk_ruuvi_reporter import create_topic_dict, RuuviDataHandler


DATA_FILE = expanduser("~/.fdbk-ruuvi.json")


def read_data():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []

    return data


def add_topic_id(mac, topic_id):
    data = read_data()
    data.append(dict(mac=mac, topic_id=topic_id))

    with open(DATA_FILE, "w") as f:
        json.dump(data, f)


def create_topic(db_connection, db_parameters, name, mac):
    connection = create_db_connection(db_connection, db_parameters)
    topic_id = connection.add_topic(**create_topic_dict(mac, name))

    add_topic_id(mac, topic_id)
    return topic_id


def start_reporting(**kwargs):
    flag = RunFlag()

    def handle_sigint(sig, frame):
        flag.running = False

    sensors = read_data()
    handler = RuuviDataHandler(sensors, **kwargs)
    signal(SIGINT, handle_sigint)

    while flag.running:
        try:
            RuuviTagSensor.get_datas(handler, None, flag)
        except KeyboardInterrupt:
            return
        except Exception:
            pass
