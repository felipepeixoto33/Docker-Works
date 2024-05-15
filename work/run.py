from containers import main, Distribution
import subprocess
import re

def modify_nginx_conf(serv_qnt):
    # Leitura do arquivo nginx.conf
    with open('nginx.conf', 'r') as file:
        nginx_conf = file.read()

    # Encontrar o bloco upstream
    upstream_pattern = re.compile(r'(upstream\s+wordpress\s*{)(.*?)(\n\s*})', re.DOTALL)
    match = upstream_pattern.search(nginx_conf)
    if not match:
        raise ValueError("Bloco 'upstream wordpress' não encontrado no arquivo nginx.conf")

    # Gerar a nova lista de servidores
    servers = '\n'.join([f'    server wordpress-{i+1};' for i in range(serv_qnt)])

    # Substituir o bloco de servidores no bloco upstream
    new_upstream_block = f"{match.group(1)}\n{servers}\n{match.group(3)}"
    new_nginx_conf = upstream_pattern.sub(new_upstream_block, nginx_conf)

    # Escrever de volta ao arquivo nginx.conf
    with open('nginx.conf', 'w') as file:
        file.write(new_nginx_conf)

    print(f"nginx.conf modificado com {serv_qnt} servidores no bloco upstream.")

serv_qnt = int(input("Enter the number of services: "))
dist = str(input("""Enter your distribution (Docker = D [Default], Podman = P): """))
selected_dist = Distribution.Docker

modify_nginx_conf(serv_qnt)

if(dist.upper() == "P"):
    selected_dist = Distribution.Podman

try:
    main(serv_qnt)
except Exception as e:
    print("Error while generating services: ", e)

command = None

if(selected_dist == Distribution.Docker):
    command = f"docker-compose up"
elif(selected_dist == Distribution.Podman):
    command = f"podman compose up"
else:
    print("Invalid distribution!")
    quit(1)

subprocess.run(command, shell=True, check=True)


