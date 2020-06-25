from aws_cdk import (
    core,
    aws_ec2,
    aws_efs,
    aws_lambda
)

class LambdaEfsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        vpc = aws_ec2.Vpc(
            self, "Vpc",
            max_azs = 3,
            nat_gateways = 0,
            subnet_configuration = [
                aws_ec2.SubnetConfiguration(
                    name = "public", cidr_mask = 24, subnet_type = aws_ec2.SubnetType.PUBLIC
                )
            ]
        )

        efs_share = aws_efs.CfnFileSystem(
            self, "efs-backend",
        )

        efs_lambda = aws_lambda.Function(self, "read_efs",
            runtime = aws_lambda.Runtime.PYTHON_3_8,
            code = aws_lambda.Code.from_asset("./function"),
            handler = "efsread.handler",
            timeout = core.Duration.seconds(20),
            memory_size = 128,
			retry_attempts = 0,
            tracing = aws_lambda.Tracing.ACTIVE,
            environment = {
                "var": "x"
            }
        )
