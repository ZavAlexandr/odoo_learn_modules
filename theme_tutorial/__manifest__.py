{
    'name': 'Tutorial theme',
    'description': 'A description for your theme.',
    'version': '1.0',
    'author': 'Your name',
    'category': 'Theme/Creative',

    'depends': ['website'],
    'data': [
        'views/assets.xml',
        'views/pages.xml',
        'views/snippets.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            '/theme_tutorial/static/scss/main.css'
        ],

    },
}