import beanstalkc
beanstalk = beanstalkc.Connection(host='localhost', port=11300)

for i in xrange(0, 100000):
    beanstalk.put("testing")
