import os

import git

import config
import util.response
from linkr import app
from uri.misc import *
from util.decorators import *


@app.route(ConfigURI.get_path(), methods=ConfigURI.methods)
@require_form_args()
@require_login_api(admin_only=True)
@require_frontend_api
@api_method
@time_request('latency.api.misc.config')
def api_config(data):
    """
    Retrieve the current application configuration options.
    """
    try:
        return util.response.success({
            'config': {
                'options': dict(config.options.client(''), **config.options.server('')),
                'secrets': dict(config.secrets.client(''), **config.secrets.server('')),
            },
        })
    except:
        return util.response.undefined_error()


@app.route(VersionURI.get_path(), methods=VersionURI.methods)
@require_form_args()
@require_login_api(admin_only=True)
@require_frontend_api
@api_method
@time_request('latency.api.misc.version')
def api_version(data):
    """
    Retrieve the deployed instance's version information via Git.
    """
    repo = git.Repo(os.getcwd())

    try:
        return util.response.success({
            'version': {
                'branch': repo.active_branch.name,
                'sha': repo.active_branch.commit.hexsha,
                'message': repo.active_branch.commit.message,
                'date': repo.active_branch.commit.authored_datetime.isoformat(),
                'remote': {
                    repo.remote().name: [url for url in repo.remote().urls],
                },
            },
        })
    except:
        return util.response.undefined_error()
