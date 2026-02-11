"""
Manual Tasks Data - 50 Python Coding Challenges
Production-ready challenges covering basics to advanced topics.
"""

MANUAL_TASKS = [
    # ==================== LEVELS 1-10: PYTHON BASICS ====================
    {
        "title": "Level 1: Hello World",
        "slug": "level-1-hello-world",
        "description": "Welcome to Code of Clans! Your first task is to print 'Hello, World!' to the console.\n\nThis is the traditional first program in any programming language. Simply use Python's `print()` function to output the text.",
        "initial_code": 'print("")',
        "test_code": 'assert "Hello, World!" in output, "You must print \'Hello, World!\'"',
        "order": 1,
        "xp_reward": 10,
        "hints": [
            {"order": 1, "content": "Use the print() function to output text.", "cost": 5},
            {"order": 2, "content": "The exact text should be: Hello, World!", "cost": 10},
        ]
    },
    {
        "title": "Level 2: Simple Math",
        "slug": "level-2-simple-math",
        "description": "Calculate and print the sum of two numbers: 42 and 58.\n\nYour program should output the result of adding these two numbers.",
        "initial_code": "# Calculate 42 + 58\nresult = \nprint(result)",
        "test_code": 'assert "100" in output, "The sum of 42 and 58 should be 100"',
        "order": 2,
        "xp_reward": 20,
        "hints": [
            {"order": 1, "content": "Use the + operator to add numbers.", "cost": 5},
            {"order": 2, "content": "Assign the sum to the result variable: result = 42 + 58", "cost": 10},
        ]
    },
    {
        "title": "Level 3: Variables & Data Types",
        "slug": "level-3-variables-data-types",
        "description": "Create three variables:\n- `name` with your name as a string\n- `age` with value 25 as an integer\n- `height` with value 5.9 as a float\n\nThen print all three in the format: `Name: [name], Age: [age], Height: [height]`",
        "initial_code": "# Define your variables here\nname = \nage = \nheight = \n\nprint(f\"Name: {name}, Age: {age}, Height: {height}\")",
        "test_code": '''assert "Name:" in output and "Age:" in output and "Height:" in output, "Output must contain Name, Age, and Height"
assert "25" in output, "Age should be 25"
assert "5.9" in output, "Height should be 5.9"''',
        "order": 3,
        "xp_reward": 30,
        "hints": [
            {"order": 1, "content": "Strings are enclosed in quotes: 'text' or \"text\"", "cost": 5},
            {"order": 2, "content": "Integers are whole numbers without quotes, floats have decimal points", "cost": 10},
        ]
    },
    {
        "title": "Level 4: String Concatenation",
        "slug": "level-4-string-concatenation",
        "description": "Combine the following strings into one sentence and print it:\n- first_word = 'Python'\n- second_word = 'is'\n- third_word = 'awesome'\n\nOutput should be: 'Python is awesome'",
        "initial_code": "first_word = 'Python'\nsecond_word = 'is'\nthird_word = 'awesome'\n\n# Combine them here\nsentence = \nprint(sentence)",
        "test_code": 'assert "Python is awesome" in output, "Output should be exactly \'Python is awesome\'"',
        "order": 4,
        "xp_reward": 40,
        "hints": [
            {"order": 1, "content": "Use the + operator to concatenate strings.", "cost": 5},
            {"order": 2, "content": "Don't forget to add spaces between words: first_word + ' ' + second_word + ' ' + third_word", "cost": 10},
        ]
    },
    {
        "title": "Level 5: If Statements",
        "slug": "level-5-if-statements",
        "description": "Write a program that checks if a number is positive, negative, or zero.\n\nGiven `num = 15`, print 'Positive' if num > 0, 'Negative' if num < 0, or 'Zero' if num == 0.",
        "initial_code": "num = 15\n\n# Write your if-elif-else statement here\n",
        "test_code": 'assert "Positive" in output, "15 is a positive number"',
        "order": 5,
        "xp_reward": 50,
        "hints": [
            {"order": 1, "content": "Use if, elif, and else for multiple conditions.", "cost": 5},
            {"order": 2, "content": "Structure: if num > 0: print('Positive') elif num < 0: print('Negative') else: print('Zero')", "cost": 10},
        ]
    },
    {
        "title": "Level 6: For Loop Basics",
        "slug": "level-6-for-loop-basics",
        "description": "Print numbers from 1 to 5 using a for loop.\n\nEach number should be on a new line.",
        "initial_code": "# Write a for loop to print 1 to 5\n",
        "test_code": '''assert "1" in output and "2" in output and "3" in output and "4" in output and "5" in output, "Output must contain numbers 1 through 5"''',
        "order": 6,
        "xp_reward": 60,
        "hints": [
            {"order": 1, "content": "Use the range() function with a for loop.", "cost": 5},
            {"order": 2, "content": "for i in range(1, 6): print(i) - remember range is exclusive of the end", "cost": 10},
        ]
    },
    {
        "title": "Level 7: While Loop",
        "slug": "level-7-while-loop",
        "description": "Use a while loop to print even numbers from 2 to 10.\n\nOutput: 2, 4, 6, 8, 10 (each on a new line)",
        "initial_code": "# Write a while loop to print even numbers from 2 to 10\ncount = 2\n",
        "test_code": '''assert "2" in output and "4" in output and "6" in output and "8" in output and "10" in output, "Output must contain even numbers 2, 4, 6, 8, 10"''',
        "order": 7,
        "xp_reward": 70,
        "hints": [
            {"order": 1, "content": "Initialize count = 2, then use while count <= 10", "cost": 5},
            {"order": 2, "content": "Inside the loop: print(count), then increment count by 2: count += 2", "cost": 10},
        ]
    },
    {
        "title": "Level 8: List Creation",
        "slug": "level-8-list-creation",
        "description": "Create a list of your 5 favorite fruits and print the entire list.\n\nThen print the first fruit and the last fruit on separate lines.",
        "initial_code": "# Create a list of 5 fruits\nfruits = \n\nprint(fruits)\nprint()  # First fruit\nprint()  # Last fruit",
        "test_code": '''lines = output.strip().split("\\n")
assert len(lines) >= 3, "Should have at least 3 lines of output"''',
        "order": 8,
        "xp_reward": 80,
        "hints": [
            {"order": 1, "content": "Lists are created with square brackets: ['apple', 'banana', ...]", "cost": 5},
            {"order": 2, "content": "Access first element with fruits[0] and last with fruits[-1] or fruits[4]", "cost": 10},
        ]
    },
    {
        "title": "Level 9: List Append",
        "slug": "level-9-list-append",
        "description": "Start with an empty list. Use a for loop to add numbers 1 through 5 to the list.\n\nThen print the final list.",
        "initial_code": "numbers = []\n\n# Use a for loop to append 1-5 to the list\n\nprint(numbers)",
        "test_code": '''assert "[1, 2, 3, 4, 5]" in output, "List should contain [1, 2, 3, 4, 5]"''',
        "order": 9,
        "xp_reward": 90,
        "hints": [
            {"order": 1, "content": "Use the .append() method to add items to a list.", "cost": 5},
            {"order": 2, "content": "for i in range(1, 6): numbers.append(i)", "cost": 10},
        ]
    },
    {
        "title": "Level 10: Basic Dictionary",
        "slug": "level-10-basic-dictionary",
        "description": "Create a dictionary representing a person with keys: 'name', 'age', 'city'.\n\nUse values: 'Alice', 30, 'New York'.\n\nPrint the dictionary and then print just the person's name.",
        "initial_code": "# Create a dictionary\nperson = \n\nprint(person)\nprint()  # Print just the name",
        "test_code": '''assert "Alice" in output and "30" in output and "New York" in output, "Dictionary must contain Alice, 30, and New York"''',
        "order": 10,
        "xp_reward": 100,
        "hints": [
            {"order": 1, "content": "Dictionaries use curly braces: {'key': 'value', ...}", "cost": 5},
            {"order": 2, "content": "Access values with person['name']", "cost": 10},
        ]
    },

    # ==================== LEVELS 11-20: FUNCTIONS & DATA STRUCTURES ====================
    {
        "title": "Level 11: Simple Function",
        "slug": "level-11-simple-function",
        "description": "Create a function called `greet` that takes a name as a parameter and returns 'Hello, [name]!'\n\nCall the function with 'Python' and print the result.",
        "initial_code": "# Define the greet function\ndef greet(name):\n    \n\n# Call the function and print result\nresult = greet('Python')\nprint(result)",
        "test_code": '''assert "Hello, Python!" in output, "Function should return 'Hello, Python!'"''',
        "order": 11,
        "xp_reward": 110,
        "hints": [
            {"order": 1, "content": "Use the return keyword to send back a value from a function.", "cost": 5},
            {"order": 2, "content": "return f'Hello, {name}!' or return 'Hello, ' + name + '!'", "cost": 10},
        ]
    },
    {
        "title": "Level 12: Function with Multiple Parameters",
        "slug": "level-12-function-multiple-parameters",
        "description": "Create a function `add_numbers` that takes two parameters and returns their sum.\n\nTest it with 25 and 75, then print the result.",
        "initial_code": "# Define add_numbers function\ndef add_numbers(a, b):\n    \n\nresult = add_numbers(25, 75)\nprint(result)",
        "test_code": '''assert "100" in output, "25 + 75 should equal 100"''',
        "order": 12,
        "xp_reward": 120,
        "hints": [
            {"order": 1, "content": "Simply return the sum of the two parameters.", "cost": 5},
            {"order": 2, "content": "return a + b", "cost": 10},
        ]
    },
    {
        "title": "Level 13: List Comprehension",
        "slug": "level-13-list-comprehension",
        "description": "Use list comprehension to create a list of squares of numbers from 1 to 10.\n\nPrint the resulting list.",
        "initial_code": "# Create a list of squares using list comprehension\nsquares = \n\nprint(squares)",
        "test_code": '''assert "[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]" in output, "Should be squares from 1 to 10"''',
        "order": 13,
        "xp_reward": 130,
        "hints": [
            {"order": 1, "content": "List comprehension syntax: [expression for item in iterable]", "cost": 5},
            {"order": 2, "content": "squares = [i**2 for i in range(1, 11)]", "cost": 10},
        ]
    },
    {
        "title": "Level 14: Dictionary Iteration",
        "slug": "level-14-dictionary-iteration",
        "description": "Given a dictionary of fruits and their prices, print each fruit and its price in the format: 'apple: $1.50'\n\nfruits = {'apple': 1.50, 'banana': 0.75, 'orange': 2.00}",
        "initial_code": "fruits = {'apple': 1.50, 'banana': 0.75, 'orange': 2.00}\n\n# Iterate and print each fruit with its price\n",
        "test_code": '''assert "apple" in output and "1.5" in output, "Should contain apple and its price"
assert "banana" in output and "0.75" in output, "Should contain banana and its price"''',
        "order": 14,
        "xp_reward": 140,
        "hints": [
            {"order": 1, "content": "Use .items() to iterate over key-value pairs.", "cost": 5},
            {"order": 2, "content": "for fruit, price in fruits.items(): print(f'{fruit}: ${price}')", "cost": 10},
        ]
    },
    {
        "title": "Level 15: Filtering Lists",
        "slug": "level-15-filtering-lists",
        "description": "Given a list of numbers, create a new list containing only the even numbers.\n\nnumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n\nPrint the filtered list.",
        "initial_code": "numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n\n# Create a list of even numbers\neven_numbers = \n\nprint(even_numbers)",
        "test_code": '''assert "[2, 4, 6, 8, 10]" in output, "Should contain only even numbers"''',
        "order": 15,
        "xp_reward": 150,
        "hints": [
            {"order": 1, "content": "Use list comprehension with an if condition.", "cost": 5},
            {"order": 2, "content": "even_numbers = [n for n in numbers if n % 2 == 0]", "cost": 10},
        ]
    },
    {
        "title": "Level 16: Finding Max Value",
        "slug": "level-16-finding-max",
        "description": "Write a function `find_max` that takes a list of numbers and returns the maximum value.\n\nDo NOT use the built-in max() function. Use a loop instead.\n\nTest with: [3, 7, 2, 9, 1, 5]",
        "initial_code": "def find_max(numbers):\n    # Your code here\n    \n\nresult = find_max([3, 7, 2, 9, 1, 5])\nprint(result)",
        "test_code": '''assert "9" in output, "Maximum value should be 9"''',
        "order": 16,
        "xp_reward": 160,
        "hints": [
            {"order": 1, "content": "Initialize max_val to the first element, then loop through the rest.", "cost": 5},
            {"order": 2, "content": "max_val = numbers[0]; for n in numbers: if n > max_val: max_val = n; return max_val", "cost": 10},
        ]
    },
    {
        "title": "Level 17: String Methods",
        "slug": "level-17-string-methods",
        "description": "Given the string 'python programming', perform the following:\n1. Convert to uppercase and print\n2. Count how many times 'p' appears and print the count\n3. Replace 'programming' with 'coding' and print",
        "initial_code": "text = 'python programming'\n\n# 1. Uppercase\n\n# 2. Count 'p'\n\n# 3. Replace\n",
        "test_code": '''assert "PYTHON PROGRAMMING" in output, "Should contain uppercase version"
assert "2" in output, "Should count 2 occurrences of 'p'"
assert "python coding" in output, "Should contain replaced version"''',
        "order": 17,
        "xp_reward": 170,
        "hints": [
            {"order": 1, "content": "Use .upper(), .count(), and .replace() methods.", "cost": 5},
            {"order": 2, "content": "print(text.upper()); print(text.count('p')); print(text.replace('programming', 'coding'))", "cost": 10},
        ]
    },
    {
        "title": "Level 18: Tuple Unpacking",
        "slug": "level-18-tuple-unpacking",
        "description": "Create a tuple with 3 values: ('Alice', 25, 'Engineer')\n\nUnpack it into three variables: name, age, profession\n\nPrint each variable on a separate line.",
        "initial_code": "# Create tuple\nperson_info = \n\n# Unpack\n\n# Print each\n",
        "test_code": '''assert "Alice" in output and "25" in output and "Engineer" in output, "Should contain all three values"''',
        "order": 18,
        "xp_reward": 180,
        "hints": [
            {"order": 1, "content": "Tuples use parentheses: ('Alice', 25, 'Engineer')", "cost": 5},
            {"order": 2, "content": "name, age, profession = person_info", "cost": 10},
        ]
    },
    {
        "title": "Level 19: Set Operations",
        "slug": "level-19-set-operations",
        "description": "Create two sets:\nset_a = {1, 2, 3, 4, 5}\nset_b = {4, 5, 6, 7, 8}\n\nFind and print:\n1. Union (all unique elements)\n2. Intersection (common elements)\n3. Difference (elements in set_a but not in set_b)",
        "initial_code": "set_a = {1, 2, 3, 4, 5}\nset_b = {4, 5, 6, 7, 8}\n\n# Union\n\n# Intersection\n\n# Difference\n",
        "test_code": '''assert "1" in output and "8" in output, "Union should contain all elements"
assert "4" in output or "5" in output, "Intersection should contain common elements"''',
        "order": 19,
        "xp_reward": 190,
        "hints": [
            {"order": 1, "content": "Use | for union, & for intersection, - for difference.", "cost": 5},
            {"order": 2, "content": "print(set_a | set_b); print(set_a & set_b); print(set_a - set_b)", "cost": 10},
        ]
    },
    {
        "title": "Level 20: Nested Lists",
        "slug": "level-20-nested-lists",
        "description": "Create a 3x3 matrix (nested list) with values:\n[[1, 2, 3],\n [4, 5, 6],\n [7, 8, 9]]\n\nPrint the matrix, then print the center element (5).",
        "initial_code": "# Create the matrix\nmatrix = \n\nprint(matrix)\n# Print center element\n",
        "test_code": '''assert "5" in output, "Should print the center element 5"''',
        "order": 20,
        "xp_reward": 200,
        "hints": [
            {"order": 1, "content": "Nested lists are lists inside lists: [[1,2,3], [4,5,6], [7,8,9]]", "cost": 5},
            {"order": 2, "content": "Access center with matrix[1][1]", "cost": 10},
        ]
    },

    # ==================== LEVELS 21-30: STRING MANIPULATION & FILE I/O ====================
    {
        "title": "Level 21: Reverse a String",
        "slug": "level-21-reverse-string",
        "description": "Write a function `reverse_string` that takes a string and returns it reversed.\n\nTest with: 'Python'",
        "initial_code": "def reverse_string(text):\n    # Your code here\n    \n\nresult = reverse_string('Python')\nprint(result)",
        "test_code": '''assert "nohtyP" in output, "Should reverse to 'nohtyP'"''',
        "order": 21,
        "xp_reward": 210,
        "hints": [
            {"order": 1, "content": "Use string slicing with [::-1]", "cost": 5},
            {"order": 2, "content": "return text[::-1]", "cost": 10},
        ]
    },
    {
        "title": "Level 22: Palindrome Checker",
        "slug": "level-22-palindrome-checker",
        "description": "Write a function `is_palindrome` that returns True if a string reads the same forwards and backwards (ignore case).\n\nTest with: 'Racecar' (should be True)",
        "initial_code": "def is_palindrome(text):\n    # Your code here\n    \n\nresult = is_palindrome('Racecar')\nprint(result)",
        "test_code": '''assert "True" in output, "Racecar is a palindrome"''',
        "order": 22,
        "xp_reward": 220,
        "hints": [
            {"order": 1, "content": "Convert to lowercase first, then compare with its reverse.", "cost": 5},
            {"order": 2, "content": "text = text.lower(); return text == text[::-1]", "cost": 10},
        ]
    },
    {
        "title": "Level 23: Count Vowels",
        "slug": "level-23-count-vowels",
        "description": "Write a function that counts the number of vowels (a, e, i, o, u) in a string.\n\nTest with: 'Hello World'",
        "initial_code": "def count_vowels(text):\n    # Your code here\n    \n\nresult = count_vowels('Hello World')\nprint(result)",
        "test_code": '''assert "3" in output, "Should count 3 vowels (e, o, o)"''',
        "order": 23,
        "xp_reward": 230,
        "hints": [
            {"order": 1, "content": "Loop through the string and check if each character is in 'aeiouAEIOU'", "cost": 5},
            {"order": 2, "content": "count = 0; for char in text: if char.lower() in 'aeiou': count += 1; return count", "cost": 10},
        ]
    },
    {
        "title": "Level 24: String Splitting",
        "slug": "level-24-string-splitting",
        "description": "Given a sentence, split it into words and print the number of words.\n\nSentence: 'The quick brown fox jumps'",
        "initial_code": "sentence = 'The quick brown fox jumps'\n\n# Split and count\n",
        "test_code": '''assert "5" in output, "Should have 5 words"''',
        "order": 24,
        "xp_reward": 240,
        "hints": [
            {"order": 1, "content": "Use .split() method to divide by spaces.", "cost": 5},
            {"order": 2, "content": "words = sentence.split(); print(len(words))", "cost": 10},
        ]
    },
    {
        "title": "Level 25: Join Words",
        "slug": "level-25-join-words",
        "description": "Given a list of words, join them into a sentence with spaces.\n\nwords = ['Python', 'is', 'fun', 'to', 'learn']",
        "initial_code": "words = ['Python', 'is', 'fun', 'to', 'learn']\n\n# Join into sentence\n",
        "test_code": '''assert "Python is fun to learn" in output, "Should join all words with spaces"''',
        "order": 25,
        "xp_reward": 250,
        "hints": [
            {"order": 1, "content": "Use ' '.join() method.", "cost": 5},
            {"order": 2, "content": "sentence = ' '.join(words); print(sentence)", "cost": 10},
        ]
    },
    {
        "title": "Level 26: Title Case",
        "slug": "level-26-title-case",
        "description": "Write a function that converts a string to title case (first letter of each word capitalized).\n\nTest with: 'hello world from python'",
        "initial_code": "def to_title_case(text):\n    # Your code here\n    \n\nresult = to_title_case('hello world from python')\nprint(result)",
        "test_code": '''assert "Hello World From Python" in output, "Each word should be capitalized"''',
        "order": 26,
        "xp_reward": 260,
        "hints": [
            {"order": 1, "content": "Use the .title() method.", "cost": 5},
            {"order": 2, "content": "return text.title()", "cost": 10},
        ]
    },
    {
        "title": "Level 27: Remove Duplicates",
        "slug": "level-27-remove-duplicates",
        "description": "Write a function that removes duplicate elements from a list while preserving order.\n\nTest with: [1, 2, 2, 3, 4, 3, 5]",
        "initial_code": "def remove_duplicates(items):\n    # Your code here\n    \n\nresult = remove_duplicates([1, 2, 2, 3, 4, 3, 5])\nprint(result)",
        "test_code": '''assert "1" in output and "2" in output and "5" in output, "Should preserve unique elements"''',
        "order": 27,
        "xp_reward": 270,
        "hints": [
            {"order": 1, "content": "Use a loop and track seen items with a list or set.", "cost": 5},
            {"order": 2, "content": "seen = []; for item in items: if item not in seen: seen.append(item); return seen", "cost": 10},
        ]
    },
    {
        "title": "Level 28: List Sorting",
        "slug": "level-28-list-sorting",
        "description": "Sort a list of numbers in ascending order, then print it.\nThen sort the same list in descending order and print it.\n\nnumbers = [64, 34, 25, 12, 22, 11, 90]",
        "initial_code": "numbers = [64, 34, 25, 12, 22, 11, 90]\n\n# Sort ascending\n\n# Sort descending\n",
        "test_code": '''assert "11" in output and "90" in output, "Should show sorted results"''',
        "order": 28,
        "xp_reward": 280,
        "hints": [
            {"order": 1, "content": "Use sorted() or .sort() method.", "cost": 5},
            {"order": 2, "content": "print(sorted(numbers)); print(sorted(numbers, reverse=True))", "cost": 10},
        ]
    },
    {
        "title": "Level 29: Dictionary Merging",
        "slug": "level-29-dictionary-merging",
        "description": "Merge two dictionaries into one and print the result.\n\ndict1 = {'a': 1, 'b': 2}\ndict2 = {'c': 3, 'd': 4}",
        "initial_code": "dict1 = {'a': 1, 'b': 2}\ndict2 = {'c': 3, 'd': 4}\n\n# Merge dictionaries\n",
        "test_code": '''assert "a" in output and "d" in output, "Should contain all keys from both dictionaries"''',
        "order": 29,
        "xp_reward": 290,
        "hints": [
            {"order": 1, "content": "Use {**dict1, **dict2} or dict1 | dict2 (Python 3.9+)", "cost": 5},
            {"order": 2, "content": "merged = {**dict1, **dict2}; print(merged)", "cost": 10},
        ]
    },
    {
        "title": "Level 30: FizzBuzz",
        "slug": "level-30-fizzbuzz",
        "description": "Write the classic FizzBuzz program:\n- Print numbers from 1 to 15\n- For multiples of 3, print 'Fizz' instead\n- For multiples of 5, print 'Buzz' instead\n- For multiples of both 3 and 5, print 'FizzBuzz'",
        "initial_code": "# FizzBuzz implementation\n",
        "test_code": '''assert "Fizz" in output and "Buzz" in output and "FizzBuzz" in output, "Should contain Fizz, Buzz, and FizzBuzz"''',
        "order": 30,
        "xp_reward": 300,
        "hints": [
            {"order": 1, "content": "Check divisibility by 15 first, then 3, then 5.", "cost": 5},
            {"order": 2, "content": "for i in range(1, 16): if i % 15 == 0: print('FizzBuzz') elif i % 3 == 0: print('Fizz') elif i % 5 == 0: print('Buzz') else: print(i)", "cost": 10},
        ]
    },

    # ==================== LEVELS 31-40: OBJECT-ORIENTED PROGRAMMING ====================
    {
        "title": "Level 31: Simple Class",
        "slug": "level-31-simple-class",
        "description": "Create a class `Dog` with:\n- `__init__` method that takes `name` and `age`\n- A method `bark()` that prints '[name] says Woof!'\n\nCreate a Dog named 'Buddy' aged 3 and call bark().",
        "initial_code": "# Define the Dog class\nclass Dog:\n    \n\n# Create instance and call bark\n",
        "test_code": '''assert "Woof" in output, "Dog should bark"
assert "Buddy" in output, "Should use the dog's name"''',
        "order": 31,
        "xp_reward": 310,
        "hints": [
            {"order": 1, "content": "Use __init__(self, name, age) to initialize attributes.", "cost": 5},
            {"order": 2, "content": "def bark(self): print(f'{self.name} says Woof!')", "cost": 10},
        ]
    },
    {
        "title": "Level 32: Class with Methods",
        "slug": "level-32-class-methods",
        "description": "Create a `Rectangle` class with:\n- `__init__` taking width and height\n- `area()` method returning width * height\n- `perimeter()` method returning 2 * (width + height)\n\nTest with width=5, height=3",
        "initial_code": "class Rectangle:\n    # Your code here\n    \n\nrect = Rectangle(5, 3)\nprint(rect.area())\nprint(rect.perimeter())",
        "test_code": '''assert "15" in output, "Area should be 15"
assert "16" in output, "Perimeter should be 16"''',
        "order": 32,
        "xp_reward": 320,
        "hints": [
            {"order": 1, "content": "Store width and height as self.width and self.height in __init__.", "cost": 5},
            {"order": 2, "content": "def area(self): return self.width * self.height", "cost": 10},
        ]
    },
    {
        "title": "Level 33: Class Inheritance",
        "slug": "level-33-class-inheritance",
        "description": "Create a `Vehicle` class with attribute `brand`.\nCreate a `Car` class that inherits from Vehicle and adds attribute `model`.\n\nCreate a Car with brand='Toyota' and model='Camry' and print both attributes.",
        "initial_code": "class Vehicle:\n    # Your code here\n    \n\nclass Car(Vehicle):\n    # Your code here\n    \n\nmy_car = Car('Toyota', 'Camry')\nprint(my_car.brand)\nprint(my_car.model)",
        "test_code": '''assert "Toyota" in output and "Camry" in output, "Should print both brand and model"''',
        "order": 33,
        "xp_reward": 330,
        "hints": [
            {"order": 1, "content": "Use super().__init__(brand) in Car's __init__ to call parent constructor.", "cost": 5},
            {"order": 2, "content": "class Car(Vehicle): def __init__(self, brand, model): super().__init__(brand); self.model = model", "cost": 10},
        ]
    },
    {
        "title": "Level 34: Encapsulation",
        "slug": "level-34-encapsulation",
        "description": "Create a `BankAccount` class with:\n- Private attribute `__balance` (starts at 0)\n- `deposit(amount)` method to add to balance\n- `get_balance()` method to return current balance\n\nDeposit 100, then print the balance.",
        "initial_code": "class BankAccount:\n    # Your code here\n    \n\naccount = BankAccount()\naccount.deposit(100)\nprint(account.get_balance())",
        "test_code": '''assert "100" in output, "Balance should be 100"''',
        "order": 34,
        "xp_reward": 340,
        "hints": [
            {"order": 1, "content": "Use double underscore __ prefix for private attributes.", "cost": 5},
            {"order": 2, "content": "def __init__(self): self.__balance = 0; def deposit(self, amount): self.__balance += amount", "cost": 10},
        ]
    },
    {
        "title": "Level 35: Magic Methods",
        "slug": "level-35-magic-methods",
        "description": "Create a `Point` class with:\n- `__init__` taking x and y coordinates\n- `__str__` method returning 'Point(x, y)'\n- `__add__` method to add two points together\n\nCreate Point(1, 2) + Point(3, 4) and print the result.",
        "initial_code": "class Point:\n    # Your code here\n    \n\np1 = Point(1, 2)\np2 = Point(3, 4)\nresult = p1 + p2\nprint(result)",
        "test_code": '''assert "4" in output and "6" in output, "Result should be Point(4, 6)"''',
        "order": 35,
        "xp_reward": 350,
        "hints": [
            {"order": 1, "content": "__str__ should return a string representation, __add__ should return a new Point.", "cost": 5},
            {"order": 2, "content": "def __add__(self, other): return Point(self.x + other.x, self.y + other.y)", "cost": 10},
        ]
    },
    {
        "title": "Level 36: Class Variables",
        "slug": "level-36-class-variables",
        "description": "Create a `Student` class with:\n- Class variable `school` = 'Python Academy'\n- Instance variables `name` and `grade`\n- Print the school name using the class variable\n\nCreate a student named 'Alice' with grade 'A'.",
        "initial_code": "class Student:\n    # Your code here\n    \n\nstudent = Student('Alice', 'A')\nprint(Student.school)\nprint(student.name)",
        "test_code": '''assert "Python Academy" in output and "Alice" in output, "Should print school and name"''',
        "order": 36,
        "xp_reward": 360,
        "hints": [
            {"order": 1, "content": "Class variables are defined inside the class but outside methods.", "cost": 5},
            {"order": 2, "content": "class Student: school = 'Python Academy'; def __init__(self, name, grade): ...", "cost": 10},
        ]
    },
    {
        "title": "Level 37: Static Methods",
        "slug": "level-37-static-methods",
        "description": "Create a `MathUtils` class with a static method `add(a, b)` that returns the sum.\n\nCall the method without creating an instance: MathUtils.add(10, 20)",
        "initial_code": "class MathUtils:\n    # Your code here\n    \n\nresult = MathUtils.add(10, 20)\nprint(result)",
        "test_code": '''assert "30" in output, "Should return 30"''',
        "order": 37,
        "xp_reward": 370,
        "hints": [
            {"order": 1, "content": "Use @staticmethod decorator before the method definition.", "cost": 5},
            {"order": 2, "content": "@staticmethod; def add(a, b): return a + b", "cost": 10},
        ]
    },
    {
        "title": "Level 38: Property Decorator",
        "slug": "level-38-property-decorator",
        "description": "Create a `Circle` class with:\n- `__init__` taking radius\n- `area` as a @property that calculates π * r²\n\nUse 3.14159 for π. Test with radius=5.",
        "initial_code": "class Circle:\n    # Your code here\n    \n\ncircle = Circle(5)\nprint(circle.area)",
        "test_code": '''assert "78.5" in output or "78.539" in output, "Area should be approximately 78.54"''',
        "order": 38,
        "xp_reward": 380,
        "hints": [
            {"order": 1, "content": "Use @property decorator to make a method accessible like an attribute.", "cost": 5},
            {"order": 2, "content": "@property; def area(self): return 3.14159 * self.radius ** 2", "cost": 10},
        ]
    },
    {
        "title": "Level 39: Multiple Inheritance",
        "slug": "level-39-multiple-inheritance",
        "description": "Create:\n- Class `Flyer` with method `fly()` printing 'Flying!'\n- Class `Swimmer` with method `swim()` printing 'Swimming!'\n- Class `Duck` inheriting from both\n\nCreate a Duck and call both methods.",
        "initial_code": "class Flyer:\n    # Your code here\n    \nclass Swimmer:\n    # Your code here\n    \nclass Duck(Flyer, Swimmer):\n    pass\n\nduck = Duck()\nduck.fly()\nduck.swim()",
        "test_code": '''assert "Flying" in output and "Swimming" in output, "Duck should fly and swim"''',
        "order": 39,
        "xp_reward": 390,
        "hints": [
            {"order": 1, "content": "Simply define fly() and swim() methods in respective classes.", "cost": 5},
            {"order": 2, "content": "class Flyer: def fly(self): print('Flying!')", "cost": 10},
        ]
    },
    {
        "title": "Level 40: Abstract Classes",
        "slug": "level-40-abstract-classes",
        "description": "Create an abstract `Shape` class with abstract method `area()`.\nCreate a `Square` class that implements area().\n\nCreate a Square with side=4 and print its area.",
        "initial_code": "from abc import ABC, abstractmethod\n\nclass Shape(ABC):\n    # Your code here\n    \nclass Square(Shape):\n    # Your code here\n    \n\nsquare = Square(4)\nprint(square.area())",
        "test_code": '''assert "16" in output, "Area of square with side 4 should be 16"''',
        "order": 40,
        "xp_reward": 400,
        "hints": [
            {"order": 1, "content": "Use @abstractmethod decorator for abstract methods.", "cost": 5},
            {"order": 2, "content": "@abstractmethod; def area(self): pass - then implement in Square", "cost": 10},
        ]
    },

    # ==================== LEVELS 41-50: ADVANCED TOPICS ====================
    {
        "title": "Level 41: Recursion - Factorial",
        "slug": "level-41-recursion-factorial",
        "description": "Write a recursive function `factorial(n)` that calculates n!.\n\nTest with n=5 (should return 120).",
        "initial_code": "def factorial(n):\n    # Your recursive code here\n    \n\nresult = factorial(5)\nprint(result)",
        "test_code": '''assert "120" in output, "5! = 120"''',
        "order": 41,
        "xp_reward": 410,
        "hints": [
            {"order": 1, "content": "Base case: if n == 0 or n == 1, return 1", "cost": 5},
            {"order": 2, "content": "Recursive case: return n * factorial(n-1)", "cost": 10},
        ]
    },
    {
        "title": "Level 42: Fibonacci Sequence",
        "slug": "level-42-fibonacci-sequence",
        "description": "Write a function that generates the first n Fibonacci numbers.\n\nTest with n=10. Print the list.",
        "initial_code": "def fibonacci(n):\n    # Your code here\n    \n\nresult = fibonacci(10)\nprint(result)",
        "test_code": '''assert "0" in output and "1" in output and "34" in output, "Should contain Fibonacci sequence"''',
        "order": 42,
        "xp_reward": 420,
        "hints": [
            {"order": 1, "content": "Start with [0, 1] and build from there.", "cost": 5},
            {"order": 2, "content": "fib = [0, 1]; for i in range(2, n): fib.append(fib[-1] + fib[-2]); return fib", "cost": 10},
        ]
    },
    {
        "title": "Level 43: Lambda Functions",
        "slug": "level-43-lambda-functions",
        "description": "Use lambda functions with map() to square a list of numbers.\n\nnumbers = [1, 2, 3, 4, 5]\n\nPrint the squared list.",
        "initial_code": "numbers = [1, 2, 3, 4, 5]\n\n# Use map with lambda\n",
        "test_code": '''assert "1" in output and "25" in output, "Should contain squared values"''',
        "order": 43,
        "xp_reward": 430,
        "hints": [
            {"order": 1, "content": "Lambda syntax: lambda x: expression", "cost": 5},
            {"order": 2, "content": "squared = list(map(lambda x: x**2, numbers)); print(squared)", "cost": 10},
        ]
    },
    {
        "title": "Level 44: Filter Function",
        "slug": "level-44-filter-function",
        "description": "Use filter() with a lambda to get numbers greater than 50 from a list.\n\nnumbers = [23, 65, 12, 87, 45, 99, 34]\n\nPrint the filtered list.",
        "initial_code": "numbers = [23, 65, 12, 87, 45, 99, 34]\n\n# Use filter with lambda\n",
        "test_code": '''assert "65" in output and "87" in output and "99" in output, "Should contain numbers > 50"''',
        "order": 44,
        "xp_reward": 440,
        "hints": [
            {"order": 1, "content": "Filter syntax: filter(lambda x: condition, iterable)", "cost": 5},
            {"order": 2, "content": "result = list(filter(lambda x: x > 50, numbers)); print(result)", "cost": 10},
        ]
    },
    {
        "title": "Level 45: Reduce Function",
        "slug": "level-45-reduce-function",
        "description": "Use reduce() from functools to find the product of all numbers in a list.\n\nnumbers = [1, 2, 3, 4, 5]\n\nPrint the product (should be 120).",
        "initial_code": "from functools import reduce\n\nnumbers = [1, 2, 3, 4, 5]\n\n# Use reduce to find product\n",
        "test_code": '''assert "120" in output, "Product should be 120"''',
        "order": 45,
        "xp_reward": 450,
        "hints": [
            {"order": 1, "content": "Reduce syntax: reduce(lambda x, y: operation, iterable)", "cost": 5},
            {"order": 2, "content": "product = reduce(lambda x, y: x * y, numbers); print(product)", "cost": 10},
        ]
    },
    {
        "title": "Level 46: Generator Function",
        "slug": "level-46-generator-function",
        "description": "Create a generator function `count_up_to(n)` that yields numbers from 1 to n.\n\nTest with n=5 and print all yielded values.",
        "initial_code": "def count_up_to(n):\n    # Your generator code here\n    \n\nfor num in count_up_to(5):\n    print(num)",
        "test_code": '''assert "1" in output and "5" in output, "Should yield 1 through 5"''',
        "order": 46,
        "xp_reward": 460,
        "hints": [
            {"order": 1, "content": "Use yield instead of return to create a generator.", "cost": 5},
            {"order": 2, "content": "i = 1; while i <= n: yield i; i += 1", "cost": 10},
        ]
    },
    {
        "title": "Level 47: Decorator Basics",
        "slug": "level-47-decorator-basics",
        "description": "Create a decorator `uppercase_decorator` that converts a function's return value to uppercase.\n\nApply it to a function that returns 'hello world'.",
        "initial_code": "def uppercase_decorator(func):\n    # Your decorator code here\n    \n\n@uppercase_decorator\ndef greet():\n    return 'hello world'\n\nprint(greet())",
        "test_code": '''assert "HELLO WORLD" in output, "Should convert to uppercase"''',
        "order": 47,
        "xp_reward": 470,
        "hints": [
            {"order": 1, "content": "Decorator returns a wrapper function that modifies the original.", "cost": 5},
            {"order": 2, "content": "def wrapper(): result = func(); return result.upper(); return wrapper", "cost": 10},
        ]
    },
    {
        "title": "Level 48: Exception Handling",
        "slug": "level-48-exception-handling",
        "description": "Write a function `safe_divide(a, b)` that handles ZeroDivisionError.\n\nIf division by zero, return 'Cannot divide by zero', otherwise return the result.\n\nTest with divide(10, 0).",
        "initial_code": "def safe_divide(a, b):\n    # Your code with try-except here\n    \n\nresult = safe_divide(10, 0)\nprint(result)",
        "test_code": '''assert "Cannot divide by zero" in output, "Should handle division by zero"''',
        "order": 48,
        "xp_reward": 480,
        "hints": [
            {"order": 1, "content": "Use try-except block to catch ZeroDivisionError.", "cost": 5},
            {"order": 2, "content": "try: return a / b; except ZeroDivisionError: return 'Cannot divide by zero'", "cost": 10},
        ]
    },
    {
        "title": "Level 49: Binary Search",
        "slug": "level-49-binary-search",
        "description": "Implement binary search to find the index of a target value in a sorted list.\n\nReturn -1 if not found.\n\nTest with: [1, 3, 5, 7, 9, 11, 13], target=7 (should return 3).",
        "initial_code": "def binary_search(arr, target):\n    # Your binary search code here\n    \n\nresult = binary_search([1, 3, 5, 7, 9, 11, 13], 7)\nprint(result)",
        "test_code": '''assert "3" in output, "7 is at index 3"''',
        "order": 49,
        "xp_reward": 490,
        "hints": [
            {"order": 1, "content": "Use left and right pointers, calculate mid, compare with target.", "cost": 5},
            {"order": 2, "content": "left, right = 0, len(arr)-1; while left <= right: mid = (left+right)//2; if arr[mid] == target: return mid; elif arr[mid] < target: left = mid+1; else: right = mid-1; return -1", "cost": 10},
        ]
    },
    {
        "title": "Level 50: Merge Sort",
        "slug": "level-50-merge-sort",
        "description": "Implement the merge sort algorithm to sort a list.\n\nTest with: [64, 34, 25, 12, 22, 11, 90]\n\nPrint the sorted list.",
        "initial_code": "def merge_sort(arr):\n    # Your merge sort code here\n    \n\nresult = merge_sort([64, 34, 25, 12, 22, 11, 90])\nprint(result)",
        "test_code": '''assert "11" in output and "90" in output, "Should be sorted"''',
        "order": 50,
        "xp_reward": 500,
        "hints": [
            {"order": 1, "content": "Base case: if len(arr) <= 1, return arr. Recursively split and merge.", "cost": 5},
            {"order": 2, "content": "Split into halves, recursively sort each, then merge them back in order.", "cost": 10},
        ]
    },
    {
        "title": "Level 51: Dictionary Comprehension",
        "slug": "level-51-dictionary-comprehension",
        "description": "Create a dictionary where keys are numbers 1 to 5 and values are their squares using dictionary comprehension.\n\nOutput the dictionary.",
        "initial_code": "# Create dictionary squares = {x: x*x for ...}\n",
        "test_code": '''assert "1: 1" in output and "5: 25" in output, "Output should contain squares"''',
        "order": 51,
        "xp_reward": 510,
        "hints": [
            {"order": 1, "content": "Syntax: {key: value for item in iterable}", "cost": 5},
            {"order": 2, "content": "{x: x**2 for x in range(1, 6)}", "cost": 10},
        ]
    },
    {
        "title": "Level 52: Sets",
        "slug": "level-52-sets",
        "description": "Create a set from a list to remove duplicates.\n\nGiven `nums = [1, 2, 2, 3, 3, 3, 4]`, convert it to a set and print it.",
        "initial_code": "nums = [1, 2, 2, 3, 3, 3, 4]\n# Convert to set and print\n",
        "test_code": '''assert "{1, 2, 3, 4}" in output or "1, 2, 3, 4" in output, "Output should be unique elements"''',
        "order": 52,
        "xp_reward": 520,
        "hints": [
            {"order": 1, "content": "Use the set() function.", "cost": 5},
            {"order": 2, "content": "unique_nums = set(nums); print(unique_nums)", "cost": 10},
        ]
    },
    {
        "title": "Level 53: Generators",
        "slug": "level-53-generators",
        "description": "Write a generator function `count_up_to(n)` that yields numbers from 1 to n.\n\nIterate through it for n=3 and print each number.",
        "initial_code": "def count_up_to(n):\n    # Use yield here\n    pass\n\nfor num in count_up_to(3):\n    print(num)",
        "test_code": '''assert "1" in output and "2" in output and "3" in output, "Should print 1, 2, 3"''',
        "order": 53,
        "xp_reward": 530,
        "hints": [
            {"order": 1, "content": "Use yield instead of return to make a generator.", "cost": 5},
            {"order": 2, "content": "for i in range(1, n+1): yield i", "cost": 10},
        ]
    },
]
