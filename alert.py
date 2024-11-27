import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from config import SENDER_EMAIL, RECEIVER_EMAIL, SMTP_SERVER, SMTP_PORT, PASSWORD, NETWORK_TRAFFIC_THRESHOLD, \
    CPU_USAGE_THRESHOLD, MEMORY_USAGE_THRESHOLD

# 配置日志记录
logging.basicConfig(filename='logs/alert.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def send_alert(subject, body):
    """
    通过SMTP服务器发送告警邮件。
    """
    try:
        message = MIMEMultipart()
        message['From'] = SENDER_EMAIL
        message['To'] = RECEIVER_EMAIL
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, PASSWORD)
            server.send_message(message)

        logging.info(f"Alert sent: {subject}")
    except Exception as e:
        logging.error(f"Failed to send alert: {e}")


def check_and_alert(monitor_data):
    """
    检查监控数据是否超过了设定的阈值，如果超过了则发送告警。
    """
    if monitor_data['network_packets'] > NETWORK_TRAFFIC_THRESHOLD:
        send_alert("High Network Traffic Alert",
                   f"Detected high network traffic: {monitor_data['network_packets']} packets")

    if monitor_data['system']['cpu'] > CPU_USAGE_THRESHOLD or monitor_data['system']['memory'] > MEMORY_USAGE_THRESHOLD:
        cpu_alert = f"CPU usage: {monitor_data['system']['cpu']}%" if monitor_data['system'][
                                                                          'cpu'] > CPU_USAGE_THRESHOLD else ""
        memory_alert = f"Memory usage: {monitor_data['system']['memory']}%" if monitor_data['system'][
                                                                                   'memory'] > MEMORY_USAGE_THRESHOLD else ""
        alert_body = f"{cpu_alert} {memory_alert}".strip()
        send_alert("High System Resource Usage", alert_body)

