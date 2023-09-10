import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (aws_apigateway as apigateway,
                     aws_lambda as lambda_,
                     aws_s3 as s3,
                     aws_s3_deployment as s3_deployment)

class UltimatumService(Construct):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # config lambda for the backend
        home_handler = lambda_.Function(self, "home_handler",
                    runtime=lambda_.Runtime.PYTHON_3_7,
                    code=lambda_.Code.from_asset("ultimatum"),
                    handler="ultimatum_handler.home"
                    )
        create_session_handler = lambda_.Function(self, "create_session_handler",
                    runtime=lambda_.Runtime.PYTHON_3_7,
                    code=lambda_.Code.from_asset("ultimatum"),
                    handler="ultimatum_handler.create_session"
                    )
        session_lobby_handler = lambda_.Function(self, "session_lobby_handler",
                    runtime=lambda_.Runtime.PYTHON_3_7,
                    code=lambda_.Code.from_asset("ultimatum"),
                    handler="ultimatum_handler.session_lobby"
                    )
        join_session_handler = lambda_.Function(self, "join_session_handler",
                    runtime=lambda_.Runtime.PYTHON_3_7,
                    code=lambda_.Code.from_asset("ultimatum"),
                    handler="ultimatum_handler.join_session"
                    )

        # config gateway for handling traffic
        api = apigateway.RestApi(self, "ultimatum-api",
                  rest_api_name="Ultimatum Service",
                  description="This service handles the Ultimatum app.")
        home_integration = apigateway.LambdaIntegration(home_handler)
        create_session_integration = apigateway.LambdaIntegration(create_session_handler)
        session_lobby_integration = apigateway.LambdaIntegration(session_lobby_handler)
        join_session_integration = apigateway.LambdaIntegration(join_session_handler)
        # /
        api.root.add_method("GET", home_integration)
        # /session
        session_api = api.root.add_resource('session')
        session_api.add_method("GET", create_session_integration)
        # /session/login
        login_api = session_api.add_resource('login')
        login_api.add_method("GET", session_lobby_integration)
        # /session/join
        join_api = session_api.add_resource('join')
        join_api.add_method("GET", join_session_integration)

        # configure S3 for static frontend
        bucket = s3.Bucket(
            self,
            id="frontend",
            block_public_access=s3.BlockPublicAccess(block_public_policy=False),
            public_read_access=True,
            website_index_document="index.html"
            )
        s3_deployment.BucketDeployment(
            self,
            id="bucket_deployment",
            sources=[s3_deployment.Source.asset("ultimatum/frontend")],
            destination_bucket=bucket)
