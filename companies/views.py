from companies.serializers import *
from companies.services.companies_service import CompanyService 
from users.permissions import IsAdministrator
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class DivisionAPIGetListView(generics.ListAPIView):
    serializer_class = DivisionReadListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CompanyService(self.request.user.id).get_divisions_list()
    
class OfficeAPIListView(generics.ListAPIView):
    serializer_class = OfficeAnalyticsSerializer
    permission_classes = [IsAuthenticated, IsAdministrator]
    
    def get_queryset(self):
        return CompanyService(self.request.user.id).get_offices_list()