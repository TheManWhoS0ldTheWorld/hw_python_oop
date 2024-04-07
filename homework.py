import typing
class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; \n' 
                f'Длительность: {self.duration} ч.; \n'
                f'Дистанция: {self.distance} км; \n'
                f'Ср. скорость - {self.speed} км/ч; \n'
                f'Калории - {self.calories}.')

class Training:
    """Базовый класс тренировки."""
    M_IN_KM: float = 1000
    LEN_STEP: float = 0.65
    M_IN_H: float = 60
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP) / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )

class Running(Training):
    """Тренировка: бег."""
    COEF_FOR_FIRST_RUN = int = 18
    COEF_FOR_SECOND_RUN = float = 1.79

    def get_spent_calories(self) -> float:
        return (((self.COEF_FOR_FIRST_RUN * self.get_mean_speed()
                + self.COEF_FOR_SECOND_RUN) * self.weight)
                / self.M_IN_KM * self.M_IN_H * self.duration
                )
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CAL_WEIGHT_MULT: float = 0.035
    CAL_SPEED_MULT: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: float = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CAL_WEIGHT_MULT * self.weight
                 + (self.get_mean_speed() * self.KMH_IN_MSEC) ** 2
                 / (self.height / self.CM_IN_M)
                 * self.CAL_SPEED_MULT * self.weight)
                 * self.duration * self.M_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    COEF_FOR_FIRST_SWIM: float = 1.1
    COEF_FOR_SECOND_SWIM: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM
                / self.duration
                )
    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.COEF_FOR_FIRST_SWIM)
                * self.COEF_FOR_SECOND_SWIM
                * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    types_workout: typing.Dict[str, typing.Type[Training]] = {'SWM': Swimming,
                                                              'RUN': Running,
                                                              'WLK': SportsWalking
                                                              }
    if workout_type not in types_workout:
        raise ValueError('Такой тренировки не найдено')
    return types_workout[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

