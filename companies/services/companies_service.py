from companies.daos import CompanyDAO


class CompanyService:
    def __init__(self, user_id: int):
        self.user_id = user_id
    
    def get_divisions_list(self):
        company = CompanyDAO().get_company_by_employee(self.user_id)
        divisions = CompanyDAO().get_divisions_by_employee(company.id)
        
        return divisions
    
    def get_offices_list(self):
        company_id = CompanyDAO().get_company_by_employee(self.user_id).id
        offices = CompanyDAO().get_offices_by_admin(company_id)
        
        return offices