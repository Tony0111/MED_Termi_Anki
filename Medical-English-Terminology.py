import os
import random
import time
import requests
import edge_tts
import aiohttp
from pathlib import Path
import asyncio
from typing import List, Dict, Optional
import genanki
import uuid
import pandas as pd
from quary import query_morpheme

# DeepSeek API 配置
DEEPSEEK_API_KEY = ""
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"


# ========================================================
# ========== 设置卡片样式 ============
# ========================================================

CSS = '''
/* --- 通用基础样式 --- */
.card {
    font-family: 'Noto Sans SC', 'Inter', 'Roboto', 'Open Sans', 'Microsoft YaHei', Arial, sans-serif;
    line-height: 1.7; /* 适当增加行高，提高阅读舒适度 */
    text-align: center; /* 默认卡片内容居中，对齐更整洁 */
    padding: 20px; /* 增加整体内边距，呼吸感更强 */
    font-size: 20px; /* 基础字号 */
    /* 卡片外观 */
    border: 1px solid #e0e0e0; /* 轻微的浅灰色边框 */
    border-radius: 12px;     /* 柔和的圆角 */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* 柔和的阴影 */
    transition: background 0.3s ease, color 0.3s ease, border-color 0.3s ease, box-shadow 0.3s ease; /* 平滑过渡 */
    /* 亮色模式背景颜色 - 使用渐变 */
    background-image: linear-gradient(to bottom right, #b9f1ef, #eca2a4); 
    background-color: #ffffff; /* 渐变不支持时的 fallback */
    color: #333; /* 比纯黑更柔和的深灰色 */
    box-sizing: border-box; /* 确保 padding 不增加总宽度 */

}
/* 核心词语样式 */
.front-word {
    font-size: 30px; /* 核心词语更大 */
    font-weight: 700; /* 加粗 */
    line-height: 1.2;
    margin-bottom: 20px;
    color: #3c88a2; /* 亮色主题下核心词语颜色 */
    background-color: transparent; /* 确保背景透明 */
    transition: color 0.3s ease;
    position: relative; /* for ::after pseudo-element */
    /* Morpheme 没有音频，所以这里不需要手型光标 */
    cursor: default; /* 保持普通光标 */
}
/* 核心词语下划线动画效果 */
.front-word::after {
    content: '';
    display: block;
    width: 90px; /* 下划线宽度 */
    height: 3px; /* 下划线高度 */
    background-color: #3c88a2; /* 亮色主题下划线颜色 */
    margin: 15px auto 0; /* 居中并在下方留白 */
    border-radius: 2px;
    transition: background-color 0.3s ease;
}
/* 各个内容区分割块的通用样式 */
.section {
    margin-top: 10px; /* 增加段落间距 */
    padding: 10px; /* 增加内边距 */
    background-color: transparent;
    color: #333; /* 亮色模式下文本颜色 */
    font-size: 16px;
    line-height: 1.7;
    text-align: left; /* 段落内容左对齐更易读 */
    /* 分隔线效果 */
    border-bottom: 1px dashed #e0e0e0; 
    margin-left: -20px; /* 负边距，让分隔符延伸到卡片边缘 */
    margin-right: -20px;
    padding-left: 20px; /* 弥补负边距，保持内容对齐 */
    padding-right: 20px;
    transition: color 0.3s ease, border-color 0.3s ease;
}
/* 最后一个 section 不要有底部分隔线 */
.section:last-of-type {
    border-bottom: none;
}
/* section 内部的强调文本（例如标题）*/
.section strong {
    font-size: 17px; /* 稍微大一点，作为小标题 */
    font-weight: 600; /* 适度加粗 */
    display: inline;  /* 保持在一行，与后面的文本继续 */
    letter-spacing: 0.5px; /* 字母间距 */
    color: #3c88a2; /* 亮色主题下的小标题颜色 */
    background-color: transparent;
    transition: color 0.3s ease;
    /* cursor: pointer; 由 JS 动态添加 */
}
/* ------------------------------------------------------------- */
/* !!! 新增：卡片右下角 Logo 样式 !!! */
/* ------------------------------------------------------------- */
.card::after {
    content: '_达__'; /* 你的 Logo 文本 */
    position: absolute;
    bottom: 15px; /* 距离卡片底部的距离 */
    right: 20px; /* 距离卡片右侧的距离 */
    font-size: 14px; /* Logo 字体大小 */
    color: rgba(0, 0, 0, 0.4); /* 柔和的深灰色，稍微透明 */
    opacity: 0.6; /* 整体透明度，使其更像水印 */
    font-weight: 500; /* 适度字重 */
    pointer-events: none; /* 确保它不可点击，不干扰卡片操作 */
    user-select: none; /* 防止用户意外选中文本 */
    z-index: 10; /* 确保 Logo 显示在其他内容之上 */
    letter-spacing: 1px; /* 增加一点字母间距，使其看起来更独特 */
}


/* 图片样式 */
img {
    max-width: 100%;
    height: auto;
    display: block;
    margin: 20px auto;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05); /* 图片也可以有轻微阴影 */
}
/* 链接样式 */
a {
    color: #007bff;
    text-decoration: none;
    transition: color 0.2s ease;
}
a:hover {
    text-decoration: underline;
}





/* --- Anki 桌面版夜间模式样式 --- */
/* (Anki 桌面版会在 body 或 html 元素上添加 'nightMode' 类) */
.nightMode .card {
    color: #eee; /* 浅色文本 */
    /* **修改：夜间模式背景渐变** */
    background-image: linear-gradient(to bottom right, #153a3d, #3d1815); /* 深蓝到深橙的渐变 */
    background-color: #2c2c2c; /* 渐变不支持时的 fallback */

    border-color: #4a4a4a;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
}

.nightMode .front-word {
    color: #4a4a4a; /* 夜间模式核心词语颜色 */
}

.nightMode .front-word::after {
    background-color: #dd8804; /* 夜间模式下划线颜色 */
}

.nightMode .section {
    color: #eee;
    border-color: #4a4a4a; /* 夜间模式下分隔线颜色 */
}

.nightMode .section strong {
    color: #dd8804; /* 夜间模式小标题颜色 */
}

.nightMode a {
    color: #8ab4f8; /* 夜间模式链接颜色 */
}


/* --- AnkiDroid / AnkiMobile 暗色主题样式 --- */
/* 使用与桌面版夜间模式一致的渐变 */
.card.night_mode, .card.night_mode.black {
    color: #eee;
    background-image: linear-gradient(to bottom right, #153a3d, #3d1815); /* 深蓝到深橙的渐变 */
    background-color: #2c2c2c; /* 渐变不支持时的 fallback */

    border-color: #4a4a4a;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
}
.card.night_mode .front-word, .card.night_mode.black .front-word {
    color: #dd8804;
}
.card.night_mode .front-word::after, .card.night_mode.black .front-word::after {
    background-color: #dd8804;
}
.card.night_mode .section, .card.night_mode.black .section {
    color: #eee;
    border-color: #4a4a4a;
}
.card.night_mode .section strong, .card.night_mode.black .section strong {
    color: #dd8804;
}
/* 确保夜间模式下的链接颜色与桌面版一致 */
.card.night_mode a, .card.night_mode.black a {
    color: #8ab4f8;
}

'''

