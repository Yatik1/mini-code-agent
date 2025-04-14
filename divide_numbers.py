def divide_numbers(numbers):
    if not numbers:
        return None
    result = numbers[0]
    for i in range(1, len(numbers)):
        if numbers[i] == 0:
            return 'Division by zero error!'
        result /= numbers[i]
    return result

