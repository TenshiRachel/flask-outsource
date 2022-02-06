import config.constants
import paypalrestsdk
import smtplib
import time
import webbrowser
from flask import Blueprint, render_template, request, url_for, redirect, flash, session
from pathlib import Path
from datetime import date
from uuid import uuid4
from middlewares.auth import is_auth
from utilities.auth import encrypt, decrypt
from models.service import Service
from models.user import User
from models.job import Job


service_bp = Blueprint('service', __name__, template_folder=config.constants.template_dir,
                       static_folder=config.constants.static_dir, static_url_path='public', url_prefix='/service')

paypalrestsdk.configure({
    "mode": "sandbox",  # sandbox or live
    "client_id": "",
    "client_secret": ""
})


@service_bp.route('/list')
def list_service():
    user_id = session.get('user_id')
    user = User.get_or_none(User.id == user_id)
    services = Service.select()
    return render_template('service/list.html', services=services, user=user)


@service_bp.route('/view/<uid>/<id>')
def view(uid, id):
    user_id = session.get('user_id')
    user = User.get_or_none(User.id == user_id)
    service = Service.get_or_none(Service.id == id)
    if service is None:
        flash('Service not found', 'error')
        return redirect(url_for('service.list_service'))
    service_user = User.get_by_id(uid)
    job = Job.get_or_none(Job.sid == id, Job.cid == user_id)

    query = Service.update(views=service.views + 1).where(Service.id == id)
    query.execute()
    return render_template('service/index.html', services=service, service_user=service_user, user=user, job=job)


@service_bp.route('/fav/<id>', methods=['POST'])
@is_auth
def fav(id):
    if request.method == 'POST':
        service = Service.get_or_none(Service.id == id)

        if service is None:
            flash('Service not found', 'error')
            return redirect(url_for('service.list_service'))

        flash('Service favorited', 'success')
        return redirect(url_for('service.list_service'))


@service_bp.route('/manage')
@is_auth
def manage():
    user_id = session['user_id']
    user = User.get_by_id(user_id)

    if user.acc_type == 'client':
        flash('You need a service provider account to manage services', 'error')
        return redirect(url_for('index.index'))

    services = Service.select().where(Service.uid == user_id)
    return render_template('service/manage.html', services=services, user=user)


@service_bp.route('/request')
@is_auth
def req():
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    jobs = Job.select().where(Job.cid == user_id)

    if user.acc_type != 'client':
        flash('You need a client account to request a service', 'error')
        redirect(url_for('service.list_service'))

    return render_template('service/request.html', jobs=jobs, user=user)


@service_bp.route('/add', methods=['GET', 'POST'])
@is_auth
def add():
    user_id = session['user_id']
    user = User.get_by_id(user_id)

    if user.acc_type == 'client':
        flash('You need a service provider account to add services', 'error')
        return redirect(url_for('index.index'))

    if request.method == 'POST':
        req = request.form

        name = req.get('name')
        desc = req.get('desc')
        price = req.get('price')
        categories = req.getlist('categories')
        categories = ' '.join(categories)
        poster = request.files['poster']

        service = Service.create(name=name, desc=desc, price=price, categories=categories,
                                 date_created=date.today().strftime('%d/%m/%Y'),
                                 views=0, favs=0, username=user.username, uid=user_id)

        Path(config.constants.uploads_dir + '/' + str(user.id) + '/services/').mkdir(exist_ok=True)
        poster.save(config.constants.uploads_dir + '/' + str(user.id) + '/services/' + str(service.id) + '.png')

        flash('Service created successfully', 'success')
        return redirect(url_for('service.manage'))

    return render_template('service/add.html', user=user)


@service_bp.route('/edit/<id>', methods=['GET', 'POST'])
@is_auth
def edit(id):
    services = Service.get_or_none(Service.id == id)
    user_id = session['user_id']
    user = User.get_by_id(user_id)

    if user.acc_type == 'client':
        flash('You need a service provider account to edit services', 'error')
        return redirect(url_for('index.index'))

    if services is None:
        flash('Service not found', 'error')
        return redirect(url_for('service.manage'))

    if request.method == 'POST':
        req = request.form

        name = req.get('name')
        desc = req.get('desc')
        price = req.get('price')
        categories = req.getlist('categories')
        categories = ' '.join(categories)
        poster = request.files['poster']

        query = Service.update(name=name, desc=desc, price=price, categories=categories).where(Service.id == id)
        query.execute()
        poster.save(config.constants.uploads_dir + '/' + str(user.id) + '/services/' + str(services.id) + '.png')

        flash('Changes saved successfully', 'success')
        return redirect(url_for('service.manage'))

    return render_template('service/edit.html', services=services, user=user)


