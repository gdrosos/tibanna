"""
CLI for tibanna package
"""

# -*- coding: utf-8 -*-
import argparse
import inspect
from ._version import __version__
# from botocore.errorfactory import ExecutionAlreadyExists
from .core import API
from .vars import TIBANNA_DEFAULT_STEP_FUNCTION_NAME

PACKAGE_NAME = 'tibanna'


class Subcommands(object):

    def __init__(self):
        pass

    @property
    def descriptions(self):
        return {
            # add more later
            'add_user': 'add an (IAM) user to a Tibanna usergroup',
            'deploy_core': 'New method of deploying packaged lambdas (BETA)',
            'deploy_unicorn': 'deploy tibanna unicorn to AWS cloud (unicorn is for everyone)',
            'kill': 'kill a specific job',
            'kill_all': 'kill all the running jobs on a step function',
            'list_sfns': 'list all step functions, optionally with a summary (-n)',
            'log': 'print execution log or postrun json for a job',
            'rerun': 'rerun a specific job',
            'rerun_many': 'rerun all the jobs that failed after a given time point',
            'run_workflow': 'run a workflow',
            'setup_tibanna_env': 'set up usergroup environment on AWS.' +
                                 'This function is called automatically by deploy_tibanna or deploy_unicorn.' +
                                 'Use it only when the IAM permissions need to be reset',
            'stat': 'print out executions with details',
            'test': 'test tibanna code (currently reserved for development at 4dn-dcic)',  # test doesn't work
            'users': 'list all users along with their associated tibanna user groups',
        }

    @property
    def args(self):
        return {
            'run_workflow':
                [{'flag': ["-i", "--input-json"], 'help': "tibanna input json file"},
                 {'flag': ["-s", "--sfn"],
                  'help': "tibanna step function name (e.g. 'tibanna_unicorn_monty'); " +
                          "your current default is %s)" % TIBANNA_DEFAULT_STEP_FUNCTION_NAME,
                  'default': TIBANNA_DEFAULT_STEP_FUNCTION_NAME},
                 {'flag': ["-j", "--jobid"],
                  'help': "specify a user-defined job id (randomly generated if not specified)"},
                 {'flag': ["-S", "--sleep"],
                  'help': "number of seconds between submission, to avoid drop-out (default 3)",
                  'default': 3}],
            'stat':
                [{'flag': ["-s", "--sfn"],
                  'help': "tibanna step function name (e.g. 'tibanna_unicorn_monty'); " +
                          "your current default is %s)" % TIBANNA_DEFAULT_STEP_FUNCTION_NAME,
                  'default': TIBANNA_DEFAULT_STEP_FUNCTION_NAME},
                 {'flag': ["-t", "--status"],
                  'help': "filter by status; 'RUNNING'|'SUCCEEDED'|'FAILED'|'TIMED_OUT'|'ABORTED'"},
                 {'flag': ["-l", "--long"],
                  'help': "more comprehensive information",
                  'action': "store_true"}],
            'kill':
                [{'flag': ["-e", "--exec-arn"],
                  'help': "execution arn of the specific job to kill"},
                 {'flag': ["-j", "--job-id"],
                  'help': "job id of the specific job to kill (alternative to --exec-arn/-e)"},
                 {'flag': ["-s", "--sfn"],
                  'help': "tibanna step function name (e.g. 'tibanna_unicorn_monty'); " +
                          "your current default is %s)" % TIBANNA_DEFAULT_STEP_FUNCTION_NAME,
                  'default': TIBANNA_DEFAULT_STEP_FUNCTION_NAME}],
            'kill_all':
                [{'flag': ["-s", "--sfn"],
                  'help': "tibanna step function name (e.g. 'tibanna_unicorn_monty'); " +
                          "your current default is %s)" % TIBANNA_DEFAULT_STEP_FUNCTION_NAME,
                  'default': TIBANNA_DEFAULT_STEP_FUNCTION_NAME}],
            'log':
                [{'flag': ["-e", "--exec-arn"],
                  'help': "execution arn of the specific job to log"},
                 {'flag': ["-j", "--job-id"],
                  'help': "job id of the specific job to log (alternative to --exec-arn/-e)"},
                 {'flag': ["-n", "--exec-name"],
                  'help': "execution name of the specific job to log " +
                          "(alternative to --exec-arn/-e or --job-id/-j"},
                 {'flag': ["-s", "--sfn"],
                  'help': "tibanna step function name (e.g. 'tibanna_unicorn_monty'); " +
                          "your current default is %s)" % TIBANNA_DEFAULT_STEP_FUNCTION_NAME,
                  'default': TIBANNA_DEFAULT_STEP_FUNCTION_NAME},
                 {'flag': ["-p", "--postrunjson"],
                  'help': "print out postrun json instead", 'action': "store_true"}],
            'add_user':
                [{'flag': ["-u", "--user"],
                  'help': "user to add to a Tibanna usergroup"},
                 {'flag': ["-g", "--usergroup"],
                  'help': "Tibanna usergroup to add the user to"}],
            'list_sfns':
                [{'flag': ["-s", "--sfn-type"],
                  'default': 'unicorn',
                  'help': "tibanna step function type ('unicorn' vs 'pony')"},
                 {'flag': ["-n", "--numbers"],
                  'help': "print out the number of executions along with the step functions",
                  'action': "store_true"}],
            'rerun':
                [{'flag': ["-e", "--exec-arn"],
                  'help': "execution arn of the specific job to rerun"},
                 {'flag': ["-s", "--sfn"],
                  'default': TIBANNA_DEFAULT_STEP_FUNCTION_NAME,
                  'help': "tibanna step function name (e.g. 'tibanna_unicorn_monty'); " +
                          "your current default is %s)" % TIBANNA_DEFAULT_STEP_FUNCTION_NAME},
                 {'flag': ["-a", "--appname_filter"],
                  'help': "rerun only the ones that match this appname"},
                 {'flag': ["-i", "--instance-type"],
                  'help': "use a specified instance type for the rerun"},
                 {'flag': ["-d", "--shutdown-min"],
                  'help': "use a specified shutdown mininutes for the rerun"},
                 {'flag': ["-b", "--ebs-size"],
                  'help': "use a specified ebs size for the rerun (GB)"},
                 {'flag': ["-T", "--ebs-type"],
                  'help': "use a specified ebs type for the rerun (gp2 vs io1)"},
                 {'flag': ["-p", "--ebs-iops"],
                  'help': "use a specified ebs iops for the rerun"},
                 {'flag': ["-k", "--key-name"],
                  'help': "use a specified key name for the rerun"},
                 {'flag': ["-n", "--name"],
                  'help': "use a specified run name for the rerun"},
                 {'flag': ["-x", "--overwrite-input-extra"],
                  'help': "overwrite input extra file if it already exists (reserved for pony)"}],
            'rerun_many':
                [{'flag': ["-s", "--sfn"],
                  'default': TIBANNA_DEFAULT_STEP_FUNCTION_NAME,
                  'help': "tibanna step function name (e.g. 'tibanna_unicorn_monty'); " +
                          "your current default is %s)" % TIBANNA_DEFAULT_STEP_FUNCTION_NAME},
                 {'flag': ["-D", "--stopdate"],
                  'default': '13Feb2018',
                  'help': "stop (end) date of the executions (e.g. '13Feb2018')"},
                 {'flag': ["-H", "--stophour"],
                  'default': 13,
                  'help': "stop (end) hour of the executions (e.g. 13, for 1pm)"},
                 {'flag': ["-M", "--stopminute"],
                  'default': 0,
                  'help': "stop (end) minute of the executions (e.g. 55)"},
                 {'flag': ["-o", "--offset"],
                  'default': 0,
                  'help': "offset for time zone between local computer and AWS step function"},
                 {'flag': ["-r", "--sleeptime"],
                  'default': 5,
                  'help': "minutes to sleep between runs to avoid drop outs"},
                 {'flag': ["-t", "--status"],
                  'default': 'FAILED',
                  'help': "filter by status (e.g. if set to FAILED, rerun only FAILED jobs); " +
                          "'RUNNING'|'SUCCEEDED'|'FAILED'|'TIMED_OUT'|'ABORTED'"},
                 {'flag': ["-a", "--appname_filter"],
                  'help': "rerun only the ones that match this appname"},
                 {'flag': ["-i", "--instance-type"],
                  'help': "use a specified instance type for the rerun"},
                 {'flag': ["-d", "--shutdown-min"],
                  'help': "use a specified shutdown mininutes for the rerun"},
                 {'flag': ["-b", "--ebs-size"],
                  'help': "use a specified ebs size for the rerun (GB)"},
                 {'flag': ["-T", "--ebs-type"],
                  'help': "use a specified ebs type for the rerun (gp2 vs io1)"},
                 {'flag': ["-p", "--ebs-iops"],
                  'help': "use a specified ebs iops for the rerun"},
                 {'flag': ["-k", "--key-name"],
                  'help': "use a specified key name for the rerun"},
                 {'flag': ["-n", "--name"],
                  'help': "use a specified run name for the rerun"},
                 {'flag': ["-x", "--overwrite-input-extra"],
                  'help': "overwrite input extra file if it already exists (reserved for pony)"}],
            'setup_tibanna_env':
                [{'flag': ["-b", "--buckets"],
                  'help': "list of buckets to add permission to a tibanna usergroup"},
                 {'flag': ["-g", "--usergroup-tag"],
                  'help': "tibanna usergroup tag you want to use " +
                          "(e.g. name of a specific tibanna usergroup"},
                 {'flag': ["-R", "--no-randomize"],
                  'help': "do not add random numbers to the usergroup tag to generate usergroup name",
                  'action': "store_true"}],
            'deploy_unicorn':
                [{'flag': ["-s", "--suffix"],
                  'help': "suffix (e.g. 'dev') to add to the end of the name of" +
                          "tibanna_unicorn and AWS Lambda functions within the same usergroup"},
                 {'flag': ["-b", "--buckets"],
                  'help': "list of buckets to add permission to a tibanna usergroup"},
                 {'flag': ["-S", "--no-setup"],
                  'help': "do not perform permission setup; just update step functions / lambdas",
                  'action': "store_true"},
                 {'flag': ["-E", "--no-setenv"],
                  'help': "Do not overwrite TIBANNA_DEFAULT_STEP_FUNCTION_NAME" +
                          "environmental variable in your .bashrc",
                  'action': "store_true"},
                 {'flag': ["-g", "--usergroup"],
                  'help': "Tibanna usergroup to share the permission to access buckets and run jobs"}],
            'deploy_core':
                [{'flag': ["-n", "--name"],
                  'help': "name of the lambda function to deploy (e.g. run_task_awsem)"},
                 {'flag': ["-t", "--tests"],
                  'help': "run test before deployment",
                  'action': 'store_true'},
                 {'flag': ["-s", "--suffix"],
                  'help': "suffix (e.g. 'dev') to add to the end of the name of the AWS " +
                          "Lambda function, within the same usergroup"},
                 {'flag': ["-g", "--usergroup"],
                  'help': "Tibanna usergroup for the AWS Lambda function"}],
            'test':
                [{'flag': ["-F", "--no-flake"],
                  'help': "skip flake8 tests", 'action': "store_true"},
                 {'flag': ["-P", "--ignore-pony"],
                  'help': "skip tests for tibanna pony", 'action': "store_true"},
                 {'flag': ["-W", "--ignore-webdev"],
                  'help': "skip tests for 4DN test portal webdev", 'action': "store_true"},
                 {'flag': ["-w", "--watch"],
                  'help': "watch", 'action': "store_true"},  # need more detail
                 {'flag': ["-f", "--last-failing"],
                  'help': "last failing", 'action': "store_true"},  # need more detail
                 {'flag': ["-i", "--ignore"],
                  'help': "ignore"},  # need more detail
                 {'flag': ["-x", "--extra"],
                  'help': "extra"},  # need more detail
                 {'flag': ["-k", "--k"],
                  'help': "k"}]  # need more detail
        }


