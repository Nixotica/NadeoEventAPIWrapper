from datetime import datetime, tzinfo
import unittest

import pytz

from src.nadeo_event_api.utils import dt_standardize


class TestUtils(unittest.TestCase):
    def test_dt_standardize_naive_utc_equals_tzaware_utc(self):
        naive_utc = datetime(year=1999, month=11, day=17, hour=12)
        aware_utc = datetime(year=1999, month=11, day=17, hour=12, tzinfo=pytz.utc)
        self.assertEqual(dt_standardize(naive_utc), dt_standardize(aware_utc))

    def test_dt_standardize_naive_utc_equals_gmt(self):
        gmt_time = datetime(
            year=1999, month=11, day=17, hour=12, tzinfo=pytz.timezone("GMT")
        )
        naive_utc = datetime(year=1999, month=11, day=17, hour=12)
        self.assertEqual(dt_standardize(naive_utc), dt_standardize(gmt_time))

    def test_dt_standardize_pst_converts_to_utc(self):
        pst_time = pytz.timezone("US/Pacific").localize(
            datetime(year=1999, month=11, day=17, hour=12)
        )
        naive_utc = datetime(year=1999, month=11, day=17, hour=20)
        self.assertEqual(dt_standardize(naive_utc), dt_standardize(pst_time))
