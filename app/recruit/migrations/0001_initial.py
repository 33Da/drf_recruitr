# Generated by Django 2.2 on 2020-04-03 10:51

import DjangoUeditor.models
import app.recruit.models
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CollegeReciuitNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', DjangoUeditor.models.UEditorField(blank=True, help_text='信息公布', null=True, verbose_name='信息公布')),
                ('type', models.IntegerField(choices=[(0, '招生政策'), (1, '招生章程'), (2, '招生简介'), (3, '招生计划')], help_text='类型', verbose_name='类型')),
            ],
        ),
        migrations.CreateModel(
            name='CountryLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.IntegerField(choices=[(0, '哲学'), (1, '经济学'), (2, '法学'), (3, '教育学'), (4, '文学'), (5, '历史学'), (6, '理学'), (7, '工学'), (8, '农学'), (9, '医学'), (10, '军事学'), (11, '艺术学')], default=0)),
                ('total', models.IntegerField()),
                ('passsubject1', models.IntegerField()),
                ('passsubject2', models.IntegerField()),
                ('year', models.IntegerField(default=2020)),
            ],
        ),
        migrations.CreateModel(
            name='DownLoad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='链接名', max_length=50, verbose_name='链接名')),
                ('link', models.FileField(blank=True, null=True, upload_to='data/download/')),
            ],
        ),
        migrations.CreateModel(
            name='Information1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', DjangoUeditor.models.UEditorField(blank=True, help_text='信息公布', null=True, verbose_name='信息公布')),
                ('type', models.IntegerField(choices=[(0, '本科生'), (1, '研究生'), (2, '专插本')], help_text='类型', verbose_name='类型')),
            ],
        ),
        migrations.CreateModel(
            name='Information2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', DjangoUeditor.models.UEditorField(blank=True, help_text='信息公布', null=True, verbose_name='信息公布')),
                ('type', models.IntegerField(choices=[(0, '本科生'), (1, '研究生'), (2, '专插本')], help_text='类型', verbose_name='类型')),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('polit_physcs', models.CharField(max_length=5)),
                ('history_chemistry', models.CharField(max_length=5)),
                ('geography_biology', models.CharField(max_length=5)),
                ('year', models.IntegerField(default=2020)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='链接名', max_length=50, verbose_name='链接名')),
                ('link', models.URLField(help_text='链接', max_length=100, verbose_name='链接')),
                ('type', models.IntegerField(choices=[(1, '管理机构'), (2, '服务机构'), (3, '教辅机构及其他')], help_text='类型', verbose_name='类型')),
            ],
        ),
        migrations.CreateModel(
            name='Major',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.IntegerField(default=0)),
                ('type', models.IntegerField(choices=[(0, '普通专业'), (1, '研究生专业')], default=0)),
                ('subject', models.IntegerField(choices=[(0, '哲学'), (1, '经济学'), (2, '法学'), (3, '教育学'), (4, '文学'), (5, '历史学'), (6, '理学'), (7, '工学'), (8, '农学'), (9, '医学'), (10, '军事学'), (11, '艺术学')], default=7)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='majors', to='recruit.College')),
            ],
        ),
        migrations.CreateModel(
            name='Pic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='图片名', max_length=100, verbose_name='图片名')),
                ('pic', models.FileField(blank=True, null=True, upload_to='pic/')),
                ('publish', models.BooleanField(default=False, help_text='是否发布', verbose_name='是否发布')),
            ],
        ),
        migrations.CreateModel(
            name='PostgraduateReciuitNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', DjangoUeditor.models.UEditorField(blank=True, help_text='信息公布', null=True, verbose_name='信息公布')),
                ('type', models.IntegerField(choices=[(0, '招生简介'), (1, '考试大纲'), (2, '专业目录')], help_text='类型', verbose_name='类型')),
            ],
        ),
        migrations.CreateModel(
            name='SchoolNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', DjangoUeditor.models.UEditorField(blank=True, help_text='信息公布', null=True, verbose_name='信息公布')),
                ('type', models.IntegerField(choices=[(0, '学校简介'), (1, '现任领导'), (2, '历任领导'), (3, '学校章程'), (4, '校训 校徽校歌')], help_text='类型', verbose_name='类型')),
            ],
        ),
        migrations.CreateModel(
            name='SpecialCheckStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_pass', models.BooleanField()),
                ('name', models.CharField(max_length=32)),
                ('address', models.CharField(max_length=100)),
                ('idcard', models.CharField(max_length=18)),
                ('phone', models.CharField(max_length=12)),
                ('file', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SpecialReciuitNews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', DjangoUeditor.models.UEditorField(blank=True, help_text='信息公布', null=True, verbose_name='信息公布')),
                ('type', models.IntegerField(choices=[(0, '招生简介'), (1, '考试大纲'), (2, '专业目录')], help_text='类型', verbose_name='类型')),
            ],
        ),
        migrations.CreateModel(
            name='ToOur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', DjangoUeditor.models.UEditorField(blank=True, help_text='活动内容', null=True, verbose_name='活动内容')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='指导老师名', max_length=50, verbose_name='指导老师名')),
                ('content', DjangoUeditor.models.UEditorField(blank=True, help_text='活动内容', null=True, verbose_name='活动内容')),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teachers', to='recruit.College')),
            ],
        ),
        migrations.CreateModel(
            name='SpecialRecruit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('people_num', models.IntegerField(default=0)),
                ('is_ok', models.BooleanField(default=False)),
                ('year', models.IntegerField(default=2020)),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specialrecruit', to='recruit.Major')),
            ],
        ),
        migrations.CreateModel(
            name='PostgraduateRecruit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstexam', models.FileField(blank=True, null=True, upload_to=app.recruit.models.upload_to)),
                ('secondexam', models.FileField(blank=True, null=True, upload_to=app.recruit.models.upload_to)),
                ('secondexamtime', models.DateTimeField(blank=True, null=True)),
                ('secondexamaddress', models.CharField(blank=True, max_length=200, null=True)),
                ('year', models.IntegerField(default=2020)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='secondexam', to='recruit.College')),
            ],
        ),
        migrations.CreateModel(
            name='MajorRecruit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('people_num', models.IntegerField(default=0)),
                ('art_people_num', models.IntegerField(default=0)),
                ('is_ok', models.BooleanField(default=False)),
                ('is_art_ok', models.BooleanField(default=False)),
                ('year', models.IntegerField(default=2020)),
                ('major', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wantrecruit', to='recruit.Major')),
            ],
        ),
        migrations.CreateModel(
            name='LastPass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='data/pass/')),
                ('year', models.CharField(help_text='年', max_length=4, verbose_name='年')),
                ('type', models.IntegerField(choices=[(0, '文史类'), (1, '理工类'), (2, '艺术类')])),
                ('name', models.CharField(max_length=100, verbose_name='文件名')),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lastpass', to='recruit.College')),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.IntegerField(choices=[(0, '普通老师'), (1, '管理员')], default=0)),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='admin', to='recruit.College')),
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
