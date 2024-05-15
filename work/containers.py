from jinja2 import Environment, FileSystemLoader, environment
from service import Service
from enum import Enum

class Distribution(Enum):
    Docker = 1
    Podman = 2

def create_wordpress_services(services_qnt: int, default_host_port: int = 8080, container_port: int = 80):
    services = []
    for i in range(services_qnt):
        serv = Service(f"wordpress-{i+1}", "docker.io/library/wordpress:5.4.2-php7.2-apache", default_host_port+(i), container_port)
        serv.add_dependency(nginx_serv)
        serv.add_dependency(mysql_serv)
        services.append(serv)
    return services

def main(serv_qnt: int = 3):
    services = [nginx_serv, mysql_serv]
    services += create_wordpress_services(serv_qnt, default_host_port=(8080+len(services)))

    env = Environment(loader=FileSystemLoader('.'))

    template = env.get_template('docker-compose-template.yml.j2')
    rendered_template = template.render(services=services)

    with open('docker-compose.yml', 'w') as f:
        f.write(rendered_template)

    print("Docker Compose file generated successfully!")

    def run(serv_qnt: int = 3, distribution: Distribution = Distribution.Docker):
        if(distribution == Distribution.Docker):
            command = f"docker"

nginx_serv = Service("nginx", "docker.io/library/nginx:1.19.0", 80, 80)
mysql_env = {"MYSQL_ROOT_PASSWORD": "pwd-wordpress", "MYSQL_DATABASE": "wordpress", "MYSQL_USER": "usr-wordpress"}
mysql_serv = Service("mysql", "docker.io/library/mysql:5.7", 8081, 80, environment=mysql_env)
 