TEMPLATE = [
    {
                    'name': 'Card 1',
                    'qfmt': '''

                    <div class="front-word" data-anki-audio-field="MorphemeAudio">
                        {{Morpheme}}
                    </div>

                    ''',
                    'afmt': '''


                        <div class="front-word">{{Morpheme}}</div>
                        <hr>
                        <div class="section">
                            <!-- 将 data-audio-source 改为 data-audio-field-name -->
                            <strong data-audio-field-name="EnglishExplanationAudio">English Explanation:</strong> {{EnglishExplanation}}<br>
                            <strong>Chinese Translation:</strong> {{ChineseTranslation}}<br>
                            {{EnglishExplanationAudio}}
                        </div>
                        <div class="section">
                            <strong data-audio-field-name="ExampleWordsAudio">Example Words:</strong> {{ExampleWords}}<br>
                            {{ExampleWordsAudio}}
                        </div>
                        <div class="section">
                            <strong data-audio-field-name="ExampleSentenceAudio">Example Sentence:</strong> {{ExampleSentence}}<br>
                            {{ExampleSentenceAudio}}
                        </div>

                        <!-- !!! 关键改动 !!! -->
                        <!-- 这个 div 专门用来存放 Anki 需要“看见”的音频字段，以便它打包音频。 -->
                        <!-- 由于它被彻底隐藏，Anki 不会为其渲染任何默认播放按钮。 -->
                        <!-- 每个音频字段都被包裹在一个带有唯一ID的span中，便于JavaScript查找。 -->
                        <div id="anki-sound-data" style="display:none; visibility:hidden;">
                            <span id="EnglishExplanationAudio_sound">{{EnglishExplanationAudio}}</span>
                            <span id="ExampleWordsAudio_sound">{{ExampleWordsAudio}}</span>
                            <span id="ExampleSentenceAudio_sound">{{ExampleSentenceAudio}}</span>
                        </div>


                    ''',
                },
]

