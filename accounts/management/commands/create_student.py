from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = "Create student user"

    def handle(self, *args, **kwargs):

        username = input("Username: ")
        password = input("Password: ")

        user = User.objects.create_user(
            username=username,
            password=password,
            role="student"
        )

        self.stdout.write(self.style.SUCCESS(
            f"Student created: {user.username}"
        ))