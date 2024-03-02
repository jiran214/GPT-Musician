# GPT-Musician
AI生成简单音乐 —— 使用ChatGPT稳定生成和播放

项目思路：Prompt -> ABC记谱法表示的音乐 -> abc转wav

喜欢的话点个Star支持一下！



## 快速开始
安装python >= 3.8
```shell
# 拉取项目 
git clone https://github.com/jiran214/GPT-Musician.git
# 进入目录安装依赖
pip install symusic openai
# 查看用法
python main -h
# 生成 eg: python main.py -p 把月光曲改成现代流行音乐 -key xxx
python main.py -p <your_prompt> -key <your openai_api_key>
```

## 想说的话
1. 生成效果差强人意，简单的音乐没问题
2. 默认的GPT4效果明显好于3.5
3. prompt经常对应不上生成结果，prompt对音乐描述越简单成功率越高
4. 可尝试修改SYSTEM变量修改prompt
5. 后续值得尝试的方向：通过HuggingFace ABC数据集微调ChatGPT实现更复杂(多声部、复杂节奏)的输出
6. 有想法在issue分享
7. 项目启发 https://twitter.com/reach_vb/status/1763315222285009297