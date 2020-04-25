# -*- coding: utf-8 -*-

# from celery import Celery, current_app
# from time import sleep


# def make_celery(app):
#     celery_app = Celery(
#         app.import_name,
#         backend="redis://:cm9vdEByZWRpczpwd2Q=@zeyinredis.redis.zhangbei.rds.aliyuncs.com:6379/39",
#         broker="redis://:cm9vdEByZWRpczpwd2Q=@zeyinredis.redis.zhangbei.rds.aliyuncs.com:6379/39"
#     )
#     celery_app.conf.timezone = 'UTC'
#     celery_app.conf.update(app.config)
#
#     class ContextTask(celery_app.Task):
#         def __call__(self, *args, **kwargs):
#             with app.app_context():
#                 return self.run(*args, **kwargs)
#
#     celery_app.Task = ContextTask
#
#     return celery_app

#
#
# @current_app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # sender.add_periodic_task(30.0, add.s(5, 6), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )


# @current_app.task
# def test(args):
#     sleep(30)
#     print("this is test function")
#     print(args)
#
#
# @celery.task
# def add(x, y):
#     print("this is add")
#     return x + y
#
#
# # celery.conf.beat_schedule = {
# #     'add-every-30-seconds': {
# #         'task': "add",
# #         'schedule': 10.0,
# #         'args': (16, 16)
# #     },
# # }
#
#
# celery.conf.timezone = 'UTC'
