from companies.daos import CompanyDAO, OfficeDAO


class OfficeService:
    def __init__(self, user_id: int = None, office_id: int = None):
        self.user_id = user_id
        self.office_id = office_id
    
    def get_divisions_list(self):
        divisions = OfficeDAO().get_divisions_by_employee(self.user_id)
        
        return divisions
        