# Session 2026-04-06~08 — 战略方向讨论与 AI 人生电影发现

> 日期：2026-04-06 至 2026-04-08
> 模型：Claude Opus 4.6
> 环境：Claude 手机 App（云端沙盒，无法 SSH 到 VPS）
> 时长：跨 3 天长 session，覆盖战略讨论 → 市场调研 → 技术方案 → 知识库同步 → Muse Bot 改进 → 项目命名

---

## 一、战略梳理：项目优先级重排

### 讨论背景
sz 有多条业务线同时推进，核心瓶颈不是执行力而是方向判断。需要一次系统性的优先级排序。

### 决策结论

| 优先级 | 业务线 | 决策 | 理由 |
|--------|--------|------|------|
| **主线 A** | AI 短剧工作室（海外） | 继续推进 | 导演团队就位，海外 CPM 高 |
| **主线 B** | 闲鱼 AI 托管 或 Polymarket 频道 | 二选一 | 技术基建已完成，瓶颈是获客 |
| 🔥 **潜在主线** | AI 人生电影 | Phase 0 验证中 | 唯一出现自发需求的方向 |
| 搁置 | 闲鱼自己卖票 | 停止 | ISV 资质硬卡点 |
| 搁置 | SmartMoney 监控 | 停止 | 红海，230+ 竞品 |
| 低维持 | 数字分身/内容 IP | 保持迭代 | SOP 已跑通但不作为变现主线 |

### 关键认知
- **Closure Problem** 是 sz 最大的弱点 — 系统建好 ≠ 商业闭环
- **系统建设瘾** — 倾向于先建基础设施再想变现，应反过来
- **信息差三层理论** — 速度差（无价值）→ 数据组合差（中等）→ 规则理解差（高价值）

---

## 二、AI 人生电影 — 关键发现

### 起源故事
sz 开车时和母亲（69 岁）聊天。母亲之前体验了 AI 视频全流程 skill（创意→剧本→出图→分镜→网站），看到第 5 步生成的项目网站后非常有感觉。

**关键时刻**：母亲**自发**想到为已故的母亲（sz 的外婆）做一个纪念视频。没有任何引导，她自己提出这个想法，并且**表达了付费意愿**。

这是 sz 所有项目中唯一出现的"未经引导的真实用户自发需求"。

### 后续自发行为
- 母亲主动拉了家族微信群
- 让小姨、舅舅在群里回忆外婆的往事
- 已经在自发地"素材收集"

### 产品定义
**一句话**：让每个人都能拍自己（或亲人）的人生电影。

- 输入：5-20 张老照片 + 文字回忆 + 可选语音口述
- 输出：3-10 分钟 AI 叙事短片
- 多场景：纪念逝者、生日/金婚、孩子成长、婚礼、毕业

### 为什么可能是最优方向
- 用户自发需求 vs 假设需求
- 用户直接付费 vs 流量间接变现
- 天然病毒传播 vs 需要投放
- 100% 自己的 vs 55:45 分成
- 空白市场 vs 红海
- 同一套 AI 视频管线，技术复用

### 独立运营决策
- 不和导演合作这个方向（导演合作是短剧工作室，55:45 分成）
- AI 人生电影 = sz 独立项目，100% 自己的
- 在拍摄质量方面可以按需请教导演，但不分成

---

## 三、市场调研核心结论

> 详见：`docs/AI人生电影-市场调研报告.md`（完整 9 章节报告）

### 竞品格局
- **市场空白** — 没有一家公司专门做"AI + 人生叙事 + 纪念"
- StoryShop.ai 最接近（$69-99，$3M seed），但依赖视频采访，不适合纪念逝者
- MyHeritage Deep Nostalgia 证明了需求（48h 100万次，1.12亿+），但只做动效不做叙事

### 定价空间
- 传统纪念视频：¥2000-50000
- AI 版本定价：¥99-299（10-100 倍降维）
- 边际成本：¥10-20/单
- 毛利率：80-90%

### 核心风险
1. Lensa 效应（新奇感消退）→ 对策：多场景+节日周期
2. 紧迫感缺失 → 对策：绑定节日营销
3. AI 质量 → 对策：真实照片+AI过渡画面混合
4. 信任门槛 → 对策：从家族圈口碑开始

---

## 四、Phase 0 验证方案

**目标**：最小成本验证"有人愿意付费"

### 步骤
1. **Day 1-3**：帮母亲完成外婆纪念视频（用现有 skill + 手动调整）
2. **Day 3-7**：母亲分享到家族群，观察自然传播（指标：≥3 人主动问"怎么做"）
3. **Day 7-14**：帮 3 个亲戚做，收费 ¥99（指标：≥2 人愿意付费）
4. **Day 14+**：观察二次传播

### 通过标准
- ≥2/3 亲戚付费
- ≥1 次二次传播
- 全部通过 → AI 人生电影升级为主线 A

### 绝对不做
- Phase 0 之前不建系统、不写代码
- 不告诉导演
- 不优化成本
- 不做品牌/域名/注册公司

---

## 五、AI 短剧工作室 — 主线 A

