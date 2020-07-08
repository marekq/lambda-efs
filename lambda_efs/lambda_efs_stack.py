from aws_cdk import (
    core,
    aws_ec2,
    aws_lambda,
    aws_efs,
    aws_iam
)

class LambdaEfsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create vpc
        vpc = aws_ec2.Vpc(
            self, "vpc",
            max_azs = 3,
            nat_gateways = 1
        )

        # create efs share
        efs_share = aws_efs.FileSystem(self, 
            "efs-backend", 
            vpc = vpc
        )

        # create efs acl
        efs_acl = aws_efs.Acl(
            owner_gid = "1000",
            owner_uid = "1000",
            permissions = "0777"
        )

        # create efs posix user
        efs_user = aws_efs.PosixUser(
            gid = "1000",
            uid = "1000"
        )

        # create efs access point
        efs_ap = aws_efs.AccessPoint(self, 
            "efs-accesspoint",
            path = "/efs",
            file_system = efs_share,
            posix_user = efs_user,
            create_acl = efs_acl
        )

        # create lambda with efs access
        efs_lambda = aws_lambda.Function(self, 
            "read_efs",
            runtime = aws_lambda.Runtime.PYTHON_3_8,
            code = aws_lambda.Code.from_asset("./function"),
            handler = "efsread.handler",
            timeout = core.Duration.seconds(20),
            memory_size = 128,
			retry_attempts = 0,
            filesystem = aws_lambda.FileSystem.from_efs_access_point(efs_ap, '/mnt/efs'),
            tracing = aws_lambda.Tracing.ACTIVE,
            vpc = vpc,
            environment = {
                "var": "x"
            }
        )

        # create custom iam policy with efs permissions
        efs_policy = aws_iam.PolicyStatement(
            resources = ["*"],
            actions = ["elasticfilesystem:*"]
        )

        # add efs iam policy to lambda
        efs_lambda.add_to_role_policy(efs_policy)
