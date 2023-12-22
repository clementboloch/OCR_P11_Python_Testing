from locust import HttpUser, task, between

class ClubUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def view_index(self):
        with self.client.get("/", catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure("initial loading lasts more than 2 seconds")

    @task(3)
    def view_summary(self):
        with self.client.post("/showSummary", {"email": "john@simplylift.co"}, catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure("initial loading lasts more than 5 seconds")

    @task
    def book_competition(self):
        self.client.get("/book/Spring%20Festival/Simply%20Lift")
        with self.client.get("/book/Spring%20Festival/Simply%20Lift", catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure("initial loading lasts more than 5 seconds")

    @task
    def purchase_places(self):
        with self.client.post("/purchasePlaces", {"competition": "Spring Festival", "club": "Simply Lift", "places": "1"}, catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure("initial loading lasts more than 5 seconds")