### 团队
- 导演：内容/质量把控
- 导演老婆：TikTok 投放经验（海外）
- sz：AI 生产管线

### 关键判断
- 做**内容工作室**，不做独立站/平台
- AI 杠杆在"量产效率"，质量由导演把控
- 海外 CPM 是国内 5-20 倍
- 如果 AI 人生电影验证通过，短剧工作室可能降为 A2

### Phase 路径
1. Phase 1（月1-2）：TikTok/YouTube 原生变现
2. Phase 2（月3-4）：投稿短剧平台分成
3. Phase 3（月6+）：考虑独立站（仅在盈利后）

---

## 六、技术讨论

### AI 视频 Skill SOP（已有）
7 步流程：创意 → 剧本 → 出图 → 分镜 → 网站 → 拍摄 → 剪辑
- 步骤 1-5 已自动化
- 步骤 6-7（视频生成+剪辑）尚未自动化
- 母亲是看到第 5 步（网站）后产生灵感的

### AI 视频生成成本
- 即梦/Jimeng（字节）：SeeDance 2.0 Fast = 5 credits/sec，免费 66 credits/day
- Kling AI 3.0：$0.07/sec（最便宜）
- Runway：$0.15-0.20/sec
- Sora：已于 2026-03 停服

### 剧本 Prompt 评估
用户找到一个网上的剧本生成 prompt（JSON 格式），讨论了如何写出高质量的创作型 prompt。

### 微信群素材收集
- 微信群无法拉入 bot
- 方案：手动收集 → 整理到文档
- 或用腾讯文档/石墨文档让亲戚直接编辑

---

## 七、知识库与工具链

### Obsidian 知识库架构
```
VPS: /root/.openclaw/obsidian-vault  (Markdown 源文件)
     ↓ generate.py
VPS: /root/.openclaw/obsidian-vault-site  (HTML 静态站点)
     ↓ git push
GitHub: szdbetter/clawlabs-kb  (HTML，GitHub Pages)
```

### Vault 同步方案（新建）
> 详见：`scripts/vault-sync-setup.sh`

**目标**：VPS Obsidian vault ↔ 本地 Mac Obsidian 双向同步

**架构**：
```
VPS vault ←(cron 10min)→ GitHub (private) ←(launchd 10min)→ Mac Obsidian
```

**设置步骤**：
1. GitHub 创建私有 repo: `szdbetter/obsidian-vault`
2. VPS 运行: `bash vault-sync-setup.sh vps`
3. Mac 运行: `bash vault-sync-setup.sh local`

---

## 八、CLAUDE.md 协作协议

已写入项目根目录 `CLAUDE.md`，定义了：
- **核心定位**：外脑（思考伙伴），不是执行者
- **用户画像**：技能栈、资源、已知弱点
- **项目状态**：所有业务线的优先级和 Phase 0 验证方案
- **协作模式**：Devil's Advocate 协议、方向探索协议
- **技术约定**：知识库路径、生成脚本

---

## 九、飞书 Muse Bot 记忆问题（2026-04-08 新增）

### 问题描述
母亲在飞书中使用 Muse bot（OpenClaw）收集外婆回忆时：
- Bot 记不住之前说的话
- 总结错乱，自由发挥（幻觉）
- 底层使用 MiniMax 模型，忠实复述能力不够

### Muse Bot 代码路径
`/root/.openclaw/workspace-muse`（VPS 上，本次沙盒环境无法访问）

### 诊断分析
3 层问题：
1. **消息碎片化** — 母亲发很多条短消息，bot 每条当独立请求
2. **MiniMax 模型局限** — 指令遵循和忠实复述能力不如 Claude
3. **缺乏持久记忆** — 无 memory 机制，对话历史可能被截断

### 解决方案（待执行）

**方案 A：累积式记忆文件（优先做）**
- 每次收到消息 → 原话追加到 `memories/{user_id}.md`
- 每次回复前 → 完整 memory 文件注入 system prompt
- 不让模型总结，直接存原文

```python
# 核心逻辑
MEMORY_FILE = f"memories/{user_id}.md"
# 收到消息 → 原话追加
with open(MEMORY_FILE, "a") as f:
    f.write(f"\n[{datetime.now()}] {user_name}: {msg.text}\n")
# 回复前 → 注入完整记忆
memory = open(MEMORY_FILE).read()
system_prompt = f"以下是用户已提供的所有内容...\n{memory}"
```

**方案 C：结构化引导问答**
- Bot 主动按顺序问问题，而非让母亲自由发挥
- 问题清单：基本信息 → 外貌特征 → 性格习惯 → 关键故事 → 家人关系 → 一句话总结
- 每收到回答先确认（"我记下了：xxx，对吗？"），再问下一个

### LLM 选型结论

**推荐：Claude Sonnet 4.6 替换 MiniMax**

