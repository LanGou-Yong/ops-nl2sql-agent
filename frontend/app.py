# -*- coding: utf-8 -*-
import os
import httpx
import streamlit as st

API = os.environ.get("API_BASE", "http://127.0.0.1:8012")
st.set_page_config(page_title="问数 Demo")
st.title("运营问数 Agent（脱敏 Demo，只读 SQL）")
try:
    ok = httpx.get(API + "/health", timeout=2).json().get("status") == "ok"
except Exception:
    ok = False
st.sidebar.write("后端服务在线" if ok else "后端未启动")
q = st.text_input("运营问题", "各类目退货率是多少？")
if st.button("查询") and q.strip():
    st.json(httpx.post(API + "/ask", json={"question": q}, timeout=10).json())
st.caption("试：各类目退货率 / 每天销售额 / DROP TABLE orders（应被拦截）")
if st.button("测试拦截 DROP"):
    st.json(httpx.post(API + "/sql", json={"sql": "DROP TABLE orders"}, timeout=10).json())
