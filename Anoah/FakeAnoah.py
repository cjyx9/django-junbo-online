import json
from sys import argv

import requests

arg = argv
# example: python FakeAnoah.py 1765840(uid) headpic

class User():
    def __init__(self, user_id):
        """初始化"""
    #! 用户的uid start:
        self.user_id = user_id
        #! 用户的uid end

    #! 截取优学派server的时间 start:
        time_api = "http://e.anoah.com/api_dist/?q=json/ebag/System/getServerTime&info={}"
        time_json = json.loads(requests.get(time_api).text)
        self.server_time = str(time_json["recordset"]["system_time"])
        #! 截取优学派server的时间 end
        
    #! 用户信息 start:
        info_api = "https://e.anoah.com/api/?q=json/ebag/user/score/score_rank&info={\"userid\":%s}&pmatsemit=%s" % (self.user_id,self.server_time)
        user_info = json.loads(requests.get(info_api).text)
        self.user_name = user_info["recordset"]["real_name"]
        # 用户名
        self.user_head_img = "https://static.anoah.com/" + user_info["recordset"]["avatar"]
        # 头像url
        self.uesr_point = user_info["recordset"]["points_count"]
        # 积分数量
        class_api = "https://e.anoah.com/api/?q=json/ebag5/User/getUserClasses&info={\"userid\":%s}&pmatsemit=%s" % (self.user_id,self.server_time)
        ClassScore = []
        for id in json.loads(requests.get(class_api).text)["recordset"]:
            ClassScore.append(str(id["class_id"]))
        self.user_class_ids = ",".join(ClassScore)
        #! 用户信息 end

    #! 获取所有学科 start:
        subject_api = "https://www.anoah.com/api/?q=json/ebag5/Classes/getClassSubject&info={\"class_id\":\"" + self.user_class_ids + "\"}"
        subject_info_list = requests.get(subject_api).json()["recordset"]
        self.subject_json = {}
        for subject in subject_info_list:
            self.subject_json[subject["subject_name"]] = subject["edu_subject_id"]
        #! 获取所有学科 end

    def save_head(self):
        """保存头像"""
        pic = requests.get(self.user_head_img.replace(".jpg","_private.jpg"))
        with open(r"Temp\FacePrivate.jpg","wb+") as f:
            f.write(pic.content)
        print(self.user_name + '的头像已保存到Temp文件夹')

    def get_undo_homework_page(self):
        """获取未完成的作业总页数"""
        homework_api = 'https://www.anoah.com/api/?q=json/ebag5/Homework/readHomework&info={"user_id":"' + self.user_id + '","type":1,"page":1,"class_id":"' + self.user_class_ids + '"}'
        homework_count = json.loads(requests.get(homework_api).text)['recordset']['homework_count']
        # 发送get请求
        if homework_count <= 10:
            return 1
        else:
            from math import ceil
            return ceil(homework_count / 10)

    def get_undo_homework(self, page_num):
        """获取未完成的作业"""
        homework_api = 'https://www.anoah.com/api/?q=json/ebag5/Homework/readHomework&info={"user_id":"' + self.user_id + '","type":1,"page":' + str(page_num) + ',"class_id":"' + self.user_class_ids + '"}'
        homework_json = json.loads(requests.get(homework_api).text)['recordset']
        # 发送get请求
        return homework_json

    def analysis_grade(self):
        """等级评估(仅显示已批改)"""
        return_list = []
        for i in self.subject_json:
            item = {}
            grade_api = "http://e.anoah.com/api/?q=json/ebag5/Statistics/getStudentScoreInfo&info={\"user_id\":%s,\"class_id\":\"%s\",\"type\":0,\"subject_id\":%s,\"pagesize\":1,\"page\":1,\"start_date\":\"\",\"end_date\":\"\"}&pmatsemit=%s" % (self.user_id,self.user_class_ids,self.subject_json[i],self.server_time)
            grade_json = json.loads(requests.get(grade_api).text)
            if grade_json["recordset"]:
                item['status'] = True
                item['subject'] = i
                # 科目名称
                item['time'] = grade_json["recordset"][0]["publish_time"]
                # 时间
                item['title'] = grade_json["recordset"][0]["title"]
                # 标题
                item['result'] = round(grade_json["recordset"][0]["student_right_rate"]*100,2)
                # 个人分数
                item['classr'] = round(grade_json["recordset"][0]["class_right_rate"]*100,2)
                # 班级平均
                if item['result'] >= item['classr']:
                    item['contrast'] = 'up'
                    # 高于或等于班平
                else:
                    item['contrast'] = 'down'
                    # 低于班平
            else:
                item['status'] = False
                item['subject'] = i
            return_list.append(item)
        return return_list

    def get_homeworks(self,subject_type):
        """
        获取所有作业
        subject_type: 单学科名 e.g.语文
        """
        if subject_type in self.subject_json:
            homeworks_api = "http://api2.anoah.com/jwt/homework/publish/getListForStudent?user_id=%s&status=-1&subject_id=%s&class_id=%s&from_date=&to_date=&page=1&per_page=-1&pmatsemit=%s" % (self.user_id,self.subject_json[subject_type],self.user_class_ids,self.server_time)
            homeworks_list = json.loads(requests.get(homeworks_api).text)['recordset']['lists']
            return_list = []
            for h in homeworks_list:
                item = {}
                item['publish_id'] = h['course_hour_publish_id']
                item['title'] = h['title']
                item['teacher_name'] = h['teacher_name']
                item['start_time'] = h['start_time']
                item['end_time'] = h['deadline']
                if h['has_comment'] == 1:
                    item['comment'] = h['comment']
                return_list.append(item)
            return return_list
        else:
            print("Error:没有此科目!")
            return 0

    def get_answer(self):
        """
        TODO 就是不准备做
        """
        print("想要答案?可以!50块!👍")

    def get_message(self):
        """获取信息"""
        message_api = 'https://www.anoah.com/api/?q=json/ebag/Message/getList&info={"userid":"' + self.user_id + '","page":1,"limit":800}'
        message_list = json.loads(requests.get(message_api).text)['recordset']['list']
        return_list = []
        for message in message_list:
            item = {}
            item['title'] = message['title']
            item['time'] = message['push_time']
            item['text'] = message['content']
            item['teacher'] = message['sender']
            item['id'] = message['message_id']
            return_list.append(item)
        return return_list

    def del_message(self, id):
        """删除信息"""
        if not isinstance(id, list):
            id = [id]
        del_api = 'https://www.anoah.com/api/?q=json/ebag/Message/deleteAll&info={"message_id":' + str(id).replace("'", '"') + ',"user_id":"' + self.user_id + '"}'
        del_json = requests.get(del_api).text
        return del_json

    def gen_image(self):
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        from bokeh.embed import components
        from bokeh.models import ColumnDataSource
        from bokeh.plotting import figure
        from bokeh.transform import dodge
        from bokeh.core.properties import value
        line = self.analysis_grade()
        xd = []
        yd = []
        ydt = []
        for i in line:
            if i['status'] and i['result']:
                xd.append(i['subject'])
                yd.append(i['result'])
                ydt.append(i['classr'])
        df = pd.DataFrame({'个人分数':yd,'班级平均':ydt}, index = xd)
        source = ColumnDataSource(data=df) 
        p = figure(x_range=xd, y_range=(0, 100), plot_height=350, title="分数统计",tools="")
        p.vbar(x=dodge('index', -0.25, range=p.x_range), top='个人分数', width=0.2, source=source,color="#c9d9d3", legend=value("个人分数"))
        p.vbar(x=dodge('index',  0.0,  range=p.x_range), top='班级平均', width=0.2, source=source,color="#718dbf", legend=value("班级平均"))
        p.xgrid.grid_line_color = None
        p.legend.location = "top_left"
        p.legend.orientation = "horizontal"
        script, div = components(p)
        return script, div

user = User('1765841')
user.gen_image()