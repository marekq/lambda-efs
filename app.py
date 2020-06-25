#!/usr/bin/env python3

from aws_cdk import core

from lambda_efs.lambda_efs_stack import LambdaEfsStack


app = core.App()
LambdaEfsStack(app, "lambda-efs")

app.synth()
