"""
Django Admin Configuration for AI Agent Platform
Author: Cavin Otieno
Contact: cavin.otieno012@gmail.com
"""

from django.contrib import admin
from .models import (
    Agent, Workflow, Task, ProgressLog,
    QualityAssessment, CodeContextGraph
)


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['name', 'agent_type', 'is_active', 'created_at']
    list_filter = ['agent_type', 'is_active']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'created_at', 'completed_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description', 'prompt']
    readonly_fields = ['created_at', 'updated_at', 'started_at', 'completed_at']
    filter_horizontal = ['assigned_agents']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'workflow', 'agent', 'status', 'progress_percentage', 'order']
    list_filter = ['status', 'agent__agent_type']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at', 'started_at', 'completed_at']


@admin.register(ProgressLog)
class ProgressLogAdmin(admin.ModelAdmin):
    list_display = ['workflow', 'task', 'log_level', 'message', 'timestamp']
    list_filter = ['log_level', 'timestamp']
    search_fields = ['message']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'


@admin.register(QualityAssessment)
class QualityAssessmentAdmin(admin.ModelAdmin):
    list_display = ['workflow', 'overall_score', 'assessed_by', 'assessed_at']
    list_filter = ['assessed_at', 'assessed_by']
    search_fields = ['workflow__title', 'feedback']
    readonly_fields = ['assessed_at']


@admin.register(CodeContextGraph)
class CodeContextGraphAdmin(admin.ModelAdmin):
    list_display = ['workflow', 'created_at', 'updated_at']
    search_fields = ['workflow__title']
    readonly_fields = ['created_at', 'updated_at']
