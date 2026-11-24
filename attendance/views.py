from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import Student, Course, Attendance
from django.core.mail import send_mail


@login_required
def home(request):
    if hasattr(request.user, 'student'):
        return redirect('/dashboard/')
    return redirect('/mark/')


@login_required
def mark_attendance(request):
    if hasattr(request.user, 'student'):
        return redirect('/dashboard/')

    courses = Course.objects.all()
    students = Student.objects.all()

    if request.method == 'POST':
        course = Course.objects.get(id=request.POST['course'])
        att_date = request.POST['date']
        for student in students:
            status = request.POST.get(f'status_{student.id}', 'A')
            Attendance.objects.update_or_create(
                student=student, course=course, date=att_date,
                defaults={'status': status},
            )
        return redirect('/mark/?saved=1')

    return render(request, 'attendance/mark.html', {
        'courses': courses,
        'students': students,
        'today': date.today().isoformat(),
    })


@login_required
def student_dashboard(request):
    if not hasattr(request.user, 'student'):
        return redirect('/mark/')

    student = request.user.student
    stats = (
        Attendance.objects.filter(student=student)
        .values('course__code', 'course__name')
        .annotate(total=Count('id'), present=Count('id', filter=Q(status='P')))
    )
    rows = []
    for s in stats:
        percent = round(s['present'] * 100 / s['total'], 1)
        rows.append({
            'course': f"{s['course__code']} - {s['course__name']}",
            'total': s['total'],
            'present': s['present'],
            'percent': percent,
            'low': percent < 75,
        })
    return render(request, 'attendance/dashboard.html', {'student': student, 'rows': rows}) 

@login_required
def defaulters(request):
    if hasattr(request.user, 'student'):
        return redirect('/dashboard/')

    stats = (
        Attendance.objects
        .values('student__name', 'student__roll_number', 'course__code')
        .annotate(total=Count('id'), present=Count('id', filter=Q(status='P')))
    )
    rows = []
    for s in stats:
        percent = round(s['present'] * 100 / s['total'], 1)
        if percent < 75:
            rows.append({
                'roll': s['student__roll_number'],
                'name': s['student__name'],
                'course': s['course__code'],
                'total': s['total'],
                'present': s['present'],
                'percent': percent,
            })
    rows.sort(key=lambda r: r['percent'])
    return render(request, 'attendance/defaulters.html', {'rows': rows})

@login_required
def send_alerts(request):
    if hasattr(request.user, 'student'):
        return redirect('/dashboard/')
    if request.method != 'POST':
        return redirect('/defaulters/')

    stats = (
        Attendance.objects
        .values('student__name', 'student__email', 'course__code')
        .annotate(total=Count('id'), present=Count('id', filter=Q(status='P')))
    )
    sent = 0
    for s in stats:
        percent = round(s['present'] * 100 / s['total'], 1)
        if percent < 75 and s['student__email']:
            send_mail(
                subject='Low Attendance Alert',
                message=f"Hello {s['student__name']}, your attendance in {s['course__code']} is {percent}%. Please attend more classes to reach 75%.",
                from_email='attendance@college.local',
                recipient_list=[s['student__email']],
            )
            sent += 1
    return redirect(f'/defaulters/?sent={sent}')