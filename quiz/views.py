from django.shortcuts import redirect, render

from .models import Question


def _questions():
    return list(Question.objects.prefetch_related("choices"))


def home(request):
    request.session.pop("answers", None)  # cada visita à home reinicia o quiz
    return render(request, "quiz/home.html", {"total": Question.objects.count()})


def question(request, n):
    questions = _questions()
    total = len(questions)
    answers = request.session.setdefault("answers", {})
    first_open = next((i for i, q in enumerate(questions, 1) if str(q.pk) not in answers), total + 1)

    if not 1 <= n <= total:
        return redirect("home")
    if n > first_open:  # não deixa pular perguntas
        return redirect("result" if first_open > total else "question", **({} if first_open > total else {"n": first_open}))

    q = questions[n - 1]
    if request.method == "POST" and str(q.pk) not in answers:
        choice = next((c for c in q.choices.all() if str(c.pk) == request.POST.get("choice")), None)
        if choice:
            answers[str(q.pk)] = choice.pk
            request.session.modified = True

    chosen_id = answers.get(str(q.pk))
    return render(request, "quiz/question.html", {
        "q": q, "n": n, "total": total,
        "percent": round((n - 1 + bool(chosen_id)) / total * 100),
        "chosen_id": chosen_id,
        "is_last": n == total,
        "next_n": n + 1,
        "missing": request.method == "POST" and not chosen_id,
    })


def result(request):
    questions = _questions()
    answers = request.session.get("answers", {})
    if not questions:
        return redirect("home")
    for i, q in enumerate(questions, 1):
        if str(q.pk) not in answers:
            return redirect("question", n=i)

    review, score = [], 0
    for q in questions:
        ok = any(c.is_correct for c in q.choices.all() if c.pk == answers[str(q.pk)])
        score += ok
        review.append({"q": q, "ok": ok})

    total = len(questions)
    if score == total:
        headline = "Você reconhece e sabe agir."
    elif score >= total * 0.6:
        headline = "Você está no caminho certo."
    else:
        headline = "Ainda dá tempo de aprender a agir."
    return render(request, "quiz/result.html", {"score": score, "total": total, "headline": headline, "review": review})
