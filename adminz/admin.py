from django.contrib import admin
import nested_admin
from cards.models import *
from support_ticket.models import Ticket, Reply
from payout.models import Payout
from orders.models import Orders, Credit
from sellers.models import *
from wallet.models import *

# Register your models here.


class ReplyInline(nested_admin.NestedTabularInline):
    model = Reply
    extra = 0

    # fieldsets = (
    #     (
    #         "FamilyGroup Details",
    #         {
    #             "fields": (
    #                 "message",

    #             ),
    #         },
    #     ),
    # )


class CouponCardAdmin(admin.ModelAdmin):
    model = CouponCard
    list_display = ["card_first_chars", "seller", "country", "code", "price", "batch"]


class CreditAdmin(admin.ModelAdmin):
    model = Credit
    list_display = [
        "credit",
        "owner",
    ]


class TicketAdmin(nested_admin.SortableHiddenMixin, nested_admin.NestedModelAdmin):
    inlines = [
        ReplyInline,
    ]

    list_per_page = 15
    list_max_show_all = 100
    list_display = [
        "title",
        "created_by",
    ]


admin.site.register(CouponCard, CouponCardAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Payout)
admin.site.register(Batch)
admin.site.register(Orders)
admin.site.register(Users)
admin.site.register(Credit, CreditAdmin)
admin.site.register(Wallet)
