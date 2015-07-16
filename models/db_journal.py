# -*- coding: utf-8 -*-

from os.path import join

upload_folder = join(request.folder, '..', 'rcwc', 'uploads')

#article
db.define_table( 'article'
               , Field('author_user_id', 'reference auth_user', requires=IS_NOT_EMPTY(), notnull=True, label='Author')
               , Field('department_id', 'reference departments', label='Department')
               , Field('mentor_id', 'reference mentors', label='Mentor')
               , Field('title', requires=IS_NOT_EMPTY(), notnull=True)
               , Field('comments', 'text', length=65536)
               , Field('initial_approval', 'boolean', label='Initial Approval', default=None)
               , Field('final_approval', 'boolean', label='Final Approval', default=None)
               , Field('publication_date', 'date', requires=IS_DATE(), label='Date of Publication', default=None)
               , Field('attatchment', 'upload', uploadfolder=upload_folder, requires=IS_NOT_EMPTY(), notnull=True, label='Original Attatchment')
               , Field('edited_attatchment', 'upload', uploadfolder=upload_folder, default='')
               , auth.signature
               , format='%(title)s'
               )


db.executesql('CREATE UNIQUE INDEX IF NOT EXISTS article_ui_1 ON article(author_user_id, department_id, mentor_id, title);')

db.article.id.readable = False

db.define_table('departments',
    Field('name', notnull=True, unique=True),
    Field('symposium_id','reference symposium', label='Symposium'),
    Field('department_rep_user_id','reference auth_user', label='Department Representative'),
    auth.signature,
    format='%(name)s')

# added strictly because they are dependencies
db.define_table('symposium',
    Field('name', notnull=True, unique=True),
    auth.signature,
    format='%(name)s'
    )
def repr_mentor_table(referenced_mentor_record):

    retrieved_user = db(db.auth_user.id == referenced_mentor_record.auth_user_id) \
                       .select(db.auth_user.first_name, db.auth_user.last_name).first()

    return "%(first_name)s %(last_name)s" % {'first_name':retrieved_user.first_name
                                            ,'last_name':retrieved_user.last_name
                                            }
db.define_table('mentors',
    Field('auth_user_id', 'reference auth_user', unique=True),
    Field('department_id', 'reference departments', label='Department'),
    auth.signature,
    format=repr_mentor_table)