def test(watch=False, last_failing=False, no_flake=False, k='',  extra='',
         ignore='', ignore_pony=False, ignore_webdev=False):
    """Run the tests.
    Note: --watch requires pytest-xdist to be installed.
    """
    from .test_utils import test as _test
    _test(watch=watch, last_failing=last_failing, no_flake=no_flake, k=k,
          extra=extra, ignore=ignore, ignore_pony=ignore_pony, ignore_webdev=ignore_webdev)


def deploy_core(name, tests=False, suffix=None, usergroup=None):
    """
    New method of deploying pacaked lambdas (BETA)
    """
    API().deploy_core(name=name, tests=tests, suffix=suffix, usergroup=usergroup)


def run_workflow(input_json, sfn=TIBANNA_DEFAULT_STEP_FUNCTION_NAME, jobid='', sleep=3):
    """run a workflow"""
    API().run_workflow(input_json, sfn=sfn, jobid=jobid, sleep=sleep, verbose=True)


def setup_tibanna_env(buckets='', usergroup_tag='default', no_randomize=False):
    """set up usergroup environment on AWS
    This function is called automatically by deploy_tibanna or deploy_unicorn
    Use it only when the IAM permissions need to be reset"""
    API().setup_tibanna_env(buckets=buckets, usergroup_tag=usergroup_tag, no_randomize=no_randomize, verbose=False)


