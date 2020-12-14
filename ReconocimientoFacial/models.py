from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=80)
    lastname = models.CharField(max_length=30)
    identification = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True)
    #image = models.ImageField(upload_to='students')
    image = models.ImageField(null=True)

    address = models.CharField(max_length=50, null=True)
    birthdate = models.DateField(null=True)
    gender = models.CharField(max_length=40, null=True)
    program = models.CharField(max_length=40)
    semester = models.CharField(max_length=40)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    category = models.CharField(max_length=30)
    state = models.CharField(max_length=20)
    observations = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True)
    #student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True) # one to many
    #student = models.ManyToManyField(Student, on_delete=models.CASCADE) # many to many
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'

    def __str__(self):
        return self.name


class loanHistory(models.Model):
    state = models.CharField(max_length=20)
    return_date = models.DateTimeField(null=True)  # fecha de devolucion
    observations = models.CharField(max_length=200, null=True)
    students = models.ManyToManyField(Student)
    books = models.ManyToManyField(Book)
    created = models.DateTimeField(auto_now_add=True)  # fecha de prestamo
    updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Historial_prestamo'
        verbose_name_plural = 'Historial_prestamos'

    def __str__(self):
        return self.state