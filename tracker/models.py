from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = "TODO", "未着手"
        DOING = "DOING", "作業中"
        DONE = "DONE", "完了"

    title = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")

    role = models.CharField(max_length=50, blank=True)  # UI/DB/API など任意
    due_date = models.DateField(null=True, blank=True)

    points = models.PositiveSmallIntegerField(default=1)  # 重み(1〜5とか)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.TODO)
    progress = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

    memo_today = models.CharField(max_length=200, blank=True)
    memo_next = models.CharField(max_length=200, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # ✅ progressからstatusを自動決定（status入力欄は不要になる）
        if self.progress == 0:
            self.status = self.Status.TODO
        elif self.progress == 100:
            self.status = self.Status.DONE
        else:
            self.status = self.Status.DOING

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.owner.username})"
