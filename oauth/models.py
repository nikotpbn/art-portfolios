from django.db import models


# Create your models here.
# Class that defines groups
class Group(models.Model):
    class Meta:
        db_table = 'oauth_group'

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256, null=False)
    can_delete = models.IntegerField(default=1)


# Class that defines permissions
class Permission(models.Model):
    class Meta:
        db_table = 'oauth_permission'

    id = models.IntegerField(primary_key=True)
    url = models.CharField(max_length=512, null=False)
    description = models.CharField(max_length=128, null=False)
    permissionArea = models.CharField(max_length=128, null=False)
    needPermission = models.IntegerField(default=1)


# Class that defines users
class User(models.Model):
    class Meta:
        db_table = 'oauth_user'

    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=254, null=True, unique=True)
    name = models.CharField(max_length=512, null=False)
    email = models.EmailField(max_length=254, null=False, unique=True)
    password = models.CharField(max_length=256, null=False)
    image = models.FileField(upload_to='user_avatar')
    birth_date = models.DateField(null=True)
    last_login = models.DateTimeField(null=True)
    need_logout = models.BooleanField(default=False)
    news_letter = models.IntegerField(default=None, null=True)
    active = models.BooleanField(default=True)


# Class that relates permissions to users
class UserPermission(models.Model):
    class Meta:
        db_table = 'oauth_user_permission'

    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT, null=False)


# Class that relates users to groups
class UserGroup(models.Model):
    class Meta:
        db_table = 'oauth_user_group'

    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, null=False)


# Class that gives user groups permissions
class GroupPermission(models.Model):
    class Meta:
        db_table = 'oauth_group_permission'

    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=False)
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT, null=False)