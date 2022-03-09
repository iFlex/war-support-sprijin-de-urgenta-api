from django.db import models
from django.utils.translation import gettext_lazy as _

from app_account.models import CustomUser
from revm_site.utils.models import (
    CommonCategoryModel,
    CommonMultipleCountyModel,
    CommonOfferModel,
    CommonRequestModel,
    CommonMultipleLocationModel,
    CommonTransportableModel,
    CommonLocationModel,
    get_county_coverage_str,
)
from revm_site.utils.validators import validate_date_disallow_past


class Category(CommonCategoryModel):
    ...


class OtherOffer(CommonOfferModel, CommonMultipleLocationModel, CommonTransportableModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("category"))
    name = models.CharField(_("resource name"), max_length=100, db_index=True)

    available_until = models.DateField(
        _("resource available until"), validators=[validate_date_disallow_past], null=True
    )

    def __str__(self):
        counties_str = get_county_coverage_str(self.county_coverage)
        return f"#{self.pk} {self.name} {self.category} {self.town}({counties_str})"

    class Meta:
        verbose_name = _("other offer")
        verbose_name_plural = _("other offers")


class OtherRequest(CommonRequestModel, CommonLocationModel):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("category"))
    name = models.CharField(_("name"), max_length=100, db_index=True)

    def __str__(self):
        counties_str = get_county_coverage_str(self.county_coverage)
        return f"#{self.pk} {self.name} {self.category} {self.town}({counties_str})"

    class Meta:
        verbose_name = _("other request")
        verbose_name_plural = _("other request")


class ResourceRequest(models.Model):
    resource = models.ForeignKey(OtherOffer, on_delete=models.DO_NOTHING, verbose_name=_("donation"))
    request = models.ForeignKey(OtherRequest, on_delete=models.DO_NOTHING, verbose_name=_("request"))
    # ToDo add here app_item, app_service, app_transport_service, app_volunteering | so we can match them up later

    class Meta:
        verbose_name = _("Offer - Request")
        verbose_name_plural = _("Offer - Request")

    def save(self, *args, **kwargs):
        self.request.status = "C"
        self.request.save()

        super().save(*args, **kwargs)
