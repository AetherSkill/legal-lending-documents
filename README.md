<p align="center">
  <img src="posters/poster1.png" width="480" alt="民间借贷 AI 起诉状生成器">
</p>

<h1 align="center">民间借贷 · AI 起诉状生成器</h1>
<h3 align="center"><code>legal-lending-documents</code> · Aether Legal Lab</h3>

<p align="center">
  <b>欠钱不还？AI 帮你把账要回来，从一份专业起诉状开始。</b><br>
  输入案情要素 → 依权威法条与真实案例 → 生成公文排版起诉状 Word + 引用记录 Word
</p>

<p align="center">
  <img alt="version" src="https://img.shields.io/badge/version-v1.0.0-0a1020?style=flat-square">
  <img alt="type" src="https://img.shields.io/badge/type-AI%20Skill-d9b45c?style=flat-square">
  <img alt="license" src="https://img.shields.io/badge/license-MIT-8fa3c7?style=flat-square">
</p>

---

## 🎯 这是什么

一个**民间借贷（欠钱不还）**场景的 AI 法律文书工作流 Skill。

它不是"随便写写"的生成器——以**生成质量与可信度**为核心：**每个法律结论都标注具体法条与真实案例案号，来源可追溯、可核验、绝不编造。**

## ✨ 核心能力

| 能力 | 说明 |
|------|------|
| 🏛️ **专业** | 对齐最高法/司法部 2024 年 11 类 44 份民事起诉状示范文本（要素式），口径与法院一致 |
| 🛡️ **可信** | 每个结论标注具体法条与真实案号（含最高法公报案例），附官方核验链接 |
| 📐 **规范** | 公文排版 Word：仿宋正文/黑体小标题/首行缩进/规范页边距，拿来即用 |
| ⚡ **高效** | 一次输入，自动按「合同成立时 LPR×4」核算利率上限，双 Word 同步交付 |

## 🧠 可信度机制（为什么可以信它）

1. **法条精确到款/项**：`【依据】《中华人民共和国民法典》第五百七十九条`——不写模糊的"依据相关法律"。
2. **真实案号可引**：内置已核验的真实案例（最高法公报），如 `(2014)民一终字第38号`（本金以实际交付为准）。
3. **绝不编造**：找不到可核验的案号，就诚实标注"案号可在人民法院案例库检索"，绝不伪造。
4. **利率自动核算**：按「合同成立时 LPR×4」计算上限，约定超限部分主动提示不予支持。
5. **时效水印 + 免责声明**：标注 LPR 取值时点，明示 AI 生成非法律意见。

---

## 🚀 快速开始

### 方式一：直接下载（推荐）

| 渠道 | 链接 |
|------|------|
| **下载 ZIP** | https://github.com/jeliael/legal-lending-documents/archive/refs/heads/main.zip |
| 仓库首页 | https://github.com/jeliael/legal-lending-documents |

下载后解压，将 `SKILL.md` 放入你的 skill 目录（如 opencode 的 `.opencode/skill/legal-lending-documents/` 或 Claude 的 `~/.claude/skills/`）。

### 方式二：skills.sh 生态安装

```bash
npx skills add jeliael/legal-lending-documents
```

### 方式三：git clone

```bash
git clone https://github.com/jeliael/legal-lending-documents.git
```

---

## 📖 使用方法（三步）

### 第 1 步：装入 AI 工具
将 `SKILL.md` 放到你的 opencode / Claude Code 的 skills 目录（见快速开始）。

### 第 2 步：告诉 AI 你的案情
用自然语言描述，例如：

> "李四 2023年3月1日借了我 5 万块钱，银行转账的，约定年利率 15%，2023年9月1日到期，到现在没还，催了很多次都不理。"

### 第 3 步：获取双 Word 交付
AI 自动产出两份文档：
1. **民事起诉状 Word**（要素式 + 叙述式，公文排版）
2. **引用与借鉴记录 Word**（法条/真实案号/数据来源逐条可追溯）

## 🖥️ 实机演示

**输入：**
> 原告张三 · 被告李四｜2023-03-01 借款 50,000 元，银行转账｜约定年利率 15%，2023-09-01 到期｜到期未还，多次催收无果

**输出：**

| 环节 | 结果 |
|------|------|
| 📄 交付物 | 民事起诉状 Word（要素式+叙述式）＋ 引用与借鉴记录 Word，公文排版即用 |
| 💰 利率核算 | 合同成立时 LPR 3.65% × 4 = **14.6%**；约定 15% **超出部分不予支持**，诉请按 14.6% 主张 |
| ⚖️ 专业判断 | 转账凭证 ⇒ 合同自交付时成立（民法典§679），列为必核证据；2023 年借贷不适用旧 24%/36% 分段规则 |
| 🔗 引用核验 | 可引真实案号（2014）民一终字第38号；附 flk 法条库 / 人民法院案例库 / 央行 LPR 链接 |
| ⚠️ 风险提示 | 现行 LPR 于生成日复核；诉讼费另计；文末附时效水印与免责声明 |

**示例产物**（仓库 `examples/` 目录）：
- [示例-民事起诉状.docx](examples/示例-民事起诉状.docx)
- [示例-引用与借鉴记录.docx](examples/示例-引用与借鉴记录.docx)

---

## 📁 目录结构

```
legal-lending-documents/
├── SKILL.md                    # Skill 定义（工作流核心）
├── knowledge/
│   ├── laws/laws.json          # 核心法条库（含核验状态）
│   ├── lpr/lpr.json            # LPR 数据与利率上限
│   ├── templates/              # 起诉状模板（要素式+叙述式）
│   └── cases/cases_seed.md     # 权威类案库（已核验真实案号）
├── scripts/
│   ├── fetch_lpr.py            # LPR 自动抓取（央行官方）
│   ├── fetch_law.py            # 法条核验状态管理
│   ├── generate_docx.py        # 起诉状 Word 生成
│   └── generate_references_docx.py  # 引用记录 Word 生成
├── posters/                    # 产品海报
└── examples/                   # 示例交付物（Word）
```

## 🔧 数据与知识库

| 来源 | 权威性 | 用途 |
|------|--------|------|
| flk.npc.gov.cn（国家法律法规数据库）| 人大官方 | 法条全文核验 |
| court.gov.cn（最高法）| 最高法官方 | 司法解释、指导案例 |
| rmfyalk.court.gov.cn（人民法院案例库）| 最高法官方 | 权威类案 |
| chinamoney.com.cn（央行授权）| 官方 | LPR 数据 |
| 北大法宝 MCP（mcp.pkulaw.com）| 商业 | 规模化检索 + 引证校验 |

> LPR 每月 20 日更新，运行 `python scripts/fetch_lpr.py` 自动同步最新值。

## ⚠️ 免责声明

本文书由 AI 生成，仅供参考与初稿使用，**不构成法律意见**，不承诺诉讼结果；立案与正式提交前，请以受诉法院要求为准并建议咨询执业律师。

## 📜 许可证

[MIT](LICENSE) © Aether Legal Lab

---

<p align="center"><b>黑夜孕育光明，Aether 把你的权益锻造成文书。</b><br>AETHER · AI 法律文书工作台</p>
