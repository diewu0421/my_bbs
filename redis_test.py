from redis import Redis

rr = Redis(host="127.0.0.1",port=6379,password='buzhidao')

rr.set('username', 'xiaoto', ex=60)
print(rr.get('username'))

rr.publish("channel", "233")
