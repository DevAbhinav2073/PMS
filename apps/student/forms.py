from django import forms

from apps.authuser.models import StudentProxyModel
from apps.student.models import ElectivePriority
from apps.utils import get_student_queryset, get_subjects, get_nth_object


class PriorityForm(forms.ModelForm):
    class Meta:
        model = ElectivePriority
        fields = ('subject', 'priority')


class PriorityFormForFormset(forms.Form):
    student = forms.ModelChoiceField(queryset=StudentProxyModel.objects.all(), required=True)
    priority_text = forms.CharField()

    def __init__(self, *args, **kwargs):
        self.priority_detail_form_data = kwargs.pop('priority_detail_form_data', None)
        super().__init__(*args, **kwargs)
        self.stream = self.priority_detail_form_data.get('stream')
        self.level = self.priority_detail_form_data.get('level')
        self.batch = self.priority_detail_form_data.get('batch')
        self.semester = self.priority_detail_form_data.get('semester')
        self.student_queryset = get_student_queryset(self.batch,
                                                     self.stream)
        self.subjects = get_subjects(self.stream, self.semester)
        # self.fields['student'].queryset = student_queryset
        if 'student' in self.initial:
            self.fields['student'].queryset = self.student_queryset.filter(id=self.initial['student'].id)

    def clean_priority_text(self):
        try:
            subject_indexing = [int(i) for i in self.cleaned_data.get('priority_text').split(' ')]
        except ValueError:
            raise forms.ValidationError('Please enter numeric data only')
        subject_count = len(subject_indexing)
        if subject_count != self.subjects.count():
            raise forms.ValidationError("Please arrange all the subjects in order")
        for i in range(1, subject_count + 1):
            if i not in subject_indexing:
                raise forms.ValidationError('Invalid numbers used')

        return self.cleaned_data.get('priority_text')

    def save(self, *args, **kwargs):
        priorities = self.cleaned_data.get('priority_text')
        for priority, value in enumerate(priorities.split(' ')):
            index = int(value) - 1
            ElectivePriority.objects.create(student=self.cleaned_data.get('student'), session=self.semester,
                                            subject=get_nth_object(self.subjects, index), priority=priority + 1)
