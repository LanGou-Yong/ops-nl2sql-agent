# -*- coding: utf-8 -*-
from fastapi.testclient import TestClient
from app.main import app

c = TestClient(app)


def test_all():
    assert c.get("/health").json()["readonly"] is True
    r = c.post("/ask", json={"question": "退货率"}).json()
    assert r["ok"] and r["rows"]
    bad = c.post("/sql", json={"sql": "DROP TABLE orders"}).json()
    assert bad["ok"] is False
    miss = c.post("/ask", json={"question": "明天股价"}).json()
    assert miss["ok"] is False
    print("SMOKE_OK")


if __name__ == "__main__":
    test_all()
