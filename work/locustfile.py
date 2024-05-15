import base64
from locust import HttpUser, task, between

class WordpressUser(HttpUser):

    def on_start(self):
        # Configura a autenticação básica
        self.client.headers = {
            "Authorization": "Basic " + base64.b64encode(b"username:password").decode("utf-8")
        }

    @task
    def post_large_image(self):
        # Simula o envio de um post com uma imagem grande (~1MB)
        with open("/files/big_img.jpg", "rb") as image:
            files = {'file': ('filename.jpg', image, 'image/jpeg')}
            data = {
                'title': 'Post with Large Image',
                'content': 'This is a blog post with a large image.',
                'status': 'publish'
            }
            self.client.post("/wp-json/wp/v2/media", files=files)
            self.client.post("/wp-json/wp/v2/posts", json=data)

    @task
    def post_large_text(self):
        # Simula o envio de um post com texto grande (~400kb)
        large_text = "A" * 400000  # Gerar texto de aprox. 400kb
        data = {
            'title': 'Post with Large Text',
            'content': large_text,
            'status': 'publish'
        }
        self.client.post("/wp-json/wp/v2/posts", json=data)

    @task
    def post_small_image(self):
        # Simula o envio de um post com uma imagem menor (~300kb)
        with open("/files/small_img.jpg", "rb") as image:
            files = {'file': ('filename.jpg', image, 'image/jpeg')}
            data = {
                'title': 'Post with Small Image',
                'content': 'This is a blog post with a small image.',
                'status': 'publish'
            }
            self.client.post("/wp-json/wp/v2/media", files=files)
            self.client.post("/wp-json/wp/v2/posts", json=data)