def deploy_unicorn(suffix=None, no_setup=False, buckets='',
                   no_setenv=False, usergroup=None):
    """deploy tibanna unicorn to AWS cloud"""
    API().deploy_unicorn(suffix=suffix, no_setup=no_setup, buckets=buckets, no_setenv=no_setenv,
                         usergroup=usergroup)


def add_user(user, usergroup):
    """add a user to a tibanna group"""
    API().add_user(user=user, usergroup=usergroup)


def users():
    """list all users along with their associated tibanna user groups"""
    API().users()


def list_sfns(numbers=False):
    """list all step functions, optionally with a summary (-n)"""
    API().list_sfns(numbers=numbers)


def log(exec_arn=None, job_id=None, exec_name=None, sfn=TIBANNA_DEFAULT_STEP_FUNCTION_NAME, postrunjson=False):
    """print execution log or postrun json (-p) for a job"""
    print(API().log(exec_arn, job_id, exec_name, sfn, postrunjson))


def kill_all(sfn=TIBANNA_DEFAULT_STEP_FUNCTION_NAME):
    """kill all the running jobs on a step function"""
    API().kill_all(sfn)


def kill(exec_arn=None, job_id=None, sfn=TIBANNA_DEFAULT_STEP_FUNCTION_NAME):
    """kill a specific job"""
    API().kill(exec_arn, job_id, sfn)


