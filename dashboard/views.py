from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q
from jobs.models import Job

@login_required
def home(request):
    jobs = Job.objects.filter(user=request.user).order_by("-id")

    query = request.GET.get("q", "")
    status = request.GET.get("status", "all")

    if query:
        jobs = jobs.filter(
            Q(company__icontains=query) |
            Q(position__icontains=query)
        )

    if status != "all":
        jobs = jobs.filter(status=status)

    context = {
        "jobs": jobs[:5],
        "query": query,
        "total_jobs": jobs.count(),
        "applied_count": jobs.filter(status="applied").count(),
        "interview_count": jobs.filter(status="interview").count(),
        "offer_count": jobs.filter(status="offer").count(),
    }

    return render(request, "home.html", context)