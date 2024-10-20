"""Завдання.
Маємо набір монет [50, 25, 10, 5, 2, 1]. 
Визначити оптимальний спосіб видачі решти покупцеві.
Написати дві функції для видачі решти з наведеного набору монет.

Функція жадібного алгоритму повинна приймати суму, яку потрібно видати покупцеві, 
і повертати словник із кількістю монет кожного номіналу, що використовуються для формування цієї суми. 
Наприклад, для суми 113 це буде словник {50: 2, 10: 1, 2: 1, 1: 1}. 
Алгоритм повинен бути жадібним, тобто спочатку вибирати найбільш доступні номінали монет.

Функція динамічного програмування також повинна приймати суму для видачі решти, 
але використовувати метод динамічного програмування, щоб знайти мінімальну кількість монет, 
необхідних для формування цієї суми. Функція повинна повертати словник 
із номіналами монет та їх кількістю. Наприклад, 
для суми 113 це буде словник {1: 1, 2: 1, 10: 1, 50: 2}

Порівняти ефективність жадібного алгоритму та алгоритму динамічного програмування, 
базуючись на часі їх виконання або О великому та звертаючи увагу на їхню продуктивність при великих сумах. 
Висвітліть, як вони справляються з великими сумами та чому один алгоритм 
може бути більш ефективним за інший у певних ситуаціях. Висновки додати у файл readme.md."""
import random
import timeit

def find_coins_greedy(coinz, total):
    """Функція жадібного алгоритму"""
    d = {}
    coinz.sort(reverse=True)

    for coin in coinz:
        while total>=coin:
            total-=coin
            d[coin]=1 if not d.get(coin) else d[coin]+1 
        if coin not in d:
            d[coin] =0
    return d


def find_min_coins(coinz, total):
    """Функція динамічного програмування"""
    coinz.sort()
    result = [total+1] * (total+1)
    coins_results = [[] for _ in range(total+1)]

    result[0] = 0

    for i in range(1, total+1):
        for coin in coinz:
            if i >= coin and result[i - coin] + 1 < result[i]:
                result[i] = result[i-coin] + 1
                coins_results[i] = coins_results[i-coin] + [coin]

    if result[total] == total+1:
        return []

    return coins_results[total]


def dp(func, coinz, total):
    """Функція для представлення результатів функції динамічного програмування у вигляді словнику, 
    де ключ - елемент вхідного списку ("номінал монет"), значення - їх кількість для формування цільового значення
    """
    d = {}
    res = func(coinz, total)
    for i in coinz:
        d[i] = 0
    for j in res:
        d[j]+=1

    return d

def total_val(fd: dict):
    """Допоміжна функція для підрахунку загальної вартості словника, отриманого для кожного з алгоритмів"""
    r = 0
    for k in fd:
        r+=k*fd[k]
    return r


random.seed(7)

#Перевірка роботи функцій
coins = [50, 25, 10, 5, 2, 1] 
coins1 = [50, 25, 10, 5, 2] #буде "неповний" результат, якщо в наборі не буде "1"
coin_change = 113
print(f"Greedy: {find_coins_greedy(coins, coin_change)}")
print(f"Dynamic: {dp(find_min_coins, coins, coin_change)}")

print(f"Greedy. Efficienty without option to add '1': {find_coins_greedy(coins1, coin_change)}")
print(f"Dynamic. Efficienty without option to add '1': {dp(find_min_coins, coins1, coin_change)}")


#Порівняння швидкостей алгоритмів
algs = {'greedy': [], 'dynamic': [], 'diff': []}
 
test_arr10 = [random.randint(1, 100) for _ in range(10)]
test_arr100 = [random.randint(1, 1000) for _ in range(100)]
test_arr1000 = [random.randint(1, 10000) for _ in range(1000)]
test_arr10000 = [random.randint(1, 100000) for _ in range(10000)]
test_arrs = (test_arr10, test_arr100, test_arr1000, test_arr10000)
n = 10

change = [213, 1432, 67910, 580024]

for arr in test_arrs:
    stp = """
import random
from __main__ import find_coins_greedy
from __main__ import find_min_coins
"""
    stmnt = f"""
find_coins_greedy({arr}, {change[0]})
        """
    stt = f"""
find_min_coins({arr}, {change[0]})
        """
    greedy = (timeit.timeit(setup=stp, stmt=stmnt, number=n))/n
    algs['greedy'].append(f"{greedy:.8f}")
    dynamic = (timeit.timeit(setup=stp, stmt=stt, number=n))/n
    algs['dynamic'].append(f"{dynamic:.8f}")
    algs['diff'].append(dynamic/greedy)

print(algs)


#Порівняння точності алгоритмів
changes = [113, 264, 551, 689, 1250, 2460, 7867]

ress = {'gr': [], 'dp': []}

for i in range(len(changes)):
    t = [random.randint(1, 50) for _ in range(11)]
    r = total_val(find_coins_greedy(t, changes[i]))
    s = total_val(dp(find_min_coins, t, changes[i]))
    ress['gr'].append((changes[i] - r, sum(list(find_coins_greedy(t, changes[i]).values()))))
    ress['dp'].append((changes[i] - s, sum(list(dp(find_min_coins, t, changes[i]).values()))))
print(ress)

#{'gr': [0, 4, 1, 1, 2, 0, 1], 'dp': [0, 0, 0, 0, 0, 0, 0]} #для 6 значень
# {'gr': [0, 0, 0, 0, 0, 0, 0], 'dp': [0, 0, 0, 0, 0, 0, 0]} # для 1000 значень