def rerun(exec_arn, sfn=TIBANNA_DEFAULT_STEP_FUNCTION_NAME, appname_filter=None,
          instance_type=None, shutdown_min=None, ebs_size=None, ebs_type=None, ebs_iops=None,
          overwrite_input_extra=None, key_name=None, name=None):
    """ rerun a specific job"""
    API().rerun(exec_arn, sfn=sfn,
                appname_filter=appname_filter, instance_type=instance_type, shutdown_min=shutdown_min,
                ebs_size=ebs_size, ebs_type=ebs_type, ebs_iops=ebs_iops,
                overwrite_input_extra=overwrite_input_extra, key_name=key_name, name=name)


def rerun_many(sfn=TIBANNA_DEFAULT_STEP_FUNCTION_NAME, stopdate='13Feb2018', stophour=13,
               stopminute=0, offset=0, sleeptime=5, status='FAILED', appname_filter=None,
               instance_type=None, shutdown_min=None, ebs_size=None, ebs_type=None, ebs_iops=None,
               overwrite_input_extra=None, key_name=None, name=None):
    """rerun all the jobs that failed after a given time point
    filtered by the time when the run failed (stopdate, stophour (24-hour format), stopminute)
    By default, stophour should be the same as your system time zone. This can be changed by setting a different offset.
    If offset=5, for instance, that means your stoptime=12 would correspond to your system time=17.
    Sleeptime is sleep time in seconds between rerun submissions.
    By default, it reruns only 'FAILED' runs, but this can be changed by resetting status.

    Examples

    rerun_many('tibanna_pony-dev')
    rerun_many('tibanna_pony', stopdate= '14Feb2018', stophour=14, stopminute=20)
    """
    API().rerun_many(sfn=sfn, stopdate=stopdate, stophour=stophour,
                     stopminute=stopminute, offset=offset, sleeptime=sleeptime, status=status,
                     appname_filter=appname_filter, instance_type=instance_type, shutdown_min=shutdown_min,
                     ebs_size=ebs_size, ebs_type=ebs_type, ebs_iops=ebs_iops,
                     overwrite_input_extra=overwrite_input_extra, key_name=key_name, name=name)


