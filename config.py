import logging

# SMTP配置
SENDER_EMAIL = "your_email@example.com"
RECEIVER_EMAIL = "admin@example.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
PASSWORD = "your_password"

# 数据库配置
DB_FILE = "monitoring.db"

# 日志配置
LOG_FILE = "logs/monitoring.log"
LOG_LEVEL = logging.INFO

# 监控配置
MONITOR_INTERVAL = 60  # 监控间隔时间，单位为秒

# 告警阈值
NETWORK_TRAFFIC_THRESHOLD = 1000  # 网络流量告警阈值，单位为包数
CPU_USAGE_THRESHOLD = 90  # CPU使用率告警阈值，百分比
MEMORY_USAGE_THRESHOLD = 90  # 内存使用率告警阈值，百分比

# Flask配置
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000