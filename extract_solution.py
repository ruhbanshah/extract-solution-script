import re

def extract_code_blocks(markdown_text):
    """Extracts code blocks from strings. Do NOT modify this function."""    
    code_block_pattern = re.compile(r'```([^\n`]+)\n(.*?)```', re.DOTALL) # Changed for Universal Script

    code_blocks = code_block_pattern.findall(markdown_text)

    # Clean up the extracted code blocks by stripping leading/trailing whitespace
    cleaned_code_blocks = [(lang.strip(), code.strip()) for lang, code in code_blocks] # Changed for consistency

    fixed_code_blocks = [(lang, fix_print_statements(code)) for lang, code in cleaned_code_blocks]

    return fixed_code_blocks

def extract_solution(llm_response: str) -> list[tuple[str, str]]:
    """Extracts code blocks from the response and returns them as solution files."""
    valid_languages = {
        'js', 'jsx', 'ts', 'tsx',
        'javascript', 'typescript', 'javascript/typescript',
        'html','css',
        'python', 'json', 'java',
        'csharp', 'c#', 
        'c++', 'cpp', 'c','c/c++'
    }
    
    code_blocks = extract_code_blocks(llm_response)
    
    solutions = []
    
    for index, (language, code) in enumerate(code_blocks):
        if language.lower() not in valid_languages:
            continue
        
        file_extension = get_file_extension(language)

        if file_extension in ['js','ts']: 
            code = ensure_js_export_statement(code)
        elif file_extension == 'cpp':
            code = remove_cpp_main_function(code)

        file_name = "solution." + file_extension if index == 0 else f"solution_{index}.{file_extension}"
        
        solutions.append((file_name, code))
    
    return solutions


def get_file_extension(language: str) -> str:
    """Map a language string to the correct file extension."""
    lang = language.lower()
    if "javascript/typescript" in lang:
        lang = "javascript"

    if "c/c++" in lang:
        lang = "cpp" 
    
    if lang in ["typescript", "tsx", "ts"]:
        return "ts"
    elif lang in ["javascript", "jsx", "js"]:
        return "js"
    elif lang in ["python"]:
        return "py"
    elif lang in ["java"]:
        return "java"
    elif lang in ["csharp", "c#"]:
        return "cs"
    elif lang in ["c/c++","c++", "cpp"]:
        return "cpp"
    elif lang == "c":
        return "c"
    elif lang == "html":
        return "html"
    elif lang == "css":
        return "css"
    elif lang == "json":
        return "json"
    else:
        return "txt"  # Fallback

def fix_print_statements(code):
    """Removes `\n` inside print statements while keeping everything else intact."""
    # Match `print("some text with \n inside")`
    print_pattern = re.compile(r'(print\s*\(\s*[\'"])(.*?)([\'"]\s*\))', re.DOTALL)

    def replace_newline_in_print(match):
        before, content, after = match.groups()
        # Remove `\n` inside print statement
        fixed_content = content.replace("\n", "\\n")
        return before + fixed_content + after
    
    code = re.sub(print_pattern, replace_newline_in_print, code)

    
    # Fix C++ cout statements using regex
    cout_pattern = re.compile(
        r'((?:(?:std::)?cout\s*(?:<<\s*(?:"(?:\\.|[^"\\])*"|[^";])+)\s*;))',
        re.DOTALL
    )

    def replace_cout_statement(match):
        stmt = match.group(1)
        
        def replace_string_literal(lit_match):
            literal = lit_match.group(0)
            
            inner = literal[1:-1]
           
            fixed_inner = inner.replace("\n", "\\n")
            return '"' + fixed_inner + '"'
        
        fixed_stmt = re.sub(r'"(?:\\.|[^"\\])*"', replace_string_literal, stmt)
        return fixed_stmt

    code = re.sub(cout_pattern, replace_cout_statement, code)

    return code

def ensure_js_export_statement(code: str) -> str:
    """
    Ensure JavaScript/TypeScript code contains an export statement.
    If none exists, extract the function signature name and append an export default statement.
    """
    # Only add export if none exists
    if 'export ' in code:
        return code

    # Try pattern for a standard function declaration: "function functionName(...)"
    match = re.search(r'^\s*function\s+(\w+)\s*\(', code, re.MULTILINE)
    if match:
        func_name = match.group(1)
    else:
        # Try pattern for an arrow function or function expression assigned to a variable:
        match = re.search(r'^\s*(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?(?:\([^\)]*\)|\w+)\s*=>', code, re.MULTILINE)
        if match:
            func_name = match.group(1)
        else:
            # Fallback if no function name is detected
            func_name = "myModule"

    return code + f'\n\nexport default {func_name};'

def remove_cpp_main_function(code: str) -> str:
    """Removes the entire main function, including its content."""
    lines = code.splitlines()
    result = []
    inside_main = False
    brace_count = 0

    for line in lines:
        # Detect the start of the main function
        if not inside_main and re.match(r"\s*int\s+main\s*\(", line):
            inside_main = True
            brace_count = line.count("{") - line.count("}")
            continue

        # If inside the main function, track braces and skip lines
        if inside_main:
            brace_count += line.count("{") - line.count("}")
            if brace_count <= 0:
                inside_main = False  # End of the main function
            continue

        # If not inside the main function, keep the line
        result.append(line)

    return "\n".join(result)

