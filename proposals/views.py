import uuid

from django.db.models import Count
from proposals.mixins import CheckProposalExecutedMixin
from proposals.services.proposal_posts_service import ProposalPostService
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.core.files.base import ContentFile
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import views
from proposals.models import *
from proposals.serializers import *
from proposals.permissions import *
from proposals.services.proposals_service import ProposalCreateService, ProposalService
from users.serializers import CustomUserSerializer
from users.permissions import IsHead
from utils.generate_pdf import FileGenerator


class CategoryAPIListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
class StatusAPIListView(generics.ListAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class ProposalAPICreateView(views.APIView):
    serializer_class = ProposalSerializer
    parser_classes = (FormParser, MultiPartParser, JSONParser)
    permissions_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user_to = request.data.pop('user_to')
        file_content = dict(request.data.get('content'))
        file_generator = FileGenerator(file_content)
        file = file_generator.generate_pdf()
        filename = str(uuid.uuid4())
        
        request.data['content'] = file_content
        request.data['document'] = ContentFile(file.getvalue(), filename)
   
        proposal = ProposalCreateService(request.user.id, user_to, 
                                         request.data).execute()
        proposal_serializer = ProposalSerializer(proposal)
                
        return Response(proposal_serializer.data, status=status.HTTP_201_CREATED)
    
    
class ProposalAPIDetailView(generics.RetrieveUpdateAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated, IsProposalAuthorOrReadOnly]
    
    
class ProposalAPIGetHeadsView(generics.RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permissions_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        proposal_data = ProposalService(request.user.id, 
                                        request.GET.get('proposal_id', None)).get_current_level_heads()
        user_serializer = CustomUserSerializer(proposal_data, many=True)
        
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)
    
    
class ProposalAPIListMeView(generics.ListAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        proposals = ProposalService(user_id=self.request.user.id,
                                    status_id=self.request.query_params.get('status_id', None)).get_my_proposals()
        return proposals 


class ProposalAPIListSearchView(generics.ListAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        search_query = self.request.query_params.get('name', None)
        
        if search_query:
            proposals = ProposalService(user_id=self.request.user.id).search_proposals(search_query)

        return proposals

    
class ProposalAPIApproveView(CheckProposalExecutedMixin, views.APIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated, IsHead, IsInProposalHistories]
    
    def post(self, request, *args, **kwargs):
        executed_status = self.check_status(self.kwargs['pk'])
        
        if executed_status:
            return Response('The proposal has already been done!', status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
        proposal_data = ProposalService(request.user.id, request.data.get('user_to', None),
                                        self.kwargs['pk']).approve_proposal(request.data.get('comment', None))
        proposal_serializer = ProposalSerializer(proposal_data)
        
        return Response(proposal_serializer.data, status=status.HTTP_202_ACCEPTED)
      
      
class ProposalAPIRejectView(CheckProposalExecutedMixin, views.APIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated, IsHead, IsInProposalHistories]
    
    def post(self, request, *args, **kwargs):
        executed_status = self.check_status(self.kwargs['pk'])
        
        if executed_status:
            return Response('The proposal has already been done!', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        proposal_data = ProposalService(request.user.id, request.data.get('user_to', None),
                                        self.kwargs['pk']).reject_proposal(request.data.get('comment', None))
        proposal_serializer = ProposalSerializer(proposal_data)
        
        return Response(proposal_serializer.data, status=status.HTTP_202_ACCEPTED)
      
      
class ProposalAPIExecuteView(CheckProposalExecutedMixin, views.APIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated, IsHead, IsInProposalHistories]
    
    def post(self, request, *args, **kwargs):
        executed_status = self.check_status(self.kwargs['pk'])
        
        if executed_status:
            return Response('The proposal has already been done!', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        proposal_data = ProposalService(request.user.id, request.data.get('user_to', None),
                                        self.kwargs['pk']).execute_proposal(request.data.get('comment', None))
        proposal_serializer = ProposalSerializer(proposal_data)
        
        return Response(proposal_serializer.data, status=status.HTTP_202_ACCEPTED)
      
      
class ProposalAPIProcessView(CheckProposalExecutedMixin, views.APIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated, IsHead, IsInProposalHistories]
    
    def post(self, request, *args, **kwargs):
        executed_status = self.check_status(self.kwargs['pk'])
        
        if executed_status:
            return Response('The proposal has already been done!', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        proposal_data = ProposalService(request.user.id, request.data.get('user_to', None),
                                        self.kwargs['pk']).process_proposal(request.data.get('comment', None))
        proposal_serializer = ProposalSerializer(proposal_data)
        
        return Response(proposal_serializer.data, status=status.HTTP_202_ACCEPTED)


class ProposalAPIRevisionView(views.APIView):
    serializer_class = ProposalSerializer
    permission_classes = [IsAuthenticated, IsHead, IsInProposalHistories]
    
    def post(self, request, *args, **kwargs):
        executed_status = self.check_status(self.kwargs['pk'])
        
        if executed_status:
            return Response('The proposal has already been done!', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        
        proposal_data = ProposalService(request.user.id, request.data.get('user_to', None),
                                        self.kwargs['pk']).revision_proposal(request.data.get('comment', None))
        proposal_serializer = ProposalSerializer(proposal_data)
        
        return Response(proposal_serializer.data, status=status.HTTP_202_ACCEPTED)
    
    
class ProposalPostAPIListView(generics.ListAPIView):
    serializer_class = ProposalPostReadListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        proposal_posts = ProposalPostService(self.request.user.id).get_proposal_posts_by_company()
        
        return proposal_posts
    
    
class ProposalPostAPICreateCommentView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        proposal_post_data = ProposalPostService(self.request.user.id, 
                                            self.kwargs['pk']).send_comment(request.data.get('content', None))
        proposal_serializer = ProposalPostReadDetailSerializer(proposal_post_data)

        return Response(proposal_serializer.data, status=status.HTTP_201_CREATED)
    
    
class ProposalPostAPIAddViewsView(generics.UpdateAPIView):
    serializer_class = ProposalPostReadDetailSerializer
    permissions_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        proposal_post_data = ProposalPostService(request.user.id, 
                                                 self.kwargs['pk']).add_post_views(1)
        proposal_post_serializer = ProposalPostReadDetailSerializer(proposal_post_data)
        
        return Response(proposal_post_serializer.data, status=status.HTTP_200_OK)
    
    
class ProposalPostAPIAddLikesView(generics.UpdateAPIView):
    serializer_class = ProposalPostReadDetailSerializer
    permissions_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        proposal_post_data = ProposalPostService(request.user.id, 
                                                 self.kwargs['pk']).add_post_likes(1)
        proposal_post_serializer = ProposalPostReadDetailSerializer(proposal_post_data)
        
        return Response(proposal_post_serializer.data, status=status.HTTP_200_OK)
    
    
class ProposalPostAPIRemoveLikesView(generics.UpdateAPIView):
    serializer_class = ProposalPostReadDetailSerializer
    permissions_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        proposal_post_data = ProposalPostService(request.user.id, 
                                                 self.kwargs['pk']).remove_post_likes(1)
        proposal_post_serializer = ProposalPostReadDetailSerializer(proposal_post_data)
        
        return Response(proposal_post_serializer.data, status=status.HTTP_200_OK)
    
    
class ProposalPostAPIDetailView(generics.RetrieveAPIView):
    serializer_class = ProposalPostReadDetailSerializer
    permissions_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        proposal_post_data = ProposalPostService(request.user.id, 
                                                 self.kwargs['pk']).add_post_views(1)
        proposal_post_serializer = ProposalPostReadDetailSerializer(proposal_post_data)
        
        return Response(proposal_post_serializer.data, status=status.HTTP_201_CREATED)
    
    
class ProposalPostAPIGetRatingView(generics.ListAPIView):
    serializer_class = ProposalPostReadListSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        proposal_posts = ProposalPostService(self.request.user.id).get_proposal_posts_by_company()
        proposal_posts = proposal_posts.annotate(num_related_objects=Count('likes')).order_by('-likes', '-views')
        
        return proposal_posts
        
   