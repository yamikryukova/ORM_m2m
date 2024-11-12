from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):

    def clean(self):
        is_mains = [form.cleaned_data["is_main"] for form in self.forms]
        if not any(is_mains):
            raise ValidationError('Укажите основной раздел')
        if sum(filter(lambda x: x, is_mains)) != 1:
            raise ValidationError('Основным может быть только один раздел')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    extra = 0
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        ScopeInline,
    ]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Scope)
class ScopeAdmin(admin.ModelAdmin):
    pass
