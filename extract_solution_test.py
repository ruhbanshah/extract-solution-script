import os
import re
from extract_solution import extract_solution

llm_response =r'''
  Please Do Not Change The `r` before the backticks as that converts the code to a docstring which handles `\n` in the code.
'''
    
try:
    extracted_blocks = extract_solution(llm_response)

    if not isinstance(extracted_blocks, list):
        raise ValueError("Expected extracted blocks to be a list of (language, code) tuples.")
    
    for index, (file_name, code) in enumerate(extracted_blocks):
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(code)
        print(f"File '{file_name}' written successfully.")
except FileNotFoundError as fnf_error:
    print(f"File error: {fnf_error}")
except Exception as e:
    print(f"An error occurred while running extract solution test: {e}")