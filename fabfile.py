from fabric.api import env, local, cd, run

env.hosts = ['cloud']


def deploy():
    local('git push')
    with cd('~/code/cad'):
        run('git pull')
        run('./build.sh')
