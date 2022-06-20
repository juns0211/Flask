from pathlib import Path
import yaml

path = Path('config/config.yaml')

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
