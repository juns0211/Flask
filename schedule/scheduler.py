# 排程工具 例如在server啓動爬蟲等等
from setting import app
import datetime
from configs import config
default_setting = config.load_setting()
import requests
from platforms import shopee
import re
import datetime


# 排程server計時器
#@scheduler.task('interval', id='printting', seconds=60)
def printting():
    resp = requests.get(url='http://127.0.0.1:5000/scheduler/jobs')
    print(resp.json())

def test():
    # 取得蝦皮活動時間
    result = shopee.module.get_all_session()
    if not result['success']:
        print(result)
        return
    start_time = []
    for r in result['data']:
        start_time.append(datetime.datetime.fromtimestamp(r['start_time']))
    print(f'補捉到蝦皮活動時間:{start_time}')
    fstart_time = ','.join(sorted(list({str((s - datetime.timedelta(minutes=2)).hour) for s in start_time}), key=lambda x:int(x)))
    print(f'執行蝦皮捕捉hour為:{fstart_time}')
    # 回存yaml用
    for i,d in enumerate(default_setting['SCHEDULER_JOBS']):
        if d['name'] == 'test':
            jobs = d
            break
        else:
            print('查無任務=test')
            return
    jobs['minute'] = '58'
    jobs['hour'] = fstart_time
    default_setting['SCHEDULER_JOBS'][i] = jobs
    config.save_setting(default_setting)
    print(f'回存yaml成功:{jobs}')
    # 更新SCHEDULER_JOBS用
    resp = requests.patch(url='http://127.0.0.1:5000/scheduler/jobs/2', json={'minute':jobs['minute'], 'hour':jobs['hour'], 'trigger':jobs['trigger']})
    print(resp.json())
    return
