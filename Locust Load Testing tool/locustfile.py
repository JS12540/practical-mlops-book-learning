from locust import HttpUser, task, between

class ApiUser(HttpUser):
    # Wait time between tasks (simulates real users)
    wait_time = between(1, 3)

    @task(2)
    def get_posts(self):
        """
        Fetch all posts
        """
        self.client.get("/posts")

    @task(1)
    def get_single_post(self):
        """
        Fetch a single post
        """
        self.client.get("/posts/1")

    @task(1)
    def create_post(self):
        """
        Create a new post
        """
        payload = {
            "title": "Load testing with Locust",
            "body": "This is a test post",
            "userId": 1
        }
        self.client.post("/posts", json=payload)