| 模型 | 指令遵循 | 忠实复述 | 中文 | 成本 | 推荐 |
|------|---------|---------|------|------|------|
| Claude Sonnet 4.6 | 极强 | 极强 | 优秀 | $3/15 per M | ⭐⭐⭐⭐⭐ |
| GPT 5.4 | 强 | 强 | 好 | 类似 | ⭐⭐⭐⭐ |
| Gemini 3.1 Pro | 强 | 中等 | 好 | 便宜 | ⭐⭐⭐ |
| MiniMax | 中等 | 弱 | 好 | 免费额度大 | ⭐⭐ |

理由：母亲对话量不大（几十条消息），API 成本几毛钱。Claude 在"不编造、忠实引用"方面最强。

**飞书接入 Claude 的方式**：
- 飞书无官方 Claude 插件
- 方案：现有飞书 bot 框架 → 后端 LLM 从 MiniMax 换成 Claude API
- 或通过 OpenRouter 中转（如果 bot 用 OpenAI 兼容格式）

### 待执行（需在 VPS 上操作）
- [ ] 查看 `/root/.openclaw/workspace-muse` 代码结构
- [ ] 找到 LLM 调用层，替换 MiniMax → Claude Sonnet API
- [ ] 加入 memory.md 累积式记忆机制
- [ ] 加入结构化引导 prompt
- [ ] 测试后让母亲继续使用

---

## 十、项目命名讨论（2026-04-08 新增）

### 用户初始想法
"人生电影"，英文 "Moment"

### 分析
- "Moment" 太通用，已被多个产品占用（Samsung、Twitter），且含义是"瞬间"而非"一生"，方向反了

### 推荐命名

| 名称 | 英文 | 理由 | 推荐 |
|------|------|------|------|
| **一生** | **LifeReel** | 人生+胶片，直觉清晰 | ⭐⭐⭐⭐⭐ |
| 光影人生 | LifeFilm | 直白好理解 | ⭐⭐⭐⭐ |
| 念 | Memoire | 法语"记忆"，高级感 | ⭐⭐⭐⭐ |
| 时光机 | TimeCapsule | 时间胶囊概念 | ⭐⭐⭐ |
| 家书 | DearFamily | 限制了非家族场景 | ⭐⭐⭐ |

### 结论
Phase 0 阶段命名不重要，先用朴素名字做出第一条片子，验证通过再定品牌。

---

## 十一、环境与工具链问题（2026-04-08 新增）

### 当前环境
- 本次 session 在 **Claude 手机 App** 中运行
- 代码执行在 **云端 Linux 沙盒**（hostname: vm），不是本地 iMac
- 沙盒无 ssh，无法访问 VPS

### Claude Code 运行方式对比

| 方式 | 执行环境 | 能 SSH? | 能访问本地文件? |
|------|---------|---------|----------------|
| 手机 App / Desktop Web (claude.ai/code) | 云端沙盒 VM | ❌ | ❌ |
| **Desktop App 本地模式** | 本地 Mac | ✅ | ✅ |
| **CLI** (`claude` 命令) | 本地 Mac | ✅ | ✅ |

### 结论
要操作 VPS（改 Muse bot 代码、部署 vault 同步等），必须在 **Desktop App 本地模式** 或 **CLI** 中运行。

Desktop App 下载：https://claude.ai/download
CLI 安装：`curl -fsSL https://claude.ai/install.sh | bash`

---

## 十二、待办事项汇总（Next Actions）

### 🔴 紧急（回到 iMac 后立即做）
- [ ] 安装 Claude Code CLI 或使用 Desktop App 本地模式
- [ ] `git clone` 并切换到 `claude/人生电影项目` 分支
- [ ] 整理家族群外婆照片和回忆文字

### 🟡 本周
- [ ] 改 Muse Bot：替换 MiniMax → Claude Sonnet API + 加记忆机制（VPS: `/root/.openclaw/workspace-muse`）
- [ ] 用现有 skill 制作外婆纪念视频
- [ ] 完成视频交给母亲，观察反应
- [ ] 设置 Obsidian vault 双向同步

### 🟢 下周
- [ ] 如有亲戚询问 → 服务 + 收费 ¥99
- [ ] 观察付费意愿和二次传播
- [ ] Phase 0 结果评估

### 🔧 环境准备
- [ ] GitHub 创建私有 repo `szdbetter/obsidian-vault`
- [ ] VPS 运行: `bash vault-sync-setup.sh vps`
- [ ] Mac 运行: `bash vault-sync-setup.sh local`
- [ ] 删除旧分支: `git push origin --delete claude/switch-opus-4.6-m4ZCq`

---

## 十三、本 Session 产出的文件

| 文件 | 说明 | 状态 |
|------|------|------|
| `CLAUDE.md` | AI 协作协议 | ✅ 已提交 |
| `scripts/vault-sync-setup.sh` | Obsidian 双向同步脚本 | ✅ 已提交 |
| `docs/AI人生电影-市场调研报告.md` | 完整 9 章节市场调研 | ✅ 已提交 |
| `docs/Session-2026-04-06-战略讨论与AI人生电影.md` | 本文件（session 全记录） | ✅ 已提交 |

**所有文件在 `szdbetter/clawlabs-kb` repo，分支 `claude/人生电影项目`**
