
from datadog import DogStatsd

# By default DogStatsd listens to port 8125
statsd = DogStatsd()

#You can explicitly provide a custom port for DogStatsd like this :
#statsd = DogStatsd(port=8135)


statsd.gauge('myapp.cpu_load', 75.5, tags=["env:prod", "host:webserver"])
statsd.increment('myapp.request_count', tags=["env:prod", "endpoint:/api"])

print("Metrics sent via DogStatsD!")
