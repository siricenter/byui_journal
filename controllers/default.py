# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


import os

from gluon.tools import Crud

def index():
    """
    Homepage
    """
    recentArticles = db(db.article.publication_date != None).select(db.article.ALL, limitby=(0, 5))
    return locals()

def chapter():

    response.view = 'chapter_list.html'
    try:
        chapter = db.departments[request.args[0]]
    except IndexError:
        raise HTTP(404)

    if not chapter:
        raise HTTP(404)

    article_list = db(
        (db.article.department_id == chapter.id) &
        (db.auth_user.id == db.article.author_user_id) &
        (db.article.publication_date != None)
    ).select(orderby=~db.article.publication_date)

    return locals()

def article():
    response.view = 'article_view.html'

    article = db.article(request.args(0))

    if not article or not article.publication_date:
        raise HTTP(404)

    author_user = db.auth_user(article.author_user_id)

    return locals()

def search():
    response.view = 'search.html'

    crud = Crud(db)

    search_fields = [
        db.auth_user.first_name,
        db.auth_user.last_name,
        db.article.title,
    ]

    form = FORM(
        INPUT(
            _name="query",
        ),
        INPUT(
            _name="Search",
            _type='submit',
            _id="search-button",
        ),
        _method="GET",
    )

    article_list = []
    no_results = 'Please enter search terms'

    if request.get_vars.query:
        terms = request.get_vars.query.split()
        article_list = db(
            (
                # Search by author name
                (
                    db.auth_user.first_name.contains(terms)
                |
                    db.auth_user.last_name.contains(terms)
                )
                # Search by article title
                |
                    db.article.title.contains(terms)

            )
            # Make sure the article is actually published
            &
                (db.article.publication_date != None)
            &
                (db.article.author_user_id == db.auth_user.id)
        ).select(
            db.article.title,
            db.article.id,
            db.article.edited_attatchment,
            db.article.publication_date,
            db.auth_user.first_name,
            db.auth_user.last_name,
            #distinct=True,
        )

        no_results = "Nothing. Perhaps use more generic terms?"
        response.flash = None



    return locals()

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

@cache.action()
def embed_download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """

    if not request.args(0):
        raise HTTP(404)

    path = os.path.join('applications', 'rcwc', 'uploads', request.args(0))

    return response.stream(path, 400)

def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
