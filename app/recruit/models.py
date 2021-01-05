from django.db import models
import mongoengine
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from DjangoUeditor.models import UEditorField
import datetime
from drf_recruitr.settings import MEDIA_ROOT

#让上传的文件路径动态地与user的名字有关
def upload_to(instance, filename):

    return '/'.join([MEDIA_ROOT,"data/upload/Postgraduate/",datetime.datetime.now().strftime("%Y%m%d%H%M%S")+ ".xls"])

class College(models.Model):
    """学院"""
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Admin(AbstractUser):
    ROLE_TYPE = (
        (0, "普通老师"),
        (1, "管理员"),
    )

    role = models.IntegerField(choices=ROLE_TYPE, default=0)

    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="admin",null=True,blank=True)

    def __str__(self):
        return self.username



class Major(models.Model):
    """专业表"""
    TYPE = (
        (0,"普通专业"),
        (1,"研究生专业"),

    )

    SUBJECT = (
        (0, "哲学"),
        (1, "经济学"),
        (2, "法学"),
        (3, "教育学"),
        (4, "文学"),
        (5, "历史学"),
        (6, "理学"),
        (7, "工学"),
        (8, "农学"),
        (9, "医学"),
        (10,"军事学"),
        (11,"艺术学"),
    )
    name = models.CharField(max_length=100)  # 专业名

    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name="majors")

    code = models.IntegerField(default=0)   # 专业代码

    type = models.IntegerField(choices=TYPE,default=0)

    subject = models.IntegerField(choices=SUBJECT,default=7)


class MajorRecruit(models.Model):
    major = models.ForeignKey(Major,related_name="wantrecruit",on_delete=models.CASCADE)

    people_num = models.IntegerField(default=0)  # 招生人数

    art_people_num = models.IntegerField(default=0)  # 艺考生人数

    is_ok = models.BooleanField(default=False)  # 该专业是否招满

    is_art_ok = models.BooleanField(default=False)  # 该专业艺术生是否招满

    year = models.IntegerField(default=int(datetime.date.today().year))

    def __str__(self):
        return self.name

class CountryLine(models.Model):
    """记录每年国家线"""
    SUBJECT = (
        (0, "哲学"),
        (1, "经济学"),
        (2, "法学"),
        (3, "教育学"),
        (4, "文学"),
        (5, "历史学"),
        (6, "理学"),
        (7, "工学"),
        (8, "农学"),
        (9, "医学"),
        (10, "军事学"),
        (11, "艺术学"),
    )


    subject = models.IntegerField(choices=SUBJECT,default=0)

    total = models.IntegerField()  # 总分

    passsubject1 = models.IntegerField()  # 100分满分的单科过线分

    passsubject2 = models.IntegerField()  # 大于100分的单科过线分

    year = models.IntegerField(default=int(datetime.date.today().year))

    def __str__(self):
        return self.name

class PostgraduateRecruit(models.Model):
    """每个员招生情况"""
    # 初试通过名单
    firstexam = models.FileField(upload_to=upload_to,blank=True,null=True)

    # 复试通过名单
    secondexam = models.FileField(upload_to=upload_to,blank=True,null=True)

    # 复试时间
    secondexamtime = models.DateTimeField(blank=True,null=True)

    # 复试地点
    secondexamaddress = models.CharField(max_length=200,blank=True,null=True)

    # 院
    college = models.ForeignKey(College,related_name="secondexam",on_delete=models.CASCADE)

    year = models.IntegerField(default=int(datetime.date.today().year))


class SpecialRecruit(models.Model):
    major = models.ForeignKey(Major,related_name="specialrecruit",on_delete=models.CASCADE)

    people_num = models.IntegerField(default=0)  # 招生人数

    is_ok = models.BooleanField(default=False)  # 该专业是否招满

    year = models.IntegerField(default=int(datetime.date.today().year))



