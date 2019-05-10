import json5
import json


class Config:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}
        self.reload()

    def reload(self):
        with open(self.filename, "r", encoding="utf-8") as fp:
            content = fp.read()
            self.data = json5.loads(content)

    def save(self):
        with open(self.filename, "w") as fp:
            fp.write(json.dumps(self.data, indent=4, ensure_ascii=False))


global_config = Config("config/config.json")
global_data = Config("config/data.json")
global_template = Config("config/template.json")
global_module = Config("config/module.json")


def save_all_config():
    global_config.save()
    global_data.save()
    global_template.save()
    global_module.save()
