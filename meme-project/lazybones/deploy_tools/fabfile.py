from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run

REPO_URL = 'https://github.com/dvgbiogeek/voting-app.git'


def deploy():
    site_folder = '/home/%s/sites/%s' % (env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)


def _create_directory_structure_if_necessary(site_folder):
    """Build directory structure if it doesn't already exist."""
    for subfolder in ('database', 'static', 'source', 'virtualenv'):
        # run says "run this shell command on the server"
        run('mkdir -p %s/%s' % (site_folder, subfolder))


def _get_latest_source(source_folder):
    """Pulls the latest source code."""
    # check if director exists on the server
    if exists(source_folder):
        # git fetch pulls the latest commit
        run('cd %s && git fetch' % (source_folder,))
    else:
        # clone repo from designated repo url into source folder
        run('git clone %s %s' % (REPO_URL, source_folder))
    # capture output from git log invocation to get a hash of the current
    # commit in the local tree.
    current_commit = local("git log -n 1 --format=%H", capture=True)
    # reset hard to current_commit to get rid of any current changes in the
    # server's code directory
    run('cd %s && git reset --hard %s' % (source_folder, current_commit))


def _update_settings(source_folder, site_name):
    """Update settings.py to set ALLOWED_HOSTS, DEBUG, and a new secret key."""
    settings_path = source_folder +
            'meme_project/lazybones/lazybones/settings.py'
    # string substitution from "DEBUG = True" to "DEBUG = False"
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    # string substitution in ALLOWED_HOSTS from regex to site_name
    # sed(settings_path, 'ALLOWED_HOSTS = .+$',
    #         'ALLOWED_HOSTS = ["%s"]' % (site_name))
    secret_key_file = source_folder +
            'meme_project/lazybones/lazybones/secret_key.py'
    # Generate a new secret_key and put it in the secret_key_file import it
    # into settings.py
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    # adds line to the end of the file to import the SECRET_KEY
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    """Update the virtual environment and install all the dependencies."""
    virtualenv_folder = source_folder + '/../virtualenv'
    # check if pip is installed in the virtualenv, and if not install it
    if not exists(virtualenv_folder + '/bin/pip'):
        run('virtualenv --python=python3 %s' % (virtualenv_folder,))
    # pip install all the requirements for the source code
    run('%s/bin/pip install -r %s/requirements.txt' % (
            virtualenv_folder, source_folder))


def _update_static_files(source_folder):
    """Update all the static files."""
    run('cd %s + "/meme_project/lazybones/" && ../../../virtualenv/bin/python3 manage.py collectstatic --noinput' % (source_folder))


def _update_database(source_folder):
    """Update the database using migrate (should not change contents)."""
    run('cd %s + "/meme_project/lazybones/" && ../../../virtualenv/bin/python3 manage.py migrate --noinput' % (source_folder))