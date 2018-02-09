import json
import urllib
import fedoidc
from urllib.parse import unquote_plus
from fedoidc.operator import Operator
from flask import current_app
from werkzeug.exceptions import NotAcceptable
from fedoidc_ss.models import Entity, Superior
from oic.utils.keyio import build_keyjar


def _get_sup_sms():
    """
    Fetches superior SMS corresponding to this MSS / FO. If two superiors provide SMS for the
    same FO, it just takes the last one.
    """
    result = {}
    superiors = Superior.query.all()
    for superior in superiors:
        result.update(json.loads(urllib.request.urlopen(superior.uri).read()))
    return result


def create_jwks(pub=False):
    """
    Create a JWKS with keys defined in KEYDEFS
    :param: set `pub` to True to make it return also a JWKS with only the public part of the keys
    :return: a JWKS
    :return: a tuple with the full JWKS, and a JWKS with only the public part of the keys
    """

    jwks = None

    _jwks, _keyjar, _ = build_keyjar(
        current_app.config['KEYDEFS']
    )

    jwks = json.dumps(_keyjar.export_jwks(private=True),
                      sort_keys=True,
                      indent=2
                      )

    if pub:
        pub_jwks = json.dumps(_keyjar.export_jwks(),
                              sort_keys = True,
                              indent = 2
                              )

        return (jwks, pub_jwks)

    return jwks


def get_entity_sig_key(issuer_urlsafe):
    """
    Returns the entity's signing key
    """
    issuer = unquote_plus(issuer_urlsafe)
    entity = Entity.query.filter(Entity.issuer == issuer).first()
    if not entity:
        raise NotAcceptable("Could not find entity {}".format(issuer))
    return entity.signing_keys


def generate_sms(issuer_urlsafe):
    """
    Generates SMS for the indicated entity
    """
    sign_keys = get_entity_sig_key(issuer_urlsafe)
    superior_sms = _get_sup_sms()
    # Add ourselves as a superior without SMS
    superior_sms[current_app.config['FO_NAME']] = None
    result = {}

    # iterate superior's SMS and generate a new SMS for each one of them
    for superior, sms in superior_sms.items():
        req = {'signing_keys': json.loads(sign_keys)}
        if sms:
            req['metadata_statements'] = {superior: sms}
        _req = fedoidc.MetadataStatement(**req)
        kj = fedoidc.read_jwks_file(current_app.config['FO_SIG_KEYS'])
        op = Operator(keyjar=kj, iss=current_app.config['FO_NAME'], lifetime=current_app.config['FO_SIG_LIFETIME'])
        result[superior] = op.pack_metadata_statement(_req)

    return result
