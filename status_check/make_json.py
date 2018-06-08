import json


def make_json(input):
    json_result = json.dumps(input, ensure_ascii=False, indent='')
    return json_result


def load_json(input):
    json_result = json.loads(input, encoding='UTF-8')
    return json_result
