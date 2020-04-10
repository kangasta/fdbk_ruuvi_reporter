from unittest import TestCase
from unittest.mock import Mock, patch

from fdbk_ruuvi_reporter import RuuviTag

class RuuviTagTest(TestCase):
    def test_provides_function_to_create_topic_dict(self):
        tag = RuuviTag("mac", "name", "description")
        data = tag.topic

        self.assertEqual(data.get("name"), "name")
        self.assertEqual(data.get("type_str"), "ruuvitag")
        self.assertEqual(data.get("description"), "description")
        self.assertEqual(data.get("metadata").get("mac"), "mac")

    def test_mac_is_used_as_name_dy_default(self):
        tag = RuuviTag("mac")
        data = tag.topic

        self.assertEqual(data.get("name"), "mac")
        self.assertEqual(data.get("type_str"), "ruuvitag")
        self.assertEqual(data.get("description"), None)
        self.assertEqual(data.get("metadata").get("mac"), "mac")
