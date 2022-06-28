# 排程工具 例如在server啓動爬蟲等等
from flask_apscheduler import APScheduler
from setting import app
import datetime
scheduler = APScheduler(app=app)

# 排程server計時器
@scheduler.task('interval', id='printting', seconds=60)
def printting():
    print(datetime.datetime.now())
