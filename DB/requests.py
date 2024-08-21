from DB.database import Session
from DB.Companies import Company
from DB.Users import User
from sqlalchemy import and_, asc, desc


def user_sent_check(field_id, user_id):
    session = Session()
    try:
        if session.query(User).filter(and_(User.user_id == user_id, User.field_id == field_id)).scalar():
            return True
        else:
            return False
    except Exception as error:
        print(f"[Error] {error}")
    finally:
        session.close()


def add_user(user_id, field_id, last_comp_id):
    session = Session()
    try:
        user = User(user_id=user_id,
                    field_id=field_id,
                    last_comp_id=last_comp_id
                    )

        session.add(user)
        session.commit()

        return True
    except Exception as error:
        print(f"[ERROR] {error}")
    finally:
        session.close()


def get_last_sent_company(field_id, user_id):
    session = Session()
    try:
        if user_sent_check(field_id=field_id,
                           user_id=user_id
                           ):

            return session.query(User.last_comp_id).filter(and_(User.user_id == user_id,
                                                                User.field_id == field_id
                                                                )
                                                           ).scalar()
        else:
            last_comp_id = session.query(Company.id).filter(Company.field_id == field_id).order_by(asc(Company.id)).first()[0]
            add_user(user_id=user_id, field_id=field_id, last_comp_id=last_comp_id)
            return last_comp_id
    except Exception as error:
        print(f"[Error] {error}")
    finally:
        session.close()


def get_companies(field_id, last_comp_id):
    session = Session()
    try:
        return session.query(Company).filter(and_(Company.field_id == field_id,
                                                  Company.id > last_comp_id
                                                  )
                                             ).limit(5)
    except Exception as error:
        print(f"[Error] {error}")
    finally:
        session.close()


def get_last_company_id(field_id):
    session = Session()
    try:
        return session.query(Company.id).filter(Company.field_id == field_id).order_by(desc(Company.id)).first()[0]
    except Exception as error:
        print(f"[Error] {error}")
    finally:
        session.close()


def check_show_more_ability(field_id, user_id):
    session = Session()
    try:
        last_company_id = get_last_company_id(field_id=field_id)
        if session.query(User.user_id).filter(and_(User.user_id == user_id,
                                                   User.last_comp_id == last_company_id
                                                   )
                                              ).first():
            return False
        else:
            return True
    except Exception as error:
        print(f"[Error] {error}")
    finally:
        session.close()


def see_more_count(field_id, last_comp_id):
    session = Session()
    try:
        return session.query(Company.id).filter(and_(Company.field_id == field_id,
                                                     Company.id > last_comp_id
                                                     )
                                                ).count()
    except Exception as error:
        print(f"[Error] {error}")
    finally:
        session.close()


def update_user_last_comp(field_id, last_comp_id, user_id):
    session = Session()
    try:
        expired_comp = session.query(User).filter(and_(User.user_id == user_id,
                                                       User.field_id == field_id
                                                       )
                                                  ).first()
        expired_comp.last_comp_id = last_comp_id
        session.commit()
        return True

    except Exception as error:
        print(f"[Error] {error}")
    finally:
        session.close()


def clean_user_last_comp_info(user_id, field_id):
    session = Session()
    try:
        session.query(User).filter(and_(User.user_id == user_id,
                                        User.field_id == field_id
                                        )
                                   ).delete()

        session.commit()
    except Exception as error:
        print(f"[Error] {error}")
    finally:
        session.close()


def get_company_by_id(company_id):
    session = Session()
    try:
        return session.query(Company).filter(Company.company_id == company_id).first()
    except Exception as error:
        print(f"[Error] {error}")
    finally:
        session.close()


if __name__ == '__main__':
    pass
