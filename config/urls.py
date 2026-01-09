from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # ✅ loginだけ上書き（ログイン済みなら自動でリダイレクト）
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name="login",
    ),

    # 残りのauth（logoutなど）
    path("accounts/", include("django.contrib.auth.urls")),

    # tracker
    path("", include("tracker.urls")),
]
