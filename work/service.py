class Service:
    def __init__(self, name: str, image: str, host_port: int, container_port: int, depends_on=None, environment=None):
        self.name = name
        self.image = image
        self.host_port = host_port
        self.container_port = container_port
        self.dependencies = depends_on if depends_on is not None else []
        self.environment = environment if environment is not None else []

    def add_dependency(self, service):
        self.dependencies.append(service.name)

    def get_service_template(self):
        template = {
            "name": self.name,
            "image": self.image,
            "host_port": self.host_port,
            "container_port": self.container_port,
            "depends_on": self.dependencies
        }
        return template

