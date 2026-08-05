import pytest

from PyNoto.database import Database
from PyNoto.models import Priority, Todo


@pytest.fixture
def db(tmp_path):
    # 用:memory:可以0污染本地数据库，将数据库放在内存中
    database = Database(":memory:")
    database.init_db()
    yield database
    database.close()


@pytest.fixture
def sample_todo():
    todo = Todo()
    todo.text = "Test task"
    todo.priority = Priority.HIGH
    return todo


class TestInitDb:
    def test_creates_todos_table(self, db: Database):
        row = db.conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='todos'"
        ).fetchone()
        assert row is not None

    def test_idempotent(self, db: Database):
        # 重复初始化不报错
        db.init_db()
        db.init_db()


class TestSave:
    def test_assigns_id(self, db, sample_todo):
        assert sample_todo.id is None
        db.save(sample_todo)
        assert sample_todo.id is not None
        assert isinstance(sample_todo.id, int)

    def test_persists_all_fields(self, db, sample_todo):
        db.save(sample_todo)
        row = db.conn.execute(
            "SELECT * FROM todos WHERE id = ?", (sample_todo.id,)
        ).fetchone()
        assert row["text"] == "Test task"
        assert row["priority"] == Priority.HIGH.value
        assert row["status"] == 0

    def test_multiple_saves_get_unique_ids(self, db):
        t1, t2 = Todo(), Todo()
        t1.text = t2.text = "task"
        db.save(t1)
        db.save(t2)
        assert t1.id != t2.id


class TestListTodos:
    def test_empty_returns_empty_list(self, db):
        assert db.list_todos() == []

    def test_returns_all_saved_todos(self, db):
        for i in range(3):
            t = Todo()
            t.text = f"task {i}"
            db.save(t)
        assert len(db.list_todos()) == 3

    def test_default_order_by_priority_desc(self, db):
        for p in [Priority.LOW, Priority.HIGH, Priority.MEDIUM]:
            t = Todo()
            t.text = "task"
            t.priority = p
            db.save(t)
        todos = db.list_todos()
        assert todos[0]["priority"] == Priority.HIGH.value
        assert todos[-1]["priority"] == Priority.LOW.value

    def test_custom_order_by(self, db):
        for text in ["c", "a", "b"]:
            t = Todo()
            t.text = text
            db.save(t)
        todos = db.list_todos(order_by="text ASC")
        assert [t["text"] for t in todos] == ["a", "b", "c"]


class TestResourceManagement:
    def test_context_manager_closes_connection(self, tmp_path):
        with Database(":memory:") as db:
            db.init_db()
            conn = db.conn
        # 退出后连接应关闭
        with pytest.raises(Exception):  # noqa: B017
            conn.execute("SELECT 1")

    def test_close_is_idempotent(self, db):
        db.close()
        db.close()  # 不应报错

    def test_reconnect_after_close(self, db):
        db.close()
        db.init_db()  # 应自动重连
        row = db.conn.execute("SELECT 1").fetchone()
        assert row[0] == 1
