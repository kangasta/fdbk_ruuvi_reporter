import json
from os.path import expanduser
import os
from signal import SIGINT
from threading import Timer

from unittest import TestCase
from unittest.mock import MagicMock, patch

from pyfakefs.fake_filesystem_unittest import patchfs

from fdbk_ruuvi_reporter.main import DATA_FILE, read_data, read_data_from_db, create_topic, start_reporting, update_topics
from fdbk_ruuvi_reporter._topic import FIELDS, UNITS, DATA_TOOLS

V0_TOPIC = dict(
    name="Test v0",
    id="test_v0_id",
    template=None,
    type="ruuvitag",
    description="description",
    fields=FIELDS,
    units=UNITS,
    data_tools=DATA_TOOLS,
    metadata=dict(mac="mac"),
)

def mock_get_datas(handler, macs, flag):
    flag.running = False

class RuuviTagTest(TestCase):
    @patchfs
    def test_read_data_returns_empty_lïst_if_file_not_found(self, fs):
        data = read_data()
        self.assertEqual([], data)

    @patchfs
    def test_read_data_reads_config_file(self, fs):
        config_data = [dict(mac="mac", topic_id="topic_id")]
        fs.create_file(DATA_FILE, contents=json.dumps(config_data))

        data = read_data()
        self.assertEqual(config_data, data)

    @patchfs
    @patch("fdbk_ruuvi_reporter.main.create_db_connection")
    def test_create_topic_adds_config_to_config_file(self, fs, db_mock):
        fs.makedirs(expanduser("~/"))
        connection = MagicMock()
        connection.add_topic.return_value = "topic_id"
        db_mock.return_value = connection

        params = ("connection", ["params"], )
        topic_id = create_topic(*params, "name", "mac")
        self.assertEqual(topic_id, "topic_id")

        db_mock.assert_called()
        connection.add_topic.assert_called()

        data = read_data()
        self.assertEqual(data, [dict(mac="mac", topic_id="topic_id")])

    @patchfs
    @patch("fdbk_ruuvi_reporter.main.RuuviDataHandler")
    @patch("fdbk_ruuvi_reporter.main.RuuviTagSensor")
    def test_start_reporting_returns_on_sigint(self, fs, sensor_mock, handler_mock):
        sensor_mock.get_datas.side_effect = (Exception(), KeyboardInterrupt(),)
        start_reporting()

        handler_mock.assert_called()
        sensor_mock.get_datas.assert_called()

    @patchfs
    @patch("fdbk_ruuvi_reporter.main.RuuviDataHandler")
    @patch("fdbk_ruuvi_reporter.main.RuuviTagSensor")
    def test_stops_reporting_when_flag_is_set_to_false(self, fs, sensor_mock, handler_mock):
        sensor_mock.get_datas.side_effect = mock_get_datas
        start_reporting()

        handler_mock.assert_called()
        sensor_mock.get_datas.assert_called()

    @patchfs
    def test_read_data_from_db(self, fs):
        dict_params = ("DictConnection", (expanduser("~/.fdbk.json"), ), )

        fs.makedirs(expanduser("~/"))
        create_topic(*dict_params, "name1", "mac1")
        create_topic(*dict_params, "name1", "mac1")
        data = read_data()

        fs.remove_object(DATA_FILE)
        self.assertEqual(read_data(), [])

        read_data_from_db(*dict_params)
        self.assertEqual(read_data(), data)

    @patchfs
    def test_update_topics(self, fs):
        fs.create_file(expanduser("~/.fdbk.json"), contents=json.dumps(dict(topics=[V0_TOPIC])))
        dict_params = ("DictConnection", (expanduser("~/.fdbk.json"), ), )

        update_topics(*dict_params)

        with open(expanduser("~/.fdbk.json"), 'r') as f:
            topics = json.load(f).get('topics')

        self.assertEqual(len(topics), 2)

        self.assertEqual(topics[0]["type"], "topic")
        self.assertEqual(topics[0]["template"], "ruuvitag")

        self.assertEqual(topics[1]["type"], "template")
        self.assertEqual(topics[1]["template"], None)
