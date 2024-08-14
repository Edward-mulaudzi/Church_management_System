# Generated by Django 3.2.12 on 2024-08-07 18:29

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='church_branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch_name', models.CharField(max_length=100)),
                ('fb_number', models.CharField(max_length=100)),
                ('branch_head', models.CharField(max_length=200)),
                ('centre_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='church_member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=250)),
                ('gender', models.CharField(max_length=100)),
                ('grade', models.CharField(max_length=100)),
                ('id_number', models.CharField(max_length=13)),
                ('place', models.CharField(max_length=150)),
                ('parent_contact', models.CharField(max_length=150)),
                ('institution_name', models.CharField(max_length=150)),
                ('field_of_study', models.CharField(max_length=150)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managementSystem.church_branch')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=250)),
                ('structure', models.CharField(max_length=250)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managementSystem.church_branch')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managementSystem.church_member')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance_List',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=250)),
                ('students_present', models.CharField(max_length=250)),
                ('students_absent', models.CharField(max_length=250)),
                ('students_total', models.CharField(max_length=250)),
                ('teachers_present', models.CharField(max_length=250)),
                ('teachers_absent', models.CharField(max_length=250)),
                ('teachers_total', models.CharField(max_length=250)),
                ('committee_present', models.CharField(max_length=250)),
                ('committee_absent', models.CharField(max_length=250)),
                ('committee_total', models.CharField(max_length=250)),
                ('health_present', models.CharField(max_length=250)),
                ('health_absent', models.CharField(max_length=250)),
                ('health_total', models.CharField(max_length=250)),
                ('LCDC_Management_present', models.CharField(max_length=250)),
                ('LCDC_Management_absent', models.CharField(max_length=250)),
                ('LCDC_Management_total', models.CharField(max_length=250)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managementSystem.church_branch')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance_date',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=250)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managementSystem.church_branch')),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.CharField(max_length=250)),
                ('attendance', models.CharField(max_length=250)),
                ('structure', models.CharField(max_length=250)),
                ('role', models.CharField(max_length=250)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managementSystem.church_branch')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managementSystem.church_member')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Is superuser')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is admin')),
                ('is_user', models.BooleanField(default=False, verbose_name='Is user')),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='managementSystem.church_branch')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
