from datetime import timezone

from apscheduler.schedulers.background import BackgroundScheduler

from src.tasks.update_stations_by_ids import update_stations_by_ids


def main() -> None:
    scheduler = BackgroundScheduler(timezone=timezone.utc)
    scheduler.add_job(
        update_stations_by_ids,
        trigger='cron',
        day_of_week='*',
        hour=7,
        minute=0
    )
    scheduler.start()


if __name__ == '__main__':
    main()
