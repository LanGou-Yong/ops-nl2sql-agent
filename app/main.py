# -*- coding: utf-8 -*-
from fastapi import FastAPI
from pydantic import BaseModel

from app.db import connect, init_db
from app.sql_guard import is_readonly, nl_to_sql

init_db()
app = FastAPI(title="ops-nl2sql-agent-demo")


class AskIn(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok", "demo": True, "readonly": True}


@app.post("/ask")
def ask(body: AskIn):
    sql, how = nl_to_sql(body.question)
    if not sql:
        return {
            "ok": False,
            "reason": "当前 Demo 只用规则把常见问法映射成 SQL，未覆盖的问题会拒答，避免幻觉查数。",
            "sql": None,
        }
    if not is_readonly(sql):
        return {"ok": False, "reason": "拦截非 SELECT", "sql": sql}
    conn = connect()
    try:
        rows = [dict(r) for r in conn.execute(sql).fetchall()]
    except Exception as e:
        conn.close()
        return {"ok": False, "reason": "SQL 执行失败: %s" % e, "sql": sql, "retry": False}
    conn.close()
    return {
        "ok": True,
        "mapper": how,
        "sql": sql,
        "rows": rows,
        "note": "口径以 SQL 为准。本 Demo 无真实数仓。",
    }


@app.post("/sql")
def raw_sql(body: dict):
    sql = str(body.get("sql") or "")
    if not is_readonly(sql):
        return {"ok": False, "reason": "only SELECT is allowed"}
    conn = connect()
    try:
        rows = [dict(r) for r in conn.execute(sql).fetchall()]
    except Exception as e:
        conn.close()
        return {"ok": False, "reason": str(e)}
    conn.close()
    return {"ok": True, "rows": rows}
