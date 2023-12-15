from datetime import timedelta, datetime
from apps.project.models import ProjectMember
from django.db.models import Q

from apps.team.models import Team
from django.db.models import Prefetch
from collections import defaultdict


def calculate_working_days_project(start_date, qs_project):
    data = []
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    one_day = timedelta(days=1)
    for pro in qs_project:
        schedule_hour = timedelta(hours=0)
        pro_data = {
            "id": pro.id,
            "project_name": pro.project_name,
            "project_code": pro.project_code,
            "color_code": pro.color_code,
            "client": {
                "id": pro.client_id,
                "name": pro.client.name,
            },
            "start_date": pro.start_date,
            "end_date": pro.end_date,
            "project_type": pro.project_type,
            "notes": pro.notes,
            "future_schedule_hours": schedule_hour,
            "project_member": [],
        }
        qs_project_member = pro.projectmember_set.all()
        if qs_project_member:
            for p_m in qs_project_member:
                total_hours = timedelta(hours=0)
                pm = {
                    "id": p_m.id,
                    "member": p_m.member_id,
                    "member": {
                        "id": p_m.member_id,
                        "capacity": p_m.member.capacity,
                        "department": {
                            "id": p_m.member.department.id,
                            "name": p_m.member.department.name,
                        },
                        "work_days": p_m.member.work_days,
                        "user": {
                            "id": p_m.member.user.id,
                            "full_name": p_m.member.user.full_name,
                            "email": p_m.member.user.email,
                            "role": p_m.member.user.role.id,
                            "phone_number": p_m.member.user.phone_number,
                            "designation": p_m.member.user.designation,
                        },
                        "emp_id": p_m.member.emp_id,
                        "scheduled_hours": total_hours,
                        "schedules": [],
                    },
                }
                work_days = set(p_m.member.work_days)
                qs_schedule = p_m.schedule_set.all().filter(
                    end_at__gte=start_date
                )
                if qs_schedule:
                    for sch in qs_schedule:
                        working_dates = []
                        end_at = sch.end_at
                        start_at = sch.start_at
                        current_date = (
                            start_date if start_at <= start_date else start_at
                        )
                        while current_date <= end_at:
                            # Check if the current day is a working day
                            if (
                                str(current_date.strftime("%a")[:3]).upper()
                                in work_days
                            ):
                                working_dates.append(
                                    f'{current_date}-{current_date.strftime("%a")[:3].upper()}'
                                )

                            # Move to the next day
                            current_date += one_day

                        total_hours += sch.assigned_hour * len(working_dates)
                        pm["member"]["schedules"].append(
                            {
                                "id": f"{sch.id}",
                                "start_at": sch.start_at,
                                "end_at": sch.end_at,
                                "notes": sch.notes,
                                "schedule_type": sch.schedule_type,
                                "assigned_hour": sch.assigned_hour,
                                "work_dates": working_dates,
                                "total_hours": sch.assigned_hour
                                * len(working_dates),
                            }
                        )
                schedule_hour += total_hours
                pm["member"]["scheduled_hours"] = total_hours
                pro_data["project_member"].append(pm)
        pro_data["future_schedule_hours"] = schedule_hour
        data.append(pro_data)
    return data


def working_days(current_date, stop_date, work_days):
    working_dates = []
    one_day = timedelta(days=1)
    while current_date <= stop_date:
        # Check if the current day is a working day
        if str(current_date.strftime("%a")[:3]).upper() in work_days:
            working_dates.append(
                f'{current_date}-{current_date.strftime("%a")[:3].upper()}'
            )

        # Move to the next day
        current_date += one_day
    return working_dates


