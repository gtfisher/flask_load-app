rom flask import Flask
from collections import Counter
import json
import random
import threading
import time
import platform


result = None

def background_calculation(n):
    # here goes some long calculation
    time.sleep(n)

    # when the calculation is done, the result is stored in a global variable
    global result
    result = 42

def busy_wait(n):

    start = time.time()
    print('n is:', n)
    thread = threading.Thread(target=background_calculation(n))
    thread.start()

    # wait here for the result to be available before continuing
    while result is None:
        pass

    end = time.time()
    payload = {'start': start, 'end': end, 'n': n, 'dur': end-start}
    return json.dumps(payload)


app = Flask(__name__)
@app.route('/')
def hello_world():
  return 'Hello from Flask!'

@app.route('/random/<rand_str>')
def get_random(rand_str):
  r = random.randint(-1, 2)
  return  busy_wait(int(rand_str)+r)

@app.route('/countme/<input_str>')
def count_me(input_str):
    input_counter = Counter(input_str)
    response = []
    for letter, count in input_counter.most_common():
            response.append('"{}": {}'.format(letter, count))
    return '<br>'.join(response)
    
    
if __name__ == '__main__':
  app.run(dubug=True, host='0.0.0.0')
    
