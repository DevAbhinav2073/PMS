from django.shortcuts import get_object_or_404

from apps.authuser.models import StudentProxyModel
from apps.course.models import ElectiveSubject
from apps.one_subject_algorithm import OneSubjectAlgorithm
from apps.student.models import ElectivePriority
from apps.two_subject_algorithm import TwoSubjectAlgorithm


def get_suitable_algorithm_class(subject_count=1):
    print(subject_count)
    if subject_count == 1:
        return OneSubjectAlgorithm
    elif subject_count == 2:
        return TwoSubjectAlgorithm
    else:
        raise NotImplementedError


def normalize_result(result):
    normalized_data_list = []
    for subject_id in result:
        normalized_data = {}
        normalized_data['subject_name'] = get_object_or_404(ElectiveSubject, pk=subject_id).subject_name
        normalized_data['students'] = [{'student_name': student.name, 'roll_number': student.roll_number} for student in
                                       StudentProxyModel.objects.filter(roll_number__in=result[subject_id])]
        normalized_data['student_count'] = StudentProxyModel.objects.filter(roll_number__in=result[subject_id]).count()
        normalized_data['student_count_1'] = StudentProxyModel.objects.filter(
            roll_number__in=result[subject_id]).count() + 1
        normalized_data_list.append(normalized_data)
    return normalized_data_list


def check_if_the_data_entry_is_complete(batch, stream, semester):
    available_subjects_count = ElectiveSubject.objects.filter(elective_for=semester, stream=stream).count()
    student_queryset = StudentProxyModel.objects.filter(batch=batch, stream=stream)
    if available_subjects_count == 0:
        return False
    for student in student_queryset:
        priority_selection_count = ElectivePriority.objects.filter(student=student, session=semester).count()
        if priority_selection_count != available_subjects_count:
            return False
    return True


def get_outliers_message(batch, stream, semester):
    outliers = dict()
    incomplete_data_entry = list()
    available_subjects_count = ElectiveSubject.objects.filter(elective_for=semester, stream=stream).count()
    student_queryset = StudentProxyModel.objects.filter(batch=batch, stream=stream)
    for student in student_queryset:
        priority_selection_count = ElectivePriority.objects.filter(student=student, session=semester).count()
        if priority_selection_count != available_subjects_count:
            message = '%s (%s) has only %d elective selections' % (
                student.name, student.roll_number, priority_selection_count)
            incomplete_data_entry.append(message)
    outliers['Incomplete data entry'] = incomplete_data_entry
    return incomplete_data_entry
