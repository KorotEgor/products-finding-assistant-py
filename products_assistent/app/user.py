from products_assistent.app.utils import FieldsFormErrs

from flask import Blueprint, render_template

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/<int:id>/profile", methods=["GET"])
def profile(id):
    return render_template(
        "user/edit_profile.html",
        fields_errs=FieldsFormErrs(
            username=[],
            email=[],
            password=[],
            access_password=[],
        ),
    )
