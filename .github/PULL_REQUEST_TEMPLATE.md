## spec

- spec_id:
- paper_id / report path:（无文献则写 idea）
- Gate: pass / pending / done

CI 读 `spec_id`，必须与分支 `spec/<id>/<slug>` 一致。改 `src/` 的 PR 禁止同时把 Gate 改成 pass。

## 做了什么

## 门禁

- [ ] `python3 scripts/team.py check` 本地绿
- [ ] 未改 `AGENTS.md`（除非本 PR 就是改宪法）
