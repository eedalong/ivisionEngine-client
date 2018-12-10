import six
import json

show_start = "=============== {} ================"


def show(prompt, content):
    content = json.dumps(content)
    print(show_start.format(prompt))
    print(content)
    print(show_start.format('END'))


def show_error(prompt, error):
    print(show_start.format(prompt))
    print("Short Description: {}".format(error['reason']))
    print("Long Description: {}".format(error['description']))
    print(show_start.format('END'))


def show_dir(prompt,content):
    print(show_start.format(prompt))
    file_list = content["entities"]
    for files in file_list:
        file_name = files["name"] + ("/ " if files["isdir"] else "")
        print("{file_name:10}".format(file_name = file_name),)

    print(show_start.format('END'))
def show_task_list(prompt, tasklist):
    print(show_start.format(prompt))
    index = 0
    print(
        "{:31}\n| {:5} | {:25} | {:12} |".format("_" * 52, "index", "task_id",
                                                 "task_status"))
    for task in tasklist:
        print(
            "{:31}\n| {index:5} | {task_id:25} | {task_status:12} |".format(
                "_" * 52,
                index=index,
                task_id=
                task[
                    "id"],
                task_status=
                task[
                    "status"]))
        index = index + 1

    print(show_start.format('END'))


def TestNoUse():
    return 'TestNoUse'
