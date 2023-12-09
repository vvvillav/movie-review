import graphene

from graphene_django.types import DjangoObjectType
from .models import Review


class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
