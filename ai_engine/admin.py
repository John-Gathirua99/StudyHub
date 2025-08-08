from django.contrib import admin
from .models import EducationalContent,Dataset

@admin.register(EducationalContent)
class EducationalContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'content_type', 'uploaded_by', 'created_at', 'is_published')
    list_filter = ('content_type', 'is_published', 'created_at')
    search_fields = ('title', 'description')
    actions = ['publish_content', 'unpublish_content']

    def publish_content(self, request, queryset):
        queryset.update(is_published=True)
    publish_content.short_description = "Publish selected content"

    def unpublish_content(self, request, queryset):
        queryset.update(is_published=False)
    unpublish_content.short_description = "Unpublish selected content"

admin.site.register(Dataset)
from .models import KcsePastPaper,SubjectNote,SharedResource,Notification,Profile

admin.site.register(KcsePastPaper)
admin.site.register(SubjectNote)
admin.site.register(SharedResource)
admin.site.register(Notification)
admin.site.register(Profile)

