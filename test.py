import re

def extract_patterns(input_string):
    patterns = []

    # Define a recursive function to parse nested patterns
    def parse_pattern(s):
        nonlocal patterns
        i = 0
        n = len(s)
        while i < n:
            if s[i].isspace():
                i += 1
                continue
            elif s[i] == '(':
                # Find the closing parenthesis
                stack = ['(']
                j = i + 1
                while stack and j < n:
                    if s[j] == '(':
                        stack.append('(')
                    elif s[j] == ')':
                        stack.pop()
                    j += 1
                patterns.append(s[i:j].strip())
                i = j
            elif s[i] == '+':
                patterns.append('+')
                i += 1
            else:
                # Find the next space or parenthesis
                j = i
                while j < n and not s[j].isspace() and s[j] != '(' and s[j] != ')' and s[j] != '+':
                    j += 1
                patterns.append(s[i:j].strip())
                i = j

    # Preprocess the input string to remove extra spaces
    input_string = re.sub(r'\s+', ' ', input_string).strip()

    # Parse the input_string recursively
    parse_pattern(input_string)

    return patterns

# Test the function
input_string = "(list < (list < int >) + str >) + int + set < int >"
result = extract_patterns(input_string)

print(result)