# ========================================================

class AnkiCardGenerator:

    def __init__(self, output_dir: str = "medical_anki_cards", csv_path: str = None):
        self.start_time = time.time()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.media_files = []  # 存储所有媒体文件
        
        # 加载 CSV 文件
        self.csv_df = None
        if csv_path:
            try:
                self.csv_df = pd.read_csv(csv_path, usecols=['morpheme', 'meaning'], encoding='utf-8')
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 成功加载 CSV 文件: {csv_path}")
            except Exception as e:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 加载 CSV 文件失败: {str(e)}")
        
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Anki卡片生成器初始化开始")
        
        # 定义Anki模型
        self.model_id = random.randrange(1 << 30, 1 << 31)
        self.model = genanki.Model(
            self.model_id,
            'Medical Morpheme Model by Da',
            fields=[
                {'name': 'Morpheme'},
                {'name': 'EnglishExplanation'},
                {'name': 'ChineseTranslation'},
                {'name': 'ExampleWords'},
                {'name': 'ExampleSentence'},
                {'name': 'EnglishExplanationAudio'},
                {'name': 'ExampleWordsAudio'},
                {'name': 'ExampleSentenceAudio'},
            ],
            templates=TEMPLATE,
            css=CSS
        )
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Anki卡片生成器初始化完成，耗时: {time.time() - self.start_time:.2f}秒")

    def get_morpheme_info_from_deepseek(self, morpheme: str, english_explanation: str) -> Optional[Dict[str, str]]:
        """调用DeepSeek API生成医学词素的中文翻译、例词和例句"""
        start_time = time.time()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始从DeepSeek获取 {morpheme} 的信息")
        
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""
        为医学英语词素 '{morpheme}' 生成学习内容，适合医学生使用。已提供英文解释 '{english_explanation}'，请基于此生成中文翻译，并提供例词和例句。内容需准确且贴近医学场景，提供以下信息：

        1. ChineseTranslation: 提供英文解释 '{english_explanation}' 的中文翻译，简洁，控制在1-5词。
        2. ExampleWords: 提供3个包含该词素的医学单词，每个单词后跟中文解释，中文用括号分隔，单词间用逗号分隔，单词需准确且常用。
        3. ExampleSentence: 提供一个使用上述例词之一的例句，英文例句后跟中文翻译，中文用括号分隔，单行显示，例句应具描述性，每部分控制在15-25词。

        要求：
        - 内容准确，符合医学专业术语规范，例句需与医学场景相关，提供足够的上下文。
        - 返回格式如下：
        ChineseTranslation: ...
        ExampleWords: ...
        ExampleSentence: ...

        示例：
        输入：morpheme: aden-o, english_explanation: Gland
        输出：
        ChineseTranslation: 腺体
        ExampleWords: Adenoma (腺瘤), Adenitis (腺炎), Adenopathy (腺病)
        ExampleSentence: The patient underwent surgery to remove a benign adenoma from her thyroid gland last month (患者上个月接受手术切除甲状腺上的良性腺瘤)
        """
        
        payload = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
            "max_tokens": 1000
        }
        
        try:
            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
            response.raise_for_status()
            
            content = response.json()['choices'][0]['message']['content']
            info = {}
            current_field = None
            current_content = []
            
            for line in content.split('\n'):
                line = line.strip()
                if line.startswith("ChineseTranslation:"):
                    if current_field and current_content:
                        info[current_field] = "\n".join(current_content).strip()
                    current_field = "chinese_translation"
                    current_content = [line.replace("ChineseTranslation:", "").strip()]
                elif line.startswith("ExampleWords:"):
                    if current_field and current_content:
                        info[current_field] = "\n".join(current_content).strip()
                    current_field = "example_words"
                    current_content = [line.replace("ExampleWords:", "").strip()]
                elif line.startswith("ExampleSentence:"):
                    if current_field and current_content:
                        info[current_field] = "\n".join(current_content).strip()
                    current_field = "example_sentence"
                    current_content = [line.replace("ExampleSentence:", "").strip()]
                elif line and current_field:
                    current_content.append(line)
            
            if current_field and current_content:
                info[current_field] = "\n".join(current_content).strip()
                
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 成功获取 {morpheme} 的信息，耗时: {time.time() - start_time:.2f}秒")
            return info
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 获取 {morpheme} 信息失败: {str(e)}，耗时: {time.time() - start_time:.2f}秒")
            return None

    def generate_random_filename(self, prefix: str) -> str:
        """生成随机文件名"""
        return f"{prefix}_{uuid.uuid4().hex}.mp3"

    def is_valid_audio_file(self, file_path, min_size=1024):
        """检查音频文件是否有效（基于文件大小）"""
        if not os.path.exists(file_path):
            return False
        file_size = os.path.getsize(file_path)
        return file_size >= min_size

    async def generate_tts(self, text: str, output_file: Path, semaphore, max_retries: int = 3, retry_delay: int = 5) -> bool:
        """生成TTS音频，包含重试机制和完整性检查"""
        start_time = time.time()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始生成音频: {output_file}")
        
        async with semaphore:
            # 检查现有文件是否有效
            if self.is_valid_audio_file(output_file):
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 音频文件已存在且有效，跳过生成: {output_file}")
                return True

            voice = "en-US-AriaNeural"
            for attempt in range(max_retries):
                try:
                    communicate = edge_tts.Communicate(text, voice)
                    await communicate.save(str(output_file))
                    if self.is_valid_audio_file(output_file):
                        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 成功生成音频: {output_file}，耗时: {time.time() - start_time:.2f}秒")
                        return True
                    else:
                        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 生成的音频文件无效: {output_file}")
                        if attempt == max_retries - 1:
                            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 音频生成最终失败: {output_file}，耗时: {time.time() - start_time:.2f}秒")
                            return False
                except aiohttp.client_exceptions.WSServerHandshakeError as e:
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 生成音频失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                    if attempt == max_retries - 1:
                        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 音频生成最终失败: {output_file}，耗时: {time.time() - start_time:.2f}秒")
                        return False
                    await asyncio.sleep(retry_delay)
                except edge_tts.exceptions.NoAudioReceived as e:
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 生成音频失败: {output_file} (NoAudioReceived: {str(e)})")
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 跳过文本: {text}")
                    return False  # 跳过生成，不重试
                except Exception as e:
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 生成音频失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                    if attempt == max_retries - 1:
                        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 音频生成最终失败: {output_file}，耗时: {time.time() - start_time:.2f}秒")
                        return False
                    await asyncio.sleep(retry_delay)

    async def create_anki_card(self, morpheme: str, english_explanation: str, deck: genanki.Deck, semaphore) -> Optional[bool]:
        """创建Anki卡片并生成相关音频，限制并发请求"""
        start_time = time.time()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始处理词素: {morpheme}")

        try:
            # 如果 english_explanation 为空，尝试从 CSV 查询
            if not english_explanation:
                if self.csv_df is not None:
                    results = query_morpheme(df=self.csv_df, query=morpheme)
                    if results:
                        english_explanation = results[0]  # 取第一个匹配的解释
                        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 从 CSV 查询到 {morpheme} 的解释: {english_explanation}")
                    else:
                        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 未在 CSV 中找到 {morpheme} 的解释")
                        return False
                else:
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 无 CSV 文件，无法查询 {morpheme} 的解释")
                    return False

            # 调用 DeepSeek API 获取中文翻译、例词和例句
            content = self.get_morpheme_info_from_deepseek(morpheme, english_explanation)
            if not content:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 获取 {morpheme} 内容失败，耗时: {time.time() - start_time:.2f}秒")
                return False

            # 清理词素中的斜杠，生成安全的目录名
            safe_morpheme = morpheme.replace('/', '_')
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 使用安全目录名: {safe_morpheme}")

            # 创建词素目录
            morpheme_dir = self.output_dir / safe_morpheme
            morpheme_dir.mkdir(exist_ok=True)

            # 生成音频文件名
            audio_files = {
                "english_explanation": os.path.join(morpheme_dir, self.generate_random_filename("eng_exp")),
                "example_words": os.path.join(morpheme_dir, self.generate_random_filename("words")),
                "example_sentence": os.path.join(morpheme_dir, self.generate_random_filename("sent"))
            }

            # 准备音频生成任务
            audio_tasks = [
                (english_explanation, audio_files["english_explanation"]),
                (content["example_words"], audio_files["example_words"]),
                (content["example_sentence"], audio_files["example_sentence"])
            ]

            # 并发生成音频
            audio_results = await asyncio.gather(
                *[self.generate_tts(text, Path(file), semaphore) for text, file in audio_tasks]
            )

            if not all(audio_results):
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 部分音频生成失败: {morpheme}，耗时: {time.time() - start_time:.2f}秒")
                return False

            # 创建 Anki 卡片
            note = genanki.Note(
                model=self.model,
                fields=[
                    morpheme,  # 使用原始词素（包含 /）
                    english_explanation,
                    content["chinese_translation"],
                    content["example_words"],
                    content["example_sentence"],
                    f"[sound:{os.path.basename(audio_files['english_explanation'])}]",
                    f"[sound:{os.path.basename(audio_files['example_words'])}]",
                    f"[sound:{os.path.basename(audio_files['example_sentence'])}]"
                ]
            )
            deck.add_note(note)

            # 添加音频文件到媒体列表
            self.media_files.extend(list(audio_files.values()))

            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 成功创建卡片: {morpheme}，耗时: {time.time() - start_time:.2f}秒")
            return True

        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 创建卡片失败: {morpheme}, 错误: {str(e)}，耗时: {time.time() - start_time:.2f}秒")
            return False

    def save_deck(self, deck: genanki.Deck, chapter: int, filename: str = None) -> None:
        """保存Anki deck到文件，支持自定义文件名"""
        start_time = time.time()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始保存第 {chapter} 章deck")
        
        try:
            # 如果未提供filename，则使用默认格式
            default_filename = f"Medical_Terminology_ch{chapter}.apkg"
            output_filename = self.output_dir / (filename if filename else default_filename)
            package = genanki.Package(deck)
            package.media_files = self.media_files
            package.write_to_file(output_filename)
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Anki deck已保存: {output_filename}，耗时: {time.time() - start_time:.2f}秒")
        except Exception as e:
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 保存Anki deck失败 (章节 {chapter}): {str(e)}，耗时: {time.time() - start_time:.2f}秒")
            raise

    def create_deck_for_chapter(self, chapter: int, deck_name: str = None) -> genanki.Deck:
        """为指定章节创建新的deck，支持自定义牌组名称"""
        start_time = time.time()
        deck_id = random.randrange(1 << 30, 1 << 31)
        default_deck_name = f"Medical Terminology - Chapter {chapter}"
        deck = genanki.Deck(deck_id, deck_name if deck_name else default_deck_name)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 创建第 {chapter} 章deck，名称: {deck.name}，耗时: {time.time() - start_time:.2f}秒")
        return deck

    def log_total_time(self):
        """记录总运行时间"""
        total_time = time.time() - self.start_time
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 总运行时间: {total_time:.2f}秒")

CHAPTER_MORPHEMES_TEST = {
    1: {
    "my/o": "",
    "leiomy/o": ""
    },
    2: {
        'append/o': '',
        'sigmoid/o': ''
    },
}

CHAPTER_MORPHEMES_2 = {
    1: {
        "-ation": "",
        "-cian": "",
        "-ia": "",
        "-ism": "",
        "-ist": "",
        "-ity": "",
        "-logy": "",
        "-or": "",
        "-sis": "",
        "-um": ""
    },
    2: {
        "-al": "",
        "-ar": "",
        "-ary": "",
        "-eal": "",
        "-ible": "",
        "-ic": "",
        "-less": "",
        "-ous": ""
    },
    3: {
        "-algia": "",
        "-dynia": "",
        "-cele": "",
        "-itis": "",
        "-megaly": "",
        "-osis": "",
        "-pathy": "",
        "-gram": "",
        "-graph": "",
        "-graphy": ""
    },
    4: {
        "ped/o": "",
        "iatr/o": "",
        "neur/o": "",
        "megal/o": "",
        "cardi/o": "",
        "embol/o": "",
        "dent/i": "",
        "pharmac/o": "",
        "bi/o": "",
        "psych/o": "",
        "erect": "",
        "stern/o": "",
        "cec/o": "",
        "arteri/o": "",
        "muscul/o": "",
        "venul/o": "",
        "bil/i": "",
        "coron/o": "",
        "laryng/o": "",
        "pharyng/o": "",
        "cephal/o": "",
        "ven/o": "",
        "reticul/o": "",
        "trache/o": "",
        "bronchi/o": "",
        "arthr/o": "",
        "my/o": "",
        "encephal/o": "",
        "enter/o": "",
        "hepat/o": "",
        "splen/o": "",
        "aden/o": "",
        "angi/o": "",
        "electr/o": "",
        "radi/o": "",
        "gynec/o": "",
        "acr/o": "",
        "cholecyst/o": "",
        "steth/o": "",
        "ur/o": "",
        "omphal/o": ""
    }
}

CHAPTER_MORPHEMES_3 = {
    1: {
        'a-': '',
        'an-': '',
        'anti-': '',
        'contra-': '',
        'counter-': '',
        'de-': '',
        'dis-': '',
        'in-': '',
        'im-': '',
        'non-': '',
        'un-': ''
    },
    2: {
        'bi-': '',
        'di-': '',
        'centi-': '',
        'deca-': '',
        'deci-': '',
        'hecto-': '',
        'kilo-': '',
        'milli-': '',
        'mono-': '',
        'uni-': '',
        'hemi-': '',
        'semi-': '',
        'tri-': ''
    },
    3: {
        'ab-': '',
        'ad-': '',
        'circum-': '',
        'dia-': '',
        'epi-': '',
        'extra-': '',
        'inter-': '',
        'intra-': '',
        'per-': '',
        'peri-': '',
        'sub-': '',
        'trans-': ''
    },
    4: {
        '-tic': '',
        'ox/i': '',
        '-emia': '',
        'coagul/o': '',
        '-ception': '',
        'later/o': '',
        'hydr/o': '',
        'somn/i': '',
        'cusp': '',
        '-oxide': '',
        'watt': '',
        'ocul/o': '',
        'nucle/o': '',
        'sphere': '',
        '-plegia': '',
        'lunar': '',
        '-ceps': '',
        '-opia': '',
        '-gon': '',
        'duct': '',
        'articul/o': '',
        'or/o': '',
        'an/o': '',
        'therm/o': '',
        '-lysis': '',
        'dermis': '',
        'cost/o': '',
        'atri/o': '',
        'crani/o': '',
        'nas/o': '',
        'cutane/o': '',
        'oste/o': '',
        'odont/o': '',
        'lingu/o': '',
        'dur/o': '',
        'urethr/o': '',
        'vertebr/o': '',
        'ren/o': '',
        '-rrhea': '',
        'derm/o': ''
    }
}

CHAPTER_MORPHEMES_4 = {
    1: {
        "chir/o": "",
        "cost/o": "",
        "crani/o": "",
        "dactyl/o": "",
        "lumb/o": "",
        "myel/o": "",
        "oste/o": "",
        "ped/o": "",
        "pod/o": "",
        "rachi/o": "",
        "spondyl/o": "",
        "vertebr/o": ""
    },
    2: {
        "arthr/o": "",
        "burs/o": "",
        "chondr/o": "",
        "disk/o": "",
        "fibr/o": "",
        "ligament/o": "",
        "menisc/o": "",
        "synovi/o": "",
        "ten/o": "",
        "tendin/o": "",
        "tend/o": ""
    },
    3: {
        "-blast": "",
        "-clasia": "",
        "-clasis": "",
        "-clast": "",
        "-desis": "",
        "-listhesis": "",
        "-porosis": "",
        "-physis": "",
        "-shisis": "",
        "amphi-": "",
        "meta-": ""
    },
    4: {
        "-plasty": "",
        "pneum/o": "",
        "-meter": "",
        "cerebr/o": "",
        "abdomin/o": "",
        "-pexy": "",
        "-cyte": "",
        "-tome": "",
        "-centesis": "",
        "-lysis": "",
        "-scope": "",
        "-lith": "",
        "-tomy": "",
        "-sarcoma": "",
        "pleur/o": "",
        "anter/o": "",
        "sym-": "",
        "carp/o": "",
        "tars/o": ""
    }
}

CHAPTER_MORPHEMES_5 = {
    1: {
        "my/o": "muscle",
        "leiomy/o": "smooth muscle",
        "myocardi/o": "heart muscle",
        "cardiomy/o": "heart muscle",
        "fasci/o": "fascia",
        "sphincter/o": "sphincter",
        "sarc/o": "flesh",
        "rhabd/o": "rod-shaped",
        "myx/o": "mucus",
        "troph/o": "nourishment"
    },
    2: {
        "cephal/o": "head",
        "faci/o": "face",
        "bucc/o": "cheek",
        "gloss/o": "tongue",
        "lingu/o": "tongue",
        "cervic/o": "neck",
        "abdomin/o": "abdomen",
        "inguin/o": "groin",
        "somat/o": "body",
        "axill/o": "armpit",
        "brachi/o": "arm",
        "acr/o": "extremity",
        "-kinesia": "movement",
        "-kinesis": "movement",
        "-plasty": "surgical repair",
        "-rrhaphy": "surgical suture",
        "-meter": "instrument for measuring",
        "-metry": "process of measuring",
        "-spasm": "involuntary contraction",
        "-tonia": "tone, pressure",
        "-lysis": "breaking down",
        "-oid": "resembling",
        "-ceps": "muscular point or head"
    },
    3: {
        "dys-": "bad, difficult or abnormal",
        "eu-": "good, normal",
        "is/o": "equal, same",
        "quadri-": "four",
        "-ad": "toward",
        "femor/o": "femur",
        "poplit/o": "back of the knee",
        "caud/o": "tail",
        "cyst/o": "sac, bladder",
        "hem/o": "blood",
        "hermi/o": "hernia",
        "lip/o": "fat",
        "spher/o": "sphere, ball",
        "phag/o": "eating, swallowing",
        "-scopy": "process of viewing",
        "-plasm": "material forming cells or tissue",
        "-rrhaphy": "surgical suture"
    }
}

CHAPTER_MORPHEMES_6 = {
    1: {
        'aden/o': '',
        'cheil/o': '',
        'labi/o': '',
        'dent/i': '',
        'odont/o': '',
        'duoden/o': '',
        'enter/o': '',
        'esophag/o': '',
        'gastr/o': '',
        'ile/o': '',
        'jejun/o': '',
        'or/o': '',
        'stomat/o': ''
    },
    2: {
        'append/o': '',
        'appendic/o': '',
        'cec/o': '',
        'chol/e': '',
        'cholangi/o': '',
        'cholecyst/o': '',
        'choledoch/o': '',
        'col/o': '',
        'colon/o': '',
        'hepat/o': '',
        'pancreat/o': '',
        'proct/o': '',
        'rect/o': '',
        'sigmoid/o': ''
    },
    3: {
        'amyl/o': '',
        'glyc/o': '',
        'gluc/o': '',
        'lip/o': '',
        'phag/o': '',
        '-ase': '',
        '-ectomy': '',
        '-orexia': '',
        '-pepsia': '',
        '-pexy': '',
        '-stomy': '',
        '-tomy': ''
    },
    4: {
        '-schisis': '',
        '-cle': '',
        'orth/o': '',
        '-ptosis': '',
        '-emesis': '',
        '-stasis': '',
        '-lithiasis': '',
        '-penia': '',
        'eu-': '',
        'nephr/o': ''
    }
}

CHAPTER_MORPHEMES_7 = {
    1: {
        "angi/o": "",
        "aort/o": "",
        "arteri/o": "",
        "arteriol/o": "",
        "atri/o": "",
        "cardi/o": "",
        "pericardi/o": "",
        "phleb/o": "",
        "ven/o": "",
        "sept/o": "",
        "valvul/o": "",
        "ventricul/o": "",
        "venul/o": ""
    },
    2: {
        "cyt/o": "",
        "electr/o": "",
        "erythr/o": "",
        "granul/o": "",
        "hem/o": "",
        "hemat/o": "",
        "kary/o": "",
        "nucle/o": "",
        "leuk/o": "",
        "morph/o": "",
        "sider/o": "",
        "sphygm/o": "",
        "thromb/o": ""
    },
    3: {
        "-cytosis": "",
        "-emia": "",
        "-malacia": "",
        "-penia": "",
        "-phil": "",
        "-rrhage": "",
        "-rrhagia": "",
        "-sclerosis": "",
        "-stasis": "",
        "brady-": "",
        "tachy-": ""
    },
    4: {
        "-sclerosis": "",
        "-malacia": "",
        "-oma": "",
        "-cide": "",
        "-cyte": "",
        "-globin": "",
        "mega-": "",
        "-lytic": "",
        "-roid": "",
        "-blast": "",
        "-clast": "",
        "-lysis": "",
        "bas/o": ""
    }
}

CHAPTER_MORPHEMES_8 = {
    1: {
        "alveol/o": "",
        "bronch/o": "",
        "bronchi/o": "",
        "bronchiol/o": "",
        "epiglott/o": "",
        "laryng/o": "",
        "mediastin/o": "",
        "palat/o": "",
        "pharyng/o": "",
        "rhin/o": "",
        "trache/o": ""
    },
    2: {
        "atel/o": "",
        "coni/o": "",
        "lob/o": "",
        "orth/o": "",
        "ox/i": "",
        "phren/o": "",
        "pneumon/o": "",
        "pneum/o": "",
        "pulmon/o": "",
        "py/o": "",
        "spir/o": "",
        "thorac/o": ""
    },
    3: {
        "-capnia": "",
        "-ectasis": "",
        "-ectasia": "",
        "-form": "",
        "-oxia": "",
        "-phonia": "",
        "-pnea": "",
        "-ptysis": "",
        "-stenosis": "",
        "-thorax": "",
        "brachy-": ""
    },
    4: {
        "-edema": "",
        "cruc/i": "",
        "dendr/i": "",
        "melan/o": "",
        "hydr/o": ""
    }
}

CHAPTER_MORPHEMES_9 = {
    1: {
        "astr/o": "",
        "cortic/o": "",
        "gangli/o": "",
        "ganglion/o": "",
        "gli/o": "",
        "medull/o": "",
        "mnes/o": "",
        "myel/o": "",
        "neur/o": "",
        "psych/o": "",
        "radicul/o": "",
        "schiz/o": ""
    },
    2: {
        "cerebell/o": "",
        "cerebr/o": "",
        "dur/o": "",
        "encephala/o": "",
        "lept/o": "",
        "mening/o": "",
        "poli/o": "",
        "pont/o": "",
        "thalam/o": ""
    },
    3: {
        "-asthenia": "",
        "-esthesia": "",
        "-in": "",
        "-lemma": "",
        "-lexia": "",
        "-mania": "",
        "-paresis": "",
        "-phasia": "",
        "-phobia": "",
        "-phrenia": "",
        "-plegia": "",
        "-taxia": ""
    },
    4: {
        "-tropic": "",
        "-plegic": "",
        "-plasia": "",
        "gyr/o": "",
        "prosop/o": "",
        "arachn/o": "",
        "pyr/o": "",
        "gynec/o": "",
        "hebe-": "",
        "cry/o": "",
        "klept/o": "",
        "para-": ""
    }
}


async def main():

    # 获取当前脚本的绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # 定义数据目录名和CSV文件名
    DATA_DIRECTORY_NAME = 'data'
    CSV_FILE_NAME = 'Medical_Word_Elements_Cleaned.csv'

    # 构建完整路径：在脚本目录内拼接 'data' 文件夹
    data_directory_path = os.path.join(script_dir, DATA_DIRECTORY_NAME)
    csv_file_path = os.path.join(data_directory_path, CSV_FILE_NAME)

    generator = AnkiCardGenerator(csv_path=csv_file_path)
    semaphore = asyncio.Semaphore(1)
    
    CHAPTER_MORPHEMES = CHAPTER_MORPHEMES_9  # 可切换到其他 CHAPTER_MORPHEMES
    
    total_start_time = time.time()
    
    for chapter, morpheme_dict in CHAPTER_MORPHEMES.items():
        chapter_start_time = time.time()
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 开始处理第 {chapter} 章，词素数量: {len(morpheme_dict)}")
        
        custom_deck_name = f"My Medical Terminology - Group{chapter}"
        deck = generator.create_deck_for_chapter(chapter, deck_name=custom_deck_name)
        
        success_count = 0
        for morpheme, english_explanation in morpheme_dict.items():
            result = await generator.create_anki_card(morpheme, english_explanation, deck, semaphore)
            if result:
                success_count += 1
        
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 第 {chapter} 章处理完成: 成功 {success_count}/{len(morpheme_dict)} 个卡片，耗时: {time.time() - chapter_start_time:.2f}秒")
        
        custom_filename = f"my_medical_group_{chapter}.apkg"
        generator.save_deck(deck, chapter, filename=custom_filename)
    
    generator.log_total_time()

if __name__ == "__main__":
    asyncio.run(main())