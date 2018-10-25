# author    python
# time      18-10-25 下午5:07
# project   SuperMall

# 发送短信模板ID
from celery_tasks.main import celery_app
from celery_tasks.sms.yuntongxun.sms import CCP

SMS_CODE_TEMP_ID = 1

# 获取日志
import logging

logger = logging.getLogger('django')


# 一定要注意添加装饰其
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code, expires):
    """发送短信的任务函数"""
    try:
        res = CCP().send_template_sms(mobile, [sms_code, expires], SMS_CODE_TEMP_ID)
    except Exception as e:
        logger.error("发送验证码短信[异常][mobile:%s,message:%s]" % (mobile, e))
    else:
        if res != 0:
            logger.warning("发送验证码短信[失败][mobile:%s]" % mobile)
        else:
            logger.info('发送验证码短信[正常][mobile:%s]' % mobile)
