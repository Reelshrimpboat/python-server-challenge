def fizz_buzz(number):
    if number % 3 == 0 and number % 5 == 0 :
        return("FizzBuzz")
    elif number%3 == 0:
        return("Fizz")
    elif number%5 == 0:
        return("Buzz")
    else:
        return(number)

    
def fb_range(b, e):
    for i in range(b, e):
        print(fizz_buzz(i))

print(fizz_buzz(1))
print(fizz_buzz(2))
print(fizz_buzz(3))
print(fizz_buzz(5))
print(fizz_buzz(15))

fb_range(1, 25)