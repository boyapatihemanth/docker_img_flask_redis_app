from flask import Flask
from redis import Redis, RedisError
import os
import socket

redis_host = os.environ['redis_host']
redis_port = os.environ['redis_port']
username = os.getenv("username", "world")

# Connect to Redis
redis = Redis(host=redis_host, port=redis_port, db=0, socket_connect_timeout=2, socket_timeout=2)

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        visits = "<i>cannot connect to Redis, counter disabled - check if redis conatiner/pod is running and validate the redis_host/redis_port env var</i>"

    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=username, hostname=socket.gethostname(), visits=visits)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
