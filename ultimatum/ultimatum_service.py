import aws_cdk as cdk
from constructs import Construct
from aws_cdk import (aws_apigateway as apigateway,
                     aws_lambda as lambda_)

class UltimatumService(Construct):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        handler = lambda_.Function(self, "UltimatumHandler",
                    runtime=lambda_.Runtime.PYTHON_3_7,
                    code=lambda_.Code.from_asset("ultimatum"),
                    handler="ultimatum_handler.hello"
                    )

        api = apigateway.RestApi(self, "ultimatum-api",
                  rest_api_name="Ultimatum Service",
                  description="This service handles the Ultimatum app.")
        get_widgets_integration = apigateway.LambdaIntegration(handler,
                request_templates={"application/json": '{ "statusCode": "200" }'})
        api.root.add_method("GET", get_widgets_integration)
