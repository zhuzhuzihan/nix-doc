#!/usr/bin/env python3
"""mdbook preprocessor: 将 store types 生成页中的英文 Settings 描述替换为中文。

映射对来自 preprocessor/zh-map.json（[英文md段落, 中文md段落] 列表）。
替换使用空白鲁棒正则（源码 R"(...)" 的换行/缩进不影响匹配）；
未命中的段落保持英文，安全降级。
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    data = json.load(sys.stdin)
    if 'supports' in data:
        json.dump({'supports': data['supports']}, sys.stdout)
        return
    with open(os.path.join(HERE, 'zh-map.json'), encoding='utf-8') as f:
        pairs = json.load(f)
    rules = []
    for item in pairs:
        en, zh = item[0], item[1]
        pat = re.compile(r'\s+'.join(map(re.escape, en.split(' '))))
        rules.append((pat, zh.replace('\\', '\\\\')))

    def repl(content):
        for pat, zh in rules:
            content = pat.sub(zh, content)
        return content

    def walk(items):
        for it in items:
            if isinstance(it, dict) and 'Chapter' in it:
                ch = it['Chapter']
                ch['content'] = repl(ch['content'])
                walk(ch.get('sub_items', []))

    walk(data['book']['sections'])
    json.dump(data, sys.stdout, ensure_ascii=False)

if __name__ == '__main__':
    main()
