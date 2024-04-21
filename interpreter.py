import json

def print_json_error(string, pos):
#{"hello": "world","hola": "mundo,"some": {"more": "complex"},"count": 0}
    new_string = string[:pos-1] + '\033[1;37;40m' 
    new_string += '\033[0;37;41m'+ string[pos-1:pos] 
    new_string += '\033[1;37;40m' + string[pos:]
    print(new_string)

# read file lines
program_lines = []
with open("request.leo") as f:
    program_lines = [line.strip() for line in f]

tokens = ['GET', "HTTP", "POSTMAN"]
program = []
token_counter = 0
arbitrary_string = ""

for line_number, line in enumerate(program_lines):
    parts  = line.split(" ")

    if parts[0] in tokens:

        # save arbitrary string if there is one
        if len(arbitrary_string) > 0:
            try:
                body = json.loads(arbitrary_string)
                program.append(body)
                token_counter += 1
                arbitrary_string = ""
            except json.decoder.JSONDecodeError as e:
                print(f'Invalid json:')
                print(e.msg)
                print_json_error(arbitrary_string, e.pos)
                exit()

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
            try:
                url = parts[1]
                if url.startswith("http://") or url.startswith("https://"):
                    program.append(url)
                    token_counter += 1
                else:
                    raise Exception
            except:
                print(f'Error in line ({line_number + 1}): Invalid url')
                print(f'>>> {line}')
                exit()

        elif opcode == "HTTP":
            # expecting a number
            try:
                number = int(parts[1])
                program.append(number)
                token_counter += 1
            except:
                print(f'Error in line ({line_number + 1}): Number was expected.') 
                print(f'>>> {line}')
                exit()
            
        
        elif opcode == "POSTMAN":
            try:
                title = line.split(" ", 1)[1]
                program.append(title)
                token_counter += 1
            except:
                print(f'Error in line ({line_number + 1}): String was expected')
                print(f'>>> {line}')
                exit()

    else:
        arbitrary_string += line
    
    
# add strings in case the text is by the end of the file
if len(arbitrary_string) > 0:
    try:
        body = json.loads(arbitrary_string)
        program.append(body)
        token_counter += 1
    except json.decoder.JSONDecodeError as e:
        print(f'Invalid json:')
        print(e.msg)
        print_json_error(arbitrary_string, e.pos)
        exit()

#for p in program:
#    print(p)



def run(params):
    print(params)


pc = 0
params = {}

while pc < len(program):
    opcode = program[pc]
    pc += 1

    if opcode == "GET":
        # the request should be the first instruction of a block
        # if a new block is starting, try to execute the previous block
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
        # arbitrary string
        params['body'] = opcode


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