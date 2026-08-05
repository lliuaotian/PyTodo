import pytest

from PyNoto import cli


@pytest.fixture(autouse=True)
def reset_state():
    original_args = cli._parse_args.copy()
    original_cmds = cli._commands.copy()
    yield
    cli._parse_args.clear()
    cli._parse_args.update(original_args)
    cli._commands.clear()
    cli._commands.update(original_cmds)


def test_add_command_via_dispatch():
    # 模拟终端输入
    cli._parse_args = {0: "add", 1: "Buy milk", 2: 2}

    # 通过命令模拟处罚
    todo = cli._commands["add"]()

    assert todo.text == "Buy milk"
    assert todo.priority == cli.models.Priority.HIGH


def test_add_alias_a():
    # 模拟终端输入
    cli._parse_args = {0: "-a", 1: "Buy milk"}

    # 通过命令模拟处罚
    todo = cli._commands["-a"]()
    print(f"TODO priority {cli.models.Priority.MEDIUM}")

    assert todo.text == "Buy milk"
    assert todo.priority == cli.models.Priority.MEDIUM
