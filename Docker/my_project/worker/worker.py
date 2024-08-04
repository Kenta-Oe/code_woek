import time
import redis
import psycopg2

def main():
    print("Worker is running...")
    # RedisとPostgresへの接続を設定
    redis_client = redis.Redis(host='cache', port=6379)
    conn = psycopg2.connect(
        dbname="myapp",
        user="user",
        password="password",
        host="db"
    )
    while True:
        print("Working...")
        time.sleep(10)

if __name__ == '__main__':
    main()
