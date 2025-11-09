from rest_framework import serializers

from .models import Transaction, Category, BankAccount, CreditCard


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ["id", "name", "bank_name", "balance_initial", "currency"]


class CreditCardSerializer(serializers.ModelSerializer):
    bank_account = BankAccountSerializer(read_only=True)

    class Meta:
        model = CreditCard
        fields = ["id", "name", "limit", "closing_day", "due_day", "bank_account"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "is_approved"]


class TransactionSerializer(serializers.ModelSerializer):
    bank_account = serializers.PrimaryKeyRelatedField(
        queryset=BankAccount.objects.all(), required=False, allow_null=True
    )
    credit_card = serializers.PrimaryKeyRelatedField(
        queryset=CreditCard.objects.all(), required=False, allow_null=True
    )
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = Transaction
        fields = [
            "id",
            "bank_account",
            "credit_card",
            "category",
            "description",
            "type",
            "amount",
            "date",
            "status",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Add simple names for convenience in frontend
        data["bank_account_name"] = (
            instance.bank_account.name if instance.bank_account else None
        )
        data["credit_card_name"] = instance.credit_card.name if instance.credit_card else None
        data["category_name"] = instance.category.name if instance.category else None
        return data

    def validate(self, attrs):
        # Ensure either bank_account or credit_card is present
        if not attrs.get("bank_account") and not attrs.get("credit_card"):
            raise serializers.ValidationError(
                "Either bank_account or credit_card must be provided"
            )
        return attrs
