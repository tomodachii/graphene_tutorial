import json
from graphene_django.utils.testing import GraphQLTestCase
from ..models import Category
from ...schema import *
from graphene import Schema


class CategoryQueryTestCase(GraphQLTestCase):
    def setUp(self):
        number_of_category = 13

        for category_id in range(number_of_category):
            Category.objects.create(
                name=f'Category {category_id}',
            )

    def test_get_all_category(self):
        # categories = Category.objects.all()
        # print(categories)
        # schema = Schema(query=Query)
        results = schema.execute('''
          query {
            allCategories {
              id
              name
            }
          }
        ''')
        print(results.data)
        response = self.query(
          '''
          query {
            allCategories {
              id
              name
            }
          }
          '''
        )
        # self.assertResponseNoErrors(response)
        print(response)
    
    # def test_get_all_ingredients(self):
    #     # categories = Category.objects.all()
    #     # print(categories)
    #     response = self.query(
    #       """
    #       query {
    #         allIngredients {
    #           id
    #           name
    #         }
    #       }
    #       """
    #     )
    #     self.assertResponseNoErrors(response)
    #     print(response)
