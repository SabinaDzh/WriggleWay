"""Вызываем из библиотеки random модули randint и choice."""
from random import choice, randint

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


class GameObject:
    """
    Базовый класс игры.
    Он содержит общие атрибуты игровых объектов.
    """

    def __init__(self, bg_color=None, fg_color=None):
        """
        Инициализирует базовые атрибуты объекта,
        такие как его позиция и цвет.
        """
        self.body_color = bg_color
        self.figure_color = fg_color
        self.position = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]

    def draw(self):
        """
        Заготовка метода для отрисовки
        объекта на игровом поле.
        """


class Apple(GameObject):
    """
    Класс описывающий яблоко и действия с ним.
    Яблоко должно отображаться в случайных клетках игрового поля.
    """

    def __init__(self, bg_color=None, fg_color=None):
        super().__init__(bg_color, fg_color)
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def draw(self):
        """Метод для отрисовки объекта на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )


class Snake(GameObject):
    """
    Класс описывающий змейку и её поведение.
    Этот класс управляет её движением, отрисовкой,
    а также обрабатывает действия пользователя.
    """

    def __init__(self, bg_color=None, fg_color=None):
        super().__init__(bg_color, fg_color)
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.length = 1
        self.body_color = SNAKE_COLOR

    def draw(self):
        """Метод для отрисовки объекта на игровом поле."""
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        start_direction = [UP, DOWN, LEFT, RIGHT]
        self.last = None
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice(start_direction)

    def get_head_position(self):
        """
        Возвращает позицию головы змейки
        (первый элемент в списке positions).
        """
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
            first_elem_dx = SCREEN_WIDTH - GRID_SIZE
        elif first_elem_dx >= SCREEN_WIDTH:
            first_elem_dx = 0

        if first_elem_dy < 0:
            first_elem_dy = SCREEN_HEIGHT - GRID_SIZE
        elif first_elem_dy >= SCREEN_HEIGHT:
            first_elem_dy = 0

        if self.length <= len(self.positions):
            self.positions.pop()

        self.positions.insert(0, (first_elem_dx, first_elem_dy))

        if (first_elem_dx, first_elem_dy) in self.positions[2:]:
            return self.reset()


def main():
    """Основной цикл игры."""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(10)

        handle_keys(snake)

        head_position = snake.get_head_position()

        if head_position == apple.position:
            snake.length += 1
            apple.randomize_position()

        snake.update_direction()
        snake.move()

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
