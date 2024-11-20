from app.helpers import get_latest_git_tag

api_description = {
    'title': 'SaveMyWallet API',
    'description': 'API RESTful manage personal finance',
    'version': get_latest_git_tag(),
}
