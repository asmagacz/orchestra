# !/usr/bin/python3
import argparse
import datetime
import json
import os
from collections import OrderedDict


def get_log():
    with open('logsfile.txt', 'w') as logsfile:
        command = 'xo-cli backupNg.getLogs > /home/zabbix/scripts/logsfile.txt'
    resp = os.system(command)


def read_json():
    with open('logsfile.txt', 'r') as jsonfile:
        data = jsonfile.read()
    logs = json.loads(data)
    return logs


def discovery_job_names():
    get_log()
    log_data = read_json()
    job_names_dict = []
    discovery = []
    for val in log_data:
        if val['message'] == 'backup':
            job_names_dict.append(val['jobName'])
    job_names_dict = list(OrderedDict.fromkeys(job_names_dict))
    for name in job_names_dict:
        discovery.append({"{#JOBNAME}": name})
    print(json.dumps({"data": discovery}, indent=4))


def get_job_status(parameter):
    get_log()
    log_data = read_json()
    status_dict = {}
    date_format = "%Y-%m-%d"
    for val in log_data:
        start_timestamp = val['start']
        start_date = datetime.datetime.fromtimestamp(float(start_timestamp) / 1000.)
        if val['message'] == 'backup':
            status_dict[val['jobName']] = {'{#START}': start_date.strftime(date_format), '{#STATUS}': val['status']}
    for val in status_dict:
        if val == parameter:
            print("Status: " + status_dict[val]['{#STATUS}'])


def get_job_start_time(parameter):
    get_log()
    log_data = read_json()
    status_dict = {}
    date_format = "%Y-%m-%d"
    for val in log_data:
        start_timestamp = val['start']
        start_date = datetime.datetime.fromtimestamp(float(start_timestamp) / 1000.)
        if val['message'] == 'backup':
            status_dict[val['jobName']] = {'{#START}': start_date.strftime(date_format), '{#STATUS}': val['status']}
    for val in status_dict:
        if val == parameter:
            print("Start: " + status_dict[val]['{#START}'])


class switch(object):
    value = None

    def __new__(class_, value):
        class_.value = value
        return True


def case(*args):
    return any((arg == switch.value for arg in args))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--method', help='method name to call')
    parser.add_argument('-p', '--parameter', help='parameter')
    args = parser.parse_args()

    parameter = str(args.parameter).strip()
    method = str(args.method).strip()

    while switch(method):
        if case('discovery'):
            discovery_job_names()
            break
        if case('statuses'):
            get_job_status(parameter)
            break
        if case('start'):
            get_job_start_time(parameter)
            break
        break
