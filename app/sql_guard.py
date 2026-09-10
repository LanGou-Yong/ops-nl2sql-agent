# -*- coding: utf-8 -*-
import re

FORBIDDEN = re.compile(r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|ATTACH|PRAGMA|REPLACE|CREATE)\b", re.I)


def is_readonly(sql: str) -> bool:
    s = sql.strip().rstrip(";")
    if FORBIDDEN.search(s):
        return False
    return s.lower().startswith("select")


def nl_to_sql(question: str) -> tuple[str, str]:
    q = question.replace(" ", "")
    if "退货率" in q or "退款率" in q:
        sql = (
            "SELECT o.category AS category, "
            "ROUND(1.0 * IFNULL(r.refund_amt,0) / o.sales_amt, 4) AS refund_rate, "
            "o.sales_amt, IFNULL(r.refund_amt,0) AS refund_amt "
            "FROM (SELECT category, SUM(amount) AS sales_amt FROM orders GROUP BY category) o "
            "LEFT JOIN (SELECT category, SUM(amount) AS refund_amt FROM refunds GROUP BY category) r "
            "ON o.category = r.category"
        )
        return sql, "rule:refund_rate"
    if "销售额" in q or "GMV" in q.upper() or "销售" in q:
        sql = "SELECT day, category, SUM(amount) AS sales FROM orders GROUP BY day, category ORDER BY day"
        return sql, "rule:sales"
    if "仓库" in q or "仓" in q:
        sql = "SELECT warehouse, category, SUM(amount) AS sales FROM orders GROUP BY warehouse, category"
        return sql, "rule:warehouse"
    return "", "no_rule"
