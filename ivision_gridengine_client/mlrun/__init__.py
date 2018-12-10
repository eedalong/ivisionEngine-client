import sys
import click
from .runner import Runner
import sys
from . import Configs

if sys.version[0] == '3':
    pass
elif sys.version[0] == '2':
    pass
__all__ = ['mlrun']
myrunner = Runner()


@click.group()
def mlrun():
    pass


@mlrun.command()
@click.option("--server", type=str, required=True, help="server address")
def inspect(server):
    myrunner.inspect_server(server)


# Execute Script File Command
@mlrun.command()
@click.option('--config_file', type=str, required=True,
              help='task config file path')
@click.option('--server', type=str, required=True, help='confirm server ')
@click.argument('args', nargs=-1)
def createTask(server, config_file, args):
    myrunner.create_task(server, config_file, args)


@mlrun.command()
@click.option("--task_id", type=str, required=True, help="task id")
@click.option("--server", type=str, required=True, help="server")
@click.option("--assets", type=str, required=False, help="assets list file")
def launchtask(task_id, server, assets):
    myrunner.launch_task(task_id, server, assets)


@mlrun.command()
@click.option('--task_id', required=True, help='choose a task_id to cancel')
@click.option('--server', type=str, required=True, help='confirm server ')
def killtask(server, task_id):
    myrunner.kill_task(server, task_id)


@mlrun.command()
@click.option('--task_id', required=True,
              help='choose a task to delete if it is still in the waiting list')
@click.option('--server', type=str, required=True, help='confirm server ')
def deletetask(server, task_id):
    myrunner.delete_task(server, task_id)


@mlrun.command()
@click.option('--skip', type=int, required=False, default=0,
              help='number of tasks to skip at the front')
@click.option('--limit', type=int, required=False, default=Configs.MAX_LIMIT,
              help='maximum number of tasks to obtain')
@click.option('--query', type=str, required=False, default='',
              help='query string')
@click.option('--server', type=str, required=True, help='confirm server ')
def querytask(server, skip, limit, query):
    myrunner.query_task(server, skip, limit, query)


@mlrun.command()
@click.option('--task_id', required=True, default=None,
              help='choose a task_id to operate')
@click.option('--server', type=str, required=True, help='confirm server ')
def taskresult(server, task_id):
    # runner.task_result(task_id)
    # TODO
    pass


@mlrun.command()
@click.option('--task_id', required=True, default=None,
              help='choose a task_id to operate')
@click.option('--server', type=str, required=True, help='confirm server ')
def taskdoc(server, task_id):
    myrunner.task_doc(server, task_id)


@mlrun.command()
@click.option('--task_id', required=True, help='choose a task')
@click.option('--name', required=False, default='')
@click.option('--description', required=False, default='')
@click.option('--tags', required=False, default='')
@click.option('--server', type=str, required=True, help='confirm server ')
def updateTaskDoc(server, task_id, name, description, tags):
    myrunner.update_task_doc(server, task_id, name, description, tags)


@mlrun.command()
@click.option('--task_id', required=True,
              help='choose a task to check its workdir')
@click.option('--path', required=False, default='WORKDIR',
              help='choose a path to list')
@click.option('--server', type=str, required=True, help='confirm server ')
def listdir(server, task_id, path):
    myrunner.list_dir(server, task_id, path)


@mlrun.command()
@click.option('--task_id', required=True, help='choose a task ')
@click.option('--path', required=False, default="", help='choose a file path')
@click.option('--server', type=str, required=True, help='confirm server ')
def getfile(server, task_id, path):
    myrunner.get_file(server, task_id, path)


@mlrun.command()
@click.option('--task_id', required=True, help='choose a task')
@click.option('--format', required=True,
              type=click.Choice(['.zip', '.tar', '.tar.gz']),
              help='choose file format for downloading')
@click.option('--server', type=str, required=True, help='confirm server ')
def gettaskfile(server, task_id, format):
    myrunner.get_task_file(server, task_id, format)


@mlrun.command()
@click.option('--task_id', required=True, default=None,
              help='choose a task_id to operate')
@click.option('--server', type=str, required=True, help='confirm server ')
def taskoutput(server, task_id):
    myrunner.task_output(server, task_id)


if __name__ == '__main__':
    mlrun()
