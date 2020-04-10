from fdbk import Reporter


class RuuviDataHandler:
    def __init__(self, sensors, **kwargs):
        self._reporters = {}
        for sensor in sensors:
            self._reporters[sensor.get("mac")] = Reporter(
                topic_id=sensor.get("topic_id"), **kwargs)

    def __call__(self, raw_data):
        mac, data = raw_data
        if mac not in self._reporters:
            return

        self._reporters[mac].report(dict(
            temperature=data.get("temperature"),
            humidity=data.get("humidity"),
            pressure=data.get("pressure"),
        ))
