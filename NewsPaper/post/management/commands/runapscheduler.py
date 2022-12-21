import logging
import warnings

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
import datetime

from post.models import Post
from category.models import Category
from NewsPaper.settings import BASE_URL


warnings.filterwarnings(
    "ignore",
    message="The localize method is no longer necessary, as this time zone supports the fold attribute",
)


logger = logging.getLogger(__name__)


def send_week_posts():
    for category in Category.objects.all():
        for user in category.subscribers.all():
            post_list = Post.objects.filter(time__gte=(
                datetime.datetime.today() - datetime.timedelta(days=7)), category=category)
            html_content = render_to_string('email_week.html', {
                                            'post_list': post_list, 'category': category.name, 'user': user.username,
                                            'base_url': BASE_URL})
            msg = EmailMultiAlternatives('Дайджест новостей за неделю', html_content,
                                         from_email='nbvwzbaotjrclrbea@gmx.com',
                                         to=[user.email])
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()
            except:
                continue


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_week_posts,
            trigger=CronTrigger(
                day_of_week="fri", hour="10", minute="00"
            ),
            id="send_week_posts",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'send_week_posts'."
        )

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.warning("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.warning("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