def stat(sfn=TIBANNA_DEFAULT_STEP_FUNCTION_NAME, status=None, long=False):
    """print out executions with details
    status can be one of 'RUNNING'|'SUCCEEDED'|'FAILED'|'TIMED_OUT'|'ABORTED'
    """
    API().stat(sfn=sfn, status=status, verbose=long)


def main(Subcommands=Subcommands):
    """
    Execute the program from the command line
    """
    scs = Subcommands()

    # the primary parser is used for tibanna -v or -h
    primary_parser = argparse.ArgumentParser(prog=PACKAGE_NAME, add_help=False)
    primary_parser.add_argument('-v', '--version', action='version',
                                version='%(prog)s ' + __version__)
    # the secondary parser is used for the specific run mode
    secondary_parser = argparse.ArgumentParser(prog=PACKAGE_NAME, parents=[primary_parser])
    # the subparsers collect the args used to run the hic2cool mode
    subparsers = secondary_parser.add_subparsers(
        title=PACKAGE_NAME + ' subcommands',
        description='choose one of the following subcommands to run ' + PACKAGE_NAME,
        dest='subcommand',
        metavar='subcommand: {%s}' % ', '.join(scs.descriptions.keys())
    )
    subparsers.required = True

    def add_arg(name, flag, **kwargs):
        subparser[name].add_argument(flag[0], flag[1], **kwargs)

    def add_args(name, argdictlist):
        for argdict in argdictlist:
            add_arg(name, **argdict)

    subparser = dict()
    for sc, desc in scs.descriptions.items():
        subparser[sc] = subparsers.add_parser(sc, help=desc, description=desc)
        if sc in scs.args:
            add_args(sc, scs.args[sc])

    # two step argument parsing
    # first check for top level -v or -h (i.e. `tibanna -v`)
    (primary_namespace, remaining) = primary_parser.parse_known_args()
    # get subcommand-specific args
    args = secondary_parser.parse_args(args=remaining, namespace=primary_namespace)
    subcommandf = eval(args.subcommand)
    sc_args = [getattr(args, sc_arg) for sc_arg in inspect.getargspec(subcommandf).args]
    # run subcommand
    subcommandf(*sc_args)


if __name__ == '__main__':
    main()
