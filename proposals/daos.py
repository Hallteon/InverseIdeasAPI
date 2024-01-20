from django.db.models import Q, Max
from proposals.models import *


class CategoryDAO:
    __slots__ = ('_db',)
    
    def __init__(self):
        self._db = Category
        
    def get(self, category_id: int):
        return self._db.objects.filter(id=category_id).get()


class StatusDAO:
    __slots__ = ('_db',)
    
    def __init__(self):
        self._db = Status
        
    def get(self, status_id: int):
        return self._db.objects.filter(id=status_id).get()
    
    def get_by_type(self, status_type: str):
        return self._db.objects.filter(status_type=status_type).get()


class HistoryDAO:
    __slots__ = ('_db',)
    
    def __init__(self):
        self._db = History

    def create(self, data: dict):
        return self._db.objects.create(**data)
        
    def get(self, history_id: int):
        return self._db.objects.filter(id=history_id).get()


class ProposalDAO:
    __slots__ = ('_db',)
    
    def __init__(self):
        self._db = Proposal
        
    def create(self, data: dict):
        if 'comment' in data.keys():
            comment = dict(data).pop('comment')
            return self._db.objects.create(**data)
        
        return self._db.objects.create(**data)
    
    def get(self, proposal_id: int):
        return self._db.objects.filter(id=proposal_id).get()
    
    def get_latest_history(self, proposal_id: int):
        return self._db.objects.filter(id=proposal_id).get().histories.latest()
    
    def filter_by_me(self, user_id: int, status_id: int = None):
        proposals = Proposal.objects.filter(Q(histories__by_user__id=user_id) 
                                       | Q(author__id=user_id)).distinct()
        
        if status_id:
            last_history_ids = History.objects.values('proposals_history').annotate(last_history_id=Max('id')).values_list('last_history_id',
                                                                                                                           flat=True)
            proposals = proposals.filter(histories__in=last_history_ids, histories__status__id=status_id)
            
        return proposals
    
    def update_level(self, proposal_id: int):
        proposal = self._db.objects.filter(id=proposal_id).get()

        if proposal.level < 3:
            proposal.level += 1
            proposal.save()
        
        return proposal
    
    def add_histories(self, proposal_id: int, histories: list):
        proposal = self._db.objects.filter(id=proposal_id).get()
        
        for history in histories:
            proposal.histories.add(history)
        
        proposal.save()
        
        return proposal
    
    def check_statuses(self, proposal_id: int, proposal_statuses: list):
        proposal = self._db.objects.filter(id=proposal_id).get()
        
        for proposal_status in proposal_statuses:
            for history in proposal.histories.all():
                if proposal_status == history.status:
                    return True
            
        return False
    
    
class CommentDAO:
    __slots__ = ('_db',)
    
    def __init__(self):
        self._db = Comment
        
    def create(self, data: dict):
        return self._db.objects.create(**data)
    
    
class ProposalPostDAO:
    __slots__ = ('_db',)
    
    def __init__(self):
        self._db = ProposalPost
        
    def create(self, data: dict):
        return self._db.objects.create(**data)

    def get_proposals_by_company(self, company_id: int):
        return self._db.objects.filter(proposal__author__divisions_employee__departments_division__offices_department__companies_office__id=company_id)
    
    def add_comments(self, proposal_post_id: int, comments: list):
        proposal_post = ProposalPost.objects.filter(id=proposal_post_id).get()

        for comment in comments:
            proposal_post.comments.add(comment)
            
        proposal_post.save()
        
        return proposal_post
        
    def add_views(self, proposal_post_id: int, num_views: int):
        proposal_post = ProposalPost.objects.filter(id=proposal_post_id).get()
        proposal_post.views += num_views
        proposal_post.save()
        
        return proposal_post
        
    def add_likes(self, proposal_post_id: int, num_likes: int):
        proposal_post = ProposalPost.objects.filter(id=proposal_post_id).get()
        proposal_post.likes += num_likes
        proposal_post.save()
        
        return proposal_post