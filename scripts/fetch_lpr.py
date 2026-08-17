# -*- coding: utf-8 -*-
"""
fetch_lpr.py - 自动抓取最新 LPR 并更新知识库（E 盘，不占 C 盘）
数据源：中国人民银行官网 LPR 公告（pbc.gov.cn）
用法： python fetch_lpr.py
"""
import urllib.request, re, json, os, sys

LPR_LIST_URL = "https://www.pbc.gov.cn/zhengcehuobisi/125207/125213/125440/index.html"
KB_LPR = os.path.join(os.path.dirname(__file__), "..", "knowledge", "lpr", "lpr.json")

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


def fetch(url):
    req = urllib.request.Request(url, headers=HEADERS)
    return urllib.request.urlopen(req, timeout=25).read()


def decode_gbk(raw):
    # 页面为 UTF-8 为主、含少量杂散字节；先试 UTF-8 ignore
    try:
        return raw.decode("utf-8", errors="ignore")
    except Exception:
        return raw.decode("gb18030", errors="replace")


def parse_lpr(html_text, raw):
    """从公告正文提取 1年期/5年期 LPR。
    页面为 GBK 混合编码，中文上下文易乱码；故在原始字节上定位
    GBK 编码的 "1年期" / "5年期" 字节，再取其后的第一个百分比。"""
    # GBK 编码：年=\xc4\xea 期=\xc6\xda 以=\xd2\xd4 上=\xc9\xcf 为=\xce\xaa
    pat_1y = b"1\xc4\xea\xc6\xda"                       # "1年期"
    pat_5y = b"5\xc4\xea\xc6\xda\xd2\xd4\xc9\xcf"      # "5年期以上"
    pct = re.compile(rb"[0-9]\.[0-9]{1,2}%")

    def near(pat):
        i = raw.find(pat)
        if i < 0:
            return None
        seg = raw[i:i + 80]
        m = pct.search(seg)
        return m.group(0).decode() if m else None

    lpr1, lpr5 = near(pat_1y), near(pat_5y)
    if lpr1 and lpr5:
        return lpr1, lpr5
    # 退化：5年期以上未匹配，试 "5年期"
    if lpr5 is None:
        pat_5y2 = b"5\xc4\xea\xc6\xda"
        lpr5 = near(pat_5y2)
    if lpr1 and lpr5:
        return lpr1, lpr5
    # 兜底：纯 ASCII 百分比扫描
    pcts = re.findall(rb"[0-9]\.[0-9]{1,2}%", raw)
    pcts = [p.decode() for p in pcts]
    if len(pcts) >= 2:
        uniq = list(dict.fromkeys(pcts))
        if len(uniq) == 2:
            return min(uniq, key=lambda x: float(x[:-1])), max(uniq, key=lambda x: float(x[:-1]))
        return uniq[-2], uniq[-1]
    return None, None


def latest_announcement_url():
    html = decode_gbk(fetch(LPR_LIST_URL))
    # 只取含 8 位日期段的公告详情链接，如 .../3876551/2026072008093186869/index.html
    links = re.findall(r'href="([^"]+/\d{8}\d*/index\.html)"', html)
    if not links:
        raise RuntimeError("未在央行 LPR 页找到公告链接")
    return "https://www.pbc.gov.cn" + links[0]


def main():
    ann_url = latest_announcement_url()
    raw = fetch(ann_url)
    html_text = decode_gbk(raw)
    lpr1, lpr5 = parse_lpr(html_text, raw)
    if not lpr1 or not lpr5:
        print("FAILED: 未解析出 LPR 数值，页面结构可能变化")
        sys.exit(1)

    with open(KB_LPR, "r", encoding="utf-8") as f:
        kb = json.load(f)

    # 追加历史记录
    kb["history"].append({
        "period": f"verified-{latest_date_from_url(ann_url)}",
        "lpr_1y": lpr1,
        "lpr_5y": lpr5,
    })
    # 去重
    seen = set()
    kb["history"] = [h for h in kb["history"] if not (h["period"] in seen or seen.add(h["period"]))]

    kb["current"] = {
        "as_of": latest_date_from_url(ann_url),
        "lpr_1y": lpr1,
        "lpr_5y": lpr5,
        "private_lending_cap": f"{float(lpr1[:-1])*4:.1f}% ({lpr1} x 4)",
        "note": "来自央行官方公告自动抓取",
        "source_url": ann_url,
    }
    with open(KB_LPR, "w", encoding="utf-8") as f:
        json.dump(kb, f, ensure_ascii=False, indent=2)

    print(f"LPR updated: 1年期 {lpr1}, 5年期 {lpr5}, 民间借贷上限 {kb['current']['private_lending_cap']}")
    print(f"公告: {ann_url}")


def latest_date_from_url(url):
    m = re.search(r"/(\d{8})/index\.html$", url)
    return m.group(1) if m else "unknown"


if __name__ == "__main__":
    main()
