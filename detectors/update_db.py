import sys
import yaml
from sqlalchemy import func
from app import app
from model.detector import Detector
from model.rule import Rules
from database.db import db
from model.organization import Organization

def logic_add(yaml_config_after):
    with app.app_context():
        name = yaml_config_after["id"]
        new_detector = Detector(name=name)
        db.session.add(new_detector)
        organization_filtering_type = yaml_config_after["organization-filtering"]["type"]
        organization = yaml_config_after["organization-filtering"]["organizations"]
        for org in organization:
            id_org = db.session.execute(db.select(Organization).filter(func.lower(Organization.name) == func.lower(org))).first()[0].id
            new_rule = Rules(id_detector=new_detector.id, id_organiztion=id_org, is_blacklist=organization_filtering_type == "blacklist")
            db.session.add(new_rule)

        db.session.commit()
    



def logic_remove(yaml_config_before):
    with app.app_context():
        name = yaml_config_before["id"]
        id_detector = db.session.execute(db.select(Detector).filter(func.lower(Detector.name) == func.lower(name))).first()[0].id
        Rules.query.filter(Rules.id_detector == id_detector).delete()
        Detector.query.filter(func.lower(Detector.name) == func.lower(name)).delete()
        db.session.commit()

def logic_edit(yaml_config_before, yaml_config_after):
    with app.app_context():
        old_detecor_name = yaml_config_before["id"]
        new_detecor_name = yaml_config_before["id"]

        detector = db.session.execute(db.select(Detector).filter(func.lower(Detector.name) == func.lower(old_detecor_name))).first()[0]
        id_detector = detector.id
        if old_detecor_name  != new_detecor_name:
            detector.name = new_detecor_name
        
        old_organization_filtering_type = yaml_config_before["organization-filtering"]["type"]
        new_organization_filtering_type = yaml_config_after["organization-filtering"]["type"]
        organization_old = yaml_config_before["organization-filtering"]["organizations"]
        organization_new = yaml_config_after["organization-filtering"]["organizations"]


        removed_orgs = list(set(organization_old) - set(organization_new))
        for org in removed_orgs:
            id_org = db.session.execute(db.select(Organization).filter(func.lower(Organization.name) == func.lower(org))).first()[0].id
            Rules.query.filter_by(id_detector=id_detector, id_organiztion=id_org).delete()
        
        remain_orgs = list(set(organization_old) & set(organization_new))

        if old_organization_filtering_type != new_organization_filtering_type:
            for org in remain_orgs:
                id_org = db.session.execute(db.select(Organization).filter(func.lower(Organization.name) == func.lower(org))).first()[0].id
                rule = db.session.execute(db.select(Rules).filter_by(id_detector=id_detector, id_organiztion=id_org)).first()[0]
                rule.is_blacklist = new_organization_filtering_type == "blacklist"

        
        added_orgs = list(set(organization_new) - set(organization_old))
        for org in added_orgs:
            id_org = db.session.execute(db.select(Organization).filter(func.lower(Organization.name) == func.lower(org))).first()[0].id
            new_rule = Rules(id_detector=id_detector, id_organiztion=id_org, is_blacklist=new_organization_filtering_type == "blacklist")
            db.session.add(new_rule)

        db.session.commit()

    


def update_db(yaml_name_before, yaml_name_after):
    
    if yaml_name_before == " ":
        yaml_config_before = []
    else:
        with open(yaml_name_before, 'r') as file:
            yaml_config_before = yaml.safe_load(file)

    if yaml_name_after == " ":
        yaml_config_after = []
    else:
        with open(yaml_name_after, 'r') as file:
            yaml_config_after = yaml.safe_load(file)

    if not yaml_config_before:
        logic_add(yaml_config_after)

    elif not yaml_config_after:
        logic_remove(yaml_config_before)
    
    else:
        logic_edit(yaml_config_before, yaml_config_after)

    


if __name__ == "__main__":
    yaml_name_before = sys.argv[1]
    yaml_name_after = sys.argv[2]
    update_db(yaml_name_before, yaml_name_after)


