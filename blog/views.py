from django.contrib.auth.decorators import login_required
from .models import Ticket
from .forms import TicketForm
from django.utils import timezone
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib.auth.models import Group, User
from django.db.models import Q
from django.shortcuts import redirect

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    is_tester_user = request.user.groups.filter(name='Tester').exists()
    is_reception_user = request.user.groups.filter(name='Reception').exists()
    reception_users = User.objects.filter(groups__name='Reception')

    if request.method == 'POST':
        actions = request.POST.get('actions', '')
        new_status = request.POST.get('status', '')
        #Итак, переменная new_assigned_user_id после выполнения этой строки будет содержать идентификатор пользователя,
        # на которого пользователь пытается переназначить проблему.
        # Этот идентификатор затем используется для установки значения поля assigned_user модели Ticket,
        # что позволяет изменить назначение проблемы на другого пользователя.
    #Если new_assigned_user_id имеет значение None, это означает, что пользователь не выбрал никакого пользователя для переназначения
        # , и проблема останется назначенной на текущего пользователя
        new_assigned_user_id = request.POST.get('assigned_user', None)

        if is_tester_user:
            if new_status == 'confirmed':
                ticket.delete()
                return redirect('ticket_list')
            else:
                # Другие статусы доступны для редактирования всем пользователям
                ticket.status = new_status
                ticket.actions_taken = actions
          #perenazna4enie
            if new_assigned_user_id:
                new_assigned_user = User.objects.get(id=new_assigned_user_id)
                ticket.assigned_user = new_assigned_user
                ticket.save()

        elif is_reception_user:
            # Пользователи из группы "Reception" могут устанавливать только статусы "new", "in progress" и "resolved"
            if new_status in ['new', 'in progress']:
                ticket.status = new_status
                ticket.actions_taken = actions
                if new_assigned_user_id:
                    new_assigned_user = User.objects.get(id=new_assigned_user_id)
                    ticket.assigned_user = new_assigned_user
                ticket.save()
            elif new_status == 'resolved' and ticket.status != 'resolved':
                # Запрет изменения на "resolved", если статус уже "resolved"
                ticket.status = new_status
                ticket.assigned_user = None
                ticket.actions_taken = actions
                ticket.save()

    return render(request, 'blog/ticket_detail.html', {'ticket': ticket, 'is_tester_user': is_tester_user, 'is_reception_user': is_reception_user, 'reception_users': reception_users})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('ticket_list')
    error_message = None

    ticket_count = Ticket.objects.count()
    ticket_priorities = Ticket.objects.values('priority').annotate(priority_count=Count('priority'))

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('ticket_list')
        else:
            error_message = "Неверные учетные данные. Пожалуйста, попробуйте снова."


    return render(request, 'blog/login.html', {'error_message': error_message, 'ticket_count': ticket_count, 'ticket_priorities': ticket_priorities})

@login_required
def ticket_list(request):
    reception_group = Group.objects.get(name='Reception')
    tester_group = Group.objects.get(name='Tester')
    is_reception_user = reception_group.user_set.filter(id=request.user.id).exists()
    is_tester_user = tester_group.user_set.filter(id=request.user.id).exists()

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.creator_name = request.user.username
            ticket.created_date = timezone.now()

            if is_reception_user:
                ticket.assigned_user = request.user

            ticket.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()

    if is_reception_user or is_tester_user:
        # Фильтрация проблем в зависимости от роли пользователя
        if is_reception_user:
            # Пользователи из группы "Reception" видят только те проблемы, которые им были назначены
            tickets = Ticket.objects.filter(assigned_user=request.user)
        elif is_tester_user:
            # Тестеры видят все проблемы, кроме тех, которые подтверждены
            tickets = Ticket.objects.filter(Q(creator_name=request.user.username) | Q(status='resolved', confirmed=False))
    else:
        # Другие пользователи видят только те проблемы, которые не подтверждены
        tickets = Ticket.objects.filter(confirmed=False)

    return render(request, 'blog/ticket_list.html', {'tickets': tickets, 'form': form, 'is_reception_user': is_reception_user, 'is_tester_user': is_tester_user})