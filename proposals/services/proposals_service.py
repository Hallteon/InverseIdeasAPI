from fuzzywuzzy import process, fuzz
from proposals.daos import *
from users.daos import CustomUserDAO


class ProposalCreateService:
    def __init__(self, user_id: int, user_to: int, proposal_data: dict):
        self.user_id = user_id
        self.user_to = user_to
        self.proposal_data = proposal_data
    
    def create_proposal(self):
        self.proposal_data['author'] = CustomUserDAO().get(self.user_id)
        self.proposal_data['category'] = CategoryDAO().get(self.proposal_data['category'])
        
        proposal = ProposalDAO().create(self.proposal_data)
        proposal_post = ProposalPostDAO().create({'proposal': proposal})
        
        return proposal
        
    def create_proposal_histories(self, proposal: Proposal):
        created_history = HistoryDAO().create({'by_user': CustomUserDAO().get(self.user_id), 
                                    'status': StatusDAO().get_by_type('proposal_created')})
        approval_history = HistoryDAO().create({'by_user': CustomUserDAO().get(self.user_to), 
                                    'status': StatusDAO().get_by_type('proposal_in_approve')})
        proposal.histories.set([created_history, approval_history])
        
        return approval_history
        
    def execute(self):
        proposal = self.create_proposal()
        proposal_histories = self.create_proposal_histories(proposal)
        
        return proposal
    

class ProposalService:
    def __init__(self, user_id: int = None, user_to: int = None, 
                 proposal_id: int = None, status_id: int = None):
        self.user_id = user_id
        self.user_to = user_to
        self.proposal_id = proposal_id
        self.status_id = status_id    
            
    def approve_proposal(self, history_comment: str):
        proposal = ProposalDAO().update_level(self.proposal_id)
        approval_history = HistoryDAO().create({'by_user': CustomUserDAO().get(self.user_id),
                                                'status': StatusDAO().get_by_type('proposal_approved'),
                                                'comment': history_comment})
        in_approve_history = HistoryDAO().create({'by_user': CustomUserDAO().get(self.user_to),
                                                'status': StatusDAO().get_by_type('proposal_in_approve'),
                                                'comment': history_comment})
        proposal = ProposalDAO().add_histories(self.proposal_id, [approval_history, in_approve_history])
        
        return proposal
        
    def reject_proposal(self, history_comment: str):
        proposal = ProposalDAO().get(self.proposal_id)
        approval_history = HistoryDAO().create({'by_user': CustomUserDAO().get(self.user_id),
                                                'status': StatusDAO().get_by_type('proposal_rejected'),
                                                'comment': history_comment})
        proposal = ProposalDAO().add_histories(self.proposal_id, [approval_history])
        
        return proposal
    
    def revision_proposal(self, history_comment: str):
        proposal = ProposalDAO().get(self.proposal_id)
        approval_history = HistoryDAO().create({'by_user': CustomUserDAO().get(self.user_id),
                                                'status': StatusDAO().get_by_type('proposal_need_revision'),
                                                'comment': history_comment})
        proposal = ProposalDAO().add_histories(self.proposal_id, [approval_history])
        
        return proposal
    
    def process_proposal(self, history_comment: str):
        proposal = ProposalDAO().get(self.proposal_id)
        approval_history = HistoryDAO().create({'by_user': CustomUserDAO().get(self.user_id),
                                                'status': StatusDAO().get_by_type('proposal_in_work'),
                                                'comment': history_comment})
        proposal = ProposalDAO().add_histories(self.proposal_id, [approval_history])
    
        return proposal
    
    def execute_proposal(self, history_comment: str):
        proposal = ProposalDAO().get(self.proposal_id)
        approval_history = HistoryDAO().create({'by_user': CustomUserDAO().get(self.user_id),
                                                'status': StatusDAO().get_by_type('proposal_done'),
                                                'comment': history_comment})
        proposal = ProposalDAO().add_histories(self.proposal_id, [approval_history])
        
        return proposal
                
    def get_current_level_heads(self):
        if self.proposal_id:
            proposal = ProposalDAO().get(self.proposal_id)
            proposal_level = proposal.level
            
            match proposal_level:
                case 1:
                    return CustomUserDAO().get_user_division_heads(self.user_id)
                case 2:
                    return CustomUserDAO().get_user_department_heads(self.user_id)
                case 3:
                    return CustomUserDAO().get_user_office_heads(self.user_id)
            
        return CustomUserDAO().get_user_division_heads(self.user_id) 
    
    def get_my_proposals(self):
        proposals = ProposalDAO().filter_by_me(self.user_id, self.status_id)
        
        return proposals
    
    def search_proposals(self, proposal_name):
        proposals = ProposalDAO().filter_by_me(self.user_id)
        results = process.extract(proposal_name, proposals.values_list('name', flat=True), scorer=fuzz.ratio)
        best_matches_fuzz = [result[0] for result in results if result[1] > 50]
        proposals = proposals.filter(name__in=best_matches_fuzz)
        
        return proposals
    
    def check_proposal_executed_status(self):
        executed_status = StatusDAO().get_by_type('proposal_done')
        status_check = ProposalDAO().check_statuses(self.proposal_id, [executed_status])
        
        return status_check
    
    def check_proposal_rejected_status(self):
        rejected_status = StatusDAO().get_by_type('proposal_rejected')
        status_check = ProposalDAO().check_statuses(self.proposal_id, [rejected_status])
        
        return status_check
        