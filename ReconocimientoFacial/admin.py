from django.contrib import admin
from .models import Student, Book, loanHistory

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

class BookAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')

class LoanHistoryAdmin(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')


admin.site.register(Student, StudentAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(loanHistory, LoanHistoryAdmin)