from aws_cdk import (
    Stack,
    aws_apprunner as apprunner,
)
from constructs import Construct

class InfraStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create a source code repository for App Runner
        source_repository = apprunner.CfnService.SourceConfigurationProperty(
            authentication_configuration=apprunner.CfnService.AuthenticationConfigurationProperty(
                connection_arn='arn:aws:apprunner:ap-northeast-1:450677052036:connection/t3yamoto/b483998d25ad43c581a11edce5b80fb5', # Replace with your connection arn
            ),
            code_repository=apprunner.CfnService.CodeRepositoryProperty(
                repository_url='https://github.com/t3yamoto/flask-on-app-runner',
                source_code_version=apprunner.CfnService.SourceCodeVersionProperty(
                    type='BRANCH',
                    value='main'
                ),
                code_configuration=apprunner.CfnService.CodeConfigurationProperty(
                    configuration_source='API',
                    code_configuration_values=apprunner.CfnService.CodeConfigurationValuesProperty(
                        runtime='PYTHON_3',
                        build_command='cd app && pip install -r requirements.txt',
                        start_command='cd app && flask --app main run --port 8080',
                    ),
                ),
            ),
        )

        # Create an App Runner service
        app_runner_service = apprunner.CfnService(
            self, 'AppRunnerService',
            service_name='AppRunnerExampleService',
            source_configuration=source_repository,
            instance_configuration=apprunner.CfnService.InstanceConfigurationProperty(
                cpu='1024',
                memory='2048',
            ),
        )
