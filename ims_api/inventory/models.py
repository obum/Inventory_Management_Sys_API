from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model
# Create your models here.


User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=40, null=True, blank=True)
    description = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    name = models.CharField(max_length=40, null=True, blank=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=15, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
    created_at = models.DateTimeField(default=now,editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    low_stock = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.low_stock = self.quantity < 5
        return super().save(*args, **kwargs)


    def __str__(self):
        return self.name

class ChangeReason(models.Model):
    class ChangeType(models.TextChoices):
        STOCK_INCREASE = 'Stock Increase', 'Stock Increase'
        STOCK_DECREASE = 'Stock Decrease', 'Stock Decrease'
        NO_CHANGE = 'No Change', 'No Change'

    reason = models.CharField(max_length=100, unique=True)
    change_type = models.CharField(
        max_length=100,
        choices=ChangeType.choices,
        default=ChangeType.NO_CHANGE
    )

    def __str__(self):
        return f"{self.reason}"
    
class InventoryChange(models.Model):
    change_reason = models.ForeignKey(ChangeReason, on_delete=models.CASCADE, related_name='inventory_changes')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='inventory_changes')
    change_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=now,editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inventory_changes')
    
    def save(self, *args, **kwargs):
        # Calculate the net change in inventory if it is not a no change action
        if self.change_reason.change_type != ChangeReason.ChangeType.NO_CHANGE : # perform inventory changes on only new Inventory change objects
            if self.change_reason.change_type == ChangeReason.ChangeType.STOCK_INCREASE:
                print(self.change_reason.change_type)
                # add change quantity when inventory change type is a stock increase
                self.inventory_item.quantity += self.change_quantity
                self.inventory_item.save()
            elif self.change_reason.change_type == ChangeReason.ChangeType.STOCK_DECREASE:
                # less the change quantity when inventory change type is a stock decrease
                if self.change_quantity < self.inventory_item.quantity:
                    self.inventory_item.quantity -= self.change_quantity
                    self.inventory_item.save()
                else: # check for possible negative inventory.
                    raise ValueError("Insufficient stock for this operation")
        print(self.change_reason.change_type)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.inventory_item.name}, {self.change_quantity}, {self.change_reason}"
    
    
