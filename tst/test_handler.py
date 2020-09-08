from unittest import TestCase
from unittest.mock import MagicMock, patch

from fdbk_ruuvi_reporter import RuuviDataHandler

SENSORS = [
    dict(mac="mac", topic_id="topic_id")
]

class RuuviTagTest(TestCase):
    def test_handler_does_nothing_on_unkwon_mac(self):
        handler = RuuviDataHandler(SENSORS, db_connection="DictConnection")
        r = handler(["unknown", None])
        self.assertIsNone(r)

    @patch("fdbk_ruuvi_reporter._handler.Reporter")
    def test_handler_calls_report_on_new_data(self, reporter_mock):
        reporter = MagicMock()
        reporter_mock.return_value = reporter
        handler = RuuviDataHandler(SENSORS, db_plugin="DictConnection")
        data = dict(temperature=20, humidity=50, pressure=1013)
        r = handler(["mac", data])
        reporter.report.assert_called_with(data)
