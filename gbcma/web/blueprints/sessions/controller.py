from bson import ObjectId
from flask import jsonify

from gbcma.db.config import proposals
from gbcma.web.blueprints.crud_controller import CrudController


class SessionsController(CrudController):
    def __init__(self, repository):
        super().__init__(repository, namespace="sessions")
        self._columns = ["title", "date", "status"]

        self.register_action("run", "play")
        self.register_action("stop", "pause")
        self.register_js("sessions_controller.js")

    def run(self, request, key):
        json = request.get_json(force=True)
        status = json.get("status", None)
        if status:  # todo: check status is valid
            s = self._repository.get(key)
            s["status"] = status
            self._repository.save(s)
            return jsonify({"success": True})
        else:
            return jsonify({"success": False})

    def _form_to_dict(self, form, d):
        ids_list = form.get("proposals", "").split(",")
        ids = list(map(lambda x: ObjectId(x), ids_list))

        d.update({
            "title": form.get("title", None),
            "agenda": form.get("agenda", None),
            "date": form.get("date", None),
            "proposals": ids
        })
        return d

    def _extend(self, model):
        d = proposals.find({"_id": {"$in": model.get("proposals", [])}})
        d2 = {str(key["_id"]): without_keys(key, ["_id"]) for key in d}
        v = {
            "proposals_objects": d2
        }
        return v


def without_keys(d, keys):
    return {x: d[x] for x in d if x not in keys}