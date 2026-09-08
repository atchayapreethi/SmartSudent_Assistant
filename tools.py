def attendance_tool(student_name):
    attendance_data = {
        "Aashika": "Your current attendance is 85%."
    }

    return attendance_data.get(
        student_name,
        "Attendance information is not available."
    )


def exam_tool():
    return "Students can check official examination notices for exam information."


def office_tool():
    return "Students can contact the college office during official working hours."
def notice_tool():
    from pathlib import Path

    file_path = Path("data/notices/college_notice.txt")

    if file_path.exists():
        return file_path.read_text(encoding="utf-8")

    return "College notice information is not available."