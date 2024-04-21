from pyman import POST
from postman import Postman

tokens = [
    '#',
    'GET',
    'HTTP',
    'POSTMAN'
]

commands = {} 

def execute(cmd, args, status, cache):
    if cmd == "GET":
        print(f'Get request to {args}')
        return 200
    
    elif cmd == "HTTP":
        print(f'Assert {args} == {status}')
        return 0 
    
    elif cmd == "POSTMAN":
        print(f'Exporting to Postman: {cache} with the tile "{args}"')
        return 0

    elif cmd == "#":
        print("comment")
        return 0


status = 0
cache = []

with open('request.leo') as f:
    for line in f:
        if line.strip():
            l = line.split(" ", 1)
            cmd = l[0]
            args = l[1].strip()
            
            if cmd in tokens:
                if cmd == "GET":
                    cache = [cmd, args]

                status = execute(cmd, args, status, cache)

