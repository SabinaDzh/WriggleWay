"""Вызываем из библиотеки random модули randint и choice."""
from random import choice, randint

import pygame as pg

# Инициализация PyGame:
pg.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTR = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """Базовый класс игры. Он содержит общие атрибуты игровых объектов."""

    def __init__(self, bg_color=None, fg_color=None):
        """
        Инициализирует базовые атрибуты объекта,
        такие как его позиция и цвет.
        """
        self.body_color = bg_color
        self.figure_color = fg_color
        self.position = (SCREEN_CENTR)

    def draw(self):
        """
        Заготовка метода для отрисовки
        объекта на игровом поле.
        """
        pass


class Apple(GameObject):
    """
    Класс описывающий яблоко и действия с ним.
    Яблоко должно отображаться в случайных клетках игрового поля.
    """
    def __init__(self, bg_color=APPLE_COLOR, fg_color=BORDER_COLOR):
        super().__init__(bg_color, fg_color)
        self.randomize_position([(SCREEN_CENTR)])

    def draw(self):
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, self.figure_color, rect, 1)

    def randomize_position(self, snake_positions):
        """
        Устанавливает случайное положение яблока на игровом поле.
        """
        while self.position in snake_positions:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )


class Snake(GameObject):
    """Класс описывающий змейку и её поведение.
       Этот класс управляет её движением, отрисовкой,
       а также обрабатывает действия пользователя.
    """

    def __init__(self, bg_color=SNAKE_COLOR, fg_color=BORDER_COLOR):
        super().__init__(bg_color, fg_color)
        self.next_direction = None
        self.reset()

    def draw(self):
        """Метод для отрисовки объекта на игровом поле."""
        for position in self.positions:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, self.figure_color, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, self.figure_color, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает змейку в начальное состояние
            после столкновения с собой."""
        start_direction = [UP, DOWN, LEFT, RIGHT]
        self.last = None
        self.length = 1
        self.positions = [(SCREEN_CENTR)]
        self.direction = choice(start_direction)

    def get_head_position(self):
        """Возвращает позицию головы змейки
        (первый элемент в списке positions)."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и
        удаляя последний элемент,
        если длина змейки не увеличилась.
        """
        first_elem_dx, first_elem_dy = self.get_head_position()
        dx, dy = self.direction
        first_elem_dx += dx * GRID_SIZE
        first_elem_dy += dy * GRID_SIZE

        if first_elem_dx < 0:
            first_elem_dx = (first_elem_dx + (dx * GRID_SIZE)) % SCREEN_WIDTH
        elif first_elem_dx >= SCREEN_WIDTH:
            first_elem_dx = 0
        elif first_elem_dy < 0:
            first_elem_dy = (first_elem_dy + (dy * GRID_SIZE)) % SCREEN_HEIGHT
        elif first_elem_dy >= SCREEN_HEIGHT:
            first_elem_dy = 0

        if self.length <= len(self.positions):
            self.positions.pop()

        self.positions.insert(0, (first_elem_dx, first_elem_dy))


def main():
    """Основной цикл игры."""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(5)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[2:]:
            snake.reset()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
