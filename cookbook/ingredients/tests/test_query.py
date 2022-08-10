import json
from graphene_django.utils.testing import GraphQLTestCase
from ..models import Category, Ingredient


class QueryTestCase(GraphQLTestCase):
    GRAPHQL_URL = "http://localhost:8000/graphql"

    def setUp(self):
        self.number_of_categories = 3

        for category_id in range(self.number_of_categories):
            Category.objects.create(
                name=f'Category {category_id}',
            )

        Ingredient.objects.create(
            name=f'Ingredient 0',
            notes="something about ingredient",
            category_id=1,
        )
        Ingredient.objects.create(
            name=f'Ingredient 1',
            notes="something about ingredient",
            category_id=1,
        )
        Ingredient.objects.create(
            name=f'Ingredient 2',
            notes="something about ingredient",
            category_id=2,
        )

    def test_get_all_category(self):
        response = self.query(
            '''
          query {
            allCategories {
              id
              name
              ingredients {
                id
                name
              }
            }
          }
          '''
        )
        content = json.loads(response.content)['data']['allCategories']
        self.assertResponseNoErrors(response)

        # test number of categories
        self.assertEquals(len(content), self.number_of_categories)

        # test all categories name and id
        for i in range(len(content)):
            self.assertEquals(content[i]['name'], f'Category {i}')
            self.assertEquals(content[i]['id'], str(i + 1))

        # test first category has 2 ingredients associated to !!
        self.assertEquals(len(content[0]['ingredients']), 2)

        # test first associated ingredient to first category is expected ingredient
        self.assertEquals(
            content[0]['ingredients'][0], {'id': '1', 'name': 'Ingredient 0'})

    def test_get_all_ingredients(self):
        response = self.query(
            """
          query {
            allIngredients {
              id
              name
              category {
                id
                name
              }
            }
          }
          """
        )
        content = json.loads(response.content)['data']['allIngredients']
        self.assertResponseNoErrors(response)

        # test number of ingredients
        self.assertEquals(len(content), 3)

        # test all ingredients name and id
        for i in range(len(content)):
            self.assertEquals(content[i]['name'], f'Ingredient {i}')
            self.assertEquals(content[i]['id'], str(i + 1))

        # test first ingredient belongs to first category
        self.assertEquals(content[0]['category'], {
                          'id': '1', 'name': 'Category 0'})

    def test_get_category_by_name(self):
        response = self.query(
            """
          query CategoryByName($name: String!){
            categoryByName(name: $name) {
              id
              name
              ingredients {
                id
                name
              }
            }
          }
          """,
            variables={'name': "Category 1"},
        )
        content = json.loads(response.content)['data']['categoryByName']
        self.assertResponseNoErrors(response)
        self.assertEquals(content['id'], '2')
        self.assertEquals(content['name'], 'Category 1')
        self.assertEquals(content['ingredients'][0], {
                          'id': '3', 'name': 'Ingredient 2'})

    def test_get_ingredient_by_name(self):
        response = self.query(
            """
          query IngredientByName($name: String!){
            ingredientByName(name: $name) {
              id
              name
              category {
                id
                name
              }
            }
          }
          """,
            variables={'name': "Ingredient 1"},
        )
        content = json.loads(response.content)['data']['ingredientByName']
        self.assertResponseNoErrors(response)
        self.assertEquals(content['id'], '2')
        self.assertEquals(content['name'], 'Ingredient 1')
        self.assertEquals(content['category'], {
                          'id': '1', 'name': 'Category 0'})
