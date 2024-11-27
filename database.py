import sqlite3
import logging
from config import DB_FILE

# 配置日志记录
logging.basicConfig(filename='logs/database.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_database():
    """
    创建SQLite数据库和表。
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS monitoring_data
                     (timestamp DATETIME, network_packets INTEGER, cpu_usage REAL, memory_usage REAL)''')
        conn.commit()
        logging.info("Database and table setup successfully")
    except sqlite3.Error as e:
        logging.error(f"An error occurred while setting up the database: {e}")
    finally:
        if conn:
            conn.close()


def store_data(monitor_data):
    """
    将监控数据存储到数据库中。
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO monitoring_data VALUES (datetime('now'), ?, ?, ?)",
                  (monitor_data['network_packets'], monitor_data['system']['cpu'], monitor_data['system']['memory']))
        conn.commit()
        logging.info(f"Data stored successfully: {monitor_data}")
    except sqlite3.Error as e:
        logging.error(f"An error occurred while storing data: {e}")
    finally:
        if conn:
            conn.close()


def get_monitoring_data():
    """
    从数据库中获取监控数据。
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT * FROM monitoring_data ORDER BY timestamp DESC LIMIT 10")
        data = c.fetchall()
        logging.info("Monitoring data retrieved successfully")
        return data
    except sqlite3.Error as e:
        logging.error(f"An error occurred while retrieving data: {e}")
        return []
    finally:
        if conn:
            conn.close()


def delete_old_data(days=30):
    """
    删除超过指定天数的旧数据。
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("DELETE FROM monitoring_data WHERE timestamp < datetime('now', '-%d days')" % days)
        conn.commit()
        logging.info(f"Old data older than {days} days deleted successfully")
    except sqlite3.Error as e:
        logging.error(f"An error occurred while deleting old data: {e}")
    finally:
        if conn:
            conn.close()


# 在应用启动时调用此函数来确保数据库已经设置好
if __name__ == '__main__':
    setup_database()
