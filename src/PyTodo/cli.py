"""
这里处理终端输入
"""

from PyTodo import models

_commands = {}
_parse_args = {}


def command(*names):
    def decorator(func):
        for name in names:
            _commands[name] = func

        return func

    return decorator


@command("add", "-a")
def add_todo():
    todo = models.Todo()
    if len(_parse_args) == 3:
        # 长度如果是3就是设置了priority
        todo.priority = models.Priority(_parse_args[2])
    todo.text = _parse_args[1]
    print("add_todo")
    return todo


@command("delete", "-d")
def delete_todo(id: int):
    # 得获取id，然后通过id删除
    print("delete")


@command("list", "-l")
def show_todo():
    # 直接打印全部的待办事项
    print("show list")


@command("sort", "-s")
def sort_todo():
    # 排序 直接在数据库中排序
    print("sort todo")


@command("help", "-h")
def show_help():
    print("Usage: xxx")
