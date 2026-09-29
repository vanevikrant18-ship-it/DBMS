from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Student, Company, Interview


# =========================
# LOGIN
# =========================
def login_view(request):
    if request.user.is_authenticated:
        return role_redirect(request.user)

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return role_redirect(user)
        else:
            return render(request, "main/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "main/login.html")


def role_redirect(user):
    if user.is_superuser:
        return redirect("/admin-dashboard/")
    elif hasattr(user, "student"):
        return redirect("/student/")
    elif hasattr(user, "company"):
        return redirect("/company/")
    else:
        return redirect("/admin-dashboard/")


# =========================
# REGISTER
# =========================
def register(request):
    if request.method == "POST":
        role = request.POST.get("role")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check karo username already exists to nahi
        if User.objects.filter(username=username).exists():
            return render(request, "main/register.html", {
                "error": "Username already taken. Please choose another."
            })

        user = User.objects.create_user(username=username, password=password)

        if role == "student":
            Student.objects.create(
                user=user,
                name=request.POST.get("name", ""),
                age=request.POST.get("age", 0),
                qualification=request.POST.get("qualification", ""),
                skills=request.POST.get("skills", "")
            )

        elif role == "company":
            Company.objects.create(
                user=user,
                company_name=request.POST.get("company_name", ""),
                required_skills=request.POST.get("required_skills", ""),
                qualification_required=request.POST.get("qualification_required", "")
            )

        elif role == "admin":
            user.is_staff = True
            user.is_superuser = True
            user.save()

        return redirect("/")

    return render(request, "main/register.html")


# =========================
# STUDENT DASHBOARD
# =========================
@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        return redirect("/")

    # Profile update form
    if request.method == "POST":
        student.name = request.POST.get("name", student.name)
        student.age = request.POST.get("age", student.age)
        student.qualification = request.POST.get("qualification", student.qualification)
        student.skills = request.POST.get("skills", student.skills)
        student.save()
        return redirect("/student/")

    interviews = Interview.objects.filter(student=student)

    return render(request, "main/student_dashboard.html", {
        "student": student,
        "interviews": interviews
    })


# =========================
# COMPANY DASHBOARD
# =========================
@login_required
def company_dashboard(request):
    try:
        company = Company.objects.get(user=request.user)
    except Company.DoesNotExist:
        return redirect("/")

    # Company profile update
    if request.method == "POST":
        company.company_name = request.POST.get("company_name", company.company_name)
        company.required_skills = request.POST.get("required_skills", company.required_skills)
        company.qualification_required = request.POST.get("qualification_required", company.qualification_required)
        company.save()
        return redirect("/company/")

    # Is company ke liye scheduled interviews
    interviews = Interview.objects.filter(company_name=company.company_name)

    return render(request, "main/company_dashboard.html", {
        "company": company,
        "interviews": interviews
    })


# =========================
# ADMIN DASHBOARD
# =========================
@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect("/")

    students = Student.objects.all()
    companies = Company.objects.all()
    interviews = Interview.objects.all()
    success = ""

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        company_name = request.POST.get("company_name")
        date = request.POST.get("date")

        if student_id and company_name and date:
            Interview.objects.create(
                student_id=student_id,
                company_name=company_name,
                interview_date=date
            )
            success = "Interview successfully scheduled!"

    return render(request, "main/admin_dashboard.html", {
        "students": students,
        "companies": companies,
        "interviews": interviews,
        "success": success
    })


# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    return redirect("/")