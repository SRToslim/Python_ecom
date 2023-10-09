from django.db import models

from userauth.models import User


class GuestUser(models.Model):
    name = models.CharField(max_length=5)
    ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Chatting(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='received_messages')
    guest_sender = models.ForeignKey(GuestUser, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='sent_messages')
    text = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.sender:
            sender_name = self.sender.username
        else:
            sender_name = self.guest_sender.ip

        if self.recipient:
            recipient_name = self.recipient.username
        else:
            recipient_name = self.guest_sender.ip

        return f'From {sender_name} to {recipient_name} - {self.created_at}'

        # if self.sender:
        #     return f'From {self.sender.username} to {self.recipient.username} - {self.created_at}'
        # else:
        #     return f'From Guest to {self.recipient.username} - {self.created_at}'
