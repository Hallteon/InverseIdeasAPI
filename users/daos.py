from dataclasses import dataclass
from users.models import CustomUser


class UserDAO:
    __slots__ = ('_db',)
    
    def __init__(self):
        self._db = CustomUser
            
    def get(self, user_id: int):
        return self._db.objects.get(id=user_id)
    
    def get_user_division_heads(self, user_id: int):
        return self._db.objects.get(id=user_id).divisions_employee.all()[0].heads.all()
    
    def get_user_department_heads(self, user_id: int):
        return self._db.objects.get(id=user_id).divisions_employee.all()[0].departments_division.all()[0].heads.all()
    
    def get_user_office_heads(self, user_id: int):
        return self._db.objects.get(id=user_id).divisions_employee.all()[0].departments_division.all()[0].offices_department.all()[0].heads.all()