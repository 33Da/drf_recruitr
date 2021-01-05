from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework import viewsets
from app.recruit.models import *
from app.recruit.seriailzers import *
from utils.util import ordinary_recruit, wite_to_excel, postgraduate_recruit, read_to_excle, special_recriit, \
    special_examrecriit
from drf_recruitr.settings import MEDIA_ROOT
from django_filters.rest_framework import DjangoFilterBackend
from utils.permissions import AdminPermission


class P1(PageNumberPagination):
    """
    基于页码
    """
    # 默认每页显示的数据条数
    page_size = 10
    # 获取url参数中设置的每页显示数据条数
    page_size_query_param = 'pagesize'
    # 获取url中传入的页码key
    page_query_param = 'page'
    # 最大支持的每页显示的数据条数
    max_page_size = 50


class AdminViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """用户逻辑"""
    serializer_class = AdminSerializer
    pagination_class = P1
    queryset = Admin.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ("update", "retrieve"):
            return (IsAuthenticated(),)
        else:
            return (IsAuthenticated(), AdminPermission())

    def update(self, request, *args, **kwargs):
        """修改用户"""
        # 校验参数
        serializer = UpdateAdminSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            admin = Admin.objects.get(id=int(kwargs.get("pk")))
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该用户",
                             }, status=status.HTTP_200_OK)

        if serializer.validated_data.get("username"):
            if Admin.objects.filter(username=admin.username).exclude(id=admin.id).count() != 0:
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "用户名重复",
                                 }, status=status.HTTP_200_OK)

        if serializer.validated_data.get("password"):
            admin.set_password(serializer.validated_data.pop("password"))
            admin.save()

        Admin.objects.filter(id=admin.id).update(**serializer.validated_data)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")

        if id == 0:
            serializer = AdminSerializer(instance=request.user)
        else:
            try:
                admin = Admin.objects.get(id=int(id))
            except Exception as e:
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "找不到该用户",
                                 }, status=status.HTTP_200_OK)
            serializer = AdminSerializer(instance=admin)
        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": serializer.data,
                         }, status=status.HTTP_200_OK)


class MajorViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """专业逻辑"""
    serializer_class = MajorSerializer
    pagination_class = P1
    queryset = Major.objects.all()

    # 过滤器
    filter_backends = (DjangoFilterBackend,)
    # 如果要允许对某些字段进行过滤，可以使用filter_fields属性。
    filter_fields = ('type', "subject")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ("create", 'retrieve'):
            return (IsAuthenticated(),)
        else:
            return ()


class LevelViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin):
    """水平测试逻辑"""
    serializer_class = LevelSerializer
    pagination_class = P1
    queryset = Level.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    # 如果要允许对某些字段进行过滤，可以使用filter_fields属性。
    filter_fields = ('year',)


class CollegeViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """学院逻辑"""
    serializer_class = CollegeSerializer
    pagination_class = P1
    queryset = College.objects.all().order_by("id")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ("create", "update"):
            return (IsAuthenticated(),)
        else:
            return ()


class MajorRecruitViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    """学院招生人数"""
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    serializer_class = MajorRecruitSerializer
    pagination_class = P1
    queryset = MajorRecruit.objects.all()

    filter_backends = (DjangoFilterBackend,)
    # 如果要允许对某些字段进行过滤，可以使用filter_fields属性。
    filter_fields = ('year',)

    def get_permissions(self):
        if self.action in ("create", 'retrieve'):
            return (IsAuthenticated(),)
        else:
            return ()

    def update(self, request, *args, **kwargs):
        """输入学院招生人数"""
        # 招生人数
        people_num = request.data.get("people_num", 0)
        art_people = request.data.get("art_people", 0)

        id = kwargs.get("pk", 0)  # 专业id

        try:
            major = Major.objects.get(id=int(id))
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有该专业",
                             }, status=status.HTTP_200_OK)

        want_recruit = MajorRecruit.objects.filter(major=major, year=int(datetime.date.today().year)).first()
        if want_recruit is None:
            MajorRecruit.objects.create(people_num=people_num, major=major, art_people_num=art_people)
        else:
            want_recruit.people_num = people_num
            want_recruit.art_people_num = art_people
            want_recruit.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)


