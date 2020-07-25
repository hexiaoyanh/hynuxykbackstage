
broker_url = 'redis://:@localhost:6379/1'
result_backend = 'redis://:@localhost:6379/1'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Shanghai'
enable_utc = True
imports = ('main.wxfwh.sendnotification',)
