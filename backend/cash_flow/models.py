from django.db import models


# # ------------------------
# # CATEGORY
# # ------------------------
# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.name


# # ------------------------
# # SUPPLIER
# # ------------------------
# class Supplier(models.Model):
#     name = models.CharField(max_length=150)
#     cnpj = models.CharField(max_length=18, blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     email = models.EmailField(max_length=100, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.name


# # ------------------------
# # PRODUCT
# # ------------------------
# class Product(models.Model):
#     name = models.CharField(max_length=150)
#     description = models.TextField(blank=True, null=True)
#     sale_price = models.DecimalField(max_digits=10, decimal_places=2)
#     cost_price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock_quantity = models.IntegerField(default=0)
#     category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
#     supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name="products")

#     def __str__(self):
#         return self.name


# # ------------------------
# # CUSTOMER
# # ------------------------
# class Customer(models.Model):
#     name = models.CharField(max_length=150)
#     document = models.CharField(max_length=20, blank=True, null=True)
#     phone = models.CharField(max_length=20, blank=True, null=True)
#     email = models.EmailField(max_length=100, blank=True, null=True)
#     address = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return self.name


# # ------------------------
# # ORDER
# # ------------------------
# class Order(models.Model):
#     STATUS_CHOICES = [
#         ('OPEN', 'Open'),
#         ('CLOSED', 'Closed'),
#         ('CANCELLED', 'Cancelled'),
#     ]

#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name="orders")
#     created_at = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
#     total_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     def __str__(self):
#         return f"Order #{self.id} - {self.status}"


# # ------------------------
# # ORDER ITEM
# # ------------------------
# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
#     quantity = models.IntegerField()
#     unit_price = models.DecimalField(max_digits=10, decimal_places=2)
#     discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

#     def __str__(self):
#         return f"{self.product} x {self.quantity}"


# # ------------------------
# # STOCK MOVEMENT
# # ------------------------
# class StockMovement(models.Model):
#     MOVEMENT_TYPE_CHOICES = [
#         ('PURCHASE_ENTRY', 'Purchase Entry'),
#         ('CUSTOMER_RETURN', 'Customer Return'),
#         ('SALE_EXIT', 'Sale Exit'),
#         ('LOSS', 'Loss'),
#         ('SUPPLIER_RETURN', 'Supplier Return'),
#     ]

#     product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_movements")
#     movement_type = models.CharField(max_length=30, choices=MOVEMENT_TYPE_CHOICES)
#     quantity = models.IntegerField()
#     date = models.DateTimeField(auto_now_add=True)
#     reference_id = models.IntegerField(blank=True, null=True)  # Could link to Order or Purchase ID
#     note = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.movement_type} - {self.product.name} ({self.quantity})"
