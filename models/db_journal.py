# -*- coding: utf-8 -*-

#article
db.define_table( 'article'
               , Field('author_user_id', 'reference auth_user', requires=IS_NOT_EMPTY(), notnull=True, label='Author')
               , Field('department_id', 'reference departments', label='Department')
               , Field('mentor_id', 'reference mentors', label='Mentor')
               , Field('title', requires=IS_NOT_EMPTY(), notnull=True)
               , Field('comments', 'text', length=65536)
               , Field('initial_approval', 'boolean', label='Initial Approval', default=None)
               , Field('final_approval', 'boolean', label='Final Approval', default=None)
               , Field('is_published', 'boolean', label='Article has been published', default=False)
               , Field('attatchment', 'upload', requires=IS_NOT_EMPTY(), notnull=True, label='Original Attatchment')
               , Field('edited_attatchment', 'upload', default='')
               , auth.signature
               , format='%(title)s'
               )


db.executesql('CREATE UNIQUE INDEX IF NOT EXISTS article_ui_1 ON article(author_user_id, department_id, mentor_id, title);')

db.article.id.readable = False

db.define_table('departments',
    Field('name', notnull=True, unique=True),
    Field('symposium_id','reference symposium', label='Symposium'),
    Field('submitted_sessions','boolean'),
    Field('default_sessions_created', 'boolean', default=False),
    Field('department_rep_user_id','reference auth_user', label='Department Representative'),
    auth.signature,
    format='%(name)s')

    