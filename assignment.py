import calendar as cal
import datetime as dt

from pl_translation import pl_translation


class DatesParser:
    def delta(self, event_datetime: str, current_datetime=''):
        """Method calculating time difference between event and - by default - current time."""
        event_datetime = self.convert_to_datetime_format(event_datetime)
        if current_datetime:
            current_datetime = self.convert_to_datetime_format(current_datetime)
        else:
            current_datetime = dt.datetime.now()

        # Checking if event is yet to come by analyzing time delta.
        time_delta = int((event_datetime - current_datetime).total_seconds())
        if time_delta == 0:
            return {}
        is_event_in_the_future = True if time_delta > 0 else False

        # Split datetime for cleanliness of the code:
        event_date = event_datetime.date()
        current_date = current_datetime.date()
        event_time = event_datetime.time()
        current_time = current_datetime.time()

        if is_event_in_the_future:
            # reduce_bool variable to inform if 1 day should be deducted in 'extract_from_dates' method.
            hours, minutes, seconds, reduce_bool = self.extract_from_times(event_time, current_time)
            days_delta = self.get_days_delta(event_date, current_date)
            years, months, days = self.extract_from_dates(event_date, current_date, reduce_day_flag=reduce_bool)
        else:
            hours, minutes, seconds, reduce_bool = self.extract_from_times(current_time, event_time)
            days_delta = self.get_days_delta(current_date, event_date)
            years, months, days = self.extract_from_dates(current_date, event_date, reduce_day_flag=reduce_bool)

        weekday = self.get_weekday(event_date, current_date)

        return {
            'is_event_in_the_future': is_event_in_the_future,
            'event_time': event_time, 'event_date': event_date,
            'current_datetime': current_time, 'current_date': current_date,
            'years': years, 'months': months, 'weeks': 0,
            'weekday': weekday, 'days_delta': days_delta,
            'days': days, 'hours': hours, 'minutes': minutes
        }

    @staticmethod
    def convert_to_datetime_format(time_):
        """Converts ISO str into datetime.datetime format."""
        try:
            return dt.datetime.fromisoformat(time_)
        except (ValueError, SyntaxError, TypeError):
            print('Incorrect input format!')
            quit()

    @staticmethod
    def extract_from_times(newer_date, older_date):
        """Extract data from datetime.time type params."""
        hours = newer_date.hour - older_date.hour
        minutes = newer_date.minute - older_date.minute
        seconds = newer_date.second - older_date.second
        reduce_day_flag = False

        if seconds < 0:
            seconds = 60 + seconds      # '+' since seconds has always negative value.
            minutes -= 1

        if minutes < 0:
            minutes = 60 + minutes      # Same case as comment above.
            hours -= 1

        if hours < 0:
            hours = 24 + hours
            reduce_day_flag = True

        return hours, minutes, seconds, reduce_day_flag

    @staticmethod
    def extract_from_dates(newer_date, older_date, reduce_day_flag=False):
        """Extract data from datetime.date type params."""
        years = newer_date.year - older_date.year
        months = newer_date.month - older_date.month
        days = newer_date.day - older_date.day

        if reduce_day_flag:
            days -= 1

        if days < 0:
            _, month_days = cal.monthrange(older_date.year, older_date.month)   # first value not useful thus not named.
            days = month_days + days    # '+' since days has always negative value.
            months -= 1

        if months < 0:
            months = 12 + months    # Same case as comment above.
            years -= 1

        return years, months, days

    @staticmethod
    def get_weekday(event_date, current_date):
        """Return weekday if dates are in 'neighboring' weeks."""
        current_week = current_date.isocalendar().week
        event_week = event_date.isocalendar().week

        if abs(current_week - event_week) == 1:
            return event_date.weekday()

        return None

    @staticmethod
    def get_days_delta(newer_date, older_date):
        """Return days-delta if it's not higher than 2"""
        delta = abs(newer_date - older_date)
        delta_days = delta.days

        return delta_days if delta_days in (1, 2) else None


if __name__ == '__main__':
    d = DatesParser()    # print(t.delta(event_datetime='2021-01-01 11:12:00', current_datetime=fake_now_time))
    print("Inputs below accept only ISO format (full date mandatory!) ex.: "
          "\n'YYYY-MM-DD HH:MM:SS'"
          "\n'YYYY-MM-DD HH:MM'"
          "\n'YYYY-MM-DD'")
    now = input("Leave empty for actual time or enter 'fake-now' time:\n")
    event = input("Enter event time:\n")

    data = d.delta(event_datetime=event, current_datetime=now)
    print(pl_translation(data=data))
