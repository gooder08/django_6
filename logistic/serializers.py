from rest_framework import serializers
from logistic.models import Product
from logistic.models import Stock
from logistic.models import StockProduct


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']
    # настройте сериализатор для продукта
    


class ProductPositionSerializer(serializers.ModelSerializer):
    # product = serializers.CharField()
    # quantity = serializers.IntegerField()
    # price = serializers.FloatField()
    class Meta:
        model = StockProduct
        fields = ['product', 'quantity', 'price']
    

    # настройте сериализатор для позиции продукта на складе
    


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)
    # address = serializers.CharField()
    class Meta:
        model = Stock
        fields = '__all__'

    # настройте сериализатор для склада

    def create(self, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')
        stock = super().create(validated_data)
        for position in positions:
            StockProduct.objects.create(stock=stock, **position)


        # создаем склад по его параметрам
        
        

        # здесь вам надо заполнить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock

    def update(self, instance, validated_data):
        # достаем связанные данные для других таблиц
        positions = validated_data.pop('positions')

        # обновляем склад по его параметрам
        stock = super().update(instance, validated_data)
        for position in positions:
            StockProduct.objects.update_or_create(stock=stock, product=position['product'], defaults= {'quantity': position['quantity'], 'price': position['price']})

        # здесь вам надо обновить связанные таблицы
        # в нашем случае: таблицу StockProduct
        # с помощью списка positions

        return stock
