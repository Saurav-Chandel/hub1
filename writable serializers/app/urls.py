from django.urls import path
from app import views

app_name = "app"

urlpatterns = [

    path("recipe/",views.RecipeAPi.as_view(),name="recipe"),
    path("ingredient/",views.IngredientAPi.as_view(),name="ingredient"),
]