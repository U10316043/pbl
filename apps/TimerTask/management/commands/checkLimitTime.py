# _*_ coding:utf-8 _*_
from django.core.management.base import BaseCommand, CommandError
from django.core import mail
from pbl.settings import EMAIL_HOST_USER
from courses.models import CourseHomework,StudentHomework
from operation.models import UserCourse
from django.contrib.auth.models import User
from datetime import datetime
from threading import Timer





def send_email(email, hw_name, send_type="TimeIsUp"):
    
    email_title = ""
    email_body = ""
    if send_type == "TimeIsUp":
        connection = mail.get_connection()
        connection.open()
        emailList = []
        for emailaddress in email:
            print(emailaddress)
	    if emailaddress != "":
            	emailList.append(mail.EmailMessage(
                	'專題系統通知'+hw_name,
                	'繳交期限已到',
                	EMAIL_HOST_USER,
                	[str(emailaddress)],
                	connection=connection,
            	))
        connection.send_messages(emailList)
        connection.close()
        


def cLT(inc):
    all_hw = CourseHomework.objects.all()
    for hw in all_hw:
        if datetime.now() >= hw.limit_time and hw.deadline_token == '0':
            print(str(hw.limit_time)+"->"+hw.name+'繳交期限已到')
            hw.deadline_token = 1
            hw.save()
            shHasSubmit = StudentHomework.objects.all().filter(homework_id=hw.id).values_list('user_id', flat=True)
            theStudentInCourse = UserCourse.objects.all().filter(course_id=hw.course_id).values_list('user_id', flat=True)
            shNotSubmitList = set(theStudentInCourse)-set(shHasSubmit)
            shNotSubmitList = list(shNotSubmitList)
            shNotSubmitList = [int(item) for item in shNotSubmitList]
            theStudentNotSubmitEmail = []
            for person in shNotSubmitList:
                theStudentNotSubmitEmail.append(User.objects.get(id=person).email)
            send_email(theStudentNotSubmitEmail, hw.name, "TimeIsUp")
    t = Timer(inc, cLT, (inc,))
    t.start()

class Command(BaseCommand):
    help = 'this command is designed for check the homework deadline.'
    def handle(self, *args, **options):
        cLT(1)
