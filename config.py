import json


class Config:
    def __init__(self, filename):
        self.filename = filename
        with open(filename, "r", encoding="utf-8") as fp:
            content = fp.read()
            self.config = json.loads(content)

    def save(self):
        with open(self.filename, "w") as fp:
            fp.write(json.dumps(self.config, indent=4))


global_config = Config("config.json")
global_data = Config("data.json")
