import redis

r_server = redis.Redis("localhost")

for i in xrange(0, 50000):
	r_server.set("key%s" % i, ":-)")
