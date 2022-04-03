from django.contrib import admin
from homez.models import Home
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
    list_per_page = 10
    list_max_show_all = 10
    list_display = [
        "card_first_chars",
        "seller",
        "country",
        "code",
        "price",
        "batch",
        "sold",
    ]
class SellerAdmin(admin.ModelAdmin):
    model = Users
    list_per_page = 10
    list_max_show_all = 10
    list_display = [
        "username",
        "is_staff",
    ]


class CreditAdmin(admin.ModelAdmin):
    model = Credit
    list_display = [
        "credit",
        "owner",
        "get_is_staff"
    ]
    def get_is_staff(self, obj):
        if obj.owner.is_staff:

            return 'Seller'
        else:
            return 'User'
    get_is_staff.admin_order_field  = 'author'  #Allows column order sorting
    get_is_staff.short_description = 'user type'  #Renames column head



class TicketAdmin(nested_admin.SortableHiddenMixin, nested_admin.NestedModelAdmin):
    inlines = [
        ReplyInline,
    ]

    list_per_page = 15
    list_max_show_all = 10
    list_display = [
        "title",
        "created_by",
    ]


admin.site.register(CouponCard, CouponCardAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Payout)
admin.site.register(Country)
admin.site.register(Batch)
admin.site.register(Orders)
admin.site.register(Users, SellerAdmin)
admin.site.register(Credit, CreditAdmin)
admin.site.register(Wallet)
admin.site.register(Home)
