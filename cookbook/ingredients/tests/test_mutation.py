import json
from graphene_django.utils.testing import GraphQLTestCase
from ..models import Category, Ingredient


class MutationTestCase(GraphQLTestCase):
    GRAPHQL_URL = "http://localhost:8000/graphql"

    def setUp(self):
        self.category_create_test_name = "Test Create Category"
        self.category_update_test_name = "Test Update Category"
        self.category_update_test_name_new = "Updated Test Name Category"
        self.ingredient_create_test_name = "Test Create Ingredient"
        self.ingredient_create_test_notes = "Delicious Ingredient!!"
        self.ingredient_update_test_name = "Test Update Ingredient"
        self.ingredient_update_test_name_new = "Updated Test Name Ingredient"
        self.ingredient_update_test_notes_new = "Updated Test Notes Ingredient"
        self.ingredient_update_test_notes = "Delicious Ingredient!!"
        Category.objects.create(
            name=f'{self.category_update_test_name}',
        )
        Ingredient.objects.create(
            name=f'{self.ingredient_update_test_name}',
            notes=f'{self.ingredient_update_test_notes}',
            category_id=1
        )

    def test_create_new_category(self):
        response = self.query(
            '''
          mutation CreateCategory($name: String!) {
            createCategory(name: $name) {
              category {
                id
                name
              }
            }
          }
          ''',
            variables={'name': self.category_create_test_name},
        )
        content = json.loads(response.content)[
            'data']['createCategory']['category']
        self.assertResponseNoErrors(response)
        self.assertEquals(content['name'], self.category_create_test_name)

    def test_update_new_category(self):
        response = self.query(
            '''
          mutation UpdateCategory($name: String!, $id: ID!) {
            updateCategory(name: $name, id: $id) {
              category {
                id
                name
              }
            }
          }
          ''',
            variables={"name": self.category_update_test_name_new, "id": "1"},
        )
        content = json.loads(response.content)[
            'data']['updateCategory']['category']
        self.assertResponseNoErrors(response)
        self.assertEquals(content['name'], self.category_update_test_name_new)

    def test_delete_category_true(self):
        response = self.query(
            '''
          mutation DeleteCategory($id: ID!) {
            deleteCategory(id: $id) {
              ok
            }
          }
          ''',
            variables={"id": "1"},
        )
        content = json.loads(response.content)['data']['deleteCategory']
        self.assertResponseNoErrors(response)
        self.assertEquals(content['ok'], True)

    def test_delete_category_false(self):
        response = self.query(
            '''
          mutation DeleteCategory($id: ID!) {
            deleteCategory(id: $id) {
              ok
            }
          }
          ''',
            variables={"id": "1000"},
        )
        content = json.loads(response.content)['data']['deleteCategory']
        self.assertResponseNoErrors(response)
        self.assertEquals(content['ok'], False)

    def test_create_new_ingredient(self):
        response = self.query(
            '''
          mutation CreateIngredient($name: String!, $notes: String!, $categoryID: Int!) {
            createIngredient(name: $name, notes: $notes, categoryId: $categoryID) {
              ingredient {
                id
                name
                notes
                category {
                  id
                  name
                }
              }
            }
          }
          ''',
            variables={
                "name": self.ingredient_create_test_name,
                "notes": self.ingredient_create_test_notes,
                "categoryID": 1
            },
        )
        content = json.loads(response.content)[
            'data']['createIngredient']['ingredient']
        self.assertResponseNoErrors(response)
        self.assertEquals(content['name'], self.ingredient_create_test_name)
        self.assertEquals(content['notes'], self.ingredient_create_test_notes)
        self.assertEquals(content['category']['id'], "1")

    def test_update_ingredient(self):
        response = self.query(
            '''
          mutation UpdateIngredient($id: ID!, $name: String!, $notes: String!, $categoryID: Int!) {
            updateIngredient(id: $id, name: $name, notes: $notes, categoryId: $categoryID) {
              ingredient {
                id
                name
                notes
                category {
                  id
                  name
                }
              }
            }
          }
          ''',
            variables={
                "id": 1,
                "name": self.ingredient_update_test_name_new,
                "notes": self.ingredient_update_test_notes_new,
                "categoryID": 1
            },
        )
        content = json.loads(response.content)[
            'data']['updateIngredient']['ingredient']
        self.assertResponseNoErrors(response)
        self.assertEquals(
            content['name'], self.ingredient_update_test_name_new)
        self.assertEquals(content['notes'],
                          self.ingredient_update_test_notes_new)
        self.assertEquals(content['category']['id'], "1")
