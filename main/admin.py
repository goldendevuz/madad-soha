from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Quiz, Question, Option, Score, UserOption, UserQuiz, UserSpecialty, Specialty
from .resources import (
    QuizResource, QuestionResource, OptionResource,
    ScoreResource, UserOptionResource, UserQuizResource, UserSpecialtyResource, SpecialtyResource
)

class BaseAdmin(admin.ModelAdmin):
    list_per_page = 5
    class Meta:
        abstract = True


@admin.register(Quiz)
class QuizAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_class = QuizResource
    list_display = [field.name for field in Quiz._meta.fields]


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_class = QuestionResource
    list_display = [field.name for field in Question._meta.fields]
    # list_display_links = list_display


@admin.register(Option)
class OptionAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_class = OptionResource
    list_display = ['text']
    # list_display = [field.name for field in Option._meta.fields] # ['text'] #
    list_display_links = list_display
    search_fields = ['text']


@admin.register(Score)
class ScoreAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_class = ScoreResource
    list_display = [field.name for field in Score._meta.fields]
    list_filter = ['option__text']


@admin.register(UserQuiz)
class UserQuizAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_class = UserQuizResource
    list_display = [field.name for field in UserQuiz._meta.fields]
    readonly_fields = ["completed"]


@admin.register(UserOption)
class UserOptionAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_class = UserOptionResource
    list_display = [field.name for field in UserOption._meta.fields]


@admin.register(UserSpecialty)
class UserSpecialtyAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_class = UserSpecialtyResource
    list_display = [field.name for field in UserSpecialty._meta.fields]


@admin.register(Specialty)
class SpecialtyAdmin(ImportExportModelAdmin, BaseAdmin):
    resource_class = SpecialtyResource
    list_display = [field.name for field in Specialty._meta.fields]