class CollegeStudentViewset(viewsets.GenericViewSet):
    """普通大学生招生view"""
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """上传文件"""
        file = request.FILES.get('file')

        try:
            with open("media/upload/ordinary/" + "考生电子档案.zip", 'wb+') as destination:
                for line in file.chunks():
                    destination.write(line)
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "上传错误",
                             }, status=status.HTTP_200_OK)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """生成招生名单"""

        # 从word读取学生信息
        students = ordinary_recruit()

        # 将mongodb删除
        CollegeStudent.objects.all().delete()

        # 将学生信息存入mongo
        for student in students:
            CollegeStudent.objects.create(**student)

        # 获取今年专业水平成绩
        level = Level.objects.filter(year=int(datetime.date.today().year)).first()

        major_students = {}  # 按专业分类

        # 第一轮
        # 查询所有专业
        majors = Major.objects.filter(type=0).all()

        # 专业全部设成未招满
        for major in majors:
            major.is_ok = False
            major.save()

        # 按成绩排名 专业水平测试要通过
        for major in majors:
            students = list(CollegeStudent.objects.filter(polit_physcs__lte=level.polit_physcs,
                                                          history_chemistry__lte=level.history_chemistry,
                                                          geography_biology__lte=level.geography_biology,
                                                          first_expectation=major.code, is_art=False).all().order_by(
                "-total"))

            # 专业招生预期招生情况
            wantrecruit = major.wantrecruit.filter(year=int(datetime.date.today().year)).first()
            if wantrecruit.people_num <= len(students):  # 如果实际人数超过招生人数
                students = students[0:len(students)]
                wantrecruit.is_ok = True
                wantrecruit.save()

            for student in students:  # 被录取
                student.is_pass = True
                student.expectation = major.code
                student.save()

            major_students[major.code] = students

        # 第2-6轮
        parameters = [dict(polit_physcs__lte=level.polit_physcs, history_chemistry__lte=level.history_chemistry,
                           geography_biology__lte=level.geography_biology, second_expectation=major.code,
                           is_pass=False),
                      dict(polit_physcs__lte=level.polit_physcs, history_chemistry__lte=level.history_chemistry,
                           geography_biology__lte=level.geography_biology, third_exception=major.code, is_pass=False),
                      dict(polit_physcs__lte=level.polit_physcs, history_chemistry__lte=level.history_chemistry,
                           geography_biology__lte=level.geography_biology, fourth_expectation=major.code,
                           is_pass=False),
                      dict(polit_physcs__lte=level.polit_physcs, history_chemistry__lte=level.history_chemistry,
                           geography_biology__lte=level.geography_biology, fifth_expectation=major.code, is_pass=False),
                      dict(polit_physcs__lte=level.polit_physcs, history_chemistry__lte=level.history_chemistry,
                           geography_biology__lte=level.geography_biology, sixth_expectation=major.code, is_pass=False),
                      ]
        for parameter in parameters:
            # 从未招满的人来选
            majors = Major.objects.filter(wantrecruit__is_ok=False, type=0).all()

            for major in majors:
                students = list(
                    CollegeStudent.objects.filter(**parameter).filter(is_art=False).all().order_by("-total"))

                major_students[major.code].extend(students)

                wantrecruit = major.wantrecruit.filter(year=int(datetime.date.today().year)).first()
                if wantrecruit.people_num <= len(students):  # 如果实际人数超过招生人数
                    major_students[major.code] = major_students[major.code][0:len(students)]
                    wantrecruit.is_ok = True
                    wantrecruit.save()

                for student in major_students[major.code]:  # 被录取
                    if student.is_pass == False:
                        student.is_pass = True
                        student.expectation = major.code
                        student.save()

        # 调剂的逻辑
        # 查看是否有未招满的专业
        notfull_majors = Major.objects.filter(wantrecruit__is_ok=False, type=0)

        # 随机分到各个专业去
        for major in notfull_majors:
            wantrecruit = major.wantrecruit.filter(year=int(datetime.date.today().year)).first()
            count = wantrecruit.people_num - CollegeStudent.objects.filter(expectation=major.code).count()
            for i in range(0, count):
                student = CollegeStudent.objects.filter(is_pass=False, is_dispensing=True).order_by("-total").first()
                if student == None:
                    break
                student.is_pass = True
                student.expectation = major.code
                student.save()
                if i == count:  # 证明招满了
                    wantrecruit.is_ok = True
                    wantrecruit.save()

                major_students[major.code].append(student)

        # 对结果序列化
        for major, students in major_students.items():
            major_students[major] = CollegeStudentSerializer(instance=students, many=True).data

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": major_students,
                         }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """获取招生excle名单"""
        id = kwargs.get("pk")  # 院的id
        record = []
        if 0 == int(id):  # 获取全部

            students = CollegeStudent.objects.filter(is_pass=True).all().order_by("-total")
            for student in students:
                major = Major.objects.get(code=student.expectation)

                record.append((student.name, student.examcode, student.total, major.name, major.college.name))

            filename = '录取名单'

        else:
            try:
                college = College.objects.get(id=id)
            except Exception as e:
                return Response({"status_code": status.HTTP_200_OK,
                                 "message": "ok",
                                 "results": "找不到学院",
                                 }, status=status.HTTP_200_OK)

                # 该学院的所有专业
            majors = college.majors.all()

            for major in majors:
                students = CollegeStudent.objects.filter(is_pass=True, expectation=major.code).all().order_by("-total")
                for student in students:
                    record.append((student.name, student.examcode, student.total, major.name, college.name))
            filename = college.name
        # 表头
        excle_head = ["学生姓名", '考生号', "学生总分", "专业名", "学院"]

        # 写入数据到excel中
        ret = wite_to_excel(filename, excle_head, record)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": ret,
                         }, status=status.HTTP_200_OK)

    def destory(self, request, *args, **kwargs):
        """获取退档excle名单"""

        # 表头
        excle_head = ["学生姓名", "准考证号", "学生总分"]

        record = []
        students = CollegeStudent.objects.filter(is_pass=False).all().order_by("-total")
        for student in students:
            record.append((student.name, student.examcode, student.total))

        # 写入数据到excel中
        ret = wite_to_excel("退档名单", excle_head, record)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": ret,
                         }, status=status.HTTP_200_OK)


class PicViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """滚动照片逻辑"""
    serializer_class = PicSerializer
    pagination_class = P1
    queryset = Pic.objects.all()

    filter_backends = (DjangoFilterBackend,)
    # 如果要允许对某些字段进行过滤，可以使用filter_fields属性。
    filter_fields = ('publish',)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ("create", 'retrieve'):
            return (IsAuthenticated(),)
        else:
            return ()

    def update(self, request, *args, **kwargs):
        """发布图片"""
        id = kwargs.get("pk", 0)
        publish = request.data.get("publish", 0)
        try:
            pic = Pic.objects.get(id=id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到图片",
                             }, status=status.HTTP_200_OK)
        if 0 == int(publish):
            pic.publish = False
        else:
            pic.publish = True
        pic.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)


class DownloadViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """下载逻辑"""
    serializer_class = DownLoadSerializer
    pagination_class = P1
    queryset = DownLoad.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ("create", 'update'):
            return (IsAuthenticated(),)
        else:
            return ()


class LinkViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """链接逻辑"""
    serializer_class = LinkSerializer
    pagination_class = P1
    queryset = Link.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ("create", 'update'):
            return (IsAuthenticated(),)
        else:
            return ()


class OurViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """关于我们逻辑"""
    serializer_class = ToOurSerializer
    pagination_class = P1
    queryset = ToOur.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ("create", 'update'):
            return (IsAuthenticated(),)
        else:
            return ()


class CollegeReciuitNewsViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                                mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """本科招生指南逻辑"""
    serializer_class = CollegeReciuitNewsSerializer
    pagination_class = P1
    queryset = CollegeReciuitNews.objects.all()

    # 过滤器
    filter_backends = (DjangoFilterBackend,)
    # 如果要允许对某些字段进行过滤，可以使用filter_fields属性。
    filter_fields = ('type',)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ("create", 'update'):
            return (IsAuthenticated(),)
        else:
            return ()


class SpecialReciuitNewsViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                                mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """专插本招生指南逻辑"""
    serializer_class = SpecialReciuitNewsSerializer
    pagination_class = P1
    queryset = SpecialReciuitNews.objects.all()

    filter_backends = (DjangoFilterBackend,)
    # 如果要允许对某些字段进行过滤，可以使用filter_fields属性。
    filter_fields = ('type',)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ("create", 'update'):
            return (IsAuthenticated(),)
        else:
            return ()


class PostgraduateReciuitNewsViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                                     mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """研究生招生指南逻辑"""
    serializer_class = PostgraduateReciuitNewsSerializer
    pagination_class = P1
    queryset = PostgraduateReciuitNews.objects.all()

    filter_backends = (DjangoFilterBackend,)
    # 如果要允许对某些字段进行过滤，可以使用filter_fields属性。
    filter_fields = ('type',)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ("create", 'update'):
            return (IsAuthenticated(),)
        else:
            return ()


class TeacherViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """指导老师逻辑"""
    serializer_class = TeacherSerializer
    pagination_class = P1
    queryset = Teacher.objects.all()

    filter_backends = (DjangoFilterBackend,)
    # 如果要允许对某些字段进行过滤，可以使用filter_fields属性。
    filter_fields = ('college',)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ("create", 'update'):
            return (IsAuthenticated(),)
        else:
            return ()


class LastPassViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """历年录取逻辑"""
    serializer_class = LastPassSerializer
    pagination_class = P1
    queryset = LastPass.objects.all()

    filter_backends = (DjangoFilterBackend,)
    # 如果要允许对某些字段进行过滤，可以使用filter_fields属性。
    filter_fields = ('type', "year", "college")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ("create", 'update'):
            return (IsAuthenticated(),)
        else:
            return ()


class SchoolNewsViewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                        mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """学校信息逻辑"""

    serializer_class = SchoolNewsSerializer
    pagination_class = P1
    queryset = SchoolNews.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ("create", 'update'):
            return (IsAuthenticated(),)
        else:
            return ()

    def create(self, request, *args, **kwargs):
        serializer = SchoolNewsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        schoolnew = SchoolNews.objects.filter(type=data["type"]).first()
        if schoolnew == None:
            SchoolNews.objects.create(**data)
        else:
            schoolnew.content = data["content"]
            schoolnew.title = data["title"]
            schoolnew.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)


class Information1Viewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                          mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """信息公示"""
    serializer_class = Information1Serializer
    pagination_class = P1
    queryset = Information1.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ("create", 'update'):
            return (IsAuthenticated(),)
        else:
            return ()


class Information2Viewset(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                          mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    """信息公告"""
    serializer_class = Information2Serializer
    pagination_class = P1
    queryset = Information2.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    def get_permissions(self):
        if self.action in ("create", 'update'):
            return (IsAuthenticated(),)
        else:
            return ()


class CountryLineViewset(viewsets.GenericViewSet, mixins.ListModelMixin):
    """考研国家线"""
    serializer_class = CountryLineSerializer
    pagination_class = P1
    queryset = CountryLine.objects.all()
    filter_backends = (DjangoFilterBackend,)
    # 如果要允许对某些字段进行过滤，可以使用filter_fields属性。
    filter_fields = ('subject', "year")
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)

    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """输入考研国家线"""
        subject = int(request.data.get("subject", 0))  # 学科
        subject1 = int(request.data.get("subject1", 0))  # 低于100
        subject2 = int(request.data.get("subject2", 0))  # 高于100
        total = int(request.data.get("total", 0))  # 总分

        if subject not in range(0, 12):
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "参数错误",
                             }, status=status.HTTP_200_OK)

        country_line = CountryLine.objects.filter(year=int(datetime.date.today().year), subject=subject).first()
        if country_line is None:
            CountryLine.objects.create(passsubject1=subject1, total=total, passsubject2=subject2, subject=subject)
        else:
            country_line.passsubject1 = subject1
            country_line.passsubject2 = subject2
            country_line.total = total
            country_line.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)


