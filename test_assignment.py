import unittest

from assignment import DatesParser
from pl_translation import pl_translation


class TestDatesParser(unittest.TestCase):
    """Test data returned from DatesParser class."""
    dp = DatesParser()
    current_datetime = '2022-06-20 16:55:21'

    def test_delta(self):
        self.assertEqual(self.dp.delta(event_datetime='2022-06-20 16:55:21', current_datetime=self.current_datetime),
                         {}, msg='Method should return empty dict in extreme case when time delta equals 0.')
        self.assertEqual(self.dp.delta(event_datetime='2023-06-20 16:55:21',
                                       current_datetime=self.current_datetime)['years'],
                         1, msg='Method should acknowledge year differences.')
        self.assertEqual(self.dp.delta(event_datetime='2022-07-20 16:55:21',
                                       current_datetime=self.current_datetime)['months'],
                         1, msg='Method should acknowledge month differences.')
        self.assertEqual(self.dp.delta(event_datetime='2022-06-21 02:55',
                                       current_datetime=self.current_datetime)['days_delta'],
                         1, msg="Method should acknowledge days-deltas.")


class TestPLTranslation(unittest.TestCase):
    """Test pl_translation."""
    dp = DatesParser()
    current_datetime = '2022-06-16 16:55:30'

    def test_pl_translation(self):
        """Test cases showed on GitHub repo."""
        event_datetime = '2022-06-17 15:20'
        data = self.dp.delta(event_datetime=event_datetime, current_datetime=self.current_datetime)
        self.assertEqual(pl_translation(data=data), 'Jutro o 15:20.')

        event_datetime = '2022-06-16 22:08:43'
        data = self.dp.delta(event_datetime=event_datetime, current_datetime=self.current_datetime)
        self.assertEqual(pl_translation(data=data), 'Za 5 godzin i 13 minut.')

        event_datetime = '2022-06-20 14:00'
        data = self.dp.delta(event_datetime=event_datetime, current_datetime=self.current_datetime)
        self.assertEqual(pl_translation(data=data), 'W przyszły poniedziałek o 14:00.')

        event_datetime = '2022-06-14 20:00'
        data = self.dp.delta(event_datetime=event_datetime, current_datetime=self.current_datetime)
        self.assertEqual(pl_translation(data=data), 'Przedwczoraj o 20:00.')

        event_datetime = '2022-07-19 21:55:30'
        data = self.dp.delta(event_datetime=event_datetime, current_datetime=self.current_datetime)
        self.assertEqual(pl_translation(data=data), 'Za miesiąc, 3 dni i 5 godzin.')


if __name__ == '__main__':
    unittest.main()
