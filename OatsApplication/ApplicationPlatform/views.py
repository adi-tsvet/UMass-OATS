import datetime
import sys

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import SessionForm, IssuesForm
from .models import Session
#from OatsApplication.users.models import Teacher

# Create your views here.

def generate_daylist():
    daylist = []
    today = datetime.date.today()
    for i in range(7):
        day = {}
        curr_day = today + datetime.timedelta(days=i)
        weekday = curr_day.strftime("%A").upper()
        #Teacher = Teacher.objects.filter(assigned_day=weekday).first()
        day["date"] = str(curr_day)
        day["day"] = weekday
        day["onduty"] = "asdasd" #teacher.get_name()
        day["dept"] = "erer"#teacher.dept
        day["A_booked"] = (
            Session.objects.filter(date=str(curr_day)).filter(timeblock="A").exists()
        )
        day["B_booked"] = (
            Session.objects.filter(date=str(curr_day)).filter(timeblock="B").exists()
        )
        day["C_booked"] = (
            Session.objects.filter(date=str(curr_day)).filter(timeblock="C").exists()
        )
        day["D_booked"] = (
            Session.objects.filter(date=str(curr_day)).filter(timeblock="D").exists()
        )
        day["E_booked"] = (
            Session.objects.filter(date=str(curr_day)).filter(timeblock="E").exists()
        )
        day["F_booked"] = (
            Session.objects.filter(date=str(curr_day)).filter(timeblock="F").exists()
        )
        if day["day"] != "SATURDAY":  # Writing lab doesn't open on Saturday
            daylist.append(day)
    return daylist



class SessionListView(ListView):
    model = Session
    template_name = "scheduler/sessions.html"  # <app>/<model>_<view_type>.html
    context_object_name = "sessions"
    ordering = ["-date"]


# saving code by following conventions
class SessionDetailView(DetailView):
    model = Session


# note: mixins should come before CreateView
class SessionCreateView(LoginRequiredMixin, CreateView):
    # model = Session
    # fields = ["date", "timeblock", "course_name", "course_teacher", "helptype"]
    form_class = SessionForm
    template_name = "scheduler/session_form.html"

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        return {
            "date": self.kwargs.get("date"),
            "timeblock": self.kwargs.get("timeblock"),
        }

    def get_success_url(self):
        return reverse("users:detail", args=[self.request.user.username])

    # def get_form_kwargs(self, *args, **kwargs):  # forms.py def clean()
    #     kwargs = super(SessionCreateView, self).get_form_kwargs(*args, **kwargs)
    #     kwargs["user"] = self.request.user
    #     return kwargs


class SessionEditView(SuccessMessageMixin, LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Session
    fields = ["course_name", "course_teacher", "helptype"]
    # success_url = "/users/<str:username>/"
    success_message = "Session was updated successfully"

    def form_valid(self, form):
        form.instance.student = self.request.user
        return super().form_valid(form)

    def test_func(self):
        session = self.get_object()
        if self.request.user == session.student:
            return True
        return False

    def get_success_url(self):
        return reverse("users:detail", args=[self.request.user.username])


class SessionCancelView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Session

    def test_func(self):
        session = self.get_object()
        if self.request.user == session.student:
            return True
        return False

    def get_success_url(self):
        return reverse("users:detail", args=[self.request.user.username])


def home(request):
    context = {"days": generate_daylist()}
    #context = {"days": ["1", "2"]}
    return render(request, "pages/home.html", context)


def about(request):
    return render(request, "pages/about.html")


def sessions(request):
    context = {"sessions": Session.objects.all()}
    return render(request, "scheduler/sessions.html", context)


def report_issues(request):
    if request.method == "POST":
        form = IssuesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully reported issue!")
            return redirect("scheduler-home")
    else:  # displays empty form initially
        form = IssuesForm()

    return render(request, "scheduler/report_issues.html", {"form": form})
