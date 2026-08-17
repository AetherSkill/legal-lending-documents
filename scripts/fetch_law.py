# -*- coding: utf-8 -*-
"""
fetch_law.py - 法条核验辅助脚本
flk.npc.gov.cn 现需图形验证码（405/验证码拦截），无法全自动抓取。
本脚本提供：
  1) 列出知识库中所有"待复核"法条，附官方核验链接
  2) 人工在 flk.npc.gov.cn 核对后，可将某条法条标记为"已核验"
用法：
  python fetch_law.py list            # 列出待复核条目
  python fetch_law.py mark <法律key> <条款>   # 标记某条已核验
数据均在 E 盘，不占 C 盘。
"""
import json, os, sys

KB_LAWS = os.path.join(os.path.dirname(__file__), "..", "knowledge", "laws", "laws.json")
OFFICIAL = {
    "civil_code": "https://flk.npc.gov.cn/detail2.html?ZmY4MDgxODE4MTAwYjBjZjAxODEyNTA3YTU5NzEzZTE%3D",
    "private_lending": "https://www.court.gov.cn/fabu-xiangqing-263041.html",
    "civil_procedure": "https://flk.npc.gov.cn/detail2.html?ZmY4MDgxODE4MTAwYjBjZjAxODEyNTA3YTU5NzEzZTE%3D",
}


def load():
    with open(KB_LAWS, "r", encoding="utf-8") as f:
        return json.load(f)


def save(kb):
    with open(KB_LAWS, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)


def cmd_list():
    kb = load()
    print("=== 待复核法条 ===")
    for law_key, law in kb["laws"].items():
        for art in law["articles"]:
            if art.get("verify") == "待复核":
                print(f"  [{law_key}] {law['name']} {art['article']}")
    print("\n核验入口：")
    for k, url in OFFICIAL.items():
        print(f"  {k}: {url}")
    print("\n用法：python fetch_law.py mark <law_key> <条款号>  (例如: python fetch_law.py mark civil_code 第五百七十九条)")


def cmd_mark(law_key, article):
    kb = load()
    if law_key not in kb["laws"]:
        print(f"错误：未知法律 {law_key}"); sys.exit(1)
    done = False
    for art in kb["laws"][law_key]["articles"]:
        if art["article"] == article:
            art["verify"] = "已核验"
            done = True
    if not done:
        print(f"错误：未找到条款 {law_key} / {article}"); sys.exit(1)
    save(kb)
    print(f"已标记为已核验：{law_key} / {article}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        cmd_list()
    elif sys.argv[1] == "list":
        cmd_list()
    elif sys.argv[1] == "mark" and len(sys.argv) == 4:
        cmd_mark(sys.argv[2], sys.argv[3])
    else:
        print("用法：python fetch_law.py list | mark <law_key> <条款号>")
