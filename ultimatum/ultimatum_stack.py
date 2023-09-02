from aws_cdk import (
    Stack,
    aws_lambda as lambda_
)
from constructs import Construct
from . import ultimatum_service

class UltimatumStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ultimatum_service.UltimatumService(self, "Ultimatum")
