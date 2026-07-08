from typing import List

from app.utils.enums.car_category import CarCategory


class CarService:

    def get_categories(self) -> List[str]:
        return [category.value for category in CarCategory]
