from cookbook.ingredients.models import Category, Ingredient
import graphene
from graphene_django import DjangoObjectType
from django.forms import ModelForm
from graphene_django.forms.mutation import DjangoModelFormMutation


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name", "ingredients")


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "notes", "category")


class CreateCategoryMutation(graphene.Mutation):
    class Arguments:
        # Mutation to create a category
        name = graphene.String(required=True)

    # Class attributes define the response of the mutation
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category()
        category.name = name
        category.save()

        return CreateCategoryMutation(category=category)


class UpdateCategoryMutation(graphene.Mutation):
    class Arguments:
        # The input arguments for this mutation
        name = graphene.String(required=True)
        id = graphene.ID()

    # The class attributes define the response of the mutation
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, id):
        category = Category.objects.get(pk=id)
        category.name = name
        category.save()
        # Notice we return an instance of this mutation
        return UpdateCategoryMutation(category=category)


class CreateIngredientMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        notes = graphene.String()
        category_id = graphene.Int()

    ingredient = graphene.Field(IngredientType)

    @classmethod
    def mutate(cls, root, info, name, notes, category_id):
        ingredient = Ingredient()
        ingredient.name = name
        ingredient.notes = notes
        ingredient.category_id = category_id
        ingredient.save()
        # Notice we return an instance of this mutation
        return CreateIngredientMutation(ingredient=ingredient)


class UpdateIngredientMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)
        notes = graphene.String()
        category_id = graphene.Int()

    ingredient = graphene.Field(IngredientType)

    @staticmethod
    def mutate(root, info, id, name, notes, category_id):
        ingredient = Ingredient.objects.get(pk=id)
        ingredient.name = name
        ingredient.notes = notes
        ingredient.category_id = category_id
        ingredient.save()
        return UpdateIngredientMutation(ingredient=ingredient)


class Query(graphene.ObjectType):
    all_ingredients = graphene.List(IngredientType)
    category_by_name = graphene.Field(
        CategoryType, name=graphene.String(required=True))
    all_categories = graphene.List(CategoryType)
    ingredient_by_name = graphene.Field(
        IngredientType, name=graphene.String(required=True))

    def resolve_all_ingredients(root, info):
        # We can easily optimize query count in the resolve method
        return Ingredient.objects.select_related('category').all()

    def resolve_category_by_name(root, info, name):
        try:
            return Category.objects.get(name=name)
        except Category.DoesNotExist:
            return None

    def resolve_all_categories(root, info):
        print("resolved")
        return Category.objects.all()

    def resolve_ingredient_by_name(root, info, name):
        try:
            return Ingredient.objects.select_related('category').get(name=name)
        except Ingredient.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    update_category = UpdateCategoryMutation.Field()
    create_category = CreateCategoryMutation.Field()
    create_ingredient = CreateIngredientMutation.Field()
    update_ingredient = UpdateIngredientMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
