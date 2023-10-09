import datetime
import os

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.db.models.functions import ExtractYear, ExtractMonth, TruncMonth
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone

from cart.models import Order, OrderItem
from customer.forms import UpdateAdminForm, UpdateProfileForm
from dashboard.decorator import dashboard_access_required
from dashboard.services import deactivate_user_profile
from dashboard.utils import *
from product.forms import CategoryForm, BrandForm
from product.models import Category, Brand, Product, ProductReview
from userauth.models import Profile, User


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def admin_dashboard_view(request):
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    orders = Order.objects.all()

    item_per_page = 6
    paginator = Paginator(orders, item_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    total_order = orders.count()
    total_value = orders.aggregate(total_value=Sum('total_price'))['total_value']

    current_month = timezone.now().month
    current_year = timezone.now().year

    monthly_order_counts = Order.objects.annotate(year=ExtractYear('order_date'),
                                                  month=ExtractMonth('order_date')).values('year', 'month').annotate(
        total_orders=Count('id')).annotate(month_name=TruncMonth('order_date')).order_by('year', 'month')

    current_month_income = (
        Order.objects
        .filter(order_date__month=current_month, order_date__year=current_year)
        .aggregate(total_income=Sum('grand_total'))
    )

    total_income = current_month_income['total_income'] or 0

    current_month_name = get_current_month_name()

    new_member_count = count_new_members()
    new_members = new_user_show()

    context = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_order': total_order,
        'total_value': total_value,
        'total_income': total_income,
        'current_month': current_month,
        'current_month_name': current_month_name,
        'current_year': current_year,
        'new_member_count': new_member_count,
        'new_members': new_members,
        'monthly_order_counts': monthly_order_counts,
        'page': page
    }
    return render(request, 'admin/dashboard.html', context)


def get_current_month_name():
    current_month = datetime.datetime.now().strftime('%B')
    return current_month


def count_new_members(days=30):
    find_date = datetime.datetime.now() - datetime.timedelta(days=days)

    new_member_count = Profile.objects.filter(date_joined__gte=find_date).count()
    return new_member_count


def new_user_show(days=30):
    find_date = datetime.datetime.now() - datetime.timedelta(days=days)

    new_member = Profile.objects.filter(date_joined__gte=find_date).order_by('-date_joined')[:3]
    return new_member


# ============================== Profile Section Start ==============================
@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def view_profile(request):
    if request.user.is_authenticated:
        prof = Profile.objects.get(user=request.user)
        active = str(prof.user.last_login - prof.date_joined).split('.')[0]

        if request.method == 'POST':
            handle_post_request(request, prof)

        return render(request, 'admin/profile.html', {'prof': prof, 'active': active})
    else:
        return redirect('login')


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def handle_post_request(request, prof):
    UserForm = UpdateAdminForm(request.POST, instance=request.user)
    profileForm = UpdateProfileForm(request.POST, request.FILES, instance=prof)

    if UserForm.is_valid() and profileForm.is_valid():
        UserForm.save()

        prof = profileForm.save(commit=False)
        if 'image' in request.FILES:
            if request.user.profile.image != 'default.png':
                request.user.profile.image.delete()
                prof.image = request.FILES['image']
            prof.save()
        else:
            prof.save()
        messages.success(request, 'Your profile is updated successfully')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'Invalid form data. Please check the inputs.')

    return redirect(request.META.get('HTTP_REFERER'))


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'admin/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('logout')


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def deactivate_profile(request):
    user = request.user
    if user.user_type == USER_TYPE_DEVELOPER:
        messages.warning(request, WARNING_MESSAGE_SUPER_USER)
        return redirect('profile')
    elif user.user_type in [USER_TYPE_ADMIN, USER_TYPE_STAFF]:
        deactivate_user_profile(user)
        logout(request)
        # if user.profile.image != 'default.png':
        #     user.profile.image.delete()
        # user.delete()
        messages.success(request, SUCCESS_MESSAGE_DISABLED)
        return redirect('index')
    else:
        return redirect('index')


# ============================== Profile Section End ==============================


# ============================== Product Category & Brand Section Start ==============================


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def categories_add_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category successfully added.')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        form = CategoryForm()
        category = Category.objects.all()

        item_per_page = 10
        paginator = Paginator(category, item_per_page)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)

    return render(request, 'admin/category/index.html', {'form': form, 'page': page})


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def categories_edit_view(request, slug):
    if request.method == 'post' or request.method == 'POST':
        category = Category.objects.get(slug=slug)
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            if 'image' in request.FILES:
                category.icon.delete(save=False)
                category.image.delete(save=False)
                category.banner.delete(save=False)
                category.save()
            else:
                category.save()
            messages.success(request, 'Category successfully updated.')
            return redirect(to='categories_add_view')
    else:
        category = Category.objects.get(slug=slug)
        form = CategoryForm(instance=category)

    return render(request, 'admin/category/edit.html', {'category': category, 'form': form})


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def delete_category(request, slug):
    user = request.user
    if user.user_type in [USER_TYPE_DEVELOPER, USER_TYPE_ADMIN]:
        category = Category.objects.get(slug=slug)
        if category.image:
            os.remove(category.icon.path)
            os.remove(category.image.path)
            os.remove(category.banner.path)
        category.delete()
        messages.success(request, 'Category Deleted Successfully.')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request, 'Please contact Admin to delete this category.')
        return redirect(request.META.get('HTTP_REFERER'))


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def brand_view(request):
    brand = Brand.objects.all()

    item_per_page = 10
    paginator = Paginator(brand, item_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'admin/brand/index.html', {'page': page})


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def brand_add_view(request):
    if request.method == 'post' or request.method == 'POST':
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            brand = form.save(commit=False)
            brand.save()
            messages.success(request, 'Brand successfully added.')
            return redirect('brand_view')
    else:
        form = BrandForm()
    return render(request, 'admin/brand/create.html', {'form': form})


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def brand_edit_view(request, slug):
    if request.method == 'post' or request.method == 'POST':
        brand = Brand.objects.get(slug=slug)
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            brand = form.save(commit=False)
            if 'image' in request.FILES:
                brand.image.delete(save=False)
                brand.banner.delete(save=False)
                brand.save()
            else:
                brand.save()
            messages.success(request, 'Brand successfully updated.')
            return redirect('brand_view')
    else:
        brand = Brand.objects.get(slug=slug)
        form = BrandForm(instance=brand)
    return render(request, 'admin/brand/edit.html', {'form': form})


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def delete_brand(request, slug):
    user = request.user
    if user.user_type in [USER_TYPE_DEVELOPER, USER_TYPE_ADMIN]:
        brand = Brand.objects.get(slug=slug)
        if brand.image:
            os.remove(brand.image.path)
            os.remove(brand.banner.path)
        brand.delete()
        messages.success(request, 'Brand Deleted Successfully.')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request, 'Please contact Admin to delete this category.')
        return redirect(request.META.get('HTTP_REFERER'))


