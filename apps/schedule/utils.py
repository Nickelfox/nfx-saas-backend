from datetime import timedelta, datetime


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


def calculate_working_days_team(start_date, end_date, qs_team):
    data = []
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
    one_day = timedelta(days=1)
    for t in qs_team:
        working_dates = working_days(start_date, end_date, t.work_days)
        weekly_cap = timedelta(hours=0)
        schedule_hour = timedelta(hours=0)
        team_data = {
            "id": t.id,
            "capacity": t.capacity,
            "emp_id": t.emp_id,
            "weekly_capacity": t.capacity * len(working_dates),
            "weekly_assigned_hours": schedule_hour,
            "department": {
                "id": t.department.id,
                "name": t.department.name,
            },
            "work_days": t.work_days,
            "user": {
                "id": t.user.id,
                "full_name": t.user.full_name,
                "email": t.user.email,
                "role": t.user.role.id,
                "phone_number": t.user.phone_number,
                "designation": t.user.designation,
            },
            "project_member": [],
        }
        qs_project_member = t.projectmember_set.all()
        if qs_project_member:
            for p_m in qs_project_member:
                total_hours = timedelta(hours=0)
                pm = {
                    "id": p_m.id,
                    "project": {
                        "id": p_m.project_id,
                        "project_name": p_m.project.project_name,
                        "project_code": p_m.project.project_code,
                        "color_code": p_m.project.color_code,
                        "client": {
                            "id": p_m.project.client_id,
                            "name": p_m.project.client.name,
                        },
                        "start_date": p_m.project.start_date,
                        "end_date": p_m.project.end_date,
                        "project_type": p_m.project.project_type,
                        "notes": p_m.project.notes,
                    },
                }
                work_days = set(p_m.member.work_days)
                qs_schedule = p_m.schedule_set.all().filter(
                    end_at__gte=start_date, start_at__lte=end_date
                )
                if qs_schedule.exists():
                    for sch in qs_schedule:
                        working_dates = []
                        end_at = sch.end_at
                        start_at = sch.start_at
                        current_date = (
                            start_date if start_at <= start_date else start_at
                        )
                        stop_date = end_date if end_date <= end_at else end_at
                        working_dates = working_days(
                            current_date, stop_date, work_days
                        )
                        total_hours += sch.assigned_hour * len(working_dates)
                schedule_hour += total_hours
                team_data["project_member"].append(pm)
        team_data["weekly_assigned_hours"] = schedule_hour
        data.append(team_data)
    return data
