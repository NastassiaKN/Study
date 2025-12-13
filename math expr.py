def user_value():
    expression = input("Enter a maths expression with spaces after each value: ")
    list_expression = list(expression.split(" "))
    return list_expression

def parentheses(list_expression):
    while "(" in list_expression or ")" in list_expression:
        start = len(list_expression) - 1
        while start >= 0 and list_expression[start] != "(":
            start -= 1

        end = start + 1
        while end < len(list_expression) and list_expression[end] != ")":
            end += 1

        if list_expression.count("(") != list_expression.count(")"):
            print("Check count of parentheses.")
            break

        slice_expression = list_expression[start + 1:end]
        while "*" in slice_expression or "/" in slice_expression:
            if "*" in slice_expression:
                multiplication_pos = slice_expression.index("*")
            else:
                multiplication_pos = float("inf")
            if "/" in slice_expression:
                division_pos = slice_expression.index("/")
            else:
                division_pos = float("inf")

            if multiplication_pos < division_pos:
                slice_expression = multiplication(slice_expression)
            else:
                slice_expression = division(slice_expression)

        while "+" in slice_expression or "-" in slice_expression:
            if "+" in slice_expression:
                addition_pos = slice_expression.index("+")
            else:
                addition_pos = float("inf")
            if "-" in slice_expression:
                subtraction_pos = slice_expression.index("-")
            else:
                subtraction_pos = float("inf")

            if addition_pos < subtraction_pos:
                slice_expression = addition(slice_expression)
            else:
                slice_expression = subtraction(slice_expression)

        list_expression = list_expression[:start] + [slice_expression[0]] + list_expression[end + 1:]

    return list_expression


def multiplication(list_expression):
    while "*" in list_expression:
        multiplication_pos = list_expression.index("*")
        left_start = multiplication_pos - 1
        right_end = multiplication_pos + 1
        num_left = list_expression[left_start]
        num_right = list_expression[right_end]
        multiplication_result = float(num_left) * float(num_right)
        list_expression = list_expression[:left_start] + [multiplication_result] + list_expression[right_end + 1:]
    return list_expression


def division(list_expression):
    while "/" in list_expression:
        division_pos = list_expression.index("/")
        left_start = division_pos - 1
        right_end = division_pos + 1
        num_left = list_expression[left_start]
        num_right = list_expression[right_end]
        division_result = float(num_left) / float(num_right)
        list_expression = list_expression[:left_start] + [division_result] + list_expression[right_end + 1:]
    return list_expression


def addition(list_expression):
    while "+" in list_expression:
        addition_pos = list_expression.index("+")
        left_start = addition_pos - 1
        right_end = addition_pos + 1
        num_left = list_expression[left_start]
        num_right = list_expression[right_end]
        addition_result = float(num_left) + float(num_right)
        list_expression = list_expression[:left_start] + [addition_result] + list_expression[right_end + 1:]
    return list_expression


def subtraction(list_expression):
    while "-" in list_expression:
        subtraction_pos = list_expression.index("-")
        left_start = subtraction_pos - 1
        right_end = subtraction_pos + 1
        num_left = list_expression[left_start]
        num_right = list_expression[right_end]
        subtraction_result = float(num_left) - float(num_right)
        list_expression = list_expression[:left_start] + [subtraction_result] + list_expression[right_end + 1:]
    return list_expression


def main():
    while True:
        try:
            list_expression = user_value()
            if len(list_expression) <= 1:
                print(f"{list_expression} is not a valid maths expression.")
                continue
            operators = ["*", "/", "+", "-"]
            if list_expression[0] in operators:
                print("Operator is not be in the start of maths expression.")
                continue
            if list_expression[-1] in operators:
                print("Operator is not be in the end of maths expression.")
                continue

            list_expression = parentheses(list_expression)
            if list_expression.count("(") != list_expression.count(")"):
                continue

            while "*" in list_expression or "/" in list_expression:
                if "*" in list_expression:
                    multiplication_pos = list_expression.index("*")
                else:
                    multiplication_pos = float("inf")
                if "/" in list_expression:
                    division_pos = list_expression.index("/")
                else:
                    division_pos = float("inf")

                if multiplication_pos < division_pos:
                    list_expression = multiplication(list_expression)
                else:
                    list_expression = division(list_expression)

            while "+" in list_expression or "-" in list_expression:
                if "+" in list_expression:
                    addition_pos = list_expression.index("+")
                else:
                    addition_pos = float("inf")
                if "-" in list_expression:
                    subtraction_pos = list_expression.index("-")
                else:
                    subtraction_pos = float("inf")

                if addition_pos < subtraction_pos:
                    list_expression = addition(list_expression)
                else:
                    list_expression = subtraction(list_expression)

            print(f"Result: {list_expression[0]}")

        except Exception as e:
            print(f"Error: {e}")

main()