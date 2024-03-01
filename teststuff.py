# Example list
original_list = [1, 2, 3, 4, 5]

# Index where replacement should occur
index = 2

# Replacement array
replacement_array = [6, 7, 8]

# Replace the element at the specified index with the elements of the replacement array
original_list[index:index + 1] = replacement_array

# Print the modified list
print(original_list)