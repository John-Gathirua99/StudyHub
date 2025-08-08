from rest_framework import serializers
from .models import Exam, Question, StudentExam, StudentAnswer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'max_marks']

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Exam
        fields = ['id', 'title', 'created_by', 'created_at', 'questions']

class StudentAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAnswer
        fields = ['id', 'question', 'answer_text', 'marks_awarded']

class StudentExamSerializer(serializers.ModelSerializer):
    answers = StudentAnswerSerializer(many=True, read_only=True)
    class Meta:
        model = StudentExam
        fields = ['id', 'student', 'exam', 'submitted_at', 'graded', 'total_marks', 'answers']