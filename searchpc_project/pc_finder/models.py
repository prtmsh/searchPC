from django.db import models

class SearchLog(models.Model):
    """Model to store PC part search logs"""
    timestamp = models.DateTimeField(auto_now_add=True)
    purpose = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.purpose} PC - {self.budget} INR - {self.location}"
    
    class Meta:
        ordering = ['-timestamp']
