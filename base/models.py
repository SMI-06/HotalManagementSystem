from django.db import models
from django.contrib.auth.models import AbstractUser,User



class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    ]
    room_name = models.CharField(max_length=20,null=True)
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    room_image1 = models.ImageField(upload_to="base/uploads",null=True)
    room_image2 = models.ImageField(upload_to="base/uploads",null=True)
    room_image3 = models.ImageField(upload_to="base/uploads",null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    room_description = models.TextField()
    is_booked = models.BooleanField(default=False)
    is_special = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        ordering = ['-updated','-created']


    def __str__(self):
        return f"Room {self.room_number} - {self.room_type}"

class Booking(models.Model):

    ADULTS = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    ]
    CHILDREN = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    booking_code = models.CharField(max_length=25,null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField(null=True)
    check_out_date = models.DateField(null=True)
    adults = models.CharField(max_length=10, choices=ADULTS,null=True)
    children = models.CharField(max_length=10, choices=CHILDREN,null=True)
    is_approved = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10,decimal_places=2)
    special_requests = models.TextField(default="Nothing")
    updated = models.DateTimeField(auto_now=True,null=True)
    created = models.DateTimeField(auto_now_add=True,null=True)

    
    def __str__(self):
        return self.booking_code

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    feedback_text = models.TextField()
    feedback_date = models.DateField()
    rating = models.IntegerField()
    updated = models.DateTimeField(auto_now=True,null=True)
    created = models.DateTimeField(auto_now_add=True,null=True)


    def __str__(self):
        return self.feedback_text

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
