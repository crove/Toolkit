import os
import tempfile
import pytest
from cli_taskmanager.storage.sqlite_storage import SQLiteStorage

@pytest.fixture(autouse=True)
def temp_db(monkeypatch):
    with tempfile.NamedTemporaryFile(suffix=".db") as tf:
        monkeypatch.setenv("CLI_TASKMANAGER_DB", tf.name)
        yield

def test_add_and_get():
    s = SQLiteStorage()
    tid = s.add_task("foo")
    task = s.get_task(tid)
    assert task.description == "foo"
    assert task.done == 0

def test_mark_done_and_undone():
    s = SQLiteStorage()
    tid = s.add_task("bar")
    s.mark_done(tid)
    assert s.get_task(tid).done == 1
    s.mark_undone(tid)
    assert s.get_task(tid).done == 0

def test_update_task():
    s = SQLiteStorage()
    tid = s.add_task("baz")
    s.update_task(tid, "baz updated")
    assert s.get_task(tid).description == "baz updated"

def test_delete_and_purge():
    s = SQLiteStorage()
    tid1 = s.add_task("a")
    tid2 = s.add_task("b")
    s.delete_task(tid1)
    assert s.get_task(tid1) is None
    assert s.get_task(tid2) is not None
    s.purge()
    assert s.list_tasks() == []

def test_clear_done():
    s = SQLiteStorage()
    tid1 = s.add_task("a")
    tid2 = s.add_task("b")
    s.mark_done(tid1)
    s.clear_done()
    tasks = s.list_tasks()
    assert all(t.done == 0 for t in tasks)
