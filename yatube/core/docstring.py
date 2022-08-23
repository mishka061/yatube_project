from typing import Callable, List

def test_sort(sorting_algorithm:
Callable[..., List[float]]) -> None:
    """ Тестируем алгоритм, сортирующий список по возрастанию."""
    # Напечатать имя функции
    print(f'Тестируем функции: {test_sort.__doc__}')

    sourse = [1,65]
    sorted = [65,1]
    assert sorting_algorithm(sourse) == sorted, (
        f'Алгоритм в {test_sort.__name__} работает неправильно '
        f'сo строкой "{sourse}" '
    )
    sourse = []
    result = []
    assert sorting_algorithm(sourse) == result, ('работает неправильно с пустой строкой')

    print(f'Тест для {test_sort.__name__} пройден')

#   spisok1 = '0','-3','-1'
#   result1 = '-1','-3','0'
#   assert sorting_algorithm(spisok) == result, (
#       f'Алгоритм в {sorting_algorithm.__name__} работает неправильно '
#       f'сo строкой "{spisok}" '
#   )
#   spisok = ''
#   result = ''
#   assert sorting_algorithm(spisok) == result, (
#       f'Алгоритм в {sorting_algorithm.__name__} работает'
#       f' неправильно с пустой строкой'
#   )

#   print(f'Тест для {sorting_algorithm.__name__} пройден')

test_sort(bubble_sort)
test_sort(timsort_sort)
test_sort(selection_sort)
test_sort(insertion_sort)
test_sort(merge_sort)
test_sort(heap_sort)
test_sort(stepa_sort)
test_sort(quick_sort)
test_sort(sus_sort)

