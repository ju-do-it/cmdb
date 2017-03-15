#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse

from django.forms import Form
from django.forms import widgets
from django.forms import fields

from web.service import asset

from repository import models

class AssetListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'asset_list.html')


class AssetJsonView(View):
    def get(self, request):
        obj = asset.Asset()
        response = obj.fetch_assets(request)
        return JsonResponse(response.__dict__)

    def delete(self, request):
        response = asset.Asset.delete_assets(request)
        return JsonResponse(response.__dict__)

    def put(self, request):
        response = asset.Asset.put_assets(request)
        return JsonResponse(response.__dict__)


class AssetDetailView(View):
    def get(self, request, device_type_id, asset_nid):
        response = asset.Asset.assets_detail(device_type_id, asset_nid)
        return render(request, 'asset_detail.html', {'response': response, 'device_type_id': device_type_id})


class AddAssetForm(Form):
    """桌台管理Form表单"""

    device_type_id = fields.ChoiceField(
        choices=models.Asset.device_type_choices,
        widget=widgets.Select(
            attrs={}
        )

    )
    device_status_id = fields.ChoiceField(
        choices=models.Asset.device_status_choices,
        widget=widgets.Select

    )

    hostname = fields.CharField(
        error_messages={
            "required": "主机名不能为空",
        },
        widget=widgets.Input(
            attrs={"class": "form-control", "name": "hostname", "type": "text"})
    )

    cabinet_num = fields.CharField(
        required=False,
        widget=widgets.Input(
            attrs={"class": "form-control", "placeholder": "请输入机柜号,没有可为空", "name": "hostname", "type": "text"})
    )

    cabinet_order = fields.CharField(
        required=False,
        widget=widgets.Input(
            attrs={"class": "form-control", "placeholder": "请输入机柜所在位置,没有可为空", "name": "hostname", "type": "text"})
    )

    idc = fields.ChoiceField(
        choices=[],
        widget=widgets.Select

    )

    business_unit = fields.ChoiceField(
        choices=models.BusinessUnit.objects.values('id', 'name'),
        widget=widgets.Select

    )

    tag = fields.CharField(
        required=False,
        widget=widgets.Input(
            attrs={"class": "form-control", "placeholder": "请输入机柜号,没有可为空", "name": "hostname", "type": "checkbox"})
    )

    def __init__(self, *args, **kwargs):
        super(AddAssetForm, self).__init__(*args, **kwargs)

        values = models.IDC.objects.all().values('id', 'name', 'floor')
        print(values)
        result = map(lambda x: [x.id, "%s-%s" % (x.name, x.floor)], values)
        print(list(result))
        self.fields['idc'].choices = list(result)



class AddAssetView(View):
    def get(self, request, *args, **kwargs):
        obj = AddAssetForm()

        referrer = request.META['HTTP_REFERER']
        return render(request, 'add_asset.html', {'obj': obj, 'referrer': referrer})

    def post(self, request, *args, **kwargs):

        print(request.POST)
        return redirect('/asset.html')






