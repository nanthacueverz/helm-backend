from locust import HttpUser, TaskSet, task, between
class ArticleTasks(TaskSet):
    def on_start(self):
        # Create an article and get its ID
        response = self.client.post("/add", json={
            "title": "Test Article",
            "body": "This is a test article."
        })
        self.article_id = response.json()["id"]
    @task(1)
    def get_articles(self):
        self.client.get("/get")
    @task(2)
    def get_article(self):
        self.client.get(f"/get/{self.article_id}")
    @task(3)
    def update_article(self):
        self.client.put(f"/update/{self.article_id}", json={
            "title": "Updated Test Article",
            "body": "This is an updated test article."
        })
    @task(4)
    def delete_article(self):
        self.client.delete(f"/delete/{self.article_id}")
        # Recreate the article after deleting
        response = self.client.post("/add", json={
            "title": "Test Article",
            "body": "This is a test article."
        })
        self.article_id = response.json()["id"]
class WebsiteUser(HttpUser):
    tasks = [ArticleTasks]
    wait_time = between(1, 5)
if __name__ == "__main__":
    import os
    os.system("locust -f locustfile.py")