def calculate_weekly_capacity(team_member, start_date, end_date):
    weekly_capacity_data = []

    current_date = start_date
    one_week = timedelta(days=7)

    while current_date <= end_date:
        working_dates = working_days(
            current_date,
            current_date + timedelta(days=6),
            team_member.work_days,
        )
        total_working_hours = team_member.capacity * len(working_dates)

        weekly_capacity_data.append(
            {
                "start": current_date.strftime("%Y-%m-%d"),
                "end": (current_date + timedelta(days=6)).strftime("%Y-%m-%d"),
                "total": total_working_hours,
            }
        )

        current_date += one_week

    return weekly_capacity_data


def calculate_weekly_assigned_hours(
    team_member, start_date, end_date, qs_schedule
):
    weekly_assigned_hours_data = []

    current_date = start_date
    one_week = timedelta(days=7)

    while current_date <= end_date:
        weekly_assigned_hours = timedelta(hours=0)
        for project_member in team_member.projectmember_set.all():
            project_schedules = qs_schedule.filter(
                project_member=project_member,
                end_at__gte=current_date,
                start_at__lte=current_date + timedelta(days=6),
            )

            for schedule in project_schedules:
                stop_date = min(
                    current_date + timedelta(days=6), schedule.end_at
                )
                begin_date = max(current_date, schedule.start_at)
                working_dates = working_days(
                    begin_date, stop_date, team_member.work_days
                )
                total_assigned_hours = schedule.assigned_hour * len(
                    working_dates
                )
                weekly_assigned_hours += total_assigned_hours

        weekly_assigned_hours_data.append(
            {
                "start": current_date.strftime("%Y-%m-%d"),
                "end": (current_date + timedelta(days=6)).strftime("%Y-%m-%d"),
                "total_assigned": weekly_assigned_hours,
            }
        )

        current_date += one_week

    return weekly_assigned_hours_data


def calculate_working_days_team(start_date, end_date, qs_schedule, company_id):
    data = []

    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # Fetch distinct project_member ids from schedules
    team_member_ids = qs_schedule.values("project_member__member").distinct()
    team_members_combined = (
        Team.objects.filter(
            Q(company_id=company_id)
            & (
                Q(id__in=team_member_ids)
                | ~Q(
                    id__in=ProjectMember.objects.filter(
                        project__company_id=company_id
                    ).values("member")
                )
            )
        )
        .distinct()
        .order_by("user__full_name")
    )
    # Fetch all team members not associated with projects
    team_mem_objs = team_members_combined.prefetch_related(
        Prefetch(
            "projectmember_set",
            queryset=ProjectMember.objects.filter(
                project__company_id=company_id
            ),
            to_attr="project_members",
        )
    )
    for team_member in team_mem_objs:
        weekly_capacity_data = calculate_weekly_capacity(
            team_member, start_date, end_date
        )
        weekly_assigned_hours_data = calculate_weekly_assigned_hours(
            team_member, start_date, end_date, qs_schedule
        )

        project_members_data = []
        if team_member.project_members:
            for project_member in team_member.project_members:
                project_data = {
                    "id": project_member.id,
                    "member": project_member.member_id,
                    "project": {
                        "id": project_member.project_id,
                        "project_name": project_member.project.project_name,
                        "project_code": project_member.project.project_code,
                        "color_code": project_member.project.color_code,
                        "client": {
                            "id": project_member.project.client_id,
                            "name": project_member.project.client.name,
                        },
                        "start_date": project_member.project.start_date,
                        "end_date": project_member.project.end_date,
                        "project_type": project_member.project.project_type,
                        "notes": project_member.project.notes,
                    },
                }
                project_members_data.append(project_data)
        team_member_data = {
            "id": team_member.id,
            "capacity": team_member.capacity,
            "emp_id": team_member.emp_id,
            "department": {
                "id": team_member.department.id,
                "name": team_member.department.name,
            },
            "work_days": team_member.work_days,
            "user": {
                "id": team_member.user.id,
                "full_name": team_member.user.full_name,
                "email": team_member.user.email,
                "role": team_member.user.role.id,
                "phone_number": team_member.user.phone_number,
                "designation": team_member.user.designation,
            },
            "project_members": project_members_data,
            "weekly_capacity": weekly_capacity_data,
            "weekly_assigned_hours": weekly_assigned_hours_data,
        }

        data.append(team_member_data)

    return data


