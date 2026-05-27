from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job
from .forms import JobForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Job

@login_required
def job_list(request):
    jobs = Job.objects.filter(user=request.user).order_by("-id")

    # 🔍 GET filters
    query = request.GET.get("q")
    status = request.GET.get("status")

    # 🔎 Search filter (company or position)
    if query:
        jobs = jobs.filter(
            company__icontains=query
        ) | jobs.filter(
            position__icontains=query
        )

    # 🎯 Status filter
    if status and status != "all":
        jobs = jobs.filter(status=status)

    context = {
        "jobs": jobs,
        "query": query or "",
        "status": status or "all",
    }

    return render(request, "jobs/job_list.html", context)

@login_required
def job_create(request):
    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            return redirect("job_list")
    else:
        form = JobForm()

    return render(request, "jobs/job_form.html", {"form": form})

@login_required
def job_update(request, pk):
    job = get_object_or_404(Job, pk=pk, user=request.user)

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect("job_list")
    else:
        form = JobForm(instance=job)

    return render(request, "jobs/job_form.html", {"form": form})

@login_required
def job_delete(request, pk):
    job = get_object_or_404(Job, pk=pk, user=request.user)

    if request.method == "POST":
        job.delete()
        return redirect("job_list")

    return render(request, "jobs/job_confirm_delete.html", {"job": job})