class PostgraduateViewset(viewsets.GenericViewSet):
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    # 研究生招生逻辑
    def create(self, request, *args, **kwargs):
        """上传所有学生名单"""
        file = request.FILES.get('file')

        try:
            with open("media/upload/postgraduate/firstexam/" + "考生电子档案.zip", 'wb+') as destination:
                for line in file.chunks():
                    destination.write(line)
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "上传错误",
                             }, status=status.HTTP_200_OK)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """研究生招生"""
        # 将原来的删除
        Postgraduate.objects.all().delete()

        students = postgraduate_recruit()

        # 获取国家分数线
        countrylines = CountryLine.objects.filter(year=int(datetime.date.today().year))

        # 将学生信息存入mongo
        for student in students:
            # 看学生报的科目
            major = Major.objects.filter(type=1, code=student["want_expectation"]).first()

            # 这个科目的国家线
            countryline = countrylines.filter(subject=major.subject).first()

            # 过线的
            if student["politics"] > countryline.passsubject1 and student["english"] > countryline.passsubject1 and \
                    student["speciality_subject"] > countryline.passsubject2 and student[
                "base_subject"] > countryline.passsubject2 and student["total"] > countryline.total:
                student["is_pass"] = True
                student["expectation"] = major.code

        pass_students = {}
        for student in students:
            if student["is_pass"] is True:
                if pass_students.get(student["expectation"]) is None:
                    pass_students[student["expectation"]] = [student]
                else:
                    pass_students[student["expectation"]].append(student)

            Postgraduate.objects.create(**student)

        result = {}
        for major in pass_students.keys():
            result[major] = []
            for pass_student in pass_students[major]:
                result[major].append(PostgraduateStudentSerializer(instance=pass_student).data)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": result,
                         }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """每个院下载过线学生名单"""
        """获取招生excle名单"""
        id = kwargs.get("pk")  # 院的id
        try:
            college = College.objects.get(id=id)
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到学院",
                             }, status=status.HTTP_200_OK)

        # 该学院的所有专业
        majors = college.majors.filter(type=1).all()

        record = []

        for major in majors:
            students = Postgraduate.objects.filter(is_pass=True, expectation=major.code).all().order_by("-total")
            for student in students:
                record.append((student.name, student.examcode, student.idcard, student.total, student.politics,
                               student.english, student.base_subject, student.speciality_subject, student.teacher,
                               student.research_interests, major.name, college.name))

        # 表头
        excle_head = ["学生姓名", "准考证号", "身份证", "初试总分", "政治分数", "英语分数", "基础课分数", "专业课分数", "导师", "研究方向", "专业名", "学院"]

        # 写入数据到excel中
        ret = wite_to_excel(college.name + "初试名单", excle_head, record)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": ret,
                         }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """每个院上传录取后的名单"""
        file = request.FILES.get('file')
        college_id = int(kwargs.get("pk"))

        try:
            college = College.objects.get(id=college_id)
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该院",
                             }, status=status.HTTP_200_OK)

        postgraduate_recruit = PostgraduateRecruit.objects.filter(college=college,
                                                                  year=int(datetime.date.today().year)).first()
        if postgraduate_recruit is None:
            PostgraduateRecruit.objects.create(college=college, firstexam=file)
        else:
            postgraduate_recruit.firstexam = file
            postgraduate_recruit.save()

        pass_students = read_to_excle(postgraduate_recruit.firstexam.path)

        for student in pass_students:
            Postgraduate.objects.filter(examcode=student).update(passfirstexam=True)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)


class PostgraduateRecruitViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    # 研究生招生计划逻辑
    serializer_class = PostgraduateRecruitSerializer
    pagination_class = P1
    queryset = PostgraduateRecruit.objects.all().order_by("-year")

    # 过滤器
    filter_backends = (DjangoFilterBackend,)
    # 如果要允许对某些字段进行过滤，可以使用filter_fields属性。
    filter_fields = ('year', "college")

    def create(self, request, *args, **kwargs):
        """创建或跟新复试计划时间"""

        serializer = PostgraduateSecondExamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            college = College.objects.get(id=data["college"])
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该学院",
                             }, status=status.HTTP_200_OK)

        postgraduate_recruit = PostgraduateRecruit.objects.filter(college=college,
                                                                  year=int(datetime.date.today().year)).first()
        if postgraduate_recruit is None:
            PostgraduateRecruit.objects.create(college=college, secondexamaddress=data["address"],
                                               secondexamtime=data["time"])
        else:
            postgraduate_recruit.secondexamaddress = data["address"]
            postgraduate_recruit.secondexamtime = data["time"]
            postgraduate_recruit.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """上传复试通过名单"""
        file = request.FILES.get('file')
        college_id = int(kwargs.get("pk"))

        try:
            college = College.objects.get(id=college_id)
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该院",
                             }, status=status.HTTP_200_OK)

        postgraduate_recruit = PostgraduateRecruit.objects.filter(college=college,
                                                                  year=int(datetime.date.today().year)).first()
        if postgraduate_recruit is None:
            PostgraduateRecruit.objects.create(college=college, secondexam=file)
        else:
            postgraduate_recruit.secondexam = file
            postgraduate_recruit.save()

        pass_students = read_to_excle(postgraduate_recruit.secondexam.path)

        for student in pass_students:
            Postgraduate.objects.filter(examcode=student).update(passsecondexam=True)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)


class SpecialCheckViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """专插本审核逻辑"""
    serializer_class = SpecialCheckSerializer
    pagination_class = P1
    queryset = SpecialCheckStudent.objects.all()

    # 过滤器
    filter_backends = (DjangoFilterBackend,)
    # 如果要允许对某些字段进行过滤，可以使用filter_fields属性。
    filter_fields = ('is_pass',)
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        """上传所有学生考生名单"""
        file = request.FILES.get('file')

        try:
            with open("media/upload/SpecialStudent/" + "考生电子档案.zip", 'wb+') as destination:
                for line in file.chunks():
                    destination.write(line)
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "上传错误",
                             }, status=status.HTTP_200_OK)

        data = special_recriit()

        for student in data:
            SpecialCheckStudent.objects.create(**student)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": data,
                         }, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        """审核"""
        student_id = kwargs.get("pk", 0)
        ispass = request.data.get("ispass", "True")

        if ispass not in ["True", "False"]:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该考生",
                             }, status=status.HTTP_200_OK)

        try:
            student = SpecialCheckStudent.objects.get(id=student_id)
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该考生",
                             }, status=status.HTTP_200_OK)

        student.is_pass = bool(ispass)
        student.save()
        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """获取eccle和查看某个人"""
        student_id = kwargs.get("pk", 0)  # 0表示获取表格

        if int(student_id) == 0:  # 下载excle
            # 表头
            excle_head = ["学生姓名", "身份证", "手机号"]

            students = SpecialCheckStudent.objects.filter(is_pass=True).all()
            record = []
            for student in students:
                record.append((student.name, student.idcard, student.phone))

            # 写入数据到excel中
            ret = wite_to_excel("审核通过名单", excle_head, record)

            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": ret,
                             }, status=status.HTTP_200_OK)

        try:
            student = SpecialCheckStudent.objects.get(id=student_id)
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "找不到该考生",
                             }, status=status.HTTP_200_OK)

        data = SpecialCheckSerializer(instance=student).data

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": data,
                         }, status=status.HTTP_200_OK)


class SpecialMajorViewset(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin,
                          mixins.RetrieveModelMixin):
    """专插本招生计划"""
    serializer_class = SpecialReciuitSerializer
    pagination_class = P1
    queryset = SpecialRecruit.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication)
    permission_classes = (IsAuthenticated,)

    # 过滤器
    filter_backends = (DjangoFilterBackend,)
    # 如果要允许对某些字段进行过滤，可以使用filter_fields属性。
    filter_fields = ('year', "major")

    def update(self, request, *args, **kwargs):
        """输入学院招生人数"""
        # 招生人数
        people_num = request.data.get("people_num", 0)

        id = kwargs.get("pk", 0)  # 专业id

        try:
            major = Major.objects.get(id=int(id))
        except Exception as e:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "没有该专业",
                             }, status=status.HTTP_200_OK)

        want_recruit = SpecialRecruit.objects.filter(major=major, year=int(datetime.date.today().year)).first()
        if want_recruit is None:
            SpecialRecruit.objects.create(people_num=people_num, major=major)
        else:
            want_recruit.people_num = people_num
            want_recruit.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)


