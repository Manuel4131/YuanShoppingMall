from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
# Create your models here.


class VerificationCode(models.Model):
	user_fk = models.OneToOneField(User, related_name="auth_code")
	auth_code = models.CharField(max_length=32)
	# If the timezone issue is not considered, then I guess it's OK.
	expiry_date = models.DateTimeField(default=datetime.now()+timedelta(days=3))