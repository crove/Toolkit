import os
import tempfile
import pytest
from cli_taskmanager.controller.task_service import TaskService

@pytest.fixture(autouse=True)
def temp_db(monkeypatch):
    with tempfile.NamedTemporaryFile(suffix=".db") as tf:
        monkeypatch.setenv("CLI_TASKMANAGER_DB", tf.name)
        yield

def test_add_and_list():
    service = TaskService()
    t = service.add_task("foo")
    assert t.description == "foo"
    tasks = service.list_tasks()
    assert any(task.description == "foo" for task in tasks)

def test_mark_done_and_undone():
    service = TaskService()
    t = service.add_task("bar")
    service.mark_done(t.id)
    done_task = service.list_tasks("done")[0]
    assert done_task.done == 1
    service.mark_undone(t.id)
    undone_task = service.list_tasks("todo")[0]
    assert undone_task.done == 0

def test_update():
    service = TaskService()
    t = service.add_task("baz")
    service.update_task(t.id, "baz updated")
    updated = service.list_tasks()[0]
    assert updated.description == "baz updated"

def test_delete_and_purge():
    service = TaskService()
    t1 = service.add_task("a")
    t2 = service.add_task("b")
    assert service.delete_task(t1.id)
    assert not service.delete_task(9999)
    assert len(service.list_tasks()) == 1
    service.purge()
    assert len(service.list_tasks()) == 0

def test_clear_done():
    service = TaskService()
    t1 = service.add_task("a")
    t2 = service.add_task("b")
    service.mark_done(t1.id)
    cleared = service.clear_done()
    assert cleared == 1
    tasks = service.list_tasks()
    assert all(task.done == 0 for task in tasks)
