from src.Lib.Env import env
from src.Lib.Cli import args

conf = {
    'instance_name' : env('instance_name'),
    'port' : env('port',80),
    'host' : env('host','0.0.0.0'),
    'self_url' : env('host','0.0.0.0'),
    'debug' : env('debug',True),
    'allowed_calculation_seconds' : int(env('allowed_calculation_seconds')),
    'allowed_communication_seconds' : int(env('allowed_communication_seconds')),
    'allowed_aggregation_seconds' : int(env('allowed_aggregation_seconds')),
    'allowed_test_of_train_seconds' : int(env('allowed_test_of_train_seconds')),
    'allowed_test_of_aggregation_seconds' : int(env('allowed_test_of_aggregation_seconds')),
    'communication_retries' : int(env('communication_retries')),
    'break_on_first_communication' : env('break_on_first_communication') == 'True',
    'epochs' : int(env('epochs')),
    'rounds' : int(env('rounds')),
    'neighbors' : args['neighbors'] if isinstance(args['neighbors'],list) else [args['neighbors']],
}
