import uuid
from sqlite3 import IntegrityError

from django.db.utils import IntegrityError
from django.test import TestCase
from products.models import Product
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

        cls.product_1_data = {
            "description": "Smartband XYZ 3.0",
            "price": 100.99,
            "quantity": 2,
        }

        cls.product_2_data = {
            "description": "Smarttv 40p",
            "price": 3000.99,
            "quantity": 6,
        }

        cls.product_1 = Product.objects.create(
            **cls.product_1_data, seller_id=cls.user_1.id
        )

        cls.product_2 = Product.objects.create(
            **cls.product_2_data, seller_id=cls.user_2.id
        )

    def test_product_fields(self):
        print("executando test_product_fields")

        self.assertEqual(
            self.product_1.description, self.product_1_data["description"]
        )
        self.assertEqual(self.product_1.price, self.product_1_data["price"])
        self.assertEqual(
            self.product_1.quantity, self.product_1_data["quantity"]
        )

    def test_uuid_pk(self):
        print("test_uuid_pk_products")

        def is_valid_uuid(uuid_to_test, version=4):
            try:
                uuid_obj = uuid.UUID(str(uuid_to_test), version=version)
            except ValueError:
                return False
            return str(uuid_obj) == str(uuid_to_test)

        self.assertEqual(
            is_valid_uuid(self.product_1.id),
            True,
            msg="Id is not uuid for product",
        )

    def test_quantity_must_be_integer(self):
        print("test_quantity_must_be_integer")

        product_x_data = {
            "description": "Smart",
            "price": 1.99,
            "quantity": -5,
        }

        product_x = Product(**product_x_data, seller_id=self.user_1.id)

        self.assertRaises(IntegrityError, product_x.save)

    def test_many_to_one_relationship_is_made(self):
        print("executando test_many_to_one_relationship_is_made")

        self.assertEqual( self.product_1.seller, self.user_1)

    def test_many_to_one_relationship_with_users(self):
        print("executando test_many_to_one_relationship_with_users")
        print(self.product_2.seller)
        self.product_2.seller = self.user_1
        self.product_2.save()

        self.assertEqual( self.product_2.seller, self.user_1)


