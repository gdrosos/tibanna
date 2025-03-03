from tibanna.update_cost import update_cost
from tibanna.vars import AWS_REGION


config = {
    'function_name': 'update_cost_awsem',
    'function_module': 'service',
    'function_handler': 'handler',
    'handler': 'service.handler',
    'region': AWS_REGION,
    'runtime': 'python3.8',
    'role': 'tibanna_lambda_init_role',
    'description': 'update costs of a workflow run',
    'timeout': 300,
    'memory_size': 256
}


def handler(event, context):
    return update_cost(event)
