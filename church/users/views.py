from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, RedirectView, UpdateView
from twilio.rest import Client

from church.users.models import Group, Member, Sermon

from .forms import AddMemberForm, GroupForm, MemberForm, SMSForm

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert self.request.user.is_authenticated  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


def members_view(request):
    # Get the search query from the URL parameters
    search_query = request.GET.get("search_query")

    if search_query:
        # If there's a search query, filter members based on first_name or last_name containing the search query
        members = Member.objects.filter(Q(first_name__icontains=search_query) | Q(last_name__icontains=search_query))
    else:
        # If no search query, fetch all members
        members = Member.objects.all()

    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("users:members")
    else:
        form = MemberForm()

    return render(request, "church/users/members.html", {"members": members, "form": form})


def send_sms(request):
    if request.method == "POST":
        form = SMSForm(request.POST)
        if form.is_valid():
            account_sid = settings.TWILIO_ACCOUNT_SID
            auth_token = settings.TWILIO_AUTH_TOKEN
            client = Client(account_sid, auth_token)

            message = client.messages.create(
                from_="+14177944633", to="+254790368234", body=form.cleaned_data["message"]
            )

            return render(request, "sms_sent.html", {"message_sid": message.sid})
    else:
        form = SMSForm()

    return render(request, "send_sms.html", {"form": form})


def sermon_list(request):
    sermons = Sermon.objects.all()

    # Get search parameters from query string
    title = request.GET.get("title")
    date = request.GET.get("date")
    speaker = request.GET.get("speaker")

    # Filter sermons based on search parameters
    if title:
        sermons = sermons.filter(title__icontains=title)
    if date:
        sermons = sermons.filter(date=date)
    if speaker:
        sermons = sermons.filter(speaker__icontains=speaker)

    return render(request, "sermon_list.html", {"sermons": sermons})



def create_group(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            return redirect("users:create_group")
    else:
        form = GroupForm()

    groups = Group.objects.all()  # Fetch all group objects from the database

    return render(request, "create_group.html", {"form": form, "groups": groups})


def add_member_to_group(request):
    if request.method == "POST":
        form = AddMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            group_id = form.cleaned_data["group"]
            # group = get_object_or_404(Group, id=group_id)
            member.group_id = group_id  # Assign the group ID
            member.save()
            return redirect("users:create_group")
    else:
        form = AddMemberForm()

    return render(request, "add_member_to_group.html", {"form": form})


def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    members = group.members.all()

    print(f"Group ID: {group.id}")  # Add this print statement

    context = {
        "group": group,
        "members": members,
    }
    return render(request, "group_detail.html", context)


def member_detail(request, member_id):
    # Fetch the member details from the database based on the member_id
    member = get_object_or_404(Member, id=member_id)

    context = {
        "member": member,
    }
    return render(request, "member_detail.html", context)
