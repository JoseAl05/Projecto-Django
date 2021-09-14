from app.wsgi import *
from core.erp.models import Type,Employee


# Listar #
# SELECT * FROM Tabla

query = Type.objects.all()

print(query)

# Insert #

# t = Type()
# t.name = 'Prueba Insert'
# t.save()

# Update #

# t = Type.objects.get(id = 2)
# t.name = 'Prueba Insert (Updated)'
# t.save()

# Delete #

# t = Type.objects.get(id = 2)
# t.delete()


# Lista Filter #

Employee.objects.filter(type_id = 1)

obj =Type.objects.filter(name__endswith = 'a')
print(obj)