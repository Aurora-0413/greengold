import json
from typing import Dict, Any
import uuid
import random
import os
from models import Question

# 题库文件路径
QUESTIONS_FILE = os.path.join(os.path.dirname(__file__), "questions_data.json")


# 加载题库
def load_questions() -> list:
    """从 JSON 文件加载题库"""
    try:
        with open(QUESTIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] 加载题库失败: {str(e)}")
        return []


# 全局题库变量
QUESTIONS_BANK = load_questions()


async def generate_question() -> Question:
    """从题库中随机抽取一道题目"""
    try:
        if not QUESTIONS_BANK:
            raise Exception("题库为空,请检查 questions_data.json 文件")

        # 随机选择一道题目
        question_data = random.choice(QUESTIONS_BANK)

        return Question(
            id=str(uuid.uuid4()),
            question=question_data["question"],
            correct_answer=question_data["correct_answer"],
            explanation=question_data["explanation"],
        )
    except Exception as e:
        raise Exception(f"生成题目失败: {str(e)}")
