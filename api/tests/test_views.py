import json
from ..models.category import Category, Company
from rest_framework.test import APITestCase
from django.urls import reverse


class CategoryViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(name="test_company")
        cls.top_level_category = Category.objects.create(
            name="top_level_category", company=cls.company, parent_category=None
        )
        cls.child_category = Category.objects.create(
            name="child_category", company=cls.company, parent_category=cls.top_level_category
        )

    def test_list(self):
        url = reverse("category-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)), 2)

        expected_json_dict = [
            {
                "id": str(self.top_level_category.id),
                "name": self.top_level_category.name,
                "company": str(self.top_level_category.company.id),
                "parent_category": None,
            },
            {
                "id": str(self.child_category.id),
                "name": self.child_category.name,
                "company": str(self.child_category.company.id),
                "parent_category": str(self.child_category.parent_category.id),
            }
        ]
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_retrieve(self):
        url = reverse("category-detail", args=[self.child_category.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, 200)

        expected_json_dict = {
            "id": str(self.child_category.id),
            "name": self.child_category.name,
            "company": str(self.child_category.company.id),
            "parent_category": str(self.child_category.parent_category.id),
        }
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_create(self):
        params = {
            "name": "create_category",
            "company": self.company.id,
            "parent_category": self.top_level_category.id,
        }
        url = reverse("category-list")
        response = self.client.post(url, params, format="json")
        self.assertEqual(response.status_code, 201)

        created_category = Category.objects.get(name="create_category")
        self.assertTrue(
            created_category.name == "create_category" and
            created_category.company.id == self.company.id and
            created_category.parent_category.id == self.top_level_category.id
        )

        expected_json_dict = {
            "id": str(created_category.id),
            "name": "create_category",
            "company": str(created_category.company.id),
            "parent_category": str(self.top_level_category.id),
        }
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_update(self):
        company_another = Company.objects.create(name="test_company2")
        params = {
            "name": "update_category",
            "company": company_another.id,
            "parent_category": None,
        }
        url = reverse("category-detail", args=[self.child_category.id])
        response = self.client.put(url, params, format="json")
        self.assertEqual(response.status_code, 200)

        updated_category = Category.objects.get(id=self.child_category.id)
        self.assertTrue(
            updated_category.name == "update_category" and
            updated_category.company.id == company_another.id and
            updated_category.parent_category is None
        )

        expected_json_dict = {
            "id": str(updated_category.id),
            "name": updated_category.name,
            "company": str(updated_category.company.id),
            "parent_category": None,
        }
        self.assertJSONEqual(response.content, expected_json_dict)

    def test_destroy(self):
        url = reverse("category-detail", args=[self.top_level_category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

        deleted_category = Category.objects.filter(id=self.top_level_category.id)
        self.assertEqual(deleted_category.count(), 0)
