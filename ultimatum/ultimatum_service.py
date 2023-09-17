import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (aws_apigateway as apigateway,
                     aws_lambda as lambda_,
                     aws_s3 as s3,
                     aws_s3_deployment as s3_deployment,
                     aws_dynamodb as dynamodb)

class UltimatumService(Construct):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # configure a database
        table = dynamodb.Table(
            self,
            'Sessions',
            partition_key=dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST
        )
        table_name = table.table_name

        # config lambda for the backend
        create_session_handler = lambda_.Function(self, "create_session_handler",
                    runtime=lambda_.Runtime.PYTHON_3_7,
                    code=lambda_.Code.from_asset("ultimatum"),
                    handler="ultimatum_handler.create_session",
                    environment={'TABLE_NAME': table_name}
                    )
        join_session_handler = lambda_.Function(self, "join_session_handler",
                    runtime=lambda_.Runtime.PYTHON_3_7,
                    code=lambda_.Code.from_asset("ultimatum"),
                    handler="ultimatum_handler.join_session",
                    environment={'TABLE_NAME': table_name}
                    )
        table.grant_full_access(create_session_handler)
        table.grant_full_access(join_session_handler)

        # config gateway for handling traffic
        api = apigateway.RestApi(self, "ultimatum-api",
                    rest_api_name="Ultimatum Service",
                    description="This service handles the Ultimatum app.",
                    default_cors_preflight_options=apigateway.CorsOptions(
                        allow_origins=apigateway.Cors.ALL_ORIGINS,
                        allow_methods=apigateway.Cors.ALL_METHODS
                    ))
        create_session_integration = apigateway.LambdaIntegration(create_session_handler)
        join_session_integration = apigateway.LambdaIntegration(join_session_handler)
        # POST /session
        session_api = api.root.add_resource('session')
        session_api.add_method("POST", create_session_integration)
        # POST /session/join
        join_api = session_api.add_resource('join')
        join_api.add_method("POST", join_session_integration)

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