class SpecialRecruitrViewset(viewsets.GenericViewSet):
    """专插本招生逻辑"""

    def create(self, request, *args, **kwargs):
        """上传考生名单"""
        file = request.FILES.get('file')

        try:
            with open("media/upload/SpecialStudent/exam/" + "考生电子档案.zip", 'wb+') as destination:
                for line in file.chunks():
                    destination.write(line)
        except Exception as e:
            print(e)
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "上传错误",
                             }, status=status.HTTP_200_OK)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """招生"""
        # 将原来的删除
        SpecialStudent.objects.all().delete()

        students = special_examrecriit()

        # 获取学校所有专业
        majors = Major.objects.filter(type=0).all()

        for student in students:
            SpecialStudent.objects.create(**student)

        # 按每个专业进行招生
        for major in majors:
            wantrecruit = major.specialrecruit.filter(year=int(datetime.date.today().year)).first()
            if wantrecruit != None:
                count = 0
                students = SpecialStudent.objects.filter(want_expectation=major.code).all().order_by("-total")
                for student in students:
                    if count >= wantrecruit.people_num:
                        wantrecruit.is_ok = True
                        wantrecruit.save()
                        break
                    student.is_pass = True
                    student.save()

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": [],
                         }, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """获取学院招生情况excle表"""

        file = int(kwargs.get("pk"))  # 是否excle返回 0 否 1 是

        # 该学院的所有专业
        majors = Major.objects.filter(type=0).all()

        record = []
        pass_students_dict = {}
        for major in majors:
            students = SpecialStudent.objects.filter(is_pass=True, want_expectation=major.code).all().order_by("-total")
            for student in students:
                record.append(
                    (student.name, student.examcode, student.total, major.name, major.code, major.college.name))
                if pass_students_dict.get(major.code) is None:
                    pass_students_dict[major.code] = []
                pass_students_dict[major.code].append(
                    {"学生姓名": student.name, "考生号": student.examcode, "总分": student.total,
                     "专业名": major.name, "专业代码": major.code, "学院": major.college.name})

        if file == 0:
            ret = pass_students_dict
        else:
            # 表头
            excle_head = ["学生姓名", "准考证号", "总分", "专业名", "专业代号", "学院"]

            # 写入数据到excel中
            ret = wite_to_excel("专插本考试通过", excle_head, record)

        return Response({"status_code": status.HTTP_200_OK,
                         "message": "ok",
                         "results": ret,
                         }, status=status.HTTP_200_OK)


class PassCollegeViewset(APIView):
    """用户查看是否通过考试"""

    def post(self, request, *args, **kwargs):
        idcard = request.data.get("idcard", 0)
        examcode = request.data.get("examcode", 0)

        student = CollegeStudent.objects.filter(idcard=idcard, examcode=examcode).first()

        if student == None:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "考生不存在",
                             }, status=status.HTTP_200_OK)
        elif student.is_pass == True:
            major = Major.objects.filter(code=student.expectation).first()
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": {
                                 "name": student.name,
                                 "expectation": student.expectation,
                                 "subject": major.name,
                                 "college": major.college.name
                             },
                             }, status=status.HTTP_200_OK)
        else:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "不通过",
                             }, status=status.HTTP_200_OK)


class PassSpecialViewset(APIView):
    """用户查看是否通过考试"""

    def post(self, request, *args, **kwargs):
        idcard = request.data.get("idcard", 0)
        examcode = request.data.get("examcode", 0)

        student = SpecialStudent.objects.filter(idcard=idcard, examcode=examcode, is_pass=True).first()

        if student == None:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "考生不存在",
                             }, status=status.HTTP_200_OK)
        elif student.is_pass == True:
            major = Major.objects.filter(code=student.want_expectation).first()
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": {
                                 "name": student.name,
                                 "expectation": student.want_expectation,
                                 "subject": major.name,
                                 "college": major.college.name
                             },
                             }, status=status.HTTP_200_OK)
        else:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "不通过",
                             }, status=status.HTTP_200_OK)


class PassPostgraduateViewset(APIView):
    """用户查看是否通过考试"""

    def post(self, request, *args, **kwargs):
        """初试"""
        idcard = request.data.get("idcard", 0)
        examcode = request.data.get("examcode", 0)

        student = Postgraduate.objects.filter(idcard=idcard, examcode=examcode).first()

        if student == None:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "考生不存在",
                             }, status=status.HTTP_200_OK)
        elif student.passfirstexam == True:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "通过",
                             }, status=status.HTTP_200_OK)
        else:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "不通过",
                             }, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """复试"""
        idcard = request.data.get("idcard", 0)
        examcode = request.data.get("examcode", 0)

        student = Postgraduate.objects.filter(idcard=idcard, examcode=examcode).first()

        if student == None:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "考生不存在",
                             }, status=status.HTTP_200_OK)
        elif student.passsecondexam == True:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "通过",
                             }, status=status.HTTP_200_OK)
        else:
            return Response({"status_code": status.HTTP_200_OK,
                             "message": "ok",
                             "results": "不通过",
                             }, status=status.HTTP_200_OK)
