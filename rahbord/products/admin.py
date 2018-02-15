# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Question, Group, Registration, Sku

admin.site.register(Question)
admin.site.register(Group)
admin.site.register(Registration)
admin.site.register(Sku)

