def auth():
    with open('Modules/API/github.auth', 'r') as auth:
        info = auth.readline().strip().split(',')
    return (info[0], info[1])
