#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/18 13:54
__author__ = 'F1renze'
__time__ = '2018/3/18 13:54'

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, \
    SubmitField, SelectField
from wtforms.validators import DataRequired, Length, \
    Email, EqualTo, Regexp
from wtforms import ValidationError
from app.models import VideoTag, Admin

class AdminLoginForm(FlaskForm):
    name = StringField('管理员账户', validators=[DataRequired('账户名不能为空!'), Length(1, 64),
                                            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                   '用户名只能以字母开头, 且只能包含字母, 数字, 点或下划线!')])
    password = PasswordField('密码', validators=[DataRequired('密码不能为空!')])
    login = SubmitField('登录')

class GlobalSet(FlaskForm):
    admin_url = StringField(label='后台管理URL')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('现在的密码', validators=[DataRequired('密码不能为空')])
    password = PasswordField('新的密码', validators=[DataRequired('密码不能为空'),
                                                 EqualTo('password2', message='两个密码必须一致')])
    password2 = PasswordField('再次确认新的密码', validators=[DataRequired('密码不能为空')])
    submit = SubmitField('更改密码')

class PasswordResetRequestForm(FlaskForm):
    name = StringField('管理员账户名', validators=[DataRequired('账户名不能为空!'), Length(1, 64),
                                             Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                    '用户名只能以字母开头, 且只能包含字母, 数字, 点或下划线!')])
    email = StringField('邮箱', validators=[DataRequired('账户邮箱不能为空!'), Length(1, 64), Email()])
    submit = SubmitField('重置密码')

    def validate_email(self, field):
        if not Admin.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱不存在!')

    def validate_name(self, field):
        if not Admin.query.filter_by(name=field.data).first():
            raise ValidationError('管理员账户名不存在!')

class PasswordResetForm(FlaskForm):
    password = PasswordField('新密码', validators=[DataRequired('新密码不能为空!'),
                                                EqualTo('password2', message='两个密码必须一致!')])
    password2 = PasswordField('再次确认新密码', validators=[DataRequired('密码不能为空!')])
    submit = SubmitField('重置密码')

class ChangeEmailForm(FlaskForm):
    email = StringField('新邮箱', validators=[DataRequired('新邮箱不能为空地址!'), Length(1, 64), Email()])
    password = PasswordField('密码', validators=[DataRequired('密码不能为空!')])
    submit = SubmitField('更换新邮箱')

    def validate_email(self, field):
        if Admin.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被使用')

'''
后台编辑表单
'''
from flask_admin.form import SecureForm
from wtforms import TextAreaField
from wtforms.widgets import TextArea

class CKTextAreaWidget(TextArea):
    def __call__(self, field, *args, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] = 'ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, *args, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

class UETextAreaWidget(TextArea):
    def __call__(self, field, *args, **kwargs):
        if kwargs.get('id'):
            kwargs['id'] = 'ue'
        else:
            kwargs.setdefault('id', 'ue')

        if kwargs.get('class'):
            kwargs['class'] = ''
        else:
            kwargs.setdefault('class', '')
        return super(UETextAreaWidget, self).__call__(field, *args, **kwargs)

class UETextAreaField(TextAreaField):
    widget = UETextAreaWidget()

class TagForm(SecureForm):
    name = StringField('分类名', validators=[DataRequired('分类名不能为空'), Length(1, 100),
                                          Regexp("^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]+$", 0,
                                                 '分类名只能包含汉字, 数字, 字母及下划线, 并且不能以下划线开头和结尾！')])

def tag_query_factory():
    return [t.name for t in VideoTag.query.all()]

from wtforms.ext.sqlalchemy.fields import QuerySelectField
class VideoForm(SecureForm):
    def get_pk(self):
        return self

    title = StringField('视频标题', validators=[DataRequired('视频标题不能为空'), Length(1, 200),
                                            Regexp("^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]+$", 0,
                                                   '视频标题只能包含汉字, 数字, 字母及下划线, 并且不能以下划线开头和结尾！')])
    tag = QuerySelectField('视频分类', validators=[DataRequired()],
                           query_factory=tag_query_factory, get_pk=get_pk)
    intro = CKTextAreaField('简介', validators=[DataRequired('简介不能为空')])

class UserForm(SecureForm):
    username = StringField('用户名', validators=[DataRequired('用户名不能为空'),
                                              Regexp("^(?!_)(?!.*?_$)[a-zA-Z0-9_\u4e00-\u9fa5]+$", 0,
                                                     '用户名只能包含汉字, 数字, 字母及下划线, 并且不能以下划线开头和结尾！'),
                                              Length(1, 128)])
    dis_haed_img = SelectField('禁用自定义头像',
                                    choices=[
                                        ('False', '否'), ('True', '是')
                                    ])
    locaion = StringField('所在地', validators=[Length(0, 64)])
    info = UETextAreaField('用户简介')

class AdminForm(SecureForm):
    name = StringField('账户名', validators=[DataRequired('账户名不能为空！'), Length(1, 64),
                                          Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                 '用户名只能以字母开头, 且只能包含字母, 数字, 点或下划线!')])
    email = StringField('邮箱', validators=[DataRequired('邮箱不能为空！'), Length(1, 64), Email()])
    # confirmed = SelectField('确认邮箱', choices=[
    #     ('True', '是'), ('False', '否')
    # ])
    password = PasswordField('密码', validators=[DataRequired('密码不能为空！'),
                                               EqualTo('password2', message='两次密码必须一致')])
    password2 = PasswordField('再次确认密码', validators=[DataRequired('确认密码不能为空!')])


