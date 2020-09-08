FIELDS = ['temperature', 'humidity', 'pressure']


UNITS = [
    dict(field='temperature', unit="celsius"),
    dict(field='humidity', unit="celsius"),
    dict(field='pressure', unit="hectopascal"),
]


DATA_TOOLS = [
    dict(field='temperature', method="latest"),
    dict(field='humidity', method="latest"),
    dict(field='pressure', method="latest"),
    dict(field='temperature', method="line"),
    dict(field='humidity', method="line"),
    dict(field='pressure', method="line"),
]


TEMPLATE_DICT = dict(
    name="ruuvitag",
    type_str="template",
    fields=FIELDS,
    units=UNITS,
    data_tools=DATA_TOOLS,
)


def create_topic_dict(mac, name=None, description=None, id_str=None):
    if not name:
        name = mac

    return dict(
        name=name,
        id_str=id_str,
        template="ruuvitag",
        type_str="topic",
        description=description,
        metadata=dict(mac=mac),
    )


class RuuviTag:
    def __init__(self, mac, name=None, description=None, id_str=None):
        self._mac = mac
        self._name = name
        self._description = description

    @property
    def template(self):
        return TEMPLATE_DICT

    @property
    def topic(self):
        return create_topic_dict(self._mac, self._name, self._description)
