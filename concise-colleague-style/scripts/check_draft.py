"""Lint a draft (one message per line) against the form rules in SKILL.md.

Usage: python3 -I check_draft.py draft.txt   (or pipe the draft on stdin)
"""
import re
import sys

AVOID = ["厉害", "太棒", "非常好", "哈哈", "嘿嘿", "首先", "其次", "最后", "希望对你有帮助", "您"]


def check(lines):
    issues = []
    if len(lines) > 6:
        issues.append(f"{len(lines)} 条消息，通常 1–5 条")
    for i, line in enumerate(lines, 1):
        if line.endswith("。"):
            issues.append(f"第{i}条以句号结尾")
        if len(line) > 50:
            issues.append(f"第{i}条 {len(line)} 字，偏长（除非是讲架构或公告）")
        for w in AVOID:
            if w in line:
                issues.append(f"第{i}条含“{w}”，他几乎不这样说")
    zh = [l for l in lines if re.search(r"[\u4e00-\u9fff]", l)]  # English lines run longer by nature
    short = sum(len(l) <= 15 for l in zh)
    if zh and short / len(zh) < 0.5:
        issues.append("超过一半的行长于 15 字，可以拆短")
    return issues


if __name__ == "__main__":
    text = open(sys.argv[1], encoding="utf-8").read() if len(sys.argv) > 1 else sys.stdin.read()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    problems = check(lines)
    print("\n".join(problems) if problems else "OK")
