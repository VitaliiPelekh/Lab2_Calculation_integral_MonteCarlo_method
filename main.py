import numpy as np
import matplotlib.pyplot as plt
import random


# Тестова функція
def test_function(x):
    return x**2  # Поліноміальна функція


# Основна функція
def main_function(x):
    return np.exp(x**2)


# Точне значення інтегралу від тестової функції
def exact_test_integral(a, b):
    return (b**3 / 3) - (a**3 / 3)


# Генерування випадкової точки
def generate_random_point(a, b, min_y, max_y):
    x = random.uniform(a, b)
    y = random.uniform(min_y, max_y)
    return x, y


# Точне значення підінтегральної функції в заданій точці
def exact_function_value(x, mode='test'):
    if mode == 'test':
        return test_function(x)
    elif mode == 'main':
        return main_function(x)
    else:
        raise ValueError("Invalid mode. Choose 'test' or 'main'.")


# Реалізація алгоритму Монте-Карло
def monte_carlo_integration(a, b, n, mode='test'):
    if mode not in ['test', 'main']:
        raise ValueError("Invalid mode. Choose 'test' or 'main'.")
    min_y = 0
    max_y = max(exact_function_value(a, mode), exact_function_value(b, mode))

    points_inside = 0
    total_points = 0
    points_x = []
    points_y = []
    points_color = []

    for _ in range(n):
        x, y = generate_random_point(a, b, min_y, max_y)
        if 0 <= y <= exact_function_value(x, mode):
            points_inside += 1
            points_color.append("green")
        else:
            points_color.append("red")

        total_points += 1
        points_x.append(x)
        points_y.append(y)

    ratio = points_inside / total_points
    integral_value = (b - a) * (max_y - min_y) * ratio

    return integral_value, points_x, points_y, points_color


# Візуалізація результату
def plot_result(a, b, points_x, points_y, points_color, mode='test'):
    X = np.linspace(a, b, 500)
    if mode == 'test':
        Y = test_function(X)
    elif mode == 'main':
        Y = main_function(X)
    else:
        raise ValueError("Invalid mode. Choose 'test' or 'main'.")

    plt.plot(X, Y, 'b-', linewidth=2)
    plt.scatter(points_x, points_y, c=points_color, marker='.')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Test') if mode == 'test' else plt.title('Main')
    plt.show()


if __name__ == '__main__':
    a = 2
    b = 3
    n = 1000

    # Тестовий приклад
    test_integral, points_x, points_y, points_color = monte_carlo_integration(a, b, n, mode='test')
    print(f"Тестовий інтеграл: {test_integral}")

    exact_value = exact_test_integral(a, b)
    abs_error = abs(exact_value - test_integral)
    rel_error = abs_error / exact_value
    print(f"Абсолютна похибка: {abs_error}")
    print(f"Відносна похибка: {rel_error}")

    plot_result(a, b, points_x, points_y, points_color, mode='test')

    # Основна задача
    a_main = 1
    b_main = 2
    main_integral, points_x_main, points_y_main, points_color_main = monte_carlo_integration(a_main, b_main, n, mode='main')
    print(f"Основний інтеграл: {main_integral}")

    plot_result(a_main, b_main, points_x_main, points_y_main, points_color_main, mode='main')

