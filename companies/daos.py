from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from companies.models import *


class CompanyDAO:
    __slots__ = ('_db',)
    
    def __init__(self):
        self._db = Company
        
    def get_company_by_employee(self, user_id: int):
        try:
            company = self._db.objects.filter(Q(offices__departments__divisions__employees__id=user_id) | 
                                              Q(offices__departments__divisions__heads__id=user_id)).distinct().get() 
        except ObjectDoesNotExist as e:
            return None
        else:
            return company
        
    def get_divisions_by_employee(self, company_id):
        company = self._db.objects.filter(id=company_id).get()
        divisions = []
    
        for office in company.offices.all():
            for department in office.departments.all():
                for division in department.divisions.all():
                    divisions.append(division)
                    
        return divisions
    
    def get_offices_by_admin(self, company_id):
        return self._db.objects.filter(id=company_id).get().offices.all()


class OfficeDAO:
    __slots__ = ('_db',)
    
    def __init__(self):
        self._db = Office
        
    def get_office_by_employee(self, user_id: int):
        return self._db.objects.filter(Q(departments__divisions__employees__id=user_id) |
                                       Q(departments__divisions__heads__id=user_id)).get()
    
    def get_divisions_by_employee(self, user_id: int):
        offices = self._db.objects.filter(Q(departments__divisions__employees__id=user_id) |
                                          Q(departments__divisions__heads__id=user_id))
        divisions = []
        
        for office in offices:
            for department in office.departments.all():
                for division in department.divisions.all():
                    divisions.append(division)
                    
        return divisions
    
    
class DepartmentDAO:
    __slots__ = ('_db',)
    
    def __init__(self):
        self._db = Department
        
    def get_departments_by_employee(self, user_id: int):
        return self._db.objects.filter(Q(divisions__employees__id=user_id) |
                                       Q(divisions__heads__id=user_id))
    
    
class DivisionDAO:
    __slots__ = ('_db',)
    
    def __init__(self):
        self._db = Division
        
    def get_divisions_by_employee(self, user_id: int):
        divisions = []
        self._db.objects.filter(Q(employees__id=user_id))
        
        return self._db.objects.filter(divisions__employees__id=user_id)