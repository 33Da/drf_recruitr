from rest_framework import serializers,exceptions
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from app.recruit.models import *
import datetime
import re


User = get_user_model()

class AdminSerializer(serializers.ModelSerializer):
    """一般用户序列化器"""
    username = serializers.CharField(error_messages={"required": "账号不能为空"}, validators=[UniqueValidator(queryset=User.objects.all(),message="账号存在了")])

    password = serializers.CharField(error_messages={"required": "不能为空"},style={'input_type': 'password'}, help_text="密码", label="密码",write_only=True)

    college_name = serializers.CharField(source="college.name",read_only=True)   # 管理员属于哪个学院的


    class Meta:
        model = Admin
        fields = ("id","username","role","college","password","college_name")

    def create(self, validated_data):
        """创建用户"""
        user = Admin.objects.create(**validated_data)
        user.set_password(validated_data["password"]) # 设置密码
        user.save()
        return user


class UpdateAdminSerializer(serializers.Serializer):
    """修改用户用的序列化器"""
    username = serializers.CharField( required=False)

    password = serializers.CharField(style={'input_type': 'password'}, help_text="密码", label="密码",required=False)

    college = serializers.CharField(required=False)

    def validate(self, attrs):


        if attrs.get("college"):
            try:
                attrs["college"] = College.objects.get(id= attrs.get("college"))
            except Exception as e:
                raise serializers.ValidationError("没有该部门")

        return attrs

class MajorRecruitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MajorRecruit
        fields = "__all__"

class CollegeSerializer(serializers.ModelSerializer):
    majors = serializers.SerializerMethodField()

    def get_majors(self,college):
        result = []
        for major in college.majors.all():
            result.append({"name":major.name,"id":major.id})
        return result
    class Meta:
        model = College
        fields = "__all__"

class MajorSerializer(serializers.ModelSerializer):
    """创建专业"""
    class Meta:
        model = Major
        fields = "__all__"


class LevelSerializer(serializers.ModelSerializer):
    """水平测试序列化"""
    class Meta:
        model = Level
        fields = "__all__"

class CountryLineSerializer(serializers.ModelSerializer):
    """国家线序列化"""
    class Meta:
        model = CountryLine
        fields = "__all__"

class CollegeStudentSerializer(serializers.Serializer):
    name = serializers.CharField()
    subject = serializers.IntegerField()
    is_art = serializers.BooleanField()
    total = serializers.IntegerField()
    polit_physcs = serializers.CharField()
    history_chemistry = serializers.CharField()
    geography_biology = serializers.CharField()
    first_expectation = serializers.IntegerField()
    second_expectation = serializers.IntegerField()
    third_exception = serializers.IntegerField()
    fourth_expectation = serializers.IntegerField()
    fifth_expectation = serializers.IntegerField()
    sixth_expectation = serializers.IntegerField()
    expectation = serializers.IntegerField()
    is_pass = serializers.BooleanField()

class PicSerializer(serializers.ModelSerializer):
    """滚动图片"""
    name = serializers.CharField(max_length=50,error_messages={"required": "不能为空"})

    pic = serializers.FileField(error_messages={"required": "不能为空"})

    publish = serializers.BooleanField(error_messages={"required": "不能为空"})
    class Meta:
        model = Pic
        fields = "__all__"


class LinkSerializer(serializers.ModelSerializer):
    """链接"""
    Type = (
        (1, "管理机构"),
        (2, "服务机构"),
        (3, "教辅机构及其他"),

    )
    name = serializers.CharField(max_length=50, error_messages={"required": "不能为空"})

    link = serializers.URLField(error_messages={"required": "不能为空"})

    type = serializers.ChoiceField(Type,error_messages={"required": "不能为空"})

    class Meta:
        model = Link
        fields = "__all__"


class DownLoadSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=50, error_messages={"required": "不能为空"})

    link = serializers.FileField(error_messages={"required": "不能为空"})
    class Meta:
        model = DownLoad
        fields = "__all__"

class ToOurSerializer(serializers.ModelSerializer):
    """关于我们"""
    content = serializers.CharField(error_messages={"required": "不能为空"})

    class Meta:
        model = ToOur
        fields = "__all__"


class CollegeReciuitNewsSerializer(serializers.ModelSerializer):
    """学院招生指南"""
    Type = (
        (0, "招生政策"),
        (1, "招生章程"),
        (2, "招生简介"),
        (3, "招生计划"),
    )
    title = serializers.CharField(max_length=100)

    content = serializers.CharField()

    type = serializers.ChoiceField(choices=Type)

    class Meta:
        model = CollegeReciuitNews
        fields = "__all__"

class PostgraduateReciuitNewsSerializer(serializers.ModelSerializer):
    """研究生学院招生指南"""

    Type = (
        (0, "招生简介"),
        (1, "考试大纲"),
        (2, "专业目录"),
    )
    title = serializers.CharField(max_length=100)

    content = serializers.CharField()

    type = serializers.ChoiceField(choices=Type)

    class Meta:
        model = PostgraduateReciuitNews
        fields = "__all__"

