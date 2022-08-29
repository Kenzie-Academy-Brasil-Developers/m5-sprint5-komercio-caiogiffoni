import uuid

from django.test import TestCase
from users.models import User


class UserTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.user_1_data_seller = {
            "username": "ale",
            "password": "abcd",
            "first_name": "alexandre",
            "last_name": "alves",
            "is_seller": True,
        }

        cls.user_2_data = {
            "username": "rod",
            "password": "abcd",
            "first_name": "rodrigo",
            "last_name": "portela",
        }

        cls.user_1 = User.objects.create_user(**cls.user_1_data_seller)

        cls.user_2 = User.objects.create_user(**cls.user_2_data)

    def test_user_fields_1(self):
        print("executando test_user_fields_1")

        self.assertEqual(self.user_1.username, self.user_1_data_seller["username"])
        self.assertEqual(
            self.user_1.first_name, self.user_1_data_seller["first_name"]
        )
        self.assertEqual(self.user_1.last_name, self.user_1_data_seller["last_name"])
        self.assertEqual(self.user_1.is_seller, self.user_1_data_seller["is_seller"])

    def test_user_fields_2(self):
        print("executando test_user_fields_2")

        self.assertEqual(self.user_2.username, self.user_2_data["username"])
        self.assertEqual(
            self.user_2.first_name, self.user_2_data["first_name"]
        )
        self.assertEqual(self.user_2.last_name, self.user_2_data["last_name"])
        self.assertEqual(self.user_2.is_seller, False)


    def test_first_name_max_length(self):
        print("test_first_name_max_length")
        expected_max_length = 50
        result_max_length = self.user_1._meta.get_field(
            "first_name"
        ).max_length
        msg = "Vefique o max_length de `first_name`"
        self.assertEqual(result_max_length, expected_max_length, msg)
    
    def test_last_name_max_length(self):
        print("test_last_name_max_length")
        expected_max_length = 50
        result_max_length = self.user_1._meta.get_field(
            "last_name"
        ).max_length
        msg = "Vefique o max_length de `last_name`"

        self.assertEqual(result_max_length, expected_max_length, msg)

    def test_uuid_pk(self):
        print("test_uuid_pk")

        def is_valid_uuid(uuid_to_test, version=4):
            try:
                uuid_obj = uuid.UUID(str(uuid_to_test), version=version)
            except ValueError:
                return False
            return str(uuid_obj) == str(uuid_to_test)

        self.assertEqual(is_valid_uuid(self.user_1.id), True, msg="Id is not uuid")