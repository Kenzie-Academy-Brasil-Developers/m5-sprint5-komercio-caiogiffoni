import uuid
from decimal import Decimal

from django.urls import reverse
from products.models import Product
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from users.models import User


class ProductViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.list_create_product = reverse("list_create_product")

        cls.user_1_data_seller = {
            "username": "ale",
            "password": "abcd",
            "first_name": "alexandre",
            "last_name": "alves",
            "is_seller": True,
        }

        cls.user_2_data_no_seller = {
            "username": "rod",
            "password": "abcd",
            "first_name": "rodrigo",
            "last_name": "alves",
            "is_seller": False,
        }

        cls.user_3_data_seller = {
            "username": "ravel",
            "password": "abcd",
            "first_name": "ravel",
            "last_name": "alves",
            "is_seller": True,
        }

        cls.product_1_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 2
        }

        cls.product_2_data = {
            "description": "Smart ABC 1.0",
            "price": 10.99,
            "quantity": -2
        }
        
        user_1_seller = User.objects.create_user(**cls.user_1_data_seller)
        cls.token_user_1_seller = Token.objects.create(user=user_1_seller)

        user_2_no_seller = User.objects.create_user(**cls.user_2_data_no_seller)
        cls.token_user_2_no_seller = Token.objects.create(user=user_2_no_seller)

        user_3_seller = User.objects.create_user(**cls.user_3_data_seller)
        cls.token_user_3_seller = Token.objects.create(user=user_3_seller)

        cls.product_1 = Product.objects.create(**cls.product_1_data, seller=user_1_seller)

        cls.base_url_filter_patch = reverse("filter_patch_products", args=[cls.product_1.id])

    def test_can_create_product_with_seller(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_1_seller.key)
        response = self.client.post(
            self.list_create_product, data=self.product_1_data
        )

        expected_status_code = status.HTTP_201_CREATED
        result_status_code = response.status_code

        self.assertEqual(len(response.data.keys()), 6)

        self.assertEqual(expected_status_code, result_status_code)
        self.assertIn('id', response.data)
        self.assertIn('seller', response.data)
        self.assertTrue( response.data["is_active"])
        self.assertEqual(
            response.data["description"], self.product_1_data["description"]
        )
        self.assertEqual(
            float(response.data["price"]), self.product_1_data["price"]
        )
        self.assertEqual(
            response.data["quantity"], self.product_1_data["quantity"]
        )

        expected_return_fields = (
            "id",
            "seller",
            "price",
            "quantity",
            "description",
            "is_active",
        )

        result_return_fields = tuple(response.data.keys())

        self.assertTupleEqual(expected_return_fields, result_return_fields)

        self.assertEqual(len(response.data['seller'].keys()), 8)

    def test_can_not_create_product_with_no_seller(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_2_no_seller.key)
        response = self.client.post(
            self.list_create_product, data=self.product_1_data
        )

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(response.data['detail'], "You do not have permission to perform this action.")

    def test_can_not_edit_product_from_other_seller(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_3_seller.key)
        
        response = self.client.patch(
            self.base_url_filter_patch, data={
                "description": "New Description"                
            }
        )

        expected_status_code = status.HTTP_403_FORBIDDEN
        result_status_code = response.status_code

        self.assertEqual(len(response.data.keys()), 1)
        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(
            response.data["detail"], "You do not have permission to perform this action."
        )

    def test_can_edit_product_from_same_seller(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_1_seller.key)
        
        response = self.client.patch(
            self.base_url_filter_patch, data={
                "description": "New Description"                
            }
        )

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(len(response.data.keys()), 6)
        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(
            response.data["description"], "New Description"  
        )
        self.assertEqual(
            response.data["id"], str(self.product_1.id)
        )

        expected_return_fields = (
            "id",
            "seller",
            "price",
            "quantity",
            "description",
            "is_active",
        )

        result_return_fields = tuple(response.data.keys())

        self.assertTupleEqual(expected_return_fields, result_return_fields)

    def test_can_list_products_with_no_token(self):
        response = self.client.get(
            self.list_create_product, data=self.product_1_data
        )

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(expected_status_code, result_status_code)
        self.assertIn('results', response.data)

        self.assertEqual(len(response.data['results'][0].keys()), 5)

        self.assertEqual(expected_status_code, result_status_code)
        expected_return_fields = (
            "description",
            "price",
            "quantity",
            "is_active",
            "seller",
        )

        #seller has only id (uuid), not whole user
        self.assertFalse(type(response.data['results'][0]['seller']) == dict)

        result_return_fields = tuple(response.data['results'][0].keys())

        self.assertTupleEqual(expected_return_fields, result_return_fields)

    def test_can_filter_products_with_no_token(self):
        response = self.client.get(self.base_url_filter_patch)

        expected_status_code = status.HTTP_200_OK
        result_status_code = response.status_code

        self.assertEqual(len(response.data.keys()), 5)

        self.assertEqual(expected_status_code, result_status_code)
        expected_return_fields = (
            "description",
            "price",
            "quantity",
            "is_active",
            "seller",
        )

        result_return_fields = tuple(response.data.keys())

        self.assertTupleEqual(expected_return_fields, result_return_fields)

        self.assertEqual(len(response.data['seller'].keys()), 8)

    def test_ca_not_create_product_with_no_body(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_1_seller.key)
        response = self.client.post(
            self.list_create_product, data={}
        )

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(len(response.data.keys()), 3)

        self.assertEqual(expected_status_code, result_status_code)
        expected_return_fields = (
            "price",
            "quantity",
            "description",
        )

        for field in expected_return_fields:
            self.assertEqual(response.data[field], ["This field is required."])

        result_return_fields = tuple(response.data.keys())

        self.assertTupleEqual(expected_return_fields, result_return_fields)

    def test_can_not_create_product_with_negative_quantity(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_user_1_seller.key)
        response = self.client.post(
            self.list_create_product, data=self.product_2_data
        )

        expected_status_code = status.HTTP_400_BAD_REQUEST
        result_status_code = response.status_code

        self.assertEqual(len(response.data.keys()), 1)

        self.assertEqual(expected_status_code, result_status_code)
        self.assertEqual(response.data["quantity"], ["Ensure this value is greater than or equal to 0."])
    