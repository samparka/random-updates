#! -*- coding:utf-8 -*-
# Created by F1renze on 2018/3/21 9:06
__author__ = 'F1renze'
__time__ = '2018/3/21 9:06'

from . import auth
from flask import request, redirect, url_for, flash, \
    render_template, abort, session
from app.auth.forms import LoginForm, RegistrationForm, PasswordResetRequestForm, ChangePasswordForm, ChangeEmailForm, PasswordResetForm
from app.models import User, UserLog, Admin
from flask_login import login_user, login_required, logout_user, current_user
from app import db, login_manager
from app.email import send_email

# flask-login需要提供一个 user_loader回调
@login_manager.user_loader
def load_user(user_id):
    if 'is_user' in session:
        return User.query.filter_by(id=user_id).first()
    if Admin.query.get(user_id):
        return Admin.query.get(user_id)

@auth.before_app_request
def before_request():
    if current_user.is_authenticated and not current_user.is_admin \
            and not current_user.confirmed and \
            request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))
    elif current_user.is_authenticated and not current_user.is_admin and \
            request.path[:6] == '/admin':
        abort(403)
        return redirect(url_for('home.index'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            session['is_user'] = 'True'
            login_user(user, form.remember_me.data)
            user.ping()
            user_log = UserLog(user_id=user.id,
                               ip=request.remote_addr, info='登录')
            db.session.add(user_log)
            try:
                db.session.commit()
            except:
                db.session.rollback()
            finally:
                return redirect(request.args.get('next') or url_for('home.index'))
        flash('无效用户名或密码')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    if 'is_user' in session:
        session.pop('is_user')
    logout_user()
    flash('已经退出当前账户')
    return redirect(url_for('home.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
        token = user.generate_confirmation_token()
        send_email(user.email, '确认账户', 'auth/email/confirm',
                  user=user, token=token)
        flash('一封确认邮件已经发送, 请检查你的邮箱')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)



@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('home.index'))
    return render_template('auth/unconfirmed.html')

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('home.index'))
    if current_user.confirm(token):
        flash('账户已确认啦, 随便逛逛')
    else:
        flash('账户确认链接过期或无效!')
    return redirect(url_for('home.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, '确认账户', 'auth/email/confirm', user=current_user, token=token)
    flash('一封新的确认邮件已经发送, 请检查你的邮箱')
    return redirect(url_for('home.index'))

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            try:
                db.session.commit()
            except:
                db.session.rollback()
            flash('密码已更改!')
            return redirect(url_for('home.index'))
        else:
            flash('无效密码')
    return render_template('auth/change_password.html', form=form)

@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('home.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, '重置密码', 'auth/email/reset_password',
                      user=user, token=token, next=request.args.get('next'))
            flash('重置密码邮件已经发送!')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', form=form)

@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('home.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('密码已重置')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('home.index'))
    return render_template('auth/reset_password.html', form=form)

@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, '确认新邮箱地址', 'auth/email/change_email',
                       user=current_user, token=token)
            flash('确认邮箱地址的邮件已经发送, 请检查收件箱')
            return redirect(url_for('home.index'))
        else:
            flash('无效邮箱或密码')
    return render_template('auth/change_email.html', form=form)

@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('你的邮箱已经更改')
    else:
        flash('无效请求!')
    return redirect(url_for('home.index'))


if __name__ == '__main__':
    pass