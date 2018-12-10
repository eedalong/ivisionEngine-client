import os
import sys
import logging
import requests
import six
from . import utils
from . import show_result
from . import Configs
import urllib
import json

if sys.version[0] == '3':
    from urllib.parse import urlparse
elif sys.version[0] == '2':
    import urlparse
__all__ = ['Runner']

API = {
    'inspect_server': '/api/_inspect',
    'create_task': '/api/v1/task/_create',
    "launch_task": '/api/v1/task/{task_id}/_start',
    'upload_and_lock': '/api/v1/_upload/simple',
    'kill_task': '/api/v1/task/{task_id}/_kill',
    'delete_task': '/api/v1/task/{task_id}/_delete',
    'query_task': '/api/v1/task/_query',
    'task_doc': '/api/v1/task/{task_id}',
    'update_task_doc': '/api/v1/task/{task_id}/_update',
    'list_dir': '/api/v1/task/{task_id}/_listdir/{path}',
    'get_task_file': '/api/v1/task/_download/{task_id}.{format}',
    'get_file': '/api/v1/task/{task_id}/_getfile/',
    'task_output': '/api/v1/task/{task_id}/output',
}


class Runner:
    '''
    Runner handles all communication with cloud
    :copyright: (c) 2017 by YXL.
    :license: Apache 2.0, see LICENSE for more details.
    '''
    IP = None

    def __init__(self):
        pass

    def inspect_server(self, server):
        server = server + API["inspect_server"]
        response = requests.get(url=server)
        if response.ok:
            content = response.json()
            prompt = "Inspect successfully"
            show_result.show(prompt, content)
        else:
            Configs.logger.info(
                "Inspect server failed, check the netstatus or makesure "
                "if server has finish this endpoint")

    def create_task(self, server, config_file, args):
        body = utils.parse_configfile(config_file,args)
        server = server + API['create_task']
        response = requests.post(url=server, json=json.dumps(body))
        Configs.logger.debug("check response in create task = {}".format(response.content))
        if response.ok:
            Configs.logger.info("Task create create successfully")
            content = response.json()
            prompt = 'Task Creates Successfully!'
            show_result.show(prompt, content)
        else:
            content = response.json()
            prompt = 'Task Creates Failed!'
            show_result.show_error(prompt, content)

    def launch_task(self, task_id, server, assets):
        url = server + API["launch_task"].format(task_id=task_id)
        response = requests.post(url = url,json = json.dumps({}))
        if response.ok:
            content = response.json()
            prompt = 'Task Launch Successfully!'
            show_result.show(prompt, content)
        else:
            content = response.json()
            prompt = 'Task Launch Failed!'
            show_result.show_error(prompt, content)

    def upload_and_lock(self, server, file_path, task_id, lock_until=None):
        # currently we dont support file cache
        url = server + API['upload_and_lock']
        params = {'lock_for': task_id, 'lock_until': lock_until}
        content, content_type = utils.get_file_info(file_path)
        headers = {'Content-Type': content_type, 'Content-Length': len(content)}
        response = requests.post(url=url, params=params, headers=headers,
                                 json=content)
        content = response.json()
        if response.status_code == 200:
            prompt = 'Upload File Successfully!'
            show_result.show(prompt, content)
        else:
            prompt = 'Upload File Failed!'
            show_result.show_error(prompt, content)

    # for cancel a task
    def kill_task(self, server, task_id):
        url = server + API['kill_task'].format(task_id=task_id)
        response = requests.post(url=url)
        content = response.json()
        if response.status_code == 200:
            prompt = 'Kill Task Successfully!'
            show_result.show(prompt, content)
        else:
            prompt = 'Kill Task Failed!'
            show_result.show_error(prompt, content)

    def delete_task(self, server, task_id):
        url = server + API['delete_task'].format(task_id=task_id)
        print('dalong log : check server = {} and url = {}'.format(server, url))
        response = requests.post(url=url,json = json.dumps({}))
        if response.ok:
            content = ""
            prompt = 'Delete Task Successfully!'
            show_result.show(prompt, content)
        else:
            content = response.json()
            prompt = 'Delete Task Failed!'
            show_result.show_error(prompt, content)

    def query_task(self, server, skip, limit, query):
        url = server + API['query_task']
        body = {'skip': skip, 'limit': limit}
        if query:
            body["query"] = query
        response = requests.post(url=url, json=json.dumps(body))
        if response.ok:
            content = response.json()
            prompt = 'Quert Task Succefully!'
            show_result.show_task_list(prompt, content)
        else:
            content = response.json()
            prompt = 'Query Task Failed!'
            show_result.show_error(prompt, content)

    # check task doc
    def task_doc(self, server, task_id):
        url = server + API['task_doc'].format(task_id=task_id)
        response = requests.get(url=url)
        if response.ok:
            content = response.json()
            prompt = 'Query Task Info Succefully!'
            show_result.show(prompt, content)
        else:
            content = response.json()
            prompt = 'Query Task Info Failed!'
            show_result.show_error(prompt, content)

    def update_task_doc(self, server, task_id, name, description, tags):
        url = server + API['update_task_doc'].format(task_id=task_id)
        body = {}
        if name:
            body["name"] = name
        if description:
            body["name"] = name
        if tags:
            body["name"] = name

        response = requests.post(url=url, json= json.dumps(body))
        if response.ok:
            content = response.json()
            prompt = 'Update Task Info Successfully!'
            show_result.show(prompt, content)
        else:
            content = response.json()
            prompt = 'Update Task Info Failed!'
            show_result.show_error(prompt, content)

    def list_dir(self, server, task_id, path):
        url = server + API['list_dir'].format(task_id=task_id, path=path)
        response = requests.get(url=url)
        Configs.logger.debug("check response   = {}".
                             format(response.content))
        if response.ok:
            content = response.json()
            prompt = 'List Dir Successfully!'
            show_result.show_dir(prompt, content)
        else:
            content = response.json()
            prompt = 'List Dir Failed!'
            show_result.show_error(prompt, content)

    def get_file(self, server, task_id, path):
        # Now we just use naive implementation
        url = server + os.path.join(API['get_file']
                                    .format(task_id=task_id), path)
        response = requests.get(url=url)
        content = response.json()
        if response.status_code == 200:
            prompt = 'Get File Successful!'
            result_file = open('{task_id}_{file_name}'.format(task_id=task_id,
                                                              file_name=os.path.basename(
                                                                  path)))
            result_file.write(response.content)
            result_file.close()
            show_result.show(prompt, '')
        else:
            prompt = 'Get File Failed!'
            show_result.show_error(prompt, content)

    # for check task Output
    def task_output(self, server, task_id):
        url = server + API['task_output'].format(task_id=task_id)
        response = requests.get(url)
        content = response.json()
        if response.status_code == 200:
            prompt = 'Get Task Output Successfully!'
            show_result.show(prompt, content)
        else:
            prompt = 'Get Task Output Failed!'
            show_result.show_error(prompt, content)

    def get_task_file(self, server, task_id, file_format):
        url = server + API['get_task_file'].format(
            task_id=task_id, format=file_format)
        response = requests.get(url)
        content = response.json()
        # assume received file format is the wanted file format
        if response.status_code == 200:
            prompt = 'Get Task File Successfully!'
            result_file = open('{task_id}.{file_format}'.
                               format(task_id=task_id, file_format=file_format),
                               'wb')
            result_file.write(content)
            result_file.close()
        else:
            prompt = 'Get Task File Failed!'
            show_result.show_error(prompt, content)
