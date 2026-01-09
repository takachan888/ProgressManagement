from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import TaskUpdateForm, LeaderTaskForm, LeaderUserCreateForm, LeaderUserEditForm
from .models import Task
from .utils import weighted_progress


def home(request):
    # 未ログインならログイン画面へ
    if not request.user.is_authenticated:
        return redirect("login")
    # ログイン済みなら分岐ページへ（リーダー→/leader, メンバー→/me）
    return redirect("after_login")


@login_required
def after_login(request):
    # ログイン後に役割で振り分け
    if request.user.is_staff:
        return redirect("leader_dashboard")
    return redirect("my_tasks")


@login_required
def my_tasks(request):
    tasks = Task.objects.filter(owner=request.user).order_by("due_date", "-updated_at")
    return render(request, "tracker/my_tasks.html", {"tasks": tasks})


@login_required
def update_task(request, task_id: int):
    task = get_object_or_404(Task, id=task_id)

    # 自分のタスク以外は更新できない
    if task.owner != request.user:
        return HttpResponseForbidden("自分のタスク以外は更新できません。")

    if request.method == "POST":
        form = TaskUpdateForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("my_tasks")
    else:
        form = TaskUpdateForm(instance=task)

    return render(request, "tracker/task_update.html", {"form": form, "task": task})


def _state_from_progress(p: float) -> str:
    """
    進捗(%)から状態を返す
    - 0   => 未着手
    - 100 => 完了
    - else => 作業中
    """
    try:
        p = float(p)
    except (TypeError, ValueError):
        p = 0.0

    if p <= 0:
        return "未着手"
    if p >= 100:
        return "完了"
    return "作業中"


def _badge_class(state: str) -> str:
    """
    Bootstrap badge class
    """
    if state == "未着手":
        return "text-bg-secondary"
    if state == "完了":
        return "text-bg-success"
    return "text-bg-primary"


@login_required
def leader_dashboard(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("リーダーのみ閲覧できます。")

    users = User.objects.filter(is_active=True).order_by("username")

    members = []
    for u in users:
        utasks = Task.objects.filter(owner=u)
        last = utasks.order_by("-updated_at").first()

        # ✅ statusではなく progress で完了数を数える（旧データが残ってても表示が崩れない）
        done_count = utasks.filter(progress=100).count()

        # weighted_progress(utasks) の値をカード/グラフに使う
        prog = weighted_progress(utasks)

        # ✅ 追加：カード表示用の状態（未着手/作業中/完了）
        state = _state_from_progress(prog)

        members.append({
            "user": u,
            "progress": prog,
            "state": state,                # ✅ 追加
            "state_badge": _badge_class(state),  # ✅ 追加
            "task_count": utasks.count(),
            "done_count": done_count,      # ✅ 差し替え
            "last_updated": last.updated_at if last else None,
        })

    overall = weighted_progress(Task.objects.all())
    stale_border = timezone.now() - timedelta(days=3)

    chart_labels = [m["user"].username for m in members]
    chart_values = [m["progress"] for m in members]

    # ✅ 追加：全タスク一覧（編集/削除用）
    tasks = Task.objects.select_related("owner").order_by(
        "owner__username", "due_date", "-updated_at"
    )

    return render(request, "tracker/leader_dashboard.html", {
        "members": members,
        "overall": overall,
        "stale_border": stale_border,
        "chart_labels": chart_labels,
        "chart_values": chart_values,
        "tasks": tasks,
    })


@login_required
def leader_task_create(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("リーダーのみ操作できます。")

    if request.method == "POST":
        form = LeaderTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("leader_dashboard")
    else:
        form = LeaderTaskForm()

    return render(request, "tracker/leader_task_form.html", {"form": form, "mode": "create"})


@login_required
def leader_task_edit(request, task_id: int):
    if not request.user.is_staff:
        return HttpResponseForbidden("リーダーのみ操作できます。")

    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = LeaderTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("leader_dashboard")
    else:
        form = LeaderTaskForm(instance=task)

    return render(request, "tracker/leader_task_form.html", {"form": form, "mode": "edit", "task": task})


@login_required
def leader_task_delete(request, task_id: int):
    if not request.user.is_staff:
        return HttpResponseForbidden("リーダーのみ操作できます。")

    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.delete()
        return redirect("leader_dashboard")

    return render(request, "tracker/leader_task_delete.html", {"task": task})


@login_required
def leader_user_list(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("リーダーのみ閲覧できます。")

    users = User.objects.order_by("username")
    return render(request, "tracker/leader_user_list.html", {"users": users})


@login_required
def leader_user_create(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("リーダーのみ操作できます。")

    if request.method == "POST":
        form = LeaderUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("leader_user_list")
    else:
        form = LeaderUserCreateForm(initial={"is_active": True})

    return render(request, "tracker/leader_user_form.html", {"form": form, "mode": "create"})


@login_required
def leader_user_edit(request, user_id: int):
    if not request.user.is_staff:
        return HttpResponseForbidden("リーダーのみ操作できます。")

    target = get_object_or_404(User, id=user_id)

    # superuserは編集不可（事故防止）
    if target.is_superuser:
        return HttpResponseForbidden("このユーザーは編集できません。")

    if request.method == "POST":
        form = LeaderUserEditForm(request.POST, instance=target)
        if form.is_valid():
            form.save()
            return redirect("leader_user_list")
    else:
        form = LeaderUserEditForm(instance=target)

    return render(request, "tracker/leader_user_form.html", {"form": form, "mode": "edit", "target": target})


@login_required
def leader_user_delete(request, user_id: int):
    if not request.user.is_staff:
        return HttpResponseForbidden("リーダーのみ操作できます。")

    target = get_object_or_404(User, id=user_id)

    # 自分は削除不可
    if target.id == request.user.id:
        return HttpResponseForbidden("自分自身は削除できません。")

    # superuserは削除不可（事故防止）
    if target.is_superuser:
        return HttpResponseForbidden("このユーザーは削除できません。")

    task_count = Task.objects.filter(owner=target).count()

    if request.method == "POST":
        # ⚠ owner=CASCADEなので、削除するとタスクも消える
        target.delete()
        return redirect("leader_user_list")

    return render(request, "tracker/leader_user_delete.html", {"target": target, "task_count": task_count})
