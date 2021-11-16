import re, uuid
from werkzeug.test import create_environ
from werkzeug.wrappers import Request

txt = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36."
x = re.search("[(][a-z,A-Z,]*[;] [a-z,A-Z,]* ([a-z,A-Z,\s,0-9,_]*)", txt).group()
