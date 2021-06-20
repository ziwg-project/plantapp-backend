from collections import namedtuple

from django_celery_beat.models import IntervalSchedule

from plantapp.backend.models import Reminder


class NotificationContentProvider:
    def __init__(self, serializer_data):
        self.serializer_data = serializer_data

    @property
    def title(self) -> str:
        """
        Return properly formatted notification title basing on Reminder class instance.
        """
        return f'{self.serializer_data.get("plant_fk").name}: {self.serializer_data.get("text")}'

    @property
    def body(self) -> str:
        """
        Return properly formatted notification body basing on Reminder class instance.
        """
        return f'Every {self.serializer_data.get("intrvl_num")} ' \
               f'{self.__get_intrvl_type_display_name(self.serializer_data.get("intrvl_type"))} ' \
               f'since {self.__formatted_date()}'

    def __formatted_date(self, date_format: str = "%Y-%m-%d %H:%M") -> str:
        """
        Return formatted date of Reminder instance base_tmstp attribute
        """
        return self.serializer_data.get("base_tmstp").strftime(date_format)

    @staticmethod
    def __get_intrvl_type_display_name(intrvl_type):
        """
        Return human readable form of Reminder's intrvl_type field
        """
        return dict(Reminder.INTRVL_OPTIONS).get(intrvl_type)


Schedule = namedtuple("Schedule", ['every', 'period'])


class ScheduleMapper:
    MAPPING = {
        'S': (IntervalSchedule.SECONDS, 1),
        'M': (IntervalSchedule.MINUTES, 1),
        'H': (IntervalSchedule.HOURS, 1),
        'D': (IntervalSchedule.DAYS, 1),
        'W': (IntervalSchedule.DAYS, 7),
        'm': (IntervalSchedule.DAYS, 30),
        'Y': (IntervalSchedule.DAYS, 365)
    }

    @staticmethod
    def to_celery_beat_schedule(intrvl_num: int, intrvl_type: str) -> Schedule:
        """
        Map Reminder schedule values to Celery Beat scheduling format
        """
        base_interval_type, multiplier = ScheduleMapper.MAPPING.get(intrvl_type)
        return Schedule(
            period=base_interval_type,
            every=intrvl_num * multiplier
        )
