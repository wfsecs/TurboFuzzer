import time
from colorama import Fore, init
import random
import requests
import threading
from urllib.parse import urlparse
init()


# User agents.
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:104.0) Gecko/20100101 Firefox/104.0',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33',
    'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33']

# List of status codes and their meanings.
STATUS_CODES = \
    {200: 'OK',
     201: 'CREATED',
     202: 'ACCEPTED',
     204: 'NO CONTENT',
     206: 'PARTIAL CONTENT',
     300: 'MULTIPLE CHOICES',
     301: 'MOVED PERMAMENTLY',
     302: 'FOUND',
     305: 'USE PROXY',
     306: 'UNUSED',
     307: 'TEMPORARY REDIRECT',
     308: 'PERMAMENT REDIRECT',
     400: 'BAD REQUEST',
     401: 'UNAUTHORIZED',
     402: 'PAYMENT REQUIRED',
     403: 'FORBIDDEN',
     404: 'NOT FOUND',
     405: 'METHOD NOT ALLOWED',
     406: 'NOT ACCEPTABLE',
     407: 'PROXY AUTHENTICATION REQUIRED',
     408: 'REQUEST TIMEOUT',
     409: 'CONFLICT',
     410: 'GONE',
     414: 'URL TOO LONG',
     423: 'LOCKED',
     425: 'TOO EARLY',
     429: 'TOO MANY REQUESTS',
     451: 'UNAVAILABLE FOR LEGAL REASONS',
     500: 'INTERNAL SERVER ERROR',
     501: 'NOT IMPLEMENTED',
     502: 'BAD GATEWAY',
     503: 'SERVICE UNAVAILABLE',
     504: 'GATEWAY TIMEOUT',
     505: 'HTTP VERSION NOT SUPPORTED',
     508: 'LOOP DETECTED'
     }

# Colors for status codes.
Green_codes = [200]
Red_codes = [404]
LRED_codes = [400, 401, 403, 414]
Yellow_codes = [429, 500, 408, 301, 307, 308, 405]
All_color_codes = [200, 301, 307, 308, 400, 401, 403, 404, 405, 408, 414, 429, 500]

# Colors.
C_BLA = Fore.BLACK
C_BLU = Fore.BLUE
C_CYA = Fore.CYAN
C_GRE = Fore.GREEN
C_LBLA = Fore.LIGHTBLACK_EX
C_LBLU = Fore.LIGHTBLUE_EX
C_LCYA = Fore.LIGHTCYAN_EX
C_LGRE = Fore.LIGHTGREEN_EX
C_LMAG = Fore.LIGHTMAGENTA_EX
C_LRED = Fore.LIGHTRED_EX
C_LWHI = Fore.LIGHTWHITE_EX
C_LYEL = Fore.LIGHTYELLOW_EX
C_MAG = Fore.MAGENTA
C_RED = Fore.RED
C_RESET = Fore.RESET
C_WHI = Fore.WHITE
C_YEL = Fore.YELLOW

# Print cool ascii text art.
print(f'''{C_BLU}
         /$$$$$$$$                  /$$                 /$$$$$$$$                           
        |__  $$__/                 | ${C_LBLU}$                | $$_____/                           
           | $$ /$$   /{C_BLU}$$  /$$$$$$ | $$$$$$$ {C_LBLU}  /$$$$$$ | $$    /$$   /$$ /$$$$$$$$ /$$$$$$$$
           | $$| $$  | $$ /$$__  $$| $$__ {C_BLU} $$ /$$__  $$| $$$$$| $$  | $$|____ /$$/|_{C_LBLU}___ /$$/
           | $$| $$  | $$| $$  \__/| $$  \ ${C_BLU}$| $$  \ $$| $$__/| $$  | $$   /$$$$/    /$$$$/ 
           | $$| $$  | ${C_LBLU}$| $$      | $$  | $$| $$  | $$| {C_BLU}$$   | $$  | $$  /$$__/{C_LBLU}    /$$__/  
           | $$|  $$$$$$/| $$      | {C_BLU}$$$$$$$/|  $$$$$$/| $$   |  {C_LBLU}$$$$$$/ /$$$$$$$$ /$$$$$$$$
           |_{C_BLU}_/ \______/ |_{C_LBLU}_/      |___{C_BLU}____/  \______/ |__/    \______/ |__{C_LBLU}______/|________/{C_RESET}                                      
   ''')

# Asks for URL and the file that has the directory names.
input_url = input('   URL: ')
dir_file = input('   List for fuzzing: ')

# Gets domain name from the url.
domain = urlparse(input_url).netloc
save_to = f'tf_found/{domain}.txt'

# Reads the txt file and adds them into a list.
with open(dir_file) as f:
    content_list = f.readlines()
list = [x.strip() for x in content_list]


def fuzz(url):
    user_agent = {"User-Agent": random.choice(user_agents)}
    r = requests.get(url, headers=user_agent)

    status_code = r.status_code
    meaning = STATUS_CODES[status_code]

    if status_code in Green_codes:
        print(f'    {C_LGRE}[+]{C_RESET} {url} {C_GRE}[{status_code}/{meaning}]{C_RESET}')
        f = open(save_to, "a+")
        f.write(f'{url} [{status_code}/{meaning}]\n')
        f.close()

    elif status_code in Red_codes:
        print(f'    {C_LRED}[+]{C_LBLA} {url} {C_LRED}[{status_code}/{meaning}]{C_RESET}')

    elif status_code in LRED_codes:
        print(f'    {C_RED}[+]{C_RESET} {url} {C_RED}[{status_code}/{meaning}]{C_RESET}')
        f = open(save_to, "a+")
        f.write(f'{url} [{status_code}/{meaning}]\n')
        f.close()

    elif status_code in Yellow_codes:
        print(f'    {C_LYEL}[+]{C_RESET} {url} {C_YEL}[{status_code}/{meaning}]{C_RESET}')
        f = open(save_to, "a+")
        f.write(f'{url} [{status_code}/{meaning}]\n')
        f.close()

    else:
        print(f'    {C_YEL}[+]{C_CYA} {url} {C_YEL}[{status_code}/{meaning}]{C_RESET}')
        f = open(save_to, "a+")
        f.write(f'{url} [{status_code}/{meaning}]\n')
        f.close()


for dir in list:
    try:
        url = f'{input_url}{dir}'
        FuzzThread = threading.Thread(target=fuzz, args=(url,), daemon=True)  # Starts the fuzzing thread.
        time.sleep(0.15)
        FuzzThread.start()
    except KeyboardInterrupt:  # If user presses CTRL+C it will print "Stopped fuzzing."
        print('    Stopped fuzzing.')
