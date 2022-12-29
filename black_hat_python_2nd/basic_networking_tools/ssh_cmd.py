import paramiko

def ssh_command(ip, port, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=username, password=password)
    
    (_, stdout, stderr) = client.exec_command(command)
    
    output = stdout.readlines() + stderr.readlines()
    if output:
        print('--- Output ---')
        for line in output:
            print(line.strip())

if __name__ == '__main__':
    import getpass
    
    username = input('Username: ')
    password = getpass.getpass()
    ip = input('Enter server IP: ')
    port = input('Enter port or <CR>: ')
    command = input('Enter command or <CR>: ')

    ssh_command(ip, port, username, password, command)