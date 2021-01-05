from django.urls import path
from .views import *

admin_urls = AdminViewset.as_view({
    "get": "list",  # 显示管理员
    "post": "create",  # 增加管理员

})

# 超级管理员账号
admin_detail_urls = AdminViewset.as_view({
    "get": "retrieve",  # 显示一个管理员
    "delete": "destroy",  # 删除管理员
    "put": "update"  # 更新管理员信息
})

# 学院url
college_urls = CollegeViewset.as_view({
    "get": "list",  # 学院列表
    "post": "create",  # 创建学院

})
college_detail_urls = CollegeViewset.as_view({
    "get": "retrieve",  # 获取一个具体的学院
    "delete": "destroy",  # 删除学院
    "put": "update"  # 更新学院
})

# 专业url
major_urls = MajorViewset.as_view({
    "get": "list",  # 专业列表
    "post": "create",  # 创建专业

})
major_detail_urls = MajorViewset.as_view({
    "get": "retrieve",  # 一个专业
    "delete": "destroy",  # 删除专业
    "put": "update"  # 更新专业
})

# 本科招生
majorrecruit_detail_urls = MajorRecruitViewset.as_view({
    "put": "update"  # 用于输入本科每个专业招生人数
})
collegestudents_urls = CollegeStudentViewset.as_view({
    "post": "create", # 本科上传招生压缩包
    "get": "list",      # 进行本科生成招生逻辑
    'delete':'destory',  # 获取退档学生
})
collegestudents_detail_urls = CollegeStudentViewset.as_view({
    "get": "retrieve"   # 每个学院获取自己的招生通过excle名单
})

# 水平测试
level_urls = LevelViewset.as_view({
    "get": "list",    # 查看水平测试通过成绩
    "post": "create",  # 创建水平测试通过成绩

})
level_detail_urls = LevelViewset.as_view({
    "delete": "destroy",  # 删除水平测试通过成绩
    "put": "update"        # 修改水平测试通过成绩
})

# 滚动图片
pic_urls = PicViewset.as_view({
    "get": "list",  # 滚动图片列表
    "post": "create",  # 创建滚动图片

})
pic_detail_urls = PicViewset.as_view({
    "get": "retrieve",    # 查找图片
    "delete": "destroy",  # 删除滚动图片
    "put": "update"      # 发布图片
})

# 链接
link_urls = LinkViewset.as_view({
    "get": "list",    # 链接列表
    "post": "create",    # 创建链接

})
link_detail_urls = LinkViewset.as_view({
    "delete": "destroy",  # 删除链接
    "put": "update",       # 跟新链接
    "get": "retrieve",     # 链接详情
})


# 下载
download_urls = DownloadViewset.as_view({
    "get": "list",    # 下载列表
    "post": "create",    # 下载链接

})
download_detail_urls = DownloadViewset.as_view({
    "delete": "destroy",  # 下载链接
    "put": "update",       # 下载链接
    "get": "retrieve",     # 下载详情
})

# 关于我们
our_urls = OurViewset.as_view({
    "get": "list",       # 关于我们列表
    "post": "create",     # 创建关于我们


})
our_detail_urls = OurViewset.as_view({
    "get": "retrieve",      # 查找关于我们
    "delete": "destroy",    # 删除关于我们
    "put": "update"         # 修改关于我们
})

#  学校信息
schoolnews_urls = SchoolNewsViewset.as_view({
    "get": "list",          # 获取学校信息
    "post": "create",       # 修改或创建学校信息

})
schoolnews_detail_urls = SchoolNewsViewset.as_view({
    "get": "retrieve",      # 获取学校信息
    "delete": "destroy",    # 删除学校信息
})

# 信息公示
information1_urls = Information1Viewset.as_view({
    "get": "list",     # 信息公示列表
    "post": "create",  # 创建信息公示

})
information1_detail_urls = Information1Viewset.as_view({
    "get": "retrieve",     # 查询信息公示
    "delete": "destroy",   # 删除信息公示
    "put": "update"        # 更新信息公示
})

# 信息公告
information2_urls = Information2Viewset.as_view({
    "get": "list",      # 信息公告列表
    "post": "create",   # 创建信息公告

})
information2_detail_urls = Information2Viewset.as_view({
    "get": "retrieve",    # 查询信息公告
    "delete": "destroy",  # 删除信息公告
    "put": "update"       # 跟新信息公告
})

# 导师逻辑
teacher_urls = TeacherViewset.as_view({
    "get": "list",     # 导师列表
    "post": "create",  # 创建导师列表

})
teacher_detail_urls = TeacherViewset.as_view({
    "get": "retrieve",  # 查询导师
    "delete": "destroy", # 删除导师
    "put": "update"     # 跟新导师
})

# 本科招生指南
collegereciuit_news_urls = CollegeReciuitNewsViewset.as_view({
    "get": "list",    # 本科招生指南列表
    "post": "create",  # 创建指南

})
collegereciuit_news_detail_urls = CollegeReciuitNewsViewset.as_view({
    "get": "retrieve",   # 查询指南
    "delete": "destroy",  # 删除指南
    "put": "update"       # 更新指南
})

# 研究生招生指南
postgraduatereciuit_news_urls = PostgraduateReciuitNewsViewset.as_view({
    "get": "list",      # 研究生招生指南列表
    "post": "create",    # 创建研究生招生指南

})
postgraduatereciuit_news_detail_urls = PostgraduateReciuitNewsViewset.as_view({
    "get": "retrieve",    # 查询研究生招生指南
    "delete": "destroy",  # 删除研究生招生指南
    "put": "update"        # 跟新研究生招生指南
})