# def calculate_working_days_team(start_date, end_date, qs_team):
#     data = []

#     start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
#     end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
#     one_day = timedelta(days=1)

#     # Pre-fetch project members and associated data
#     project_members_data = {}
#     for t in qs_team:
#         project_members_data[t.id] = {
#             "project_members": list(t.projectmember_set.all()),
#         }

#     for t in qs_team:
#         weekly_caps = []
#         weekly_assigned_hours = []

#         current_date = start_date
#         while current_date <= end_date:
#             working_dates = working_days(
#                 current_date, current_date + timedelta(days=6), t.work_days
#             )
#             weekly_cap = t.capacity * len(working_dates)

#             weekly_caps.append(
#                 {
#                     "start": current_date.strftime("%Y-%m-%d"),
#                     "end": (current_date + timedelta(days=6)).strftime(
#                         "%Y-%m-%d"
#                     ),
#                     "total": weekly_cap,
#                 }
#             )

#             total_assigned_hours = timedelta(hours=0)
#             project_members = []

#             for p_m in project_members_data[t.id]["project_members"]:
#                 project_member_data = {
#                     "id": p_m.id,
#                     "member": p_m.member_id,
#                     "project": {
#                         "id": p_m.project_id,
#                         "project_name": p_m.project.project_name,
#                         "project_code": p_m.project.project_code,
#                         "color_code": p_m.project.color_code,
#                         "client": {
#                             "id": p_m.project.client_id,
#                             "name": p_m.project.client.name,
#                         },
#                         "start_date": p_m.project.start_date,
#                         "end_date": p_m.project.end_date,
#                         "project_type": p_m.project.project_type,
#                         "notes": p_m.project.notes,
#                     },
#                 }

#                 work_days = set(p_m.member.work_days)
#                 qs_schedule = p_m.schedule_set.filter(
#                     end_at__gte=current_date,
#                     start_at__lte=current_date + timedelta(days=6),
#                 )

#                 for sch in qs_schedule:
#                     stop_date = min(
#                         current_date + timedelta(days=6), sch.end_at
#                     )
#                     if current_date <= sch.start_at:
#                         begin_date = sch.start_at
#                         working_dates = working_days(
#                             begin_date, stop_date, work_days
#                         )
#                     else:
#                         working_dates = working_days(
#                             current_date, stop_date, work_days
#                         )
#                     total_assigned_hours += sch.assigned_hour * len(
#                         working_dates
#                     )

#                 project_member_data[
#                     "total_assigned_hours"
#                 ] = total_assigned_hours
#                 project_members.append(project_member_data)

#             weekly_assigned_hours.append(
#                 {
#                     "start": current_date.strftime("%Y-%m-%d"),
#                     "end": (current_date + timedelta(days=6)).strftime(
#                         "%Y-%m-%d"
#                     ),
#                     "total_assigned": total_assigned_hours,
#                 }
#             )

#             current_date += timedelta(days=7)

#         data.append(
#             {
#                 "id": t.id,
#                 "capacity": t.capacity,
#                 "emp_id": t.emp_id,
#                 "department": {
#                     "id": t.department.id,
#                     "name": t.department.name,
#                 },
#                 "work_days": t.work_days,
#                 "user": {
#                     "id": t.user.id,
#                     "full_name": t.user.full_name,
#                     "email": t.user.email,
#                     "role": t.user.role.id,
#                     "phone_number": t.user.phone_number,
#                     "designation": t.user.designation,
#                 },
#                 "project_members": project_members,
#                 "weekly_capacity": weekly_caps,
#                 "weekly_assigned_hours": weekly_assigned_hours,
#             }
#         )

#     return data
