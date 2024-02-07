from flask import Blueprint, send_from_directory
from flask import request
from database.db import db
from model.organization import Organization
from model.detector import Detector
from model.rule import Rules
from sqlalchemy import func
api = Blueprint('api', __name__)


def _get_rules_case_blacklist_org(id_org:int):
    # find only whitelist rules
    detectors_names = []
    rules = db.session.execute(db.select(Rules).filter_by(id_organiztion=id_org, is_blacklist=False)).all()
    for rule_tuple in rules:
        detector_id = rule_tuple[0].id_detector
        detc_obj = db.session.execute(db.select(Detector).filter_by(id=detector_id)).first()[0]
        detectors_names.append(detc_obj.name)
    
    return detectors_names


def _get_rules_case_whitelist_org(id_org:int):
    detectors_names = []
    all_detectors = db.session.execute(db.select(Detector))
    for detect_tuple in all_detectors:
        detectors_names.append(detect_tuple[0].name)
    
    rules = db.session.execute(db.select(Rules).filter_by(id_organiztion=id_org, is_blacklist=True)).all()
    for rule_tuple in rules:
        detector_id = rule_tuple[0].id_detector
        detc_obj = db.session.execute(db.select(Detector).filter_by(id=detector_id)).first()[0]
        detectors_names.remove(detc_obj.name)
    
    return detectors_names


def get_rules_for_org(org:str):
    org_objs = db.session.execute(db.select(Organization).filter(func.lower(Organization.name) == func.lower(org))).all()

    if len(org_objs) != 1:
        return []
    
    org_obj = org_objs[0][0]
    id_org =  org_obj.id
    is_blacklist_org = org_obj.is_blacklist

    if is_blacklist_org:
        return _get_rules_case_blacklist_org(id_org)
    
    return _get_rules_case_whitelist_org(id_org)


@api.route('/')
def index():
    return send_from_directory('static', 'index.html')


@api.route('/search/<string:name>', methods=['GET'])
def search(name):
    rules = get_rules_for_org(name)
    return rules


