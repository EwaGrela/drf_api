import json
from django.test import TestCase, Client
from django.urls import reverse

from .models import Car, Rate


class PostCarsTest(TestCase):
    """ Test module for inserting a car """

    def setUp(self):
        self.client = Client()
        self.valid_data = {"make": "toyota", "model": "Camry"}
        self.invalid_data = {"make": "Fiat", "model": "Qwerty123"}
        self.faulty_data = "string"
        self.empty_list = []
        self.empty_dict = {}
        self.faulty_dict = {"car_name": "fiat", "model": "500"}

    def test_create_valid_car(self):
        "Car with specified make and model is found in external API and written to database"
        response = self.client.post(
            reverse('cars'),
            data=json.dumps(self.valid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    def test_create_invalid_car(self):
        response = self.client.post(
            reverse('cars'),
            data=json.dumps(self.invalid_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_faulty_data(self):
        response = self.client.post(
            reverse('cars'),
            data=json.dumps(self.faulty_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_empty_list(self):
        response = self.client.post(
            reverse('cars'),
            data=json.dumps(self.empty_list),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_empty_dict(self):
        response = self.client.post(
            reverse('cars'),
            data=json.dumps(self.empty_dict),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_faulty_dict(self):
        response = self.client.post(
            reverse('cars'),
            data=json.dumps(self.faulty_dict),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)


class GetCarsTest(TestCase):
    """ Test module for checking cars from our DB """

    def setUp(self):
        self.client = Client()
        self.corolla = Car.objects.create(make="toyota", model="Corolla",
                                          sum_rates=25, average_rate=5,
                                          number_of_rates=5)

        self.civic = Car.objects.create(make="honda", model="Civic")
        self.avensis = Car.objects.create(make="toyota", model="Avensis",
                                          sum_rates=18, average_rate=3,
                                          number_of_rates=6)

    def test_get_all_cars(self):
        response = self.client.get(reverse('cars'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)


class GetPopularTest(TestCase):
    """Test module for checking cars by popularity"""

    def setUp(self):
        self.client = Client()
        self.clio = Car.objects.create(make="renault", model="Clio",
                                       sum_rates=30, average_rate=3,
                                       number_of_rates=10)

        self.accord = Car.objects.create(make="honda", model="Accord")
        self.camry = Car.objects.create(make="toyota", model="Camry",
                                        sum_rates=18, average_rate=1,
                                        number_of_rates=18)

    def test_get_popular(self):
        response = self.client.get(reverse('popular'))
        self.assertEqual(response.data[0]["model"], "Camry")
        self.assertEqual(response.status_code, 200)


class PostRateTest(TestCase):
    """
    Test module for rating cars
    """

    def setUp(self):
        self.client = Client()
        self.uno = Car.objects.create(make="FIAT", model="Uno")
        self.picanto = Car.objects.create(make="KIA", model="Picanto")
        self.avensis = Car.objects.create(make="TOYOTA", model="Avensis")
        self.to_post = [
            {"make": "kia", "model": "Picanto", "score": 3},
            {"make": "kia", "model": "Picanto", "score": 4},
            {"make": "kia", "model": "Picanto", "score": 2},
            {"make": "toyota", "model": "Avensis", "score": 5},
            {"make": "toyota", "model": "Avensis", "score": 4},
            {"make": "fiat", "model": "Uno", "score": 3},
            {"make": "fiat", "model": "Uno", "score": 2}
        ]

    def test_post_rate(self):
        # check existing cars and their rating via /car endpoint
        response = self.client.get(reverse('cars'))
        self.assertEqual(len(response.data), 3)
        # they all should have 0 rating
        for i in range(3):
            self.assertEqual(response.data[i]["average_rate"], 0)

        # post ratings for cars:

        for i in range(len(self.to_post)):
            response = self.client.post(
                reverse("rate"),
                data=json.dumps(self.to_post[i]),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
        # checking if anything changed
        response = self.client.get(reverse('cars'))
        self.assertEqual(len(response.data), 3)
        for row in response.data:
            if row.get("make") == "KIA":
                self.assertEqual(row["average_rate"], 3.0)
            if row.get("make") == "TOYOTA":
                self.assertEqual(row["average_rate"], 4.5)
            if row.get("make") == "FIAT":
                self.assertEqual(row["average_rate"], 2.5)

    def test_post_invalid_rate(self):
        "Checks for posting in wrong data"
        # non-existent car
        non_existent_rate = {"make": "honda", "model": "4556", "score": 1}
        response = self.client.post(
            reverse("rate"),
            data=json.dumps(non_existent_rate),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

        # wrong data formats:
        wrong_keys_rate = {"make": "honda", "score": 1}
        response = self.client.post(
            reverse("rate"),
            data=json.dumps(wrong_keys_rate),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

        empty_dict_rate = {}
        response = self.client.post(
            reverse("rate"),
            data=json.dumps(empty_dict_rate),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

        empty_list_rate = []
        response = self.client.post(
            reverse("rate"),
            data=json.dumps(empty_list_rate),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

        string_rate = "string rate"
        response = self.client.post(
            reverse("rate"),
            data=json.dumps(string_rate),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

        # good format, but score out of range:
        wrong_score_rate = {"make": "fiat", "model": "Uno", "score": 10}

        response = self.client.post(
            reverse("rate"),
            data=json.dumps(wrong_score_rate),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

        response = self.client.get(reverse("cars"))

        # post data in right format, car exists in external API, but does not exist in internal db:
        # check what car makes are in db
        response = self.client.get(reverse("cars"))
        non_available_rate = {"make": "honda", "model": "Accord", "score": 3}
        available_makes = [row["make"] for row in response.data]
        self.assertTrue("honda" not in available_makes)

        # post valid json but such car is not in db:
        response = self.client.post(
            reverse("rate"),
            data=json.dumps(non_available_rate),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 404)

    def test_post_case_sensitivity(self):
        "Check if posting is case sensitive"
        to_post = {"make": "honda", "model": "Civic"}
        # check what is in DB
        response = self.client.get(reverse("cars"))
        self.assertEqual(len(response.data), 3)
        available_models = [row["model"] for row in response.data]
        self.assertTrue("Civic" not in available_models)
        # post new make"
        response = self.client.post(
            reverse("cars"),
            data=json.dumps(to_post),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        # See what available makes are:
        response = self.client.get(reverse("cars"))
        available_makes = [row["make"] for row in response.data]
        self.assertTrue("HONDA" in available_makes)

        # define two jsons with differently 'cased' makes and post
        rate1 = {"make": "HONDA", "model": "Civic", "score": 4}
        response = self.client.post(
            reverse("rate"),
            data=json.dumps(rate1),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        rate2 = {"make": "honda", "model": "Civic", "score": 2}
        response = self.client.post(
            reverse("rate"),
            data=json.dumps(rate2),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse("cars"))
        civic = [item for item in response.data if item["model"] == "Civic"][0]

        # assert honda Civic was rated twice, has average rate 3
        self.assertEqual(civic["average_rate"], 3)
        self.assertEqual(civic["number_of_rates"], 2)


class IntegrationTest(TestCase):
    """
    'Integration test which verifies if the whole process in API goes as specified
    """

    def setUp(self):
        self.client = Client()
        self.to_post = [{"make": "fiat", "model": "500"},
                        {"make": "fiat", "model": "500L"},
                        {"make": "fiat", "model": "Strada"}

                        ]

        self.to_rate = [
            {"make": "FIAT", "model": "500L", "score": 3},
            {"make": "FIAT", "model": "500L", "score": 4},
            {"make": "FIAT", "model": "500L", "score": 2},
            {"make": "FIAT", "model": "500", "score": 5},
            {"make": "FIAT", "model": "500", "score": 4},
            {"make": "FIAT", "model": "Strada", "score": 5},
        ]

    def test_whole_process(self):
        # GET request to /cars - check there are no cars
        no_cars = self.client.get(reverse('cars'))
        self.assertEqual(no_cars.status_code, 200)
        self.assertEqual(len(no_cars.data), 0)
        self.assertTrue(isinstance(no_cars.data, list))

        # post several cars in a loop
        # POST request to /cars
        # GET request to /cars - check if created succesfully and obtained from
        # db
        for i in range(len(self.to_post)):
            response = self.client.post(
                reverse('cars'),
                data=json.dumps(self.to_post[i]),
                content_type="application/json"
            )
            self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('cars'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

        # verify if all have 0 ratings, 0 sum and 0 average
        for i in range(len(response.data)):
            self.assertEqual(response.data[i]["sum_rates"], 0)
            self.assertEqual(response.data[i]["average_rate"], 0)
            self.assertEqual(response.data[i]["number_of_rates"], 0)

        # simulate several rating processes
        # POST request to /rate
        for i in range(len(self.to_rate)):
            response = self.client.post(
                reverse('rate'),
                data=json.dumps(self.to_rate[i]),
                content_type="application/json"
            )

            self.assertEqual(response.status_code, 200)

        # check if successfull and cars were rated:
        # GET request to /cars
        response_cars = self.client.get(reverse('cars'))
        self.assertEqual(response_cars.status_code, 200)
        self.assertEqual(len(response_cars.data), 3)
        for row in response_cars.data:
            if row["model"] == "500":
                self.assertEqual(row["average_rate"], 4.5)
                self.assertEqual(row["number_of_rates"], 2)
            if row["model"] == "500L":
                self.assertEqual(row["average_rate"], 3)
                self.assertEqual(row["number_of_rates"], 3)
            if row["model"] == "Strada":
                self.assertEqual(row["average_rate"], 5)
                self.assertEqual(row["number_of_rates"], 1)

        # check if they are sorted differently if sorted explicitely by popularity
        # GET request to /popular
        response_popular = self.client.get(reverse('popular'))

        # verify it has same length as response_cars
        self.assertEqual(response_popular.status_code, 200)
        self.assertEqual(len(response_popular.data), 3)

        # verifiy it was sorted by popularity (most rates) not by highest average
        # 500l was most popular:
        # average rate is lowest, but most rates
        self.assertEqual(response_popular.data[0]["number_of_rates"], 3)
        self.assertEqual(response_popular.data[0]["average_rate"], 3)
        self.assertEqual(response_popular.data[0]["model"], "500L")

        self.assertEqual(response_popular.data[1]["number_of_rates"], 2)
        self.assertEqual(response_popular.data[1]["average_rate"], 4.5)
        self.assertEqual(response_popular.data[1]["model"], "500")

        # Strada was least popular, but average_rate was highest
        self.assertEqual(response_popular.data[2]["number_of_rates"], 1)
        self.assertEqual(response_popular.data[2]["average_rate"], 5)
        self.assertEqual(response_popular.data[2]["model"], "Strada")
