#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import re
import time

# pip install symusic openai
from openai import OpenAI
from symusic import Score, Synthesizer, dump_wav

SYSTEM = """# 角色
你是一个才华横溢的**流行音乐创作大师**，擅长用ABC记谱法，

## 技能：
### 技能 1：打造音乐结构
- 掌握并运用流行音乐常见的乐曲形式：前奏、主歌1、副歌1、主歌2、副歌2、中段（独奏或桥梁）、副歌3以及尾声。
- 根据用户输入决定ABC内容，包含X T M K X L P标记
- 根据输入，选择和主题匹配的讨论和弦、调性、标题、情绪、速度、节奏。

### 技能 2：创作动人旋律
- 多使用七和弦和分解和弦
- 旋律好听，节奏要跟随发展产生较大的变化
- 副歌部分用简洁且重复的旋律，让人忍不住想一遍遍重复听

## 要求：
- M标记的拍数严格等于每个小节拍数，比如当M:4/4是，每小节的拍数都为4
- 音符后面的数字代表持续时长，控制每小节的拍数符合M的要求

## 输出格式：
- 和弦标记要用引号
- 在ABC乐谱中，用P:标记段落，段落之间用换行分隔
- 使用ABC谱输出乐曲内容，确保其格式完全符合ABC标准。
- 用markdown的代码块格式输出乐谱，方便用户阅读和理解。
"""


def chat(human, system=SYSTEM, model='gpt-3.5-turbo', **openai_kwargs):
    openai_kwargs['api_key'] = openai_kwargs.get('api_key') or os.environ.get("OPENAI_API_KEY")
    client = OpenAI(**openai_kwargs)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": human}
        ],
        model=model,
    )
    print(f'消耗token:{chat_completion.usage}')
    return chat_completion.choices[-1].message.content


def process(content):
    abc_notation = re.search(r'```.*(X:.*)```', content, flags=re.S) or re.search(r'```.*(T:.*)```', content, flags=re.S)
    if not abc_notation:
        print('解析失败！😭')
    abc_notation = abc_notation.group(1)
    if 'X:' not in abc_notation:
        abc_notation = f'X:1\n{abc_notation}'
    title = re.search(r'T:(.+?)\n', abc_notation, flags=re.S)
    title = (title and title.group(1)) or int(time.time())
    filename = f"{title}.wav"
    abc_notation = abc_notation.strip().replace('\n\n', '\n').replace('min', 'm')
    s = Score.from_abc(abc_notation)
    audio = Synthesizer().render(s, stereo=True)
    dump_wav(filename, audio, sample_rate=44100, use_int16=True)
    return filename


def run(human, model=None, **openai_kwargs):
    print(f'{model} 思考中🤔...\n\n')
    resp = chat(human, model=model, **openai_kwargs)
    print(resp)
    print(f'ABC乐谱 处理中...\n\n')
    filename = process(resp)
    print(f'完成! 文件:当前目录/{filename}')


def main():
    parser = argparse.ArgumentParser(description='GPT_Musician 快速生成旋律')
    parser.add_argument('-p', '--prompt', required=True, help='music prompt')
    parser.add_argument('-m', '--model', default='gpt-4', help='openai chat model name')
    parser.add_argument('-key', '--api_key', help='openai api key')
    args = parser.parse_args()
    run(args.prompt, args.model, api_key=args.api_key)


if __name__ == '__main__':
    main()
