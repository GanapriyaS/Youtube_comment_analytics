from automation_task import task_automation
from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import CronSchedule


youtube_videos = Deployment.build_from_flow(
    flow=task_automation,
    name="refresh_every_hour", 
    version=1, 
    work_queue_name="alerts",
    schedule=(CronSchedule(cron="*/5  * * * *", timezone="Asia/Kolkata")),
    # schedule=(CronSchedule(cron="0 * * * *", timezone="Asia/Kolkata")),

)


if __name__ == "__main__":
    youtube_videos.apply()
