from locust import HttpUser, task


class User(HttpUser):

    @task(2)
    def get_list_doctor(self):
        self.client.get('/api/Doctors?from=0&count=1', headers={
            'Authorization': f'Bearer {self.token}'
        })

    @task(1)
    def get_me(self):
        self.client.get('/api/Accounts/Me', headers={
            'Authorization': f'Bearer {self.token}'
        })

    @task(2)
    def validate(self):
        self.client.get('/api/Authentication/Validate', headers={
            'Authorization': f'Bearer {self.token}'
        })

    def on_start(self):
        response = self.client.post('/api/Authentication/SignIn', json={
            'username': 'user',
            'password': 'user'
        })
        self.token = response.json().get('access_token')
