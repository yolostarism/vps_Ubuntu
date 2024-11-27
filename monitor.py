import time
import logging
import scapy.all as scapy
import psutil
from threading import Thread
from database import store_data
from alert import check_and_alert
from config import LOG_FILE

# 配置日志记录
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s - %(message)s')


def monitor_network():
    """
    使用scapy捕获网络流量并返回捕获的包数量。
    """
    # 捕获10秒内的流量
    packets = scapy.sniff(timeout=10)
    total_packets = len(packets)

    # 这里可以添加更多的分析逻辑，如检测特定协议或IP
    for packet in packets:
        if packet.haslayer(scapy.TCP) and packet[scapy.TCP].dport == 80:
            logging.info(f"HTTP Traffic detected from {packet[scapy.IP].src}")

    return {"packets": total_packets}


def monitor_system():
    """
    使用psutil监控系统资源并返回CPU和内存使用率。
    """
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent
    return {"cpu": cpu_percent, "memory": memory_percent}


def log_monitor_data(monitor_data):
    """
    将监控数据记录到日志文件中。
    """
    logging.info(f"Network: {monitor_data['network_packets']}, System: {monitor_data['system']}")


def periodic_monitor():
    """
    定期执行监控任务，并处理数据存储、告警和日志记录。
    """
    while True:
        network_data = monitor_network()
        system_data = monitor_system()
        monitor_data = {
            'network_packets': network_data['packets'],
            'system': system_data
        }

        # 存储数据
        Thread(target=store_data, args=(monitor_data,)).start()

        # 检查并发送告警
        Thread(target=check_and_alert, args=(monitor_data,)).start()

        # 记录日志
        log_monitor_data(monitor_data)

        # 临时输出
        print(f"Network: {network_data}, System: {system_data}")

        time.sleep(60)  # 每60秒执行一次监控


if __name__ == '__main__':
    # 确保数据库已经设置好
    from database import setup_database

    setup_database()

    # 启动监控线程
    monitor_thread = Thread(target=periodic_monitor)
    monitor_thread.start()
