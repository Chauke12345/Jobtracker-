from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Job
from .forms import JobForm


# =====================================
# JOB LIST VIEW (with search + filters)
# =====================================
@login_required
def job_list(request):
    # Get only jobs belonging to logged-in user
    jobs = Job.objects.filter(user=request.user).order_by("-id")

    # -----------------------------
    # GET parameters (filters)
    # -----------------------------
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "all")

    # -----------------------------
    # Search filter (company/position)
    # -----------------------------
    if query:
        jobs = jobs.filter(company__icontains=query) | jobs.filter(position__icontains=query)

    # -----------------------------
    # Status filter
    # -----------------------------
    if status and status != "all":
        jobs = jobs.filter(status=status)

    # Context passed to template
    context = {
        "jobs": jobs,
        "query": query,
        "status": status,
    }

    return render(request, "jobs/job_list.html", context)


# =====================================
# CREATE NEW JOB
# =====================================
@login_required
def job_create(request):
    # Handle form submission
    if request.method == "POST":
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)  # don't save yet
            job.user = request.user       # attach logged-in user
            job.save()                    # save to database
            return redirect("job_list")

    # Display empty form
    else:
        form = JobForm()

    return render(request, "jobs/job_form.html", {"form": form})


# =====================================
# UPDATE EXISTING JOB
# =====================================
@login_required
def job_update(request, pk):
    # Get job OR return 404 if not found / not owned by user
    job = get_object_or_404(Job, pk=pk, user=request.user)

    # Handle form submission
    if request.method == "POST":
        form = JobForm(request.POST, instance=job)

        if form.is_valid():
            form.save()
            return redirect("job_list")

    # Load form with existing job data
    else:
        form = JobForm(instance=job)

    return render(request, "jobs/job_form.html", {"form": form})


# =====================================
# DELETE JOB
# =====================================
@login_required
def job_delete(request, pk):
    # Ensure user owns the job before deleting
    job = get_object_or_404(Job, pk=pk, user=request.user)

    # Confirm deletion on POST
    if request.method == "POST":
        job.delete()
        return redirect("job_list")

    return render(request, "jobs/job_confirm_delete.html", {"job": job})