# 运营问数 Agent（脱敏 Demo）

面向商家运营的最小 NL2SQL Demo：自然语言问退货率/销售额，只允许 SELECT，失败则改写重试。

这是公开技术验证，不是数仓产品。库是本地 SQLite 样例，禁止写操作。

## 30 秒看懂

| 你问 | 系统怎么走 | 用来证明什么 |
|---|---|---|
| 这周退货率？ | 模板/规则生成 SELECT | 口径写在 SQL 里 |
| DROP TABLE | 拦截 | 只读 |
| 编造的表名 | 报错后重试或拒答 | 不把幻觉结果当成数 |

## 刻意没做

- 真实数仓、权限、行列级安全
- 95% Text-to-SQL 准确率宣传
- INSERT/UPDATE/DELETE

## 快速开始

需要 Python 3.10+。**下面请一行行执行**。

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python start_demo.py
```

成功：`Backend ready`，打开 http://localhost:8512

## 接口

- `POST /ask` `{"question":"..."}`
