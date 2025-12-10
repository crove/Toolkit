import os
import tempfile
import re
import pytest
from typer.testing import CliRunner
from cli_taskmanager.cli.commands import app

@pytest.fixture(autouse=True)
def temp_db(monkeypatch):
    with tempfile.NamedTemporaryFile(suffix=".db") as tf:
        monkeypatch.setenv("CLI_TASKMANAGER_DB", tf.name)
        yield
        # Explicitly remove the file to ensure isolation
        try:
            os.remove(tf.name)
        except FileNotFoundError:
            pass

def get_task_ids(output):
    # Extract all task IDs from the output table
    return [int(m.group(1)) for m in re.finditer(r"^│\s*(\d+)\s*│", output, re.MULTILINE)]

def test_add_and_ls():
    runner = CliRunner()
    result = runner.invoke(app, ["add", "foo"])
    assert result.exit_code == 0
    result = runner.invoke(app, ["ls"])
    assert "foo" in result.output

def test_done_and_undone():
    runner = CliRunner()
    runner.invoke(app, ["add", "bar"])
    result = runner.invoke(app, ["ls"])
    ids = get_task_ids(result.output)
    assert ids, "No task IDs found in output"
    task_id = ids[0]
    runner.invoke(app, ["done", str(task_id)])
    result = runner.invoke(app, ["ls", "--status", "done"])
    assert "bar" in result.output
    runner.invoke(app, ["undone", str(task_id)])
    result = runner.invoke(app, ["ls", "--status", "todo"])
    assert "bar" in result.output

def test_upd_and_del():
    runner = CliRunner()
    runner.invoke(app, ["add", "baz"])
    result = runner.invoke(app, ["ls"])
    ids = get_task_ids(result.output)
    assert ids, "No task IDs found in output"
    task_id = ids[0]
    runner.invoke(app, ["upd", str(task_id), "baz updated"])
    result = runner.invoke(app, ["ls"])
    assert "baz updated" in result.output
    runner.invoke(app, ["del", str(task_id)])
    result = runner.invoke(app, ["ls"])
    assert "baz updated" not in result.output

def test_purge_and_clear():
    runner = CliRunner()
    runner.invoke(app, ["add", "a"])
    runner.invoke(app, ["add", "b"])
    result = runner.invoke(app, ["ls"])
    ids = get_task_ids(result.output)
    assert ids, "No task IDs found in output"
    runner.invoke(app, ["done", str(ids[0])])
    runner.invoke(app, ["clear"])
    result = runner.invoke(app, ["ls"])
    # Only one task should remain
    ids_after_clear = get_task_ids(result.output)
    assert len(ids_after_clear) == 1
    runner.invoke(app, ["purge"])
    result = runner.invoke(app, ["ls"])
    # No tasks should remain
    ids_after_purge = get_task_ids(result.output)
    assert len(ids_after_purge) == 0
