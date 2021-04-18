from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

is_active = (
    ('True', 'True'),
    ('False', 'False')
)

class MyAccountManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("User must an email")
        if not username:
            raise ValueError("User must an username")

        user = self.model(
                email= self.normalize_email(email),
                username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

        def create_superuser(self,email,username,password):
            user = self.create_user(
                    email= self.normalize_email(email),
                    password= password,
                    username = username,
                )
            user.is_admin = True
            user.is_staff = True
            user.is_superuser   = True
            user.save(using=self._db)
            return user         
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=20, null=True, blank=False ,verbose_name='first_name')
    email = models.EmailField(null=True, blank=False,unique = True, verbose_name='email')
    last_name = models.CharField(max_length=20,null=True, blank=False,verbose_name='last_name')
    password = models.CharField(max_length=20,null=True,blank=False,verbose_name='password')
    username = models.CharField(max_length=20,unique = True,verbose_name='username')
    rpassword = models.CharField(max_length=20,null=True,blank=False,verbose_name='confirm')
    is_active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name = "date joined" ,auto_now_add=True )
    last_login = models.DateTimeField(verbose_name= 'last login',null=True,blank=True,auto_now=True)  
    
    objects = MyAccountManager()
    
    
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email + "," + self.username 

    def has_perm(self, perm ,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_Label):
        return True
        

class electricity(models.Model):
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    is_solved = models.BooleanField(default=False)

#Model for contact
class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField( max_length=254)
    phone = models.CharField(max_length=13)
    message = models.TextField()
