import json


# read file lines
program_lines = []
with open("request.leo") as f:
    program_lines = [line.strip() for line in f]

tokens = ['GET', "HTTP", "POSTMAN"]
program = []
token_counter = 0
some_string = ""

for line in program_lines:
    parts  = line.split(" ")

    if parts[0] in tokens:

        # save sting if there is one
        if len(some_string) > 0:
            program.append(some_string)
            token_counter += 1
            some_string = ""
        
        opcode = parts[0]

        # check for empty line
        if opcode == "":
            continue

        # store opcode token
        program.append(opcode)
        token_counter += 1
        # handle each opcode
        if opcode == "GET":
            # expecting a url 
            url = parts[1]
            program.append(url)
            token_counter += 1
        elif opcode == "HTTP":
            # expecting a number
            number = int(parts[1])
            program.append(number)
            token_counter += 1
        elif opcode == "POSTMAN":
            title = line.split(" ", 1)[1]
            program.append(title)
            token_counter += 1
    else:
        some_string += line
    
# add strings in case the text is by the end of the file
if len(some_string) > 0:
    program.append(some_string)
    token_counter += 1

# program.append('END')

for p in program:
    print(p)

print("token_counter:", token_counter)


class Stack:

    def __init__(self, size):
        self.buf = [0 for _ in range(size)]
        self.sp    = -1

    def push(self, number):
        self.sp += 1
        self.buf[self.sp] = number
    
    def pop(self):
        number = self.buf[self.sp]
        self.sp -= 1
        return number
    
    def top(self):
        return self.buf[self.sp]

def run(params):
    print(params)


pc = 0
# stack = Stack(256)

params = {}

print(len(program))
while pc < len(program):
    opcode = program[pc]
    pc += 1

    if opcode == "GET":
        if params != {}:
            run(params)
            params = {}
        
        params['request'] = opcode
        params['url'] = program[pc]
        pc += 1

    elif opcode == "HTTP":
        params['http'] = program[pc]
        pc += 1

    elif opcode == "POSTMAN":
        params['postman'] = program[pc]
        pc += 1

    else:
        # is it json?
        try:
            body = json.loads(opcode)
            params['body'] = body
        except Exception as e:
            print(f'Error in line {pc-1}')
            print(e)


# take into account the last run
if params != {}:
    run(params)

# GET
# command = GET
# check if the stack has a request
#   if it does, execute it
# reset stack = []
# save the type of command in an array stack['command'] = 'GET'
# get the url
# validate the url
# save the url in an array stack['url'] = url

# HTTP
# command = HTTP
# get the parameter
# save http-status in stack[http] = int

# POSTMAN
# command = POSTMAN
# get the paramater (title)
# will use get stack['command']
# will use get stack['url']

# POST
# command = POST
# check the stack, and see that there is a GET command from avobe
#   execute and puts the result in an array stack[request response]
#   notes there is an HTTP command and checks the stack[response][status] field with the stack.http-status
#   notes there is a POSTMAN command and exports to postman
# reset the stack = []
# save the type of command in an array stack['command'] = 'POST'
# get the url 
# validate the url
# save the url in an array stack['url'] = url

# HTTP
# command = HTTP
# get the parameter
# save http-status in stack[http] = int

# JSON
# check that there is an arbitrary string
# check if it is a json
# save json to stack[body] = json 

# since it is end of file, try running the stack

# stack = {
#    'request_type': 'GET',
#    'url': 'http://test.com',
#    'http_status': 200,
#    'postman_title': 'The title',
#    'body': {"hola": "mundo"}
#}