from django.db import models
from django.contrib.auth.models import User


class AdminAuditLog(models.Model):
    admin = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="admin_actions",
    )
    admin_username = models.CharField(max_length=150, db_index=True)
    action = models.CharField(max_length=255, db_index=True)
    target_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="target_of_admin_actions",
    )
    target_username = models.CharField(
        max_length=150, blank=True, default="", db_index=True
    )
    target_email = models.EmailField(blank=True, default="")
    details = models.JSONField(default=dict, blank=True)
    actor_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, blank=True, default="")
    request_id = models.CharField(max_length=64, blank=True, default="", db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        admin_name = self.admin_username or (
            self.admin.username if self.admin else "unknown"
        )
        return f"{admin_name} - {self.action} - {self.timestamp}"
