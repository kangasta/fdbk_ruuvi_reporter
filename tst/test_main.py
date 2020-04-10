import json
from os.path import expanduser
import os
from signal import SIGINT
from threading import Timer

from unittest import TestCase
from unittest.mock import MagicMock, patch

from pyfakefs.fake_filesystem_unittest import patchfs

from fdbk_ruuvi_reporter.main import DATA_FILE, read_data, create_topic, start_reporting

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
    def test_create_topic_adds_config_to_config_file(self, db_mock, fs):
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
    def test_start_reporting_returns_on_sigint(self, sensor_mock, handler_mock, fs):
        sensor_mock.get_datas.side_effect = (Exception(), KeyboardInterrupt(),)
        start_reporting()

        handler_mock.assert_called()
        sensor_mock.get_datas.assert_called()

    @patchfs
    @patch("fdbk_ruuvi_reporter.main.RuuviDataHandler")
    @patch("fdbk_ruuvi_reporter.main.RuuviTagSensor")
    def test_stops_reporting_when_flag_is_set_to_false(self, sensor_mock, handler_mock, fs):
        sensor_mock.get_datas.side_effect = mock_get_datas
        start_reporting()

        handler_mock.assert_called()
        sensor_mock.get_datas.assert_called()