class SpecialReciuitNewsSerializer(serializers.ModelSerializer):
    """专插本招生指南"""
    Type = (
        (0, "招生政策"),
        (1, "招生章程"),
        (2, "招生简介"),
        (3, "招生计划"),
    )
    title = serializers.CharField(max_length=100)

    content = serializers.CharField()

    type = serializers.ChoiceField(choices=Type)

    class Meta:
        model = SpecialReciuitNews
        fields = "__all__"

class TeacherSerializer(serializers.ModelSerializer):
    """学院招生"""
    college_name = serializers.CharField(source="college.name",read_only=True)
    class Meta:
        model = Teacher
        fields = "__all__"

class LastPassSerializer(serializers.ModelSerializer):
    """学院招生"""
    file = serializers.FileField(required=True)

    college_name = serializers.CharField(read_only=True,source="college.name")
    class Meta:
        model = LastPass
        fields = "__all__"

class SchoolNewsSerializer(serializers.ModelSerializer):
    """学院招生"""
    Type = (
        (0, "学校简介"),
        (1, "现任领导"),
        (2, "历任领导"),
        (3, "学校章程"),
        (4, "校训 校徽校歌")

    )
    title = serializers.CharField(max_length=100,error_messages={"required": "不能为空"})

    content = serializers.CharField(error_messages={"required": "不能为空"})

    type = serializers.ChoiceField(choices=Type,error_messages={"required": "不能为空"})

    class Meta:
        model = SchoolNews
        fields = "__all__"



class Information1Serializer(serializers.ModelSerializer):
    """信息公告"""
    Type = (
        (0, "本科生"),
        (1, "研究生"),
        (2, "专插本"),
    )
    title = serializers.CharField(max_length=100,error_messages={"required": "不能为空"})

    content = serializers.CharField(error_messages={"required": "不能为空"})

    type = serializers.ChoiceField(choices=Type, error_messages={"required": "不能为空"})
    class Meta:
        model = Information1
        fields = "__all__"


class Information2Serializer(serializers.ModelSerializer):
    """信息公示"""
    Type = (
        (0, "本科生"),
        (1, "研究生"),
        (2, "专插本"),
    )
    title = serializers.CharField(max_length=100,error_messages={"required": "不能为空"})

    content = serializers.CharField(error_messages={"required": "不能为空"})

    type = serializers.ChoiceField(choices=Type,error_messages={"required": "不能为空"})

    class Meta:
        model = Information2
        fields = "__all__"


class PostgraduateStudentSerializer(serializers.Serializer):
    """研究生"""
    name = serializers.CharField(max_length=32)  # 姓名
    idcard = serializers.CharField(max_length=18)  # 身份证
    phone = serializers.CharField(max_length=12)  # 电话
    politics = serializers.IntegerField()  # 政治
    base_subject = serializers.IntegerField()  # 基础
    english = serializers.IntegerField()  # 英语
    speciality_subject = serializers.IntegerField()  # 专业科目
    total = serializers.IntegerField()  # 总分
    want_expectation = serializers.IntegerField()  # 志愿
    expectation = serializers.IntegerField()  # 录取专业
    is_pass = serializers.BooleanField()  # 是否录取
    teacher = serializers.CharField()  # 导师
    research_interests = serializers.CharField()  # 研究方向
    examcode = serializers.CharField()  # 准考证号


class PostgraduateRecruitSerializer(serializers.ModelSerializer):
    """研究生招生计划序列化"""
    class Meta:
        model = PostgraduateRecruit
        fields = "__all__"

class PostgraduateSecondExamSerializer(serializers.Serializer):
    """研究生招生计划序列化"""
    time = serializers.DateTimeField()

    address = serializers.CharField(max_length=200)

    college = serializers.IntegerField()

class SpecialCheckSerializer(serializers.Serializer):
    """专插本学生审核资料"""
    class Meta:
        model = SpecialCheckStudent
        fields = "__all__"

class SpecialReciuitSerializer(serializers.ModelSerializer):
    """专插本学生招生计划"""
    people_num = serializers.IntegerField()

    year = serializers.IntegerField()

    major_name = serializers.CharField(source="major.name")

    class Meta:
        model = SpecialRecruit
        fields = ("id","people_num","year","major_name","major")


class SpecialStudentSerializer(serializers.Serializer):
    """研究生"""
    name = serializers.CharField(max_length=32)  # 姓名
    idcard = serializers.CharField()  # 身份证
    total = serializers.IntegerField()  # 总分
    want_expectation = serializers.IntegerField()  # 志愿
    is_pass = serializers.BooleanField()  # 是否录取
    examcode = serializers.CharField()  # 准考证号