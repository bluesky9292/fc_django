import datetime
from multiprocessing import context
from django.contrib.admin.models import LogEntry, CHANGE
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Q
from django.contrib import admin
from django.utils.html import format_html
from django.db import transaction 
from django.template.response import TemplateResponse
from django.urls import path
from .models import Order 

# Register your models here.

def refund(modeladmin, request, queryset):
    
    with transaction.atomic():
        qs = queryset.filter(~Q(status = '환불'))
        ct = ContentType.objects.get_for_model(queryset.model)
        for obj in qs:
            # if obj.status == '환불': 
            #     print('----------여기 오나')
            #     continue
            obj.product.stock += obj.quantity
            obj.product.save()
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=ct.pk,
                object_id=obj.pk,
                object_repr='주문 환불',
                action_flag=CHANGE,
                change_message='주문 환불!'
            )

        qs.update(status = '환불')

refund.short_description = "환불처리" 
class OrderAdmin(admin.ModelAdmin):
    list_filter = ('status', 'product')
    list_display = ('fcuser', 'product', 'styled_status', 'quantity', 'action')
    change_list_template = 'admin/order_change_list.html'
    
    actions = [
        refund
    ]

    def changelist_view(self, request, extra_context= None ):
        extra_context = {'title':'주문리스트'}
        if request.method == 'POST':
            # print(request.POST)
            obj_id = request.POST.get('obj_id')
            if obj_id :
                qs = Order.objects.filter(pk=obj_id)
                ct = ContentType.objects.get_for_model(qs.model)
                for obj in qs:
                    obj.product.stock += obj.quantity
                    obj.product.save()
                    LogEntry.objects.log_action(
                        user_id=request.user.id,
                        content_type_id=ct.pk,
                        object_id=obj.pk,
                        object_repr='주문 환불',
                        action_flag=CHANGE,
                        change_message='주문 환불!'
                    )
                qs.update(status = '환불')

        return super().changelist_view(request, extra_context)
    
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        print('------------------ changieform_view')
        order = Order.objects.get(pk=object_id)
        # extra_context={'title':f'주문번호:{order.id} 수정하기'}
        extra_context={'title':f'{order.fcuser.email}의 {order.product.name} 수정하기'}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)

    def action(self, obj):
        if obj.status != '환불':
            return format_html(f'<input type="button" value="환불" onclick="order_refund_submit({obj.id});" class="btn btn-primary btn-sm">')

    def styled_status(self, obj):
        if obj.status == '환불':
            return format_html(f'<span style="color:red">{obj.status}</span>') 
        elif obj.status == '결재완료':
            return format_html(f'<span style="color:blue">{obj.status}</span>') 
        else :
            return obj.status

    def get_urls(self):
        urls = super().get_urls()
        date_urls = [
            path('date_view/', self.date_view)
        ]
        return date_urls + urls

    def date_view(self, request):
        weak_date = datetime.datetime.now() - datetime.timedelta(days=7)
        weak_data = Order.objects.filter(register_date__gte=weak_date)
        data = Order.objects.filter(register_date__lt=weak_date)
        context = dict(
            self.admin_site.each_context(request),
            weak_data = weak_data,
            data = data,
        )
        return TemplateResponse(request, 'admin/order_data_view.html', context)

    styled_status.short_description = "상태"
   
admin.site.register(Order, OrderAdmin)