# 专插本招生指南
specialreciuit_news_urls = SpecialReciuitNewsViewset.as_view({
    "get": "list",    # 专插本招生指南列表
    "post": "create",  # 创建专插本招生指南

})
specialreciuit_news_detail_urls = SpecialReciuitNewsViewset.as_view({
    "get": "retrieve",    # 查询专插本招生指南
    "delete": "destroy",   # 删除专插本招生指南
    "put": "update"       # 更新专插本招生指南
})

# 历年录取
lastpass_urls = LastPassViewset.as_view({
    "get": "list",    # 历年录取列表
    "post": "create",  # 创建历年录取

})
lastpass_detail_urls = LastPassViewset.as_view({
    "get": "retrieve",   # 查找历年录取
    "delete": "destroy",  # 删除历年录取
    "put": "update"      # 跟新历年录取
})

# 研究生招生逻辑
postgraduate_urls = PostgraduateViewset.as_view({
    "get": "list",   # 研究生招生
    "post": "create",  # 上传所有学生名单

})
postgraduate_detail_urls = PostgraduateViewset.as_view({
    "get": "retrieve",    # 每个院下载初试过线学生名单
    "put": "update"      # 每个院上传初试录取后的名单
})

# 国家线逻辑
countryline_urls = CountryLineViewset.as_view({
    "post": "create",  # 创建或修改国家线
    "get": "list"     # 国家线列表
})

# 研究生招生计划
postgraduate_recruit_urls = PostgraduateRecruitViewset.as_view({
    "get": "list",      # 查看招生计划列表
    "post": "create",   # 创建或跟新复试计划时间

})
postgraduate_recruit_detail_urls = PostgraduateRecruitViewset.as_view({
    "get": "retrieve",    # 查看某个招生计划列表
    "put": "update"    # 上传复试通过名单
})

# 研究生初试和复试通过学生查询
postgraduate_pass_urls = PassPostgraduateViewset.as_view()

# 本科通过学生查询
college_pass_urls = PassCollegeViewset.as_view()

# 专插本通过学生查询
special_pass_urls = PassSpecialViewset.as_view()

# 专插本审核
specialstudent_check_urls = SpecialCheckViewset.as_view({
    "get": "list",     # 查看所有考生
    "post": "create", # 上传所有学生考生名单

})
specialstudent_check_detail_urls = SpecialCheckViewset.as_view({
    "get": "retrieve",  # 查看某个学生
    "put": "update"   # 审核
})

# 专插本专业计划
special_major_urls = SpecialMajorViewset.as_view({
    "get": "list",   # 查看所有计划
})
special_major_detail_urls = SpecialMajorViewset.as_view({
    "get": "retrieve",   # 查看某个计划
    "put": "update"   # 输入学院招生人数
})

# 专插本招生
special_recruit_urls = SpecialRecruitrViewset.as_view({
    "get": "list",   # 招生
    "post": "create", # 上传考生名单
})
special_recruit_detail_urls = SpecialRecruitrViewset.as_view({
    "get": "retrieve",  # 获取学院招生情况excle表
})

urlpatterns = [
    path("admin/", admin_urls),
    path("admin/<int:pk>/", admin_detail_urls),

    path("college/", college_urls),
    path("college/<int:pk>/", college_detail_urls),

    path("major/", major_urls),
    path("major/<int:pk>/", major_detail_urls),

    path("college/major/<int:pk>/", majorrecruit_detail_urls),

    path("college/recruit/", collegestudents_urls),
    path("college/recruit/<int:pk>/", collegestudents_detail_urls),

    path("college/level/", level_urls),
    path("college/level/<int:pk>", level_detail_urls),

    path("postgraduate/", postgraduate_urls),
    path("postgraduate/<int:pk>/", postgraduate_detail_urls),

    path("postgraduate/countryline/", countryline_urls),

    path("postgraduate/recruit/", postgraduate_recruit_urls),
    path("postgraduate/recruit/<int:pk>/", postgraduate_recruit_detail_urls),

    path("special/", specialstudent_check_urls),
    path("special/<int:pk>/", specialstudent_check_detail_urls),

    path("special/major/", special_major_urls),
    path("special/major/<int:pk>/", special_major_detail_urls),

    path("special/recruit/", special_recruit_urls),
    path("special/recruit/<int:pk>/", special_recruit_detail_urls),

    path("pic/", pic_urls),
    path("pic/<int:pk>/", pic_detail_urls),

    path("download/", download_urls),
    path("download/<int:pk>/", download_detail_urls),


    path("link/", link_urls),
    path("link/<int:pk>/", link_detail_urls),

    path("our/", our_urls),
    path("our/<int:pk>/", our_detail_urls),

    path("schoolnews/", schoolnews_urls),
    path("schoolnews/<int:pk>/", schoolnews_detail_urls),

    path("information1/", information1_urls),
    path("information1/<int:pk>/", information1_detail_urls),

    path("information2/", information2_urls),
    path("information2/<int:pk>/", information2_detail_urls),

    path("teacher/", teacher_urls),
    path("teacher/<int:pk>/", teacher_detail_urls),

    path("college/reciuitnews/", collegereciuit_news_urls),
    path("college/reciuitnews/<int:pk>/", collegereciuit_news_detail_urls),

    path("postgraduate/reciuitnews/", postgraduatereciuit_news_urls),
    path("postgraduate/reciuitnews/<int:pk>/", postgraduatereciuit_news_detail_urls),

    path("special/reciuitnews/", specialreciuit_news_urls),
    path("special/reciuitnews/<int:pk>/", specialreciuit_news_detail_urls),

    path("lastpass/", lastpass_urls),
    path("lastpass/<int:pk>/", lastpass_detail_urls),


    # 通过
    path("postgraduate/pass/", postgraduate_pass_urls),

    path("college/pass/", college_pass_urls),

    path("special/pass/", special_pass_urls),

]
