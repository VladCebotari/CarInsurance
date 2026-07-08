from datetime import date


class DateValidator:
    MIN_YEAR = 1900
    MAX_POLICY_YEAR = 2100

    @classmethod
    def ensure_date_not_in_future(
        cls,
        value: date,
        error: Exception,
    ) -> date:
        if value > date.today():
            raise error

        return value

    @classmethod
    def ensure_date_year_at_least(
        cls,
        value: date,
        min_year: int,
        error: Exception,
    ) -> date:
        if value.year < min_year:
            raise error

        return value

    @classmethod
    def ensure_date_year_between(
        cls,
        value: date,
        min_year: int,
        max_year: int,
        error: Exception,
    ) -> date:
        if not min_year <= value.year <= max_year:
            raise error

        return value

    @classmethod
    def ensure_year_between(
        cls,
        value: int,
        min_year: int,
        max_year: int,
        error: Exception,
    ) -> int:
        if not min_year <= value <= max_year:
            raise error

        return value

    @staticmethod
    def ensure_not_before_year(
        value: int,
        min_year: int,
        error: Exception,
    ) -> int:
        if value < min_year:
            raise error

        return value

    @staticmethod
    def ensure_end_date_not_before_start_date(
        start_date: date,
        end_date: date,
        error: Exception,
    ) -> None:
        if end_date < start_date:
            raise error
