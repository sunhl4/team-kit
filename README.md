# team-kit

组员用各自的 Cursor / Claude Code / Codex，在同一 Git 仓写算法包或软件包。人读这一屏；模型读 `AGENTS.md` 和 `.agents/skills/`。

GitHub 模板仓：<https://github.com/sunhl4/team-kit>（Use this template）。当前是 **public**：免费私人仓无法锁 `main`。要私有且保留保护，转到公司 org 或升级 GitHub Pro。不要往 QVibe / qdata / ionstack 内核里套本套件。

```bash
gh repo create my-algo --template sunhl4/team-kit --private --clone
cd my-algo
python3 scripts/team.py new-spec 001 first
# 或在旁边再开一个实现仓：
python3 scripts/team.py new-pkg my_algo ../my-algo-pkg
```

文献调研**不在这里做**。用已有的 `academic-paper`（`lit-review`）。有报告之后再进本套件。

```bash
# 新规格
python3 scripts/team.py new-spec 042 shuttle-map

# 新包（module 名用 snake_case）
python3 scripts/team.py new-pkg route_map ~/src/route-map

# 门禁（本地 = CI）
python3 scripts/team.py check
```

组员口令（人只发这一句，不写 `src/`）：

```text
做 spec/042，用 implement-from-spec
```

改 `src/` 之前：人把 `Gate: pending` 改成 `pass` 并单独合进 default。agent 不准自己盖章。CLI `--schema`、`tasks.md` 的 `test_*`、`plan.md` Exclusive paths 都由 `team check` 对账。

接到**已有仓**（不覆盖已有 `AGENTS.md`）：

```bash
python3 scripts/team.py apply /path/to/existing-repo
```

新包自带四层 `src`、ruff、import-linter、pytest、GitHub / GitLab CI。

第 12–14 天作业（三家 agent 同一条 spec）：`assignments/001-makespan/`。Cursor 路径的试点实现仓：<https://github.com/sunhl4/route-pilot>。

```bash
bash scripts/day14_verify.sh
bash scripts/worktree.sh spec/001/cursor
```

保护 GitHub `main`（禁止直推，CI 必须绿；组员到齐后再把 CODEOWNERS 审开关打开）：

```bash
bash scripts/protect_main.sh sunhl4/team-kit kit
# 生成出来的实现仓检查名是 gates：
# bash scripts/protect_main.sh sunhl4/my-algo-pkg gates
```
