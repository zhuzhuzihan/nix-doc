#!/usr/bin/env python3
"""mdbook 0.5 preprocessor：将 store types 生成页中的英文 Settings 描述替换为中文。

协议（mdbook 0.5.2）：
- supports 探测：argv[1] == "supports"，退出码 0 表示支持全部 renderer。
- 处理：stdin 为 (RenderContext, Book) JSON 数组；stdout 只输出 Book 对象。
映射对来自同目录 zh-map.json（[英文md段落, 中文md段落] 列表），
替换使用空白鲁棒正则；未命中段落保持英文，安全降级。
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'supports':
        sys.exit(0)

    data = json.load(sys.stdin)
    context, book = data[0], data[1]
    with open(os.path.join(HERE, 'zh-map.json'), encoding='utf-8') as f:
        pairs = json.load(f)
    def build_pattern(text):
        # 空白鲁棒 + 智能标点归一（mdbook 渲染时 ' -> ’、" -> ""、- -> –— 等）
        text = re.sub(r'\s+', ' ', text).strip()
        out = []
        for ch in text:
            if ch.isspace():
                out.append(r'\s+')
            elif ch in "'’‘":
                out.append("['\u2019\u2018]")
            elif ch in '"“”':
                out.append('[\"\u201c\u201d]')
            elif ch in '-\u2013\u2014':
                out.append('[-\u2013\u2014]')
            else:
                out.append(re.escape(ch))
        return re.compile(''.join(out))

    rules = []
    for en, zh in pairs:
        rules.append((build_pattern(en), zh.replace('\\', '\\\\')))

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
    json.dump(book, sys.stdout, ensure_ascii=False)

if __name__ == '__main__':
    main()
