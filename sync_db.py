from database import db, VenmoRequest
from datetime import datetime
from venmo_api import VenmoSession

def sync_db(app, access_token):
    with app.app_context():
        venmo_entries = VenmoSession(access_token).get_pending_requests() # updated data from venmo
        venmo_IDs = {d["id"] for d in venmo_entries} # just the IDs from venmo

        db_entries = VenmoRequest.query.filter_by(paid=False).all() # all entries in the current db that are not paid yet
        db_IDs = {d.id for d in db_entries} # IDs of the current db that are not paid yet

        # insert new requests
        for d in venmo_entries:
            if d["id"] not in db_IDs: # if the id is not in the current db
                new_req = VenmoRequest(
                    id=d["id"],
                    username=d["username"],
                    display_name=d["display_name"],
                    amount=d["amount"],
                    note=d["note"],
                    created=datetime.fromisoformat(d["created"]),
                    paid=False
                )
                db.session.add(new_req)

                if not UserPhone.query.get(d["username"]): # if the user deos not have a UserPhone entry
                    new_user = UserPhone(
                        username=d["username"],
                        phone=""
                    )
                    db.session.add(new_user)

        # mark missing requests as paid
        for req in db_entries:
            if req.id not in venmo_IDs:
                req.paid = True

        db.session.commit()