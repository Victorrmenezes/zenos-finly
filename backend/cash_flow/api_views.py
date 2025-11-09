from datetime import datetime
import io
from openpyxl import load_workbook

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Transaction, Category, CreditCard
from .serializers import TransactionSerializer, CategorySerializer, CreditCardSerializer
from .api.transaction_manager import TransactionManager
from .api import AccountManager
from .helpers import norm_str


class TransactionViewSet(viewsets.ModelViewSet):
    """Minimal Transaction API.

    Supports list/create/delete. Update could be added later.
    Query params:
      from (YYYY-MM-DD) inclusive
      to (YYYY-MM-DD) inclusive
    Pagination handled by DRF global settings if configured.
    """

    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Transaction.objects.filter(bank_account__user=self.request.user)
        # Include credit card transactions belonging to user's accounts
        qs = qs | Transaction.objects.filter(credit_card__bank_account__user=self.request.user)
        from_date = self.request.query_params.get("from")
        to_date = self.request.query_params.get("to")
        if from_date:
            qs = qs.filter(date__gte=from_date)
        if to_date:
            qs = qs.filter(date__lte=to_date)
        return qs.order_by("-date", "-id")

    def create(self, request, *args, **kwargs):
        # Use TransactionManager to leverage existing resolution logic if category/bank_account passed as names
        data = request.data.copy()
        # Accept category name string by resolving/creating Category if not numeric
        category_value = data.get("category")
        if category_value and not str(category_value).isdigit():
            cat = Category.objects.filter(name=category_value).first()
            if not cat:
                cat = Category.objects.create(name=category_value)
            data["category"] = cat.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        # Use serializer validated data for direct creation
        instance = Transaction.objects.create(**serializer.validated_data)
        out = self.get_serializer(instance)
        headers = self.get_success_headers(out.data)
        return Response(out.data, status=status.HTTP_201_CREATED, headers=headers)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all().order_by("name")


class CreditCardTransactionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        credit_card_id = request.query_params.get("credit_card")
        date_str = request.query_params.get("date")  # reference date (billing period)
        qs = Transaction.objects.filter(credit_card__bank_account__user=request.user, credit_card__isnull=False)
        if credit_card_id:
            qs = qs.filter(credit_card_id=credit_card_id)
        if date_str:
            try:
                ref_date = datetime.fromisoformat(date_str)
                qs = qs.filter(date__year=ref_date.year, date__month=ref_date.month)
            except ValueError:
                return Response({"detail": "Invalid date format"}, status=400)
        qs = qs.order_by("-date", "-id")
        ser = TransactionSerializer(qs, many=True)
        return Response(ser.data)

    def get_paginated_response(self, data):
        return Response(data)


class AccountsSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        manager = AccountManager(request.user.id)
        accounts = manager.list_accounts()  # dict keyed by id
        total = sum([acc.get("balance", 0) or 0 for acc in accounts.values()])
        accounts_list = [
            {"id": acc_id, **details} for acc_id, details in accounts.items()
        ]
        return Response({"total_balance": total, "accounts": accounts_list})
    
class CreditCardsListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Return user's credit cards as a flat list
        qs = CreditCard.objects.filter(bank_account__user=request.user).order_by("name")
        data = CreditCardSerializer(qs, many=True).data
        return Response({"credit_cards": data})


class CreditCardImportView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get("file")
        if not file:
            return Response({"detail": "No file uploaded"}, status=400)
        mapping_dict = {
            "data": "date",
            "descricao": "description",
            "valor": "amount",
            "categoria": "category",
            "cartao": "credit_card",
        }
        try:
            raw = file.read()
            wb = load_workbook(filename=io.BytesIO(raw), data_only=True)
            ws = wb.active
            rows = list(ws.values)
            if not rows:
                return Response({"detail": "Empty file"}, status=400)
            headers = []
            for i, h in enumerate(rows[0]):
                if h is None:
                    headers.append(f"col_{i}")
                else:
                    headers.append(mapping_dict.get(norm_str(str(h)), norm_str(str(h))))

            transactions = []
            for row in rows[1:]:
                rowdict = {
                    headers[i]: (row[i] if i < len(row) and row[i] is not None else "")
                    for i in range(len(headers))
                }
                rowdict["type"] = "CREDITCARD"
                # Convert amount numeric & negative
                try:
                    rowdict["amount"] = -abs(float(rowdict["amount"]))
                except Exception:
                    rowdict["amount"] = 0
                transactions.append(rowdict)

            # Create transactions using manager (resolves category / card)
            tm = TransactionManager(request.user)
            tm.create_transactions(transactions)
            return Response({"imported": len(transactions)})
        except Exception as e:
            return Response({"detail": f"Error reading file: {e}"}, status=400)
