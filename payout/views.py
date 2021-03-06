from django.shortcuts import get_object_or_404, redirect, render

from cards.models import CouponCard
from orders.models import Credit
from .forms import PayoutCreateForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Payout
from django.contrib.auth.decorators import login_required

# Create your views here.


@user_passes_test(lambda u: u.is_superuser)
def all_payouts_view(request):
    user = request.user
    if "q" in request.GET and request.GET.get("q"):
        q = request.GET.get("q")
        all_payout = Payout.objects.filter(user__username__icontains=q)
        payout_paginator = Paginator(all_payout, 200)
    else:
        all_payout = Payout.objects.all()
        payout_paginator = Paginator(all_payout, 10)

    page_num = request.GET.get("page")
    page = payout_paginator.get_page(page_num)
    num_pages = payout_paginator.num_pages

    return render(
        request, "payout/payout_user.html", {"page": page, "num_pages": num_pages}
    )


@login_required
def payout_create_view(request):
    if request.POST:
        form = PayoutCreateForm(request.POST)
        if form.is_valid():
            
            obj = form.save()
            # set owner
            obj.user = request.user
            obj.status = "Pending"
            obj.save()
            messages.add_message(
                request, messages.SUCCESS, "Payout created successfully"
            )
            return redirect("home")

    else:
        form = PayoutCreateForm()

    total_cards = []
    sold_cards = []
    cards = CouponCard.objects.filter(seller=request.user, sold=False)
    cards_sold = CouponCard.objects.filter(seller=request.user, sold=True)
    credit = Credit.objects.filter(owner=request.user).first()
    for c in cards:
        total_cards.append(c)
    for b in cards_sold:
        sold_cards.append(b)
        
    return render(
        request,
        "payout/payout_form.html",
        {"form": form, "number_of_cards": len(total_cards), "sold_cards": len(sold_cards), "credit": credit}
    )


def payout_edit_view(request, pk):

    data = get_object_or_404(Payout, id=pk)

    context = {"payout": data}
    if request.POST:

        if data.status == "Pending":
            data.status = "Done"
            data.save()
        else:
            data.status = "Pending"
            data.save()
        messages.add_message(
            request,
            messages.SUCCESS,
            f"Payout created by ---- {data.user} ---- Updated Successfully",
        )
        return redirect("all_payouts")

    return render(
        request,
        "payout/payout_user.html",
    )
