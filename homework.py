from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};\
 Длительность: {self.duration:.3f} ч.; Дистанция: {self.distance:.3f} км;\
 Ср. скорость: {self.speed:.3f} км/ч; Потрачено ккал: {self.calories:.3f}.')


@dataclass
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    M_IN_KM = 1000
    LEN_STEP = 0.65
    MIN_K = 60
    __name__ = str

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage((self.__class__.__name__),
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""
    RUN_K_1 = 18
    RUN_K_2 = 20

    def get_spent_calories(self) -> float:
        return ((self.RUN_K_1 * self.get_mean_speed()
                - self.RUN_K_2)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.MIN_K)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    WLK_K_1 = 0.035
    WLK_K_2 = 0.029

    def get_spent_calories(self) -> float:
        c_1 = self.WLK_K_1 * self.weight
        c_2 = ((self.get_mean_speed()**2 // self.height)
               * self.WLK_K_2
               * self.weight)
        return ((c_1 + c_2) * self.duration * self.MIN_K)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: float
    count_pool: float
    LEN_STEP = 1.38
    SWM_K_1 = 1.1
    SWM_K_2 = 2

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.SWM_K_1)
                * self.SWM_K_2
                * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_dict = {
        'RUN': Running,
        'SWM': Swimming,
        'WLK': SportsWalking}
    if workout_type not in workout_dict:
        raise KeyError('Неверный тип тренировки')
    if workout_type in workout_dict:
        workout = workout_dict.get(workout_type)
        return workout(*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
