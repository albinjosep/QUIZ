from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Question, UserSubmission
import random

@csrf_exempt
def start_session(request):
    UserSubmission.objects.all().delete()
    return JsonResponse({"message": "New session started."})


def get_random_question(request):
    questions = Question.objects.all()
    if not questions:
        return JsonResponse({"error": "No questions available."}, status=404)
    question = random.choice(questions)
    return JsonResponse({
        "id": question.id,
        "text": question.text,
        "options": {
            "a": question.option_a,
            "b": question.option_b,
            "c": question.option_c,
            "d": question.option_d,
        }
    })


@csrf_exempt
def submit_answer(request):
    if request.method == "POST":
        question_id = request.POST.get("question_id")
        selected_option = request.POST.get("selected_option")
        try:
            question = Question.objects.get(id=question_id)
            is_correct = question.correct_option == selected_option
            UserSubmission.objects.create(
                question=question,
                selected_option=selected_option,
                is_correct=is_correct
            )
            return JsonResponse({"is_correct": is_correct})
        except Question.DoesNotExist:
            return JsonResponse({"error": "Question not found."}, status=404)


def results(request):
    submissions = UserSubmission.objects.all()
    total = submissions.count()
    correct = submissions.filter(is_correct=True).count()
    incorrect = total - correct
    return JsonResponse({
        "total": total,
        "correct": correct,
        "incorrect": incorrect,
        "details": [
            {
                "question": sub.question.text,
                "selected_option": sub.selected_option,
                "is_correct": sub.is_correct
            }
            for sub in submissions
        ]
    })

