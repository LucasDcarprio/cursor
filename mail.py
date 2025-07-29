import smtplib
import time
from email.mime.text import MIMEText

# 收件人邮箱列表
MAIL_ADDRESS = [
    '1050385759@qq.com',
    'w13648557984@163.com',
    '1745523595@qq.com',
    '1663471799@qq.com'
]

def sendMail(code):
    user = '548716585@qq.com'
    password = 'tqdcscuzxqtdbfhe'  # 请确保这是有效的SMTP授权码

    for toAdr in MAIL_ADDRESS:
        try:
            # 建立SMTP连接
            with smtplib.SMTP_SSL('smtp.qq.com', 465) as server:
                server.set_debuglevel(1)  # 启用调试输出
                server.login(user, password)
                print(f"成功登录SMTP服务器，为收件人：{toAdr}")

                # 构建邮件内容
                message = f'泓枢智创 支付请求验证码：{code}\n请妥善保管，该验证码可用于发起付款请求！'
                msg = MIMEText(message, 'plain', 'utf-8')
                msg['Subject'] = '24 online system 支付请求验证码'
                msg['From'] = user
                msg['To'] = toAdr

                # 发送邮件
                server.send_message(msg)
                print(f'邮件发送成功，验证码：{code}，目标地址：{toAdr}')

                # 等待2秒以防止触发SMTP服务器的频率限制
                time.sleep(2)

        except smtplib.SMTPException as e:
            print(f'发送邮件到 {toAdr} 时SMTP异常: {e.__class__.__name__}, {e}')
        except Exception as e:
            print(f'发送邮件到 {toAdr} 时出现未知异常: {e.__class__.__name__}, {e}')

    return True
