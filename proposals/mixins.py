from rest_framework import status
from rest_framework.response import Response
from proposals.services.proposals_service import ProposalService


class CheckProposalExecutedMixin:
    def check_status(self, proposal_id):
        executed_check = ProposalService(proposal_id=proposal_id).check_proposal_executed_status()
        rejected_check = ProposalService(proposal_id=proposal_id).check_proposal_rejected_status()
        
        return executed_check or rejected_check