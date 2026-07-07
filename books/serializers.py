from rest_framework import serializers
from .models import Category, Cast, Movie, Series

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

    # BONUS: This changes how the data looks when we send it back to the user
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Replace the list of IDs with a list of string names
        representation['categories'] = [category.name for category in instance.categories.all()]
        representation['casts'] = [cast.name for cast in instance.casts.all()]
        return representation

class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__'
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['categories'] = [category.name for category in instance.categories.all()]
        representation['casts'] = [cast.name for cast in instance.casts.all()]
        return representation