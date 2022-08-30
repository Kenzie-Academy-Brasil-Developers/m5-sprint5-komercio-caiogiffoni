from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User


class UserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.base_url_register = reverse("register")
        cls.base_url_login = reverse("login")
    
        cls.user_1_data_seller = {
            "username": "ale",
            "password": "abcd",
            "first_name": "alexandre",
            "last_name": "alves",
            "is_seller": True,
        }

        cls.user_1_data_seller_login = {
            "username": "ale",
            "password": "abcd",
        }

        cls.user_2_data_no_seller = {
            "username": "rod",
            "password": "abcd",
            "first_name": "rodrigo",
            "last_name": "alves",
            "is_seller": False,
        }

        cls.user_2_data_no_seller_login = {
            "username": "rod",
            "password": "abcd",
        }

        cls.user_3_data_seller = {
            "username": "ital",
            "password": "abcd",
            "first_name": "italo",
            "last_name": "queiroz",
            "is_seller": True,
        }

        cls.user_3_seller = User.objects.create_user(**cls.user_3_data_seller)
        cls.token_user_3_seller = Token.objects.create(user=cls.user_3_seller)
        cls.base_url_filter = reverse("filter", args=[cls.user_3_seller.id])
        cls.base_url_filter_admin = reverse("filter_patch_admin", args=[cls.user_3_seller.id])

        cls.user_0_admin={
            "username": "caio",
            "password": "1234",
            "first_name": "caio",
            "last_name": "junior",
        }
        cls.user_0_admin = User.objects.create_superuser(**cls.user_0_admin)
        cls.token_user_0_admin = Token.objects.create(user=cls.user_0_admin)



    def test_can_register_user_seller(self):
        response = self.client.post(
            self.base_url_register, data=self.user_1_data_seller
        )

        expect_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expect_status_code, result_status_code)
        self.assertEqual(
            response.data["username"], self.user_1_data_seller["username"]
        )
        self.assertEqual(
            response.data["first_name"], self.user_1_data_seller["first_name"]
        )
        self.assertEqual(
            response.data["last_name"], self.user_1_data_seller["last_name"]
        )
        self.assertEqual(
            response.data["is_seller"], self.user_1_data_seller["is_seller"]
        )
        self.assertFalse(response.data["is_superuser"])
        self.assertTrue(response.data["is_active"])

        expected_return_fields = (
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_superuser",
            "is_active"
        )
        self.assertEqual(len(response.data.keys()), 7)

        result_return_fields = tuple(response.data.keys())

        self.assertTupleEqual(expected_return_fields, result_return_fields)

    def test_can_register_user_no_seller(self):
        response = self.client.post(
            self.base_url_register, data=self.user_2_data_no_seller
        )

        expect_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(expect_status_code, result_status_code)
        self.assertEqual(
            response.data["username"], self.user_2_data_no_seller["username"]
        )
        self.assertEqual(
            response.data["first_name"],
            self.user_2_data_no_seller["first_name"],
        )
        self.assertEqual(
            response.data["last_name"], self.user_2_data_no_seller["last_name"]
        )
        self.assertEqual(
            response.data["is_seller"], self.user_2_data_no_seller["is_seller"]
        )
        self.assertFalse(response.data["is_superuser"])
        self.assertTrue(response.data["is_active"])


        expected_return_fields = (
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_superuser",
            "is_active"
        )
        self.assertEqual(len(response.data.keys()), 7)

        result_return_fields = tuple(response.data.keys())

        self.assertTupleEqual(expected_return_fields, result_return_fields)

    def test_can_register_with_wrong_keys(self):
        response = self.client.post(self.base_url_register, data={})

        expect_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expect_status_code, result_status_code)
        self.assertEqual(
            response.data["username"][0], "This field is required."
        )
        self.assertEqual(
            response.data["password"][0], "This field is required."
        )
        self.assertEqual(
            response.data["first_name"][0], "This field is required."
        )
        self.assertEqual(
            response.data["last_name"][0], "This field is required."
        )

    def test_can_login_1(self):
        response = self.client.post(
            self.base_url_register, data=self.user_1_data_seller
        )

        response = self.client.post(
            self.base_url_login, data=self.user_1_data_seller_login
        )

        expect_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expect_status_code, result_status_code)
        self.assertIn("token", response.data)

    def test_can_login_2(self):
        response = self.client.post(
            self.base_url_register, data=self.user_2_data_no_seller
        )
        response = self.client.post(
            self.base_url_login, data=self.user_2_data_no_seller_login
        )

        expect_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expect_status_code, result_status_code)
        self.assertIn("token", response.data)

    def test_can_login_with_wrong_keys(self):
        response = self.client.post(
            self.base_url_login, data=self.user_1_data_seller_login
        )

        expect_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(expect_status_code, result_status_code)
        self.assertIn("non_field_errors", response.data)

    def test_can_not_edit_info_from_other_user(self):
        response = self.client.post(
            self.base_url_register, data=self.user_2_data_no_seller
        )
        response = self.client.post(
            self.base_url_login, data=self.user_2_data_no_seller_login
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + response.data['token'])
        response_other_user = self.client.patch(
            self.base_url_filter, data={
                "username": "alterado",
            }
        )

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response_other_user.status_code

        self.assertEqual(len(response_other_user.data.keys()), 1)
        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(
            response_other_user.data["detail"], "You do not have permission to perform this action."
        )

    def test_can_edit_info_from_same_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_3_seller.key)
        response = self.client.patch(
            self.base_url_filter, data={
                "username": "alterado",
            }
        )

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(len(response.data.keys()), 8)
        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(
            response.data["username"], "alterado"
        )
        expected_return_fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        )

        result_return_fields = tuple(response.data.keys())

        self.assertTupleEqual(expected_return_fields, result_return_fields)

    def test_can_not_edit_is_active_info_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_3_seller.key)
        response = self.client.patch(
            self.base_url_filter, data={
                "is_active": False,
            }
        )

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(len(response.data.keys()), 8)
        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(
            response.data["is_active"], True
        )
        expected_return_fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
            "is_superuser",
        )

        result_return_fields = tuple(response.data.keys())

        self.assertTupleEqual(expected_return_fields, result_return_fields)

    def test_admin_can_edit_is_active_info_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_0_admin.key)
        response = self.client.patch(
            self.base_url_filter_admin, data={
                "is_active": False,
            }
        )

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(len(response.data.keys()), 7)
        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(
            response.data["is_active"], False
        )
        expected_return_fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "is_seller",
            "date_joined",
            "is_active",
        )

        result_return_fields = tuple(response.data.keys())

        self.assertTupleEqual(expected_return_fields, result_return_fields)
