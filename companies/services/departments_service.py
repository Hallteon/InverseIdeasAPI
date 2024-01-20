from companies.daos import DepartmentDAO


class DepartmentsService:
    def __init__(self, user_id: int):
        self.user_id = user_id
    
    def get_departments(self):
        departments = DepartmentDAO().get_departments_by_employee(self.user_id)
        
        return departments