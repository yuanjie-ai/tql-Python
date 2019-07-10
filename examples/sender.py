#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib, time

# QQ邮箱

HOST = 'smtp.qq.com'  # 服务器主机,相当于第三方客户端

PORT = '465'  # 端口 使用SSL，端口号465或587

FROM = '发件人邮箱'  # 发件人的邮箱账号,必须是本人可登录的.
TO = ['yuanjie@xiaomi.com', '邮箱账号二']  # 接收邮件的人的账号.可以是类表;也可以是用,连接的字符串 '邮箱账号1', '邮箱账号二'

SUBJECT = '这是一封测试邮件'  # 邮件的标题
CONTENT = '这是一封邮件'  # 邮件的内容

# 创建邮件发送对象
smtp_obj1 = smtplib.SMTP()  # 普通邮件的发送形式
smtp_obj = smtplib.SMTP_SSL()  # 数据在传输过程中会被加密。
smtp_obj.connect(host=HOST, port=PORT)  # 需要进行发件人的认证，授权,smtp_obj就是一个第三方客户端对象
res = smtp_obj.login(user=FROM, password='授权码')  # 如果使用第三方客户端登录，要求使用授权码，不能使用真实密码，防止密码泄露。

print(res, '登录成功')

for to in TO:
    print(to)
    msg = '\n'.join(['From: {}'.format(FROM), 'To: {}'.format(to), 'SUBJECT:{}'.format(SUBJECT), '',
                     CONTENT])  # 发送邮件,这里是我们按照邮箱的格式拼接一下.
    for num in range(1, 5):  # 循环发送
        time.sleep(5)  # 设置一下睡眠时间
        smtp_obj.sendmail(from_addr=FROM, to_addrs=[to], msg=msg.encode('utf-8'))  # 这里要编码,不然会出现ASCII码编码错误.
        print('发送成功')