from django.http import JsonResponse
import time
import redis
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

r = redis.StrictRedis(settings.REDIS_HOST, settings.REDIS_PORT)
SECONDS = 60


def get_frequencies_per_minute(timestamps):
    """
    takes a list of timestamps and returns the number of timestamps in every minute (60 seconds)
    time starts at first request
    """
    end = int(timestamps[0]) + SECONDS - 1
    count = 0
    freqs = []
    for timestamp in map(lambda x: int(x), timestamps):
        if timestamp <= end:
            count += 1
        elif end < timestamp <= end + SECONDS:
            freqs.append(count)
            end += SECONDS
            count = 1
        else:
            freqs.append(count)
            while timestamp > end + SECONDS:
                freqs.append(0)
                end += SECONDS
            count = 1
            end += SECONDS
    if count > 0:
        freqs.append(count)
    return ", ".join(str(i) for i in freqs)


def home(request):
    """
    calculate the per minute frequencies for each ip
     TODO : has to be improved to remove sparse elements
        : Algorithm can be improved from single parsing
    """
    per_minute_freqs_v1_hw = {}    # for storing data about /v1/hello-world
    per_minute_freqs_v1_hw_l = {}   # for storing data about /v1/hello-world/logs
    per_minute_freqs_v1_l = {}     # for storing data about /v1/logs

    for key in r.keys("v1_hw:*"):
        timestamps = r.lrange(key, 0, -1)
        freqs = get_frequencies_per_minute(timestamps)
        per_minute_freqs_v1_hw[key.split(':')[-1]] = freqs     # extracting ip of "hw:127.0.0.1"

    for key in r.keys("v1_hw_l:*"):
        timestamps = r.lrange(key, 0, -1)
        freqs = get_frequencies_per_minute(timestamps)
        per_minute_freqs_v1_hw_l[key.split(':')[-1]] = freqs    # extracting ip of "v1_hwl:127.0.0.1"

    for key in r.keys("v1_l:*"):
        timestamps = r.lrange(key, 0, -1)
        freqs = get_frequencies_per_minute(timestamps)
        per_minute_freqs_v1_l[key.split(':')[-1]] = freqs      # extracting ip of "v1_l:127.0.0.1"

    hw_logs = logs_v1_helloworld()                              # get the logs of /v1/logs/ dict
    v1logs = {'v1/hello-world/': logs_v1_helloworld()['logs'], '/v1/hello-world/logs/': logs_v1_helloworld_logs()['logs'],
              'v1/logs': logs_v1_logs()['logs']}                # to get the /v1/logs as a dict

    return render_to_response('home.html', {'hw_freq': per_minute_freqs_v1_hw,
                                            'hwl_freq': per_minute_freqs_v1_hw_l,
                                            'l_freq': per_minute_freqs_v1_l,
                                            'hw_logs': hw_logs,
                                            'v1_logs': v1logs
                                            }, RequestContext(request))


def v1_helloworld(request):
    """
    logs the ip address and timestamp of the request for the /v1/hello-world endpoint
        also returns JSON hello world message
    """
    ip = request.META['REMOTE_ADDR']
    timestamp = int(time.time())
    r.rpush('v1_hw:'+ip, timestamp)
    msg = {'message': 'hello world'}
    return JsonResponse(msg)


def logs_v1_helloworld():
    """
    function that returns logs for the helloworld endpoint
    """
    response = {'logs': []}
    logs = []
    keys = r.keys("v1_hw:*")
    for key in keys:
        for value in r.lrange(key, 0, -1):
            logs.append({"ip": key.split(':')[-1], "timestamp": value})
    response['logs'] = logs
    return response


def logs_v1_helloworld_logs():
    """
    helper function to the logs for the helloworld endpoint
    """
    response = {'logs': []}
    logs = []
    keys = r.keys("v1_hw_l:*")
    for key in keys:
        for value in r.lrange(key, 0, -1):
            logs.append({"ip": key.split(':')[-1], "timestamp": value})
    response['logs'] = logs
    return response


def v1_helloworld_logs(request):
    """
    logs the request ip and timestamp returns the logs for the hello world
    """
    ip = request.META['REMOTE_ADDR']
    timestamp = int(time.time())
    r.rpush('v1_hw_l:'+ip, timestamp)
    response = logs_v1_helloworld()
    return JsonResponse(response)


def v1_logs_helper():
    """
    returns the logs for all the endpoints
    """
    logs = {'logset': []}
    endpoint = {'endpoint': 'hello-world', 'logs': logs_v1_helloworld()['logs']}
    logs['logset'].append(endpoint)
    endpoint = {'endpoint': 'hello-world/logs', 'logs': logs_v1_helloworld_logs()['logs']}
    logs['logset'].append(endpoint)
    endpoint = {'endpoint': 'logs', 'logs': logs_v1_logs()['logs']}
    logs['logset'].append(endpoint)
    return logs


def v1_logs(request):
    """
    logs the ip and timestamp for /v1/logs endpoint and also returns the logs
    """
    ip = request.META['REMOTE_ADDR']
    timestamp = int(time.time())
    r.rpush('v1_l:'+ip, timestamp)
    return JsonResponse(v1_logs_helper())


def logs_v1_logs():
    """
    helper function to the logs for the helloworld endpoint
    """
    response = {'logs': []}
    logs = []
    keys = r.keys("v1_l:*")
    for key in keys:
        for value in r.lrange(key, 0, -1):
            logs.append({"ip": key.split(':')[-1], "timestamp": value})
    response['logs'] = logs
    return response


def default(request):
    """
    in case the url doesn't match the existing
    """
    msg = {'message': 'Resource Not found'}
    re = JsonResponse(msg)
    re.status_code = 404
    return re
