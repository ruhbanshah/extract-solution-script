# extract-solution-script
 
:technologist: New Extraction Script Available! :technologist:
Hey team! We've developed an Extract Solution Script that covers most of the scenarios we encounter while operating and the specific requirements mentioned by the client for different languages.

:wrench:  Script Repository
https://github.com/ruhbanshah/extract-solution-script.git

:white_check_mark: What it does:
Extracts multiple code blocks of any language from markdown.
Stores them as either Solution.FILE_EXTENSION (if there's one block) or Solution_INDEX.FILE_EXTENSION (for multiple).
Fixes issues with \n inside print and cout that previously broke the blocks.
Adds export statements for JavaScript/TypeScript if missing and tries to infer the module name.
Supports extraction for JavaScript/TypeScript and C/C++.
Removes main functions in C++.

:warning: What it doesn’t do (yet!):
Adjust Java package declarations.

:exclamation:Please test it out and ensure it works for your specific tasks. Feel free to tweak it for edge cases as needed!

React with :script_code: once you've tested it. Let me know if you have any questions! :letsgo:
