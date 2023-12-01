from datetime import timedelta, datetime


def calculate_working_days(start_date, qs_project):
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
