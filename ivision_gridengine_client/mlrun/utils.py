import six
import json
import os
import mimetypes
import base64
import zipfile
from . import Configs

support_archive_type = ['.zip', '.tar', '.tar.gz']


def valid_file_type(archive_file):
    for file_type in support_archive_type:
        if archive_file.endswith(file_type):
            return True, file_type
    return False, None



def get_file_info(archive_file):
    input_file = open(archive_file, 'rb')
    content = input_file.read()
    input_file.close()
    content = base64.b64encode(content)
    content = str(content)[2:-1]
    content_type = mimetypes.guess_type(archive_file)[0]
    return content, content_type


def check_prameter_valid(jfile):
    res = True
    try:
        float(jfile['resources']['cpu'])
        res = res and float(jfile['resources']['cpu']) > 0
    except ValueError as error:
        Configs.logger.error("cpu cannot be converted to float")
        return False
    try:
        int(jfile['resources']['memory'])
        res = res and int(jfile['resources']['memory']) > 0
    except ValueError as error:
        Configs.logger.error("memory cannot be converted to int")
        return False
    try:
        if jfile['resources'].get("disk") != "":
            res = res and int(jfile["resources"]["disk"]) > 0
    except ValueError as error:
        Configs.logger.error("disk cannot be converted to int ")
        return False
    try:
        if jfile['resources'].get("port") != "":
            res = res and int(jfile["resources"]["disk"]) > 0
    except ValueError as error:
        Configs.logger.error("port cannot be converted to int ")
        return False

    return res


def check_dependency_valid(file_list):
    res = True
    for file_path in file_list:
        if not os.path.exists(file_path):
            Configs.logger.error("{file_path} not exists".format(file_path=file_path))
            res = False
    return res


def compress_dependency_file(file_list):
    # compress the file
    target_path = "./tmp_target.zip"
    compress_file = zipfile.ZipFile(target_path, "w")
    for file in file_list:
        compress_file.write(file,os.path.basename(file))
    compress_file.close()
    content,content_type = get_file_info(target_path)
    os.remove(target_path)
    return content,content_type

def parse_configfile(config_file, args):
    assert os.path.exists(config_file), "config file at {} not exists".format(
        config_file)
    configs = open(config_file, 'r')
    jfile = json.load(configs)
    if not check_prameter_valid(jfile):
        Configs.logger.error(
            "resource parameters set invalid,please check type and value  ")
        exit(0)

    if len(jfile["dependency"]):
        if not check_dependency_valid(jfile["dependency"]):
            exit(0)

    body = {'args': jfile["args"]}
    if jfile['name']:
        body['name'] = jfile['name']
    if jfile['description']:
        body['description'] = jfile['description']
    if jfile['tags']:
        body['tags'] = jfile['tags']
    if jfile['user_env']:
        body['user_env'] = jfile['user_env']
    if jfile['container']['type'] and jfile['container']['image']:
        body['container'] = jfile['container']
    body["resources"] = {"cpu": jfile["resources"]["cpu"],
                         "memory": jfile["resources"]["cpu"]}
    if jfile["resources"]["gpu"]:
        body["resources"]["gpu"] = jfile["resources"]["gpu"]
    if jfile["resources"]["port"]:
        body["resources"]["port"] = jfile["resources"]["port"]
    if len(jfile["dependency"]):
        content,content_type = compress_dependency_file(jfile["dependency"])
        body["archive"] = {"type":content_type,"data":content}
    return body


def parse_configfile2(config_file, archive_file, args):
    assert os.path.exists(config_file), "config file at {} not exists".format(
        config_file)
    configs = open(config_file, 'r')
    jfile = json.load(configs)
    if not check_prameter_valid(jfile):
        exit()
    assert float(jfile['resources']['cpu'] > 0), "cpu nums must be assigned"
    assert int(
        jfile['resource']['memory'] > 0), "memory needs must be specified"
    file_type = ''
    file_content = ''
    if archive_file:
        assert os.path.exists(
            archive_file), "archive file at {} not exists ".format(archive_file)
        file_content, file_type = get_file_info(archive_file)
    body = {'name': jfile['name'],
            'description': jfile['description'],
            'tags': jfile['tags'],
            'user_env': jfile['user_env'],
            'container': jfile['container'],
            'options': jfile["options"],
            'resources': jfile['resources'],
            'archive': {'type': file_type, 'data': file_content}
            }
    return body
