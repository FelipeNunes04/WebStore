# coding: utf-8
import unipath
from fabric.api import *
from fabric.contrib import files


env.hosts = ['root@virtuallia.com.br']
env.server_user = 'virtuallia'
env.home_dir = unipath.Path('/home/virtuallia/')
env.virtualenv = env.home_dir.child('_env')
env.working_copy_dir = env.home_dir.child('project')
env.project_dir = env.working_copy_dir.child('django', 'app')
env.project_init_d = 'virtuallia_app'

def change_branch(b):
    sudo('su -l %s -c "cd %s && hg up %s"' % (env.server_user, env.working_copy_dir, b))


def deploy():
    puts('Deploying project')
    deploy_code()
    update_dependencies()
    syncdb()
    migrate()
    compile_js()
    compile_css()
    collectstatic()
    gunicorn('stop')
    #nginx('restart')
    gunicorn('start')

def up():
    puts('Updating project')
    deploy_code()
    syncdb()
    migrate()
    #compile_js()
    #compile_css()
    collectstatic()
    rebuild_index()
    gunicorn('stop')
    #nginx('restart')
    gunicorn('start')

def gunicorn(cmd):
    try:
        sudo('service %s %s' % (env.project_init_d, cmd))
    except:
        print '!!! Error trying to %s gunicorn' % (cmd)

def nginx(cmd):
    # start/restart/stop/reload
    sudo('service nginx %s' % cmd)

def memcached(cmd):
    puts('Memcache %s...' % cmd)
    sudo('service memcached %s' % cmd)

def rebuild_index():
    puts('rebuild index')
    manage_py('rebuild_index --noinput')

def collectstatic():
    puts('Collecting static files...')
    manage_py('collectstatic --noinput')

def rebuild_index():
    puts('rebuild index')
    manage_py('rebuild_index --noinput')

def syncdb():
    puts('Syncdb...')
    manage_py('syncdb')

def migrate(app_name=''):
    puts('Migrating...')
    manage_py('migrate %s' % app_name)

def compile_js():
    puts('Compiling JS...')
    manage_py('compilejs')

def compile_css():
    puts('Compiling CSS...')
    manage_py('compress')

def deploy_code():
    puts('Updating from BitBucket...')
    sudo('su -l %s -c "cd %s && hg pull -u"' % (env.server_user, env.working_copy_dir))

def update_dependencies():
    puts('Updating dependencies...')
    pip = env.virtualenv.child('bin', 'pip')
    reqs = env.working_copy_dir.child('django', 'requirements.txt')
    sudo('su -l %s -c "%s -q install -r %s"' % (env.server_user, pip, reqs))

def reset(app_name):
    puts('Reseting app %s...' % app_name)
    manage_py('reset %s' % app_name)

def manage_py(cmd):
    sudo('su -l %s -c "cd %s && ./manage.py %s"' % (env.server_user, env.project_dir, cmd))
