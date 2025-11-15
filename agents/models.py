"""
AI Agent Models - Prompt2Action Platform
Author: Cavin Otieno
Contact: cavin.otieno012@gmail.com

Core models for multi-agent coordination, workflow management, and real-time progress tracking.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json


class AgentType(models.TextChoices):
    """Types of AI agents available in the system"""
    PLANNER = 'PLANNER', 'Planner Agent'
    DEVELOPER = 'DEVELOPER', 'Developer Agent'
    REVIEWER = 'REVIEWER', 'Code Reviewer Agent'
    TESTER = 'TESTER', 'Testing Agent'
    DOCUMENTER = 'DOCUMENTER', 'Documentation Agent'
    COORDINATOR = 'COORDINATOR', 'Coordinator Agent'


class WorkflowStatus(models.TextChoices):
    """Workflow execution status"""
    PENDING = 'PENDING', 'Pending'
    RUNNING = 'RUNNING', 'Running'
    COMPLETED = 'COMPLETED', 'Completed'
    FAILED = 'FAILED', 'Failed'
    CANCELLED = 'CANCELLED', 'Cancelled'


class Agent(models.Model):
    """
    AI Agent model representing individual agents in the system
    Implements Chain of Responsibility pattern for multi-agent coordination
    """
    name = models.CharField(max_length=200)
    agent_type = models.CharField(
        max_length=20,
        choices=AgentType.choices,
        default=AgentType.DEVELOPER
    )
    description = models.TextField()
    capabilities = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'AI Agent'
        verbose_name_plural = 'AI Agents'
    
    def __str__(self):
        return f"{self.name} ({self.get_agent_type_display()})"


class Workflow(models.Model):
    """
    Workflow model for managing multi-agent task execution
    Supports concurrent workflows with real-time progress tracking
    """
    title = models.CharField(max_length=300)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workflows')
    prompt = models.TextField(help_text="User's input prompt")
    status = models.CharField(
        max_length=20,
        choices=WorkflowStatus.choices,
        default=WorkflowStatus.PENDING
    )
    assigned_agents = models.ManyToManyField(Agent, related_name='workflows')
    
    # Metadata
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Results
    result_data = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True, null=True)
    
    # Code Context Graph
    code_context = models.JSONField(default=dict, blank=True, help_text="Code Context Graph data")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Workflow'
        verbose_name_plural = 'Workflows'
    
    def __str__(self):
        return f"{self.title} - {self.get_status_display()}"
    
    def start(self):
        """Start the workflow execution"""
        self.status = WorkflowStatus.RUNNING
        self.started_at = timezone.now()
        self.save()
    
    def complete(self, result_data=None):
        """Mark workflow as completed"""
        self.status = WorkflowStatus.COMPLETED
        self.completed_at = timezone.now()
        if result_data:
            self.result_data = result_data
        self.save()
    
    def fail(self, error_message):
        """Mark workflow as failed"""
        self.status = WorkflowStatus.FAILED
        self.completed_at = timezone.now()
        self.error_message = error_message
        self.save()


class Task(models.Model):
    """
    Individual tasks within a workflow
    Represents granular actions performed by specific agents
    """
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='tasks')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=300)
    description = models.TextField()
    order = models.IntegerField(default=0, help_text="Execution order within workflow")
    
    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=WorkflowStatus.choices,
        default=WorkflowStatus.PENDING
    )
    progress_percentage = models.IntegerField(default=0)
    
    # Timing
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Results
    result_data = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['workflow', 'order']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
    
    def __str__(self):
        return f"{self.name} ({self.agent.name})"


class ProgressLog(models.Model):
    """
    Real-time progress tracking for workflows and tasks
    Enables live workflow monitoring
    """
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='progress_logs')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True, related_name='progress_logs')
    message = models.TextField()
    log_level = models.CharField(
        max_length=20,
        choices=[
            ('INFO', 'Info'),
            ('SUCCESS', 'Success'),
            ('WARNING', 'Warning'),
            ('ERROR', 'Error'),
        ],
        default='INFO'
    )
    metadata = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Progress Log'
        verbose_name_plural = 'Progress Logs'
    
    def __str__(self):
        return f"{self.workflow.title} - {self.message[:50]}"


class QualityAssessment(models.Model):
    """
    Multi-dimensional quality validation model
    Comprehensive quality assessment for generated code and outputs
    """
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name='quality_assessments')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True, related_name='quality_assessments')
    
    # Quality metrics
    code_quality_score = models.FloatField(default=0.0)
    test_coverage_score = models.FloatField(default=0.0)
    documentation_score = models.FloatField(default=0.0)
    performance_score = models.FloatField(default=0.0)
    security_score = models.FloatField(default=0.0)
    overall_score = models.FloatField(default=0.0)
    
    # Detailed feedback
    feedback = models.TextField(blank=True)
    recommendations = models.JSONField(default=list, blank=True)
    
    # Metadata
    assessed_at = models.DateTimeField(auto_now_add=True)
    assessed_by = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='assessments')
    
    class Meta:
        ordering = ['-assessed_at']
        verbose_name = 'Quality Assessment'
        verbose_name_plural = 'Quality Assessments'
    
    def __str__(self):
        return f"QA for {self.workflow.title} - Score: {self.overall_score}"
    
    def calculate_overall_score(self):
        """Calculate weighted overall quality score"""
        weights = {
            'code_quality': 0.25,
            'test_coverage': 0.20,
            'documentation': 0.15,
            'performance': 0.20,
            'security': 0.20,
        }
        
        self.overall_score = (
            self.code_quality_score * weights['code_quality'] +
            self.test_coverage_score * weights['test_coverage'] +
            self.documentation_score * weights['documentation'] +
            self.performance_score * weights['performance'] +
            self.security_score * weights['security']
        )
        self.save()
        return self.overall_score


class CodeContextGraph(models.Model):
    """
    Code Context Graph (CCG) model
    Advanced code relationship representation for better context understanding
    """
    workflow = models.OneToOneField(Workflow, on_delete=models.CASCADE, related_name='ccg')
    
    # Graph data
    nodes = models.JSONField(default=list, help_text="Code entities (classes, functions, modules)")
    edges = models.JSONField(default=list, help_text="Relationships between entities")
    metadata = models.JSONField(default=dict, blank=True)
    
    # Analysis results
    complexity_metrics = models.JSONField(default=dict, blank=True)
    dependencies = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Code Context Graph'
        verbose_name_plural = 'Code Context Graphs'
    
    def __str__(self):
        return f"CCG for {self.workflow.title}"
    
    def add_node(self, node_data):
        """Add a node to the graph"""
        self.nodes.append(node_data)
        self.save()
    
    def add_edge(self, edge_data):
        """Add an edge to the graph"""
        self.edges.append(edge_data)
        self.save()
