# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('billboard.views',
    url(r'^billboard/$', 'billboard', name='billboard'),

    url(r'^notice/$', 'notice', name='notice'),
    url(r'^notice_map/$', 'notice_map', name='notice_map'),
    url(r'^notice_followup/$', 'notice_followup', name='notice_followup'),

    url(r'^CMS/$', 'CMS', name='CMS'),
    url(r'^set_notice/$', 'set_notice', name='set_notice'),
    url(r'^edit_notice/$', 'edit_notice', name='edit_notice'),
    url(r'^edit_notice_followup/$', 'edit_notice_followup', name='edit_notice_followup'),
    url(r'^get_image/$', 'get_image', name='get_image'),
)