# ============================== Product Category & Brand Section End ==============================


# ============================== Customer Section Start ==============================


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def all_customers(request):
    customers = User.objects.filter(user_type=USER_TYPE_CUSTOMER).order_by('-id')

    return render(request, 'admin/all-customer.html', {'customers': customers})


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def deactivate_customer(request, id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    messages.warning(request, 'Customer de-activate is successfully.')
    return redirect(to='all_customers')


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def activate_customer(request, id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    messages.success(request, 'Customer is successfully activate.')
    return redirect(to='all_customers')


# ============================== Customer Section End ==============================


# ============================== Staff Section Start ==============================


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def admin_list(request):
    admins = User.objects.filter(user_type=USER_TYPE_ADMIN)
    return render(request, 'admin/staff/admin.html', {'admins': admins})


@dashboard_access_required(user_types=('developer', 'admin'))
def deactivate_admin(request, id):
    user = User.objects.get(id=id)
    if user == request.user:
        messages.warning(request, 'You can not de-activate yourself.')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        user.is_active = False
        user.save()
        messages.warning(request, 'Admin de-activate is successfully.')
        return redirect(request.META.get('HTTP_REFERER'))


@dashboard_access_required(user_types='developer')
def activate_admin(request, id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    messages.success(request, 'Admin is successfully activate.')
    return redirect(to='admin_list')


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def staff_list(request):
    staffs = User.objects.filter(user_type=USER_TYPE_STAFF)
    return render(request, 'admin/staff/staff.html', {'staffs': staffs})


@dashboard_access_required(user_types=('developer', 'admin'))
def deactivate_staff(request, id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    messages.warning(request, 'Staff de-activate is successfully.')
    return redirect(to='staff_list')


@dashboard_access_required(user_types=('developer', 'admin'))
def activate_staff(request, id):
    if request.user.is_authenticated:
        user = User.objects.get(id=id)
        user.is_active = True
        user.save()
        messages.success(request, 'Staff is successfully activate.')
        return redirect(to='staff_list')


# ============================== Staff Section End ==============================

# ============================== Order Section Start ==============================


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def admin_panel_order_view(request):
    orders = Order.objects.all().order_by('-order_date')

    item_per_page = 20
    paginator = Paginator(orders, item_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'admin/order/all_orders.html', {'page': page})


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def admin_panel_order_details(request, id):
    order = Order.objects.get(pk=id)

    order_item = OrderItem.objects.filter(order__id=id)

    if request.method == 'POST':
        order_status = request.POST.get('status')
        order.delivery_status = order_status
        order.save()
        return redirect(request.META.get('HTTP_REFERER'))

    context = {
        'order': order,
        'order_item': order_item
    }

    return render(request, 'admin/order/orders-detail.html', context)


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def admin_panel_seller_view(request):
    orders = Order.objects.filter(user__user_type='vendor').order_by('-order_date')

    item_per_page = 20
    paginator = Paginator(orders, item_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'admin/order/seller-orders.html', {'page': page})


# ============================== Order Section End ==============================

# ============================== Seller Section Start ==============================


# ============================== Seller Section End ==============================

# ============================== Blog Section Start ==============================


@dashboard_access_required(user_types=('developer', 'admin'))
def admin_panel_blog_view(request):
    pass


# ============================== Blog Section End ==============================

# ============================== Report Section Start ==============================


@dashboard_access_required(user_types=('developer', 'admin'))
def admin_panel_report_view(request):
    pass


# ============================== Report Section End ==============================

# ============================== Marketing Section Start ==============================


@dashboard_access_required(user_types=('developer', 'admin'))
def admin_panel_marketing_view(request):
    pass


# ============================== Marketing Section End ==============================

# ============================== Support Section Start ==============================


@dashboard_access_required(user_types=('developer', 'admin'))
def admin_panel_support_view(request):
    pass

# ============================== Support Section End ==============================

# ============================== Product Review Section Start ==============================


@dashboard_access_required(user_types=('developer', 'admin', 'staff'))
def admin_panel_product_review(request):

    reviews = ProductReview.objects.all().order_by('-date')

    item_per_page = 20
    paginator = Paginator(reviews, item_per_page)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'admin/product/reviews.html', {'page': page})

# ============================== Product Review Section End ==============================
