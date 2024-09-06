from django.contrib import admin
from .models import PostModel, Subject, ClassIn, Comment, PhotoAddModel, District,Category
from django.utils import timezone
from django.utils.html import format_html

admin.site.site_header = 'Ruhul Admin Panel'
admin.site.site_title = 'Ruhul Admin Panel'
admin.site.index_title = ''

class CommentInline(admin.TabularInline):
    model = Comment

class PhotoInline(admin.TabularInline):
    model = PhotoAddModel

class PostAdmin(admin.ModelAdmin):
    # fields = ('title', 'salary')
    # exclude = ('user', 'created_at')
    readonly_fields = ('slug',)
    list_display = ('user', 'title_html_display', 'title', 'get_subject', 'get_classin', 'salary', 'created_since',)
    list_filter = ('title', 'subject', 'classin',)
    search_fields = ('title', 'user__username', 'salary', 'subject__name', 'classin__name')
    list_editable = ('salary',)
    list_display_links = ('title',)
    filter_horizontal = ('subject', 'classin')
    actions = ('change_salary_300',)
    inlines = [CommentInline, PhotoInline,]

    def created_since(self, post_model):
        diff = timezone.now() - post_model.created_at
        return diff.days
    created_since.short_description = 'Created Since'

    def get_subject(self, obj):
        return ", ".join([p.name for p in obj.subject.all()])
    get_subject.short_description = 'Subject'

    def get_classin(self, obj):
        return ", ".join([p.name for p in obj.classin.all()])
    get_classin.short_description = 'ClassIn'

    def title_html_display(self, obj):
        return format_html(
            f'<span style="color:aqua; font-size:20px;">{obj.title}</span>'
        )

    def change_salary_300(self, request, queryset):
        count = queryset.update(salary=3000.0)
        self.message_user(request, '{}, posts updated'.format(count))

# Register your models here.
admin.site.register(PostModel, PostAdmin)
admin.site.register(Subject)
admin.site.register(ClassIn)
admin.site.register(Comment)
admin.site.register(PhotoAddModel)
admin.site.register(District)
admin.site.register(Category)
