from flask import Flask, render_template, request, jsonify
import openai
from openai import OpenAI
import os
import json

story_chapter = -1
story_choice = ""
feedback1 = None
feedback2 = None

# 确保你的 OPENAI_API_KEY 环境变量已经设置好
os.environ["OPENAI_API_KEY"] = "sess-3s5HNqOgrQcYnjUiYZjutwBgYwuMLdagEfBYI8Su"
OpenAI.api_key = "sess-3s5HNqOgrQcYnjUiYZjutwBgYwuMLdagEfBYI8Su"
client = OpenAI()
# OpenAI.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message", "").lower()
    response_message = chat(user_message)
    return jsonify({"response":response_message})

    

# 定义故事的基础素材
story_bases = {
    "小女孩": "小女孩的故事基础素材……",
    "面包": "面包的故事基础素材……",
    "小乌龟": "小乌龟觉得自己的壳很麻烦，所以把壳丢进了河里，小熊发现龟壳可以吹笛，小鸟发现龟壳可以作为自己的巢。 \
        他们都感谢小乌龟，小乌龟觉得很开心，我希望通过这个故事，教育孩子“不要歧视别人”、“珍惜自己的特点”。\
        在故事中，设计互动点1：“小熊可以用壳做什么”，互动点2：“小鸟可以用壳做什么."
}

turtle_story_templates = [
    "我需要给3-8岁的孩子讲故事。请扩充并讲述这个故事\"{story_base}\"，每一次扩充在250字以内，并且不论互动点1和2如何反馈，\
    都能够传达教育信息。在互动点中，尽量将孩子的任何回答嵌入故事的发展，假如该回答完全无法嵌入故事，或者与问题毫无关系，请再重复一次互动点\
    处生成的问题。假如孩子对讲故事这一活动本身有强烈的抗拒，请用耐心的语气劝导，并重复互动点生成的问题。\n\
    在互动点1和互动点2，你需要停下，等待我的反馈。你的回复应当以json格式返回，并且格式如下：\n\
    1.故事续写的剧情文本对应标签名称为story\n\
    2.互动点提出的问题文本对应标签为interact\n\
    3.不要出现括号包含的暗示提示性文本\n\
    4.动物、人物不要出现出现名字，直接使用名词",
    "孩子给出的反馈是“{feedback1}”，请给出反馈，\
    生成反馈时需要注意以下几点：\n\
    1、及时给孩子肯定和赞美\n\
    2、帮助孩子补充此回答的细节\n\
    生成反馈后，继续讲述直到互动点2停下，等待孩子的反馈。\n\
    你的回复应当以json格式返回，并且格式如下：\n\
    1.故事续写的剧情文本对应标签名称为story\n\
    2.互动点提出的问题文本对应标签为interact\n\
    3.不要出现括号包含的暗示提示性文本\n\
    4.动物、人物不要出现出现名字，直接使用名词",
    "孩子给出的反馈是“{feedback2}”，请给出反馈，\
    生成反馈时需要注意以下几点：\n\
    1、及时给孩子肯定和赞美\n\
    2、帮助孩子补充此回答的细节\n\
    生成反馈后，直接讲述到结局\n\
    在结局后，生成问题，“这个故事讲完了，让我们想想可以从故事里明白什么吧，「此处填入生成问题1」”\n\
    你的回复应当以json格式返回，并且格式如下：\n\
    1.故事续写的剧情文本对应标签名称为story\n\
    2.互动点提出的问题文本对应标签为interact\n\
    3.不要出现括号包含的暗示提示性文本\n\
    4.动物、人物不要出现出现名字，直接使用名词"
]

# 定义对话模板
dialogue_templates = {
    "小乌龟":turtle_story_templates,
    # "小女孩":girl_story_templates,
    # "面包":bread_story_templates
}

# 询问孩子想听的故事
def ask_for_story():
    return "你想听什么故事，关于小女孩，关于面包，还是关于小乌龟？"

# 填充故事模板并进入互动点
def fill_story_template(story_choice, feedback1=None, feedback2=None):
    if story_choice not in story_bases:
        return "以json格式返回响应”对不起，我不知道这个故事。“，标签为story"
    story_base = story_bases[story_choice]
    
    if story_chapter == 0:
        # 第一轮对话
        return dialogue_templates[story_choice][story_chapter].format(story_base=story_base)
    elif story_chapter == 1:
        # 第二轮对话
        return dialogue_templates[story_choice][story_chapter].format(feedback1=feedback1)
    elif story_chapter == 2:
        # 第三轮对话
        return dialogue_templates[story_choice][story_chapter].format(feedback2=feedback2)

# 对话管理
def chat(user_message):
    global story_chapter
    global story_choice
    global feedback1
    global feedback2

    if story_chapter == -1:
        story_chapter = story_chapter + 1
        return ask_for_story()
    elif story_chapter == 0:
        if any(keyword in user_message for keyword in ["小女孩", "面包", "小乌龟"]):
            story_choice = [keyword for keyword in ["小女孩", "面包", "小乌龟"] if keyword in user_message][0]
        user_prompt = fill_story_template(story_choice, feedback1, feedback2)
    elif story_chapter == 1:
        feedback1 = user_message
        user_prompt = fill_story_template(story_choice, feedback1, feedback2)
    elif story_chapter == 2:
        feedback2 = user_message
        user_prompt = fill_story_template(story_choice, feedback1, feedback2)
    else:
        pass
    
    res_json = send_to_gpt(user_prompt)
    response_text = ""
    if story_chapter == 0:
        response_text = res_json["story"] + res_json["interact"]
    elif story_chapter == 1:
        response_text = res_json["story"] + res_json["interact"]
    elif story_chapter == 2:
        response_text = res_json["story"] + res_json["interact"]
    
    story_chapter = story_chapter + 1
    return response_text  

def send_to_gpt(user_prompt):
    print("user prompt: ", user_prompt)
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role":"user",
                "content":user_prompt,
            }
        ],
        model="gpt-3.5-turbo",
    )
    print("gpt response: ", chat_completion.choices[0].message.content)
    return json.loads(chat_completion.choices[0].message.content)

if __name__ == "__main__":
    app.run(debug=True)