class CollegeStudent(mongoengine.Document):
    """本科生表"""
    SUBJECT = (
        (0, "文科"),
        (1, "理科")
    )
    name = mongoengine.StringField(max_length=32)  # 姓名
    idcard = mongoengine.StringField(max_length=18)  # 身份证
    address = mongoengine.StringField(max_length=100)  # 地址
    subject = mongoengine.IntField(choices=SUBJECT)  # 0文科 1 理科
    is_art = mongoengine.BooleanField()  # 艺考生
    chinese = mongoengine.IntField()  # 语文
    math = mongoengine.IntField()  # 数学
    english = mongoengine.IntField()  # 英语
    integrated_subject = mongoengine.IntField()  # 综合科目
    total = mongoengine.IntField()  # 总分
    polit_physcs = mongoengine.StringField()  # 思想政治（物理）
    history_chemistry = mongoengine.StringField()  # 历史（化学）
    geography_biology = mongoengine.StringField()  # 地理（生物）
    first_expectation = mongoengine.IntField()  # 第一志愿
    second_expectation = mongoengine.IntField()
    third_exception = mongoengine.IntField()
    fourth_expectation = mongoengine.IntField()
    fifth_expectation = mongoengine.IntField()
    sixth_expectation = mongoengine.IntField()
    expectation = mongoengine.IntField()  # 录取专业
    examcode = mongoengine.StringField()  # 准考证号
    is_dispensing = mongoengine.BooleanField()  # 是否服从调剂
    is_province = mongoengine.BooleanField()  # 是否省内
    is_city = mongoengine.BooleanField()  # 是否市内
    is_pass = mongoengine.BooleanField()  # 是否录取

class SpecialStudent(mongoengine.Document):
    """专插本"""
    name = mongoengine.StringField(max_length=32)  # 姓名
    examcode = mongoengine.StringField(max_length=15)  # 准考证号
    idcard = mongoengine.StringField(max_length=20)  # 身份证
    total = mongoengine.IntField()  # 总分
    polity = mongoengine.IntField()  # 思想政治（物理）
    english = mongoengine.IntField()  # 历史（化学）
    speciality_subject1 = mongoengine.IntField()  # 专业课1
    speciality_subject2 = mongoengine.IntField()  # 专业课2
    speciality_basesubject = mongoengine.IntField()  # 专业基础课
    want_expectation = mongoengine.IntField()  # 投递志愿
    is_pass = mongoengine.BooleanField()  # 是否录取



class SpecialCheckStudent(models.Model):
    """专插本"""
    is_pass = models.BooleanField()  # 是否录取
    name = models.CharField(max_length=32)  # 姓名
    address = models.CharField(max_length=100)  # 地址
    idcard = models.CharField(max_length=18)  # 身份证
    phone = models.CharField(max_length=12)   # 电话

    file = models.CharField(max_length=200)  # 文件url


class Postgraduate(mongoengine.Document):
    """研究生"""
    name = mongoengine.StringField(max_length=32)  # 姓名
    idcard = mongoengine.StringField(max_length=18)  # 身份证
    phone = mongoengine.StringField(max_length=12)  # 电话
    politics = mongoengine.IntField()  # 政治
    base_subject = mongoengine.IntField()  # 基础
    english = mongoengine.IntField()  # 英语
    speciality_subject = mongoengine.IntField()  # 专业科目
    total = mongoengine.IntField()  # 总分
    want_expectation = mongoengine.IntField()  # 志愿
    expectation = mongoengine.IntField()  # 录取专业
    is_pass = mongoengine.BooleanField()  # 是否录取
    teacher = mongoengine.StringField()   # 导师
    research_interests = mongoengine.StringField() # 研究方向
    passfirstexam = mongoengine.BooleanField()   # 真正通过初试
    passsecondexam = mongoengine.BooleanField()  # 通过复试
    examcode = mongoengine.StringField()  # 准考证号

    def __str__(self):
        return self.name


class Pic(models.Model):
    """滚动图片"""
    name = models.CharField(max_length=100, verbose_name="图片名", help_text="图片名")

    pic = models.FileField(blank=True, null=True, upload_to="pic/")

    publish = models.BooleanField(default=False, verbose_name="是否发布", help_text="是否发布")


class Teacher(models.Model):
    """指导老师"""
    name = models.CharField(max_length=50, help_text="指导老师名", verbose_name="指导老师名")

    content = UEditorField(verbose_name="活动内容", help_text="活动内容", null=True, blank=True, filePath='teacher/',
                           imagePath='teacher/')

    college = models.ForeignKey(College, related_name="teachers", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Link(models.Model):
    """校园链接"""
    Type = (
        (1, "管理机构"),
        (2, "服务机构"),
        (3, "教辅机构及其他"),

    )
    name = models.CharField(max_length=50, help_text="链接名", verbose_name="链接名")

    link = models.URLField(max_length=100, verbose_name="链接", help_text="链接")

    type = models.IntegerField(choices=Type, verbose_name="类型", help_text="类型")

    def __str__(self):
        return self.name


class ToOur(models.Model):
    """关于我们"""
    content = UEditorField(verbose_name="活动内容", help_text="活动内容", null=True, blank=True, filePath='our/',
                           imagePath='our/')


class SchoolNews(models.Model):
    """信息公告"""
    Type = (
        (0, "学校简介"),
        (1, "现任领导"),
        (2, "历任领导"),
        (3, "学校章程"),
        (4, "校训 校徽校歌")

    )
    title = models.CharField(max_length=100)

    content = UEditorField(verbose_name="信息公布", help_text="信息公布", null=True, blank=True, filePath='school/',
                           imagePath='school/')

    type = models.IntegerField(choices=Type, verbose_name="类型", help_text="类型")


class DownLoad(models.Model):
    """下载链接"""
    name = models.CharField(max_length=50, help_text="链接名", verbose_name="链接名")

    link = models.FileField(blank=True, null=True, upload_to="data/download/")


class CollegeReciuitNews(models.Model):
    """本科招生指南"""

    Type = (
        (0, "招生政策"),
        (1, "招生章程"),
        (2, "招生简介"),
        (3, "招生计划"),
    )
    title = models.CharField(max_length=100)

    content = UEditorField(verbose_name="信息公布", help_text="信息公布", null=True, blank=True, filePath='school/',
                           imagePath='school/')

    type = models.IntegerField(choices=Type, verbose_name="类型", help_text="类型")

    def __str__(self):
        return self.title


class PostgraduateReciuitNews(models.Model):
    """研究生招生指南"""

    Type = (
        (0, "招生简介"),
        (1, "考试大纲"),
        (2, "专业目录"),
    )
    title = models.CharField(max_length=100)

    content = UEditorField(verbose_name="信息公布", help_text="信息公布", null=True, blank=True, filePath='school/',
                           imagePath='school/')

    type = models.IntegerField(choices=Type, verbose_name="类型", help_text="类型")

    def __str__(self):
        return self.title


class SpecialReciuitNews(models.Model):
    """专插本招生简介"""

    Type = (
        (0, "招生简介"),
        (1, "考试大纲"),
        (2, "专业目录"),
    )
    title = models.CharField(max_length=100)

    content = UEditorField(verbose_name="信息公布", help_text="信息公布", null=True, blank=True, filePath='school/',
                           imagePath='school/')

    type = models.IntegerField(choices=Type, verbose_name="类型", help_text="类型")

    def __str__(self):
        return self.title


class LastPass(models.Model):
    """历年录取"""
    Type = (
        (0, "文史类"),
        (1, "理工类"),
        (2, "艺术类"),
    )

    college = models.ForeignKey(College, related_name="lastpass", on_delete=models.CASCADE)

    file = models.FileField(blank=True, null=True, upload_to="data/pass/")

    year = models.CharField(max_length=4, help_text="年", verbose_name="年")

    type = models.IntegerField(choices=Type)

    name = models.CharField(max_length=100, verbose_name="文件名")


class Information1(models.Model):
    """信息公示"""

    Type = (
        (0, "本科生"),
        (1, "研究生"),
        (2, "专插本"),
    )
    title = models.CharField(max_length=100)

    content = UEditorField(verbose_name="信息公布", help_text="信息公布", null=True, blank=True, filePath='school/',
                           imagePath='school/')

    type = models.IntegerField(choices=Type, verbose_name="类型", help_text="类型")

    def __str__(self):
        return self.title


class Information2(models.Model):
    """信息公告"""

    Type = (
        (0, "本科生"),
        (1, "研究生"),
        (2, "专插本"),
    )
    title = models.CharField(max_length=100)

    content = UEditorField(verbose_name="信息公布", help_text="信息公布", null=True, blank=True, filePath='school/',
                           imagePath='school/')

    type = models.IntegerField(choices=Type, verbose_name="类型", help_text="类型")

    def __str__(self):
        return self.title

class Level(models.Model):
    """水平测试"""
    polit_physcs = models.CharField(max_length=5) # 思想政治（物理）

    history_chemistry = models.CharField(max_length=5)  # 历史（化学）

    geography_biology = models.CharField(max_length=5)  # 地理（生物）

    year = models.IntegerField(default=int(datetime.date.today().year))

