from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('analyst', 'Analyst'),
        ('viewer', 'Viewer'),
    ]

    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # ✅ store hashed password
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_password(self, raw_password):
        """Hash and store password"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Verify password"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email
    

class recordsModel(models.Model):
    typeChoice=[
        ("income","Income"),
        ("expense","Expense")
    ]
    amount= models.IntegerField(verbose_name="amount")
    type= models.CharField(default="expense", choices=typeChoice)
    category= models.CharField(verbose_name="category", max_length=15)
    date=models.DateTimeField(auto_now_add=True)
    note= models.CharField(verbose_name="note", max_length=50)
    createdBy= models.ForeignKey(User,on_delete=models.CASCADE)