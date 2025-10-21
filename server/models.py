from pydantic import BaseModel
from typing import Optional, List


class Question(BaseModel):
    """题目模型"""

    id: str
    question: str
    correct_answer: str
    explanation: str


class PracticeResponse(BaseModel):
    """练习模式响应"""

    success: bool
    data: Question


class QuizQuestion(BaseModel):
    """测试模式题目（不含答案）"""

    id: str
    question: str


class QuizResponse(BaseModel):
    """测试模式响应"""

    success: bool
    quiz_id: str
    questions: List[QuizQuestion]


class AnswerCheck(BaseModel):
    """答案检查结果"""

    is_correct: bool
    correct_answer: str
    explanation: str


class PracticeCheckRequest(BaseModel):
    """练习模式答案检查请求"""

    question_id: str
    user_answer: str


class QuizSubmitRequest(BaseModel):
    """挑战模式提交请求"""

    quiz_id: str
    answers: List[str]
