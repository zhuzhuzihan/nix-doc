#!/usr/bin/env python3
"""mdbook preprocessor: 将 store types 生成页中的英文 Settings 描述替换为中文。

协议：stdin 为 [RenderContext, Book] JSON 数组（mdbook preprocessor v1）。
映射对来自同目录 zh-map.json（[英文md段落, 中文md段落] 列表）。
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
    if isinstance(data, dict) and 'supports' in data:
        json.dump({'supports': data['supports']}, sys.stdout)
        return
    context, book = data[0], data[1]
    with open(os.path.join(HERE, 'zh-map.json'), encoding='utf-8') as f:
        pairs = json.load(f)
    rules = []
    for en, zh in pairs:
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

    walk(book['items'])
    json.dump([context, book], sys.stdout, ensure_ascii=False)

if __name__ == '__main__':
    main()
