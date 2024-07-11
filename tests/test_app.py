import unittest
import json
from app import app
from db import db, ProductModel

class TestApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        cls.client = app.test_client()
        db.connect()
        db.create_tables([ProductModel], safe=True)

    @classmethod
    def tearDownClass(cls):
        db.drop_tables([ProductModel])
        db.close()

    def setUp(self):
        ProductModel.delete().execute()

    def test_get_products(self):
        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_create_product(self):
        response = self.client.post('/api/products', json={"name": "Test Product", "price": 99})
        self.assertEqual(response.status_code, 201)
        data = response.json
        self.assertIn("productId", data)
        self.assertEqual(data["message"], "Product added successfully.")

        product_id = data["productId"]
        product = ProductModel.get_by_id(product_id)
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 99)

    def test_get_product_by_id(self):
        product = ProductModel.create(name="Test Product", price=99)
        response = self.client.get(f'/api/products/{product.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["name"], "Test Product")

    def test_update_product(self):
        product = ProductModel.create(name="Test Product", price=99)
        response = self.client.patch(f'/api/products/{product.id}', json={"name": "Updated Product", "price": 89})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Product updated successfully.")

        updated_product = ProductModel.get_by_id(product.id)
        self.assertEqual(updated_product.name, "Updated Product")
        self.assertEqual(updated_product.price, 89)

    def test_delete_product(self):
        product = ProductModel.create(name="Test Product", price=99)
        response = self.client.delete(f'/api/products/{product.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"], "Product deleted.")

        with self.assertRaises(ProductModel.DoesNotExist):
            ProductModel.get_by_id(product.id)

if __name__ == '__main__':
    unittest.main()
