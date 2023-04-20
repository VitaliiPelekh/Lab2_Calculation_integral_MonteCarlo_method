import numpy as np
import scipy.special
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


# Точне значення інтегралу від основної функції
def exact_main_integral(a, b):
    return scipy.integrate.quad(main_function, a, b)


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
    a = 1
    b = 2
    n = 10000

    # Тестовий приклад
    test_integral, points_x, points_y, points_color = monte_carlo_integration(a, b, n, mode='test')
    print(f"Тестовий інтеграл: {test_integral}")

    result_exact_value1 = exact_test_integral(a, b)
    abs_error1 = abs(result_exact_value1 - test_integral)
    rel_error1 = abs_error1 / result_exact_value1
    print(f"Абсолютна похибка test: {abs_error1}")
    print(f"Відносна похибка test: {rel_error1}")

    plot_result(a, b, points_x, points_y, points_color, mode='test')

    # Основна задача
    a_main = 1
    b_main = 2
    main_integral, points_x_main, points_y_main, points_color_main = monte_carlo_integration(a_main, b_main, n, mode='main')
    print(f"Основний інтеграл: {main_integral}")

    result_exact_value2 = exact_main_integral(a_main, b_main)[0]
    abs_error2 = abs(result_exact_value2 - main_integral)
    rel_error2 = abs_error2 / result_exact_value2
    print(f"Абсолютна похибка main: {abs_error2}")
    print(f"Відносна похибка main: {rel_error2}")

    plot_result(a_main, b_main, points_x_main, points_y_main, points_color_main, mode='main')

