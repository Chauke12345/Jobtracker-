from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from jobs.models import Job

@login_required
def home(request):
    jobs = Job.objects.filter(user=request.user).order_by("-id")

    context = {
        "jobs": jobs[:5],  # recent 5
        "total_jobs": jobs.count(),
        "applied_count": jobs.filter(status="applied").count(),
        "interview_count": jobs.filter(status="interview").count(),
        "offer_count": jobs.filter(status="offer").count(),
    }

    return render(request, "home.html", context)