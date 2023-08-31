from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from .models import Team, TeamMember
from django.contrib.auth.models import User
from django.db.models import Q  
from django.shortcuts import get_object_or_404
from django.db.models import Count, Max


def add_team(request):
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        email = request.POST.get('email')
        team_lead_ids = request.POST.getlist('team_lead')
        team_member_ids = request.POST.getlist('team_member')
       

        team = Team.objects.create(name=team_name, email=email)
     
        all_member_ids = set(team_lead_ids + team_member_ids)
        
        
        for user_id in all_member_ids:
            user_is_lead = False
            if user_id in team_lead_ids:
                user_is_lead = True

            team_member = TeamMember(team=team, member_id=user_id, is_lead=user_is_lead )
            team_member.save()  


        # common_members = set(team_lead_ids) & set(team_member_ids)

        # if common_members:
        #     team_member_ids = list(set(team_member_ids) - common_members)


        # for user_id in team_lead_ids:
        #     team_member = TeamMember(team=team, member_id=user_id, is_lead=True)
        #     team_member.save()

        # for user_id in team_member_ids:
        #     team_member = TeamMember(team=team, member_id=user_id, is_lead=False)
        #     team_member.save()

        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


    
def team_list(request):
    teams = Team.objects.all()
    users = User.objects.all()
    return render(request, 'team_list.html', {'teams': teams, 'users': users})

def delete_team(request):
    if request.method == "POST":
        team_id = request.POST.get("team_id")
        if team_id:
            try:
                team = Team.objects.get(pk=team_id)
                team.delete()
                return JsonResponse({"success": True})
            except Team.DoesNotExist:
                pass
    return JsonResponse({"success": False})


def team_list(request):
    search_query = request.GET.get('search', '')
    teams = Team.objects.all()

    if search_query:
        # Use Q objects to perform a complex query that searches multiple fields
        teams = teams.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(teammember__member__username__icontains=search_query) |
            Q(teammember__member__email__icontains=search_query)
        ).distinct()  # Use distinct() to remove duplicates

    users = User.objects.all()
    return render(request, 'team_list.html', {'teams': teams, 'users': users})

def get_team_data(request):
    if request.method == "GET":
        team_id = request.GET.get("team_id")
        if team_id:
            try:
                team = Team.objects.get(pk=team_id)
                team_leads = list(team.teammember_set.filter(is_lead=True).values_list("member__id", flat=True))
                team_members = list(team.teammember_set.filter(is_lead=False).values_list("member__id", flat=True))

                # Return the team data in JSON format
                return JsonResponse({
                    "success": True,
                    "team": {
                        "id": team.id,
                        "name": team.name,
                        "email": team.email,
                        "team_leads": team_leads,
                        "team_members": team_members,
                    },
                })
            except Team.DoesNotExist:
                pass

    return JsonResponse({"success": False})

def update_team(request):
    if request.method == 'POST':
        team_id = request.POST.get('editTeamId')
        if team_id:
            team = get_object_or_404(Team, pk=team_id)
            team.name = request.POST.get('edit_team_name')
            team.email = request.POST.get('edit_email')
            team_lead_ids = request.POST.getlist('edit_team_lead')
            team_member_ids = request.POST.getlist('edit_team_member')

            # Remove existing team members and leads
            team.teammember_set.all().delete()

            all_member_ids = set(team_lead_ids + team_member_ids)

            for user_id in all_member_ids:
                user_is_lead = False
                if user_id in team_lead_ids:
                    user_is_lead = True

                team_member = TeamMember(team=team, member_id=user_id, is_lead=user_is_lead)
                team_member.save()

            team.save()

            return JsonResponse({'success': True})
    return JsonResponse({'success': False})

def team_report(request):
    total_teams = Team.objects.count()
    total_members = TeamMember.objects.count()
    total_leads = TeamMember.objects.filter(is_lead=True).count()
    total_users = TeamMember.objects.values('member').distinct().count()

    max_leads_in_single_team = Team.objects.annotate(num_leads=Count('teammember', filter=Q(teammember__is_lead=True))).aggregate(max_leads=Max('num_leads'))['max_leads']
    max_members_in_single_team = Team.objects.annotate(num_members=Count('teammember__member')).aggregate(max_members=Max('num_members'))['max_members']

    context = {
        'total_teams': total_teams,
        'total_members': total_members,
        'total_leads': total_leads,
        'total_users': total_users,
        'max_leads_in_single_team': max_leads_in_single_team,
        'max_members_in_single_team': max_members_in_single_team,
    }

    return render(request, 'team_report.html', context)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def login(request):
    template = 'login.html'
    return render(request, template, {})


class CustomLoginView(LoginView):
    template_name = 'login.html'  # Your login template
