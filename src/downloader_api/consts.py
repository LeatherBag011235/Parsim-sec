import re

start_pattern = re.compile(r'.*?</ix:resources>\s*.*?</ix:header>.*?', re.IGNORECASE | re.DOTALL)
end_pattern = re.compile(r'.*?</html>.*?', re.IGNORECASE | re.DOTALL)
