import json

import fedoidc
from urllib.parse import quote_plus, unquote_plus
from flask import Blueprint, jsonify, render_template, redirect, url_for, current_app
from flask import request
from oic.utils.keyio import KeyJar
from werkzeug.exceptions import NotAcceptable
from fedoidc_ss.models import Entity, Superior
from fedoidc_ss.database import db_session
from fedoidc_ss import sms_services

sigserv = Blueprint('sigserv', __name__, url_prefix='')


@sigserv.route('/')
def main():
    """
    Main entrypoint. Just lists options
    """
    return render_template('hello.html', fo_name=current_app.config['FO_NAME'])


@sigserv.route('/fo_key')
def fo_key():
    """
    Entrypoint that provides public FO key (for information)
    :return: public FO key
    """
    kj = fedoidc.read_jwks_file(current_app.config['SIG_KEY'])
    return jsonify(kj.export_jwks())


@sigserv.route('/enrol', methods=['GET', 'POST'])
def enrol():
    """
    Performs the enrolment of an entity.
    """
    if request.method == 'GET':
        return render_template('enrol.html')
    elif request.method == 'POST':
        # Import entity singing key (just to make sure it is a valid JKWS
        try:
            kj = KeyJar()
            kj.import_jwks(json.loads(request.form['signing_key']), '')
        except Exception:
            raise NotAcceptable("That is no a JWKS.")

        issuer = request.form['issuer']
        signing_keys = json.dumps(kj.export_jwks())
        # Store (issuer, signing_key) in the database
        try:
            entity = Entity(issuer, signing_keys)
            db_session.add(entity)
            db_session.commit()
        except Exception as ex:
            raise NotAcceptable("There was a problem storing the entity in the DB ({})".format(ex))

        return redirect(url_for('sigserv.list_entities'))


@sigserv.route('/list')
def list_entities():
    """
    List entities currently enrolled
    """
    entities = Entity.query.all()
    for entity in entities:
        print(entity.issuer, entity.signing_keys)

    return render_template("list.html", entities=entities,
                           federations=[(current_app.config['FO_NAME'],
                                         quote_plus(current_app.config['FO_NAME']))])


@sigserv.route('/delete/<issuer_urlsafe>')
def delete_entity(issuer_urlsafe):
    """
    Deletes an entity from the DB
    """
    issuer = unquote_plus(issuer_urlsafe)
    entity = Entity.query.filter(Entity.issuer == issuer).first()
    db_session.delete(entity)
    db_session.commit()
    return redirect(url_for('sigserv.list_entities'))


@sigserv.route('/getms/<issuer_urlsafe>')
def getms(issuer_urlsafe):
    """
    Returns SMS for the indicated entity
    """
    return jsonify(sms_services.generate_sms(issuer_urlsafe))


@sigserv.route('/getms/<issuer_urlsafe>/<fo_urlsafe>')
def getms_by_fo(issuer_urlsafe, fo_urlsafe):
    """ Returns SMS for the indicated entity and FO
    """
    result = sms_services.generate_sms(issuer_urlsafe)
    if unquote_plus(fo_urlsafe) in result:
        return result[unquote_plus(fo_urlsafe)]
    raise NotAcceptable("There is no SMS for that entity and FO")


@sigserv.route('/getsk/<issuer_urlsafe>')
def getsk(issuer_urlsafe):
    """ Returns entity's signing key"""
    sig_key = sms_services.get_entity_sig_key(issuer_urlsafe)
    return jsonify(json.loads(sig_key))


@sigserv.route('/addsup/', methods=['GET', 'POST'])
def addsup():
    """
    Adds a superior. The URI attribute is for the uri for this FO in that superior
    That is, "SUPERIOR_BASE_URL/getms/{FO}". This should change
    """
    if request.method == 'GET':
        return render_template('addsup.html')
    elif request.method == 'POST':
        try:
            issuer = request.form['issuer']
            uri = request.form['uri']
            superior = Superior(issuer, uri)
            db_session.add(superior)
            db_session.commit()
        except Exception as ex:
            raise NotAcceptable("There was a problem storing the entity in the DB ({})".format(ex))

        return redirect(url_for('sigserv.list_superiors'))


@sigserv.route('/list_superiors')
def list_superiors():
    """
    List superiors
    """
    superiors = Superior.query.all()
    return render_template('list_superiors.html', superiors=superiors)


@sigserv.route('/delete_sup/<issuer_urlsafe>')
def delete_sup(issuer_urlsafe):
    """
    Delete superior
    """
    superior = Superior.query.filter(Superior.issuer == unquote_plus(issuer_urlsafe)).first()
    db_session.delete(superior)
    db_session.commit()
    return redirect(url_for('sigserv.list_superiors'))
