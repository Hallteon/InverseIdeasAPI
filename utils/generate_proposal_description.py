import requests
import json
import os
from yandexgptlite import YandexGPTLite


class ProposalGeneratorGPT:
    query_url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completion'
    
    def __init__(self, proposal_content, token, folder_id):
        self.proposal_content = proposal_content
        self.token = token
        self.folder_id = folder_id
        
    def generate_funcional_requirements(self):
        account = YandexGPTLite(self.folder_id, self.token)
        respose_text = account.create_completion(f'Составь функциональное требования для корпоративной заявки от сотрудника\
            в соответствии с твоей ролью на основе следующего JSON. В качестве ответа отправь только текст функционального требования\
                без лишних комментариев. Название возьми строго из предоставленного JSON файла. Текст ответа сформатируй с использованием разметки MarkDown.\
                    JSON: {self.proposal_content}', temperature=0.7, 
            system_prompt='ПЕННИИИИИИИИИИИИС')
        
        return respose_text