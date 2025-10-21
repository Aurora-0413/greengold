from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import (
    Question,
    QuizResponse,
    PracticeResponse,
    PracticeCheckRequest,
    QuizSubmitRequest,
)
from ai_service import generate_question
import random

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 默认端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 题目库（实际项目中应该存储在数据库中）
questions_pool = []
# 题目缓存（用于练习模式的答案检查）
questions_cache = {}


@app.get("/api/practice/question")
async def get_practice_question():
    """获取一道练习题"""
    try:
        question = await generate_question()
        # 缓存题目信息用于后续答案检查
        questions_cache[question.id] = question
        print(f"[DEBUG] Generated and cached question: {question.id}")
        print(f"[DEBUG] Total cached questions: {len(questions_cache)}")
        return PracticeResponse(success=True, data=question)
    except Exception as e:
        print(f"[ERROR] Failed to generate question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/practice/check")
async def check_practice_answer(request: PracticeCheckRequest):
    """检查练习模式答案"""
    try:
        # 从缓存中获取题目
        question = questions_cache.get(request.question_id)
        if not question:
            raise HTTPException(
                status_code=404, detail=f"Question not found: {request.question_id}"
            )

        # 直接比较答案，不再调用 AI
        is_correct = question.correct_answer.upper() == request.user_answer.upper()

        return {
            "success": True,
            "data": {
                "is_correct": is_correct,
                "correct_answer": question.correct_answer,
                "explanation": question.explanation,
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/quiz/start")
async def start_quiz():
    """开始一次挑战模式答题（10题）"""
    try:
        # 生成10道新题
        quiz_questions = []
        for _ in range(10):
            question = await generate_question()
            quiz_questions.append(question)

        # 生成quiz_id并保存题目
        quiz_id = f"quiz_{random.randint(1000, 9999)}"
        questions_pool.append(
            {"quiz_id": quiz_id, "questions": quiz_questions, "submitted": False}
        )

        # 返回问题（不含答案）
        return {
            "success": True,
            "data": {
                "quiz_id": quiz_id,
                "questions": [
                    q.dict(exclude={"correct_answer", "explanation"})
                    for q in quiz_questions
                ],
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/quiz/submit")
async def submit_quiz(request: QuizSubmitRequest):
    """提交挑战模式答案"""
    try:
        # 查找对应的quiz
        quiz = next(
            (q for q in questions_pool if q["quiz_id"] == request.quiz_id), None
        )
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        if quiz["submitted"]:
            raise HTTPException(status_code=400, detail="Quiz already submitted")

        # 计算得分和解析
        total_questions = len(quiz["questions"])
        correct_count = 0
        results = []

        for i, (question, user_answer) in enumerate(
            zip(quiz["questions"], request.answers)
        ):
            is_correct = question.correct_answer.lower() == user_answer.lower()
            if is_correct:
                correct_count += 1

            results.append(
                {
                    "question_number": i + 1,
                    "question": question.question,
                    "user_answer": user_answer,
                    "correct_answer": question.correct_answer,
                    "is_correct": is_correct,
                    "explanation": question.explanation,
                }
            )

        # 标记为已提交
        quiz["submitted"] = True

        score = (correct_count / total_questions) * 100

        return {
            "success": True,
            "data": {
                "quiz_id": request.quiz_id,
                "score": score,
                "correct_count": correct_count,
                "total_questions": total_questions,
                "results": results,
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
