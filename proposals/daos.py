from django.db.models import Q, Max
from dataclasses import dataclass
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
        if data['comment']:
            comment = dict(data).pop('comment')
            return self._db.objects.create(**data)
        
        return self._db.objects.create(**data)
    
    def get(self, proposal_id: int):
        return self._db.objects.filter(id=proposal_id).get()
    
    def get_latest_history(self, proposal_id: int):
        return self._db.objects.filter(id=proposal_id).get().histories.latest()
    
    def filter_by_me(self, user_id: int, status_id: int = None):
        proposals = Proposal.objects.filter(Q(histories__by_user__id=user_id) 
                                       | Q(author__id=user_id))
        
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