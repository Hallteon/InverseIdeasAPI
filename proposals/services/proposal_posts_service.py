from companies.daos import *
from proposals.daos import *
from users.daos import *


class ProposalPostService:
    def __init__(self, user_id: int = None, proposal_post_id: int = None):
        self.user_id = user_id
        self.proposal_post_id = proposal_post_id
    
    def get_proposal_posts_by_company(self):
        user_company = CompanyDAO().get_company_by_employee(self.user_id)
        
        if user_company:
            proposal_posts = ProposalPostDAO().get_proposals_by_company(user_company.id)
        
            return proposal_posts
        
        return []
    
    def send_comment(self, comment_content):
        comment = CommentDAO().create({'author': CustomUserDAO().get(self.user_id),
                                       'content': comment_content})
        proposal_post = ProposalPostDAO().add_comments(self.proposal_post_id, [comment])
        
        return proposal_post
    
    def add_post_likes(self):
        user = CustomUserDAO().get(self.user_id)
        proposal_post = ProposalPostDAO().add_likes(self.proposal_post_id,
                                                    [user])
        return proposal_post
    
    def remove_post_likes(self):
        user = CustomUserDAO().get(self.user_id)
        proposal_post = ProposalPostDAO().remove_likes(self.proposal_post_id,
                                                    [user])
        return proposal_post
    
    def add_post_views(self, num_views):
        proposal_post = ProposalPostDAO().add_views(self.proposal_post_id,
                                                    num_views)
        return proposal_post
        
    
        