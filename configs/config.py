from pathlib import Path
import yaml, json
from flask import abort, Response
from jsonschema import draft7_format_checker, validate


path = Path('configs/config.yaml')

# 讀取YAML
def load_setting():
    with path.open('r', encoding='utf-8') as f:
        data = yaml.load(f.read(), yaml.SafeLoader)
    return data


# 寫入YAML
def save_setting(data):
    with path.open('w', encoding='utf-8') as w:
        yaml.dump(data, w, allow_unicode=True, encoding='utf-8', sort_keys=False)
    return

# flasgger驗證json參數用
def validation_function(data, main_def):
    return validate(instance=data, schema=main_def, format_checker=draft7_format_checker)

# flasgger驗證json錯誤時funtion
def validation_error_handler(err, data , main_def):
    message = str(err).split('\n')[0]
    print(err)
    abort(Response(json.dumps({'success':False, 'message':message}), status=401))