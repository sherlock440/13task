import unittest
from db import (create_product, get_product_by_id, update_product, delete_product, ProductModel, db)

class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        db.connect()
        db.create_tables([ProductModel], safe=True)

    @classmethod
    def tearDownClass(cls):
        db.drop_tables([ProductModel])
        db.close()

    def setUp(self):
        ProductModel.delete().execute()

    def test_create_product(self):
        product = create_product("Test Product", 99)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 99)

    def test_get_product_by_id(self):
        product = create_product("Test Product", 99)
        fetched_product = get_product_by_id(product.id)
        self.assertIsNotNone(fetched_product)
        self.assertEqual(fetched_product.name, "Test Product")

    def test_update_product(self):
        product = create_product("Test Product", 99)
        update_product(product.id, name="Updated Product", price=89)
        updated_product = get_product_by_id(product.id)
        self.assertEqual(updated_product.name, "Updated Product")
        self.assertEqual(updated_product.price, 89)

    def test_delete_product(self):
        product = create_product("Test Product", 99)
        self.assertTrue(delete_product(product.id))
        self.assertIsNone(get_product_by_id(product.id))

if __name__ == '__main__':
    unittest.main()