@service_bp.route('/delete/<id>')
@is_auth
def delete(id):
    if Service.get_or_none(Service.id == id) is None:
        flash('Service not found', 'error')
        return redirect(url_for('service.manage'))

    query = Service.delete().where(Service.id == id)
    query.execute()
    flash('Service deleted successfully', 'success')
    return redirect(url_for('service.manage'))


@service_bp.route('/payment/<sid>/<id>', methods=['GET', 'POST'])
@is_auth
def payment(sid=None, id=None):
    user = User.get_by_id(session['user_id'])
    if sid is None or id is None:
        flash('Service/Request not found', 'error')
        return redirect(url_for('service.request'))

    job = Job.get_by_id(id)
    if job.cid != user.id:
        flash('Unauthorized', 'error')
        return redirect(url_for('service.request'))

    freelancer = User.get_by_id(job.uid)
    service = Service.get_by_id(sid)

    if request.method == 'POST':
        token = str(uuid4())
        token = encrypt(token)

        user.update(token=token, token_expiry=int(time.time() + 60*60)).where(User.id == user.id)

        sender = 'outsource.automated@gmail.com'
        receiver = [user.email]

        link = 'http://127.0.0.1:5000/service/paymentSuccess/' + str(service.id) + '?token=' + token

        message = """
        Subject: Outsource payment
        
        <p>You are receiving this because you (or someone else) is trying to pay for a service on Outsource.</p>
                Service Name: """ + service.name + """</p>
                <p>Price: $""" + str(service.price) + """</p>
                <p>Please click on the following link or paste it into your browser to complete the payment.</p>
                <a href='""" + link + """'>""" + link + """</a>
                <p>If you did not request this, please ignore this email and your balance will not be deducted.</p>
        """

        # try:
        #     smtpObj = smtplib.SMTP('localhost')
        #     smtpObj.sendmail(sender, receiver, message)
        #     flash('A confirmation email has been sent to ' + user.email, 'success')
        #
        # except smtplib.SMTPException:
        #     flash('Unable to send email', 'error')
        return redirect(url_for('service.payment_success', sid=service.id))

    return render_template('service/payment.html', client=user, freelancer=freelancer, service=service)


@service_bp.route('/paymentSuccess/<sid>')
@is_auth
def payment_success(sid=None):
    # token = str.encode(request.args.get('token'))
    service = Service.get_by_id(sid)
    user = User.get_by_id(session['user_id'])

    # token = decrypt(token)
    # if user.token != token:
    #     flash('Invalid token', 'error')
    #     return redirect(url_for('service.req'))
    #
    # if int(time.time()) - user.token_expiry >= 0:
    #     flash('Token has expired, please resend email to continue', 'error')
    #     return redirect(url_for('service.payment'))

    payment = paypalrestsdk.Payment({
        "intent": "sale",

        "payer": {
            "payment_method": "paypal"},

        # Redirect URLs
        "redirect_urls": {
            "return_url": "http://127.0.0.1:5000/service/paymentExecute",
            "cancel_url": "http://127.0.0.1:5000/service/request"},

        "transactions": [{

            "item_list": {
                "items": [{
                    "name": service.name,
                    "sku": service.name,
                    "price": float(service.price),
                    "currency": "USD",
                    "quantity": 1}]},

            "amount": {
                "total": float(service.price),
                "currency": "USD"},
            "description": service.desc}]})

    if payment.create():
        for link in payment.links:
            if link.method == 'REDIRECT':
                approval_url = str(link.href)
                print("Redirect for approval: %s" % approval_url)
                webbrowser.open(approval_url)

        flash('Your payment was created, redirecting to paypal for authorization', 'success')

    else:
        flash("Error while creating payment: " + payment.error, 'error')

    return redirect(url_for('service.req'))


@service_bp.route('/paymentExecute')
@is_auth
def payment_execute():
    payment_id = request.args.get('paymentID')
    payment = paypalrestsdk.Payment.find(payment_id)
    payer_id = request.args.get('payerID')

    if payment.execute({'payer_id': payer_id}):
        flash('Payment completed successfully', 'success')
        return redirect(url_for('service.req'))

    else:
        flash(payment.error, 'error')
