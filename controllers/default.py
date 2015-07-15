# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


from gluon.tools import Crud

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to the BYU-I Research Journal")
    recentArticles = db(db.article.is_published == True).select(db.article.ALL, limitby=(0, 5))
    return locals()

def chapter():

    response.view = 'article_list.html'
    try:
        chapter = db.departments[request.args[0]]
    except IndexError:
        raise HTTP(404)

    if not chapter:
        raise HTTP(404)

    article_list = db(
        (db.article.department_id == chapter.id) &
        (db.auth_user.id == db.article.author_user_id) &
        (db.article.is_published == True)
    ).select()

    return locals()

def article():
    response.view = 'article_view.html'

    article = db.article(request.args(0))

    if not article or not article.is_published:
        raise HTTP(404)

    author_user = db.auth_user(article.author_user_id)

    return locals()

def search():
    response.view = 'search.html'

    crud = Crud(db)

    search_fields = [
        'title',
        'author_user_id',
        'department_id',
    ]
    form, records = crud.search(db.article, fields=search_fields)

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
