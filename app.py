"""
Portfolio Website - Flask Application
Môn: Nhập môn Công nghệ số và Ứng dụng Trí tuệ nhân tạo
Author: Sinh viên năm nhất
"""

from flask import Flask, render_template, jsonify
import json
import os

# Khởi tạo Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'portfolio-secret-key-2024'

# ============================================================
# DỮ LIỆU MẪU - Thay thế bằng thông tin thực của bạn
# ============================================================

# Thông tin cá nhân
STUDENT_INFO = {
    "name": "Đỗ Đinh Đạt",
    "student_id": "23IT001",
    "major": "Công nghệ Thông tin",
    "university": "Đại học Việt Nhật",
    "faculty": "Khoa Công nghệ Thông tin",
    "year": "Sinh viên năm nhất (2025 - 2026)",
    "email": "dodinhdat@st.vju.ac.vn",
    "phone": "0901 234 567",
    "avatar": "/static/images/placeholder.svg",
    "hobbies": [
        {"title": "Lập trình", "desc": "Thích tìm hiểu ngôn ngữ lập trình mới"},
        {"title": "Đọc sách", "desc": "Đặc biệt yêu thích sách công nghệ và khoa học"},
        {"title": "Thiết kế", "desc": "Thiết kế giao diện và đồ họa cơ bản"},
        {"title": "Khám phá công nghệ", "desc": "Theo dõi xu hướng AI và công nghệ mới"},
    ],
    "learning_goals": [
        "Nắm vững kiến thức nền tảng về Công nghệ Thông tin",
        "Thành thạo ít nhất 2 ngôn ngữ lập trình (Python, Java)",
        "Hiểu và ứng dụng được các thuật toán AI cơ bản",
        "Xây dựng được các dự án thực tế có giá trị",
        "Phát triển kỹ năng làm việc nhóm và tư duy phản biện",
    ],
    "portfolio_goals": [
        "Lưu lại hành trình học tập trong học kỳ đầu tiên",
        "Thể hiện những gì đã học được qua các bài tập thực hành",
        "Tạo nền tảng để xây dựng portfolio chuyên nghiệp trong tương lai",
        "Chia sẻ kiến thức và kinh nghiệm với các bạn cùng khóa",
    ],
    "quote": "\"Hành trình ngàn dặm bắt đầu từ một bước chân.\"",
    "quote_author": "— Lão Tử"
}

# Dữ liệu 6 bài tập
PROJECTS = [
    {
        "id": 1,
        "slug": "may-tinh-thiet-bi-ngoai-vi",
        "title": "Máy tính và Thiết bị Ngoại vi",
        "icon": "",
        "color": "#2ecc71",
        "category": "Phần cứng",
        "week": "Tuần 1 - 2",
        "objective": "Tìm hiểu cấu trúc và nguyên lý hoạt động của máy tính, các loại thiết bị ngoại vi phổ biến và cách kết nối chúng. Hiểu được vai trò của từng thành phần trong hệ thống máy tính.",
        "process": [
            "Nghiên cứu tài liệu về kiến trúc máy tính (CPU, RAM, Storage, Motherboard)",
            "Tìm hiểu các loại thiết bị ngoại vi: input (chuột, bàn phím), output (màn hình, máy in)",
            "Thực hành tháo lắp và nhận biết các linh kiện trên máy tính thực tế",
            "Viết báo cáo tổng hợp và thuyết trình trước lớp",
        ],
        "results": "Hiểu rõ cấu trúc phần cứng máy tính, nhận biết được các thiết bị ngoại vi phổ biến, biết cách kết nối và cấu hình cơ bản. Hoàn thành báo cáo 15 trang với đầy đủ hình ảnh minh họa.",
        "skills_learned": ["Kiến trúc máy tính", "Nhận biết phần cứng", "Kỹ năng báo cáo"],
        "grade": "9.5/10",
        "image": "/static/images/project1.svg",
        "pdf": "/static/uploads/pdfs/baitap1.pdf",
        "video": "",
        "tags": ["Hardware", "Phần cứng", "Thiết bị ngoại vi"]
    },
    {
        "id": 2,
        "slug": "khai-thac-du-lieu",
        "title": "Khai thác Dữ liệu và Thông tin",
        "icon": "",
        "color": "#27ae60",
        "category": "Dữ liệu",
        "week": "Tuần 3 - 4",
        "objective": "Học cách thu thập, xử lý và phân tích dữ liệu từ nhiều nguồn khác nhau. Hiểu tầm quan trọng của dữ liệu trong thời đại số và các phương pháp khai thác thông tin có giá trị.",
        "process": [
            "Tìm hiểu các khái niệm cơ bản về dữ liệu: cấu trúc, phi cấu trúc, bán cấu trúc",
            "Thực hành thu thập dữ liệu từ website sử dụng Google Sheets",
            "Phân tích dữ liệu khảo sát lớp học (30 mẫu) bằng công cụ Excel",
            "Vẽ biểu đồ và trình bày kết quả phân tích",
            "Thảo luận về đạo đức trong việc sử dụng dữ liệu",
        ],
        "results": "Thu thập và phân tích thành công bộ dữ liệu 30 mẫu khảo sát. Tạo được 5 loại biểu đồ khác nhau, rút ra 3 insight có giá trị từ dữ liệu. Điểm bài tập: xuất sắc.",
        "skills_learned": ["Phân tích dữ liệu", "Excel", "Tư duy phân tích"],
        "grade": "9.0/10",
        "image": "/static/images/project2.svg",
        "pdf": "/static/uploads/pdfs/baitap2.pdf",
        "video": "https://youtube.com",
        "tags": ["Data", "Phân tích", "Excel", "Thống kê"]
    },
    {
        "id": 3,
        "slug": "tong-quan-ai",
        "title": "Tổng quan về Trí tuệ Nhân tạo",
        "icon": "",
        "color": "#1abc9c",
        "category": "Trí tuệ nhân tạo",
        "week": "Tuần 5 - 6",
        "objective": "Nắm được lịch sử phát triển, các khái niệm cơ bản và ứng dụng thực tiễn của Trí tuệ Nhân tạo. Phân biệt được AI, Machine Learning và Deep Learning.",
        "process": [
            "Nghiên cứu lịch sử AI từ 1950 đến nay (Test Turing, mùa đông AI, thời đại deep learning)",
            "Tìm hiểu các nhánh chính: Machine Learning, Deep Learning, NLP, Computer Vision",
            "Phân tích 5 ứng dụng AI trong cuộc sống: ChatGPT, Google Maps, Netflix, Face ID, Siri",
            "Thực hành sử dụng công cụ AI: ChatGPT, Midjourney, GitHub Copilot",
            "Làm slide thuyết trình 20 trang về tương lai AI",
        ],
        "results": "Hiểu sâu về lịch sử và phát triển AI, biết sử dụng thành thạo 3 công cụ AI phổ biến. Bài thuyết trình được giảng viên đánh giá cao về nội dung và hình thức.",
        "skills_learned": ["Kiến thức AI/ML", "Sử dụng AI tools", "Thuyết trình"],
        "grade": "9.8/10",
        "image": "/static/images/project3.svg",
        "pdf": "/static/uploads/pdfs/baitap3.pdf",
        "video": "https://youtube.com",
        "tags": ["AI", "Machine Learning", "Deep Learning", "ChatGPT"]
    },
    {
        "id": 4,
        "slug": "giao-tiep-hop-tac",
        "title": "Giao tiếp và Hợp tác Môi trường Số",
        "icon": "",
        "color": "#16a085",
        "category": "Kỹ năng mềm",
        "week": "Tuần 7 - 8",
        "objective": "Rèn luyện kỹ năng giao tiếp và làm việc nhóm trong môi trường kỹ thuật số. Sử dụng thành thạo các công cụ cộng tác trực tuyến hiện đại.",
        "process": [
            "Học sử dụng các công cụ: Google Workspace, Microsoft Teams, Slack, Trello",
            "Thực hiện dự án nhóm 4 người hoàn toàn online trong 2 tuần",
            "Viết tài liệu kỹ thuật cộng tác trên Google Docs (real-time)",
            "Tổ chức và tham gia 5 buổi họp nhóm qua Zoom/Meet",
            "Quản lý task và deadline bằng Trello board",
        ],
        "results": "Hoàn thành dự án nhóm đúng deadline với chất lượng tốt. Thành thạo 5 công cụ cộng tác số. Phát triển kỹ năng lãnh đạo khi đảm nhận vai trò nhóm trưởng.",
        "skills_learned": ["Teamwork", "Google Workspace", "Quản lý dự án", "Giao tiếp số"],
        "grade": "8.5/10",
        "image": "/static/images/project4.svg",
        "pdf": "/static/uploads/pdfs/baitap4.pdf",
        "video": "",
        "tags": ["Teamwork", "Google Docs", "Trello", "Online Collaboration"]
    },
    {
        "id": 5,
        "slug": "sang-tao-noi-dung-so",
        "title": "Sáng tạo Nội dung Số",
        "icon": "",
        "color": "#2ecc71",
        "category": "Sáng tạo",
        "week": "Tuần 9 - 10",
        "objective": "Học cách tạo ra nội dung số chất lượng cao bằng các công cụ hiện đại. Kết hợp kỹ năng thiết kế, viết lách và sử dụng AI để tạo nội dung sáng tạo.",
        "process": [
            "Học thiết kế cơ bản với Canva: poster, infographic, social media",
            "Tạo video giới thiệu bản thân bằng CapCut (2 phút)",
            "Viết bài blog 800 từ về chủ đề công nghệ trên Medium",
            "Sử dụng AI (Midjourney, DALL-E) để tạo hình ảnh minh họa",
            "Xây dựng portfolio online đơn giản trên Notion",
        ],
        "results": "Tạo ra 3 sản phẩm nội dung số: 1 infographic, 1 video, 1 bài blog. Bài blog đạt 150 lượt đọc trong tuần đầu. Phát triển được phong cách thiết kế cá nhân.",
        "skills_learned": ["Canva", "Video editing", "Content writing", "AI Image generation"],
        "grade": "9.2/10",
        "image": "/static/images/project5.svg",
        "pdf": "/static/uploads/pdfs/baitap5.pdf",
        "video": "https://youtube.com",
        "tags": ["Design", "Canva", "Video", "Blog", "AI Art"]
    },
    {
        "id": 6,
        "slug": "an-toan-liem-chinh",
        "title": "An toàn và Liêm chính Học thuật",
        "icon": "",
        "color": "#27ae60",
        "category": "Đạo đức số",
        "week": "Tuần 11 - 12",
        "objective": "Nâng cao nhận thức về an toàn thông tin cá nhân, bản quyền số và liêm chính trong học thuật. Hiểu trách nhiệm của công dân số trong thời đại AI.",
        "process": [
            "Nghiên cứu các quy định về bản quyền và Creative Commons",
            "Tìm hiểu về bảo mật thông tin cá nhân: mật khẩu mạnh, 2FA, VPN",
            "Phân tích các tình huống đạo đức khi sử dụng AI trong học tập",
            "Viết essay về trách nhiệm sử dụng AI có đạo đức (1000 từ)",
            "Tổ chức buổi thảo luận nhóm về học thuật liêm chính",
        ],
        "results": "Hoàn thiện nhận thức về đạo đức số và liêm chính học thuật. Xây dựng được bộ nguyên tắc cá nhân khi sử dụng công nghệ và AI. Essay được chọn làm tài liệu tham khảo cho lớp.",
        "skills_learned": ["Bảo mật thông tin", "Đạo đức số", "Tư duy phản biện", "Academic integrity"],
        "grade": "9.0/10",
        "image": "/static/images/project6.svg",
        "pdf": "/static/uploads/pdfs/baitap6.pdf",
        "video": "",
        "tags": ["Security", "Ethics", "Academic Integrity", "Digital Citizenship"]
    }
]

# Dữ liệu trang Tổng kết
SUMMARY = {
    "lessons_learned": [
            {
            "icon": "",
            "title": "Tư duy số",
            "desc": "Hiểu rõ cách công nghệ số ảnh hưởng đến mọi khía cạnh của cuộc sống và công việc hiện đại."
        },
        {
            "icon": "",
            "title": "Bản chất của AI",
            "desc": "AI không phải phép màu mà là kết quả của toán học, dữ liệu và kỹ thuật lập trình tinh vi."
        },
        {
            "icon": "",
            "title": "Trách nhiệm số",
            "desc": "Mỗi hành động trong không gian số đều có hậu quả - cần có trách nhiệm và đạo đức khi sử dụng công nghệ."
        },
        {
            "icon": "",
            "title": "Sức mạnh cộng tác",
            "desc": "Làm việc nhóm hiệu quả với công cụ số giúp tăng năng suất và chất lượng sản phẩm lên nhiều lần."
        },
        {
            "icon": "",
            "title": "Học liên tục",
            "desc": "Công nghệ thay đổi nhanh chóng, kỹ năng tự học và cập nhật kiến thức là tài sản quý giá nhất."
        },
        {
            "icon": "",
            "title": "Tư duy giải quyết vấn đề",
            "desc": "Mỗi bài tập là cơ hội rèn luyện kỹ năng phân tích và giải quyết vấn đề có hệ thống."
        }
    ],
    "skills": {
        "technical": [
            {"name": "Python cơ bản", "level": 60},
            {"name": "HTML/CSS", "level": 55},
            {"name": "Phân tích dữ liệu (Excel)", "level": 75},
            {"name": "Sử dụng AI tools", "level": 80},
            {"name": "Thiết kế (Canva)", "level": 70},
            {"name": "Bảo mật thông tin cơ bản", "level": 65},
        ],
        "soft": [
            {"name": "Làm việc nhóm", "level": 85},
            {"name": "Thuyết trình", "level": 70},
            {"name": "Quản lý thời gian", "level": 75},
            {"name": "Viết báo cáo kỹ thuật", "level": 80},
            {"name": "Tư duy phản biện", "level": 65},
            {"name": "Giao tiếp số", "level": 90},
        ]
    },
    "challenges": [
        {
            "icon": "",
            "title": "Quản lý thời gian",
            "desc": "Ban đầu gặp khó khăn trong việc cân bằng nhiều môn học cùng lúc. Giải quyết bằng cách lập kế hoạch học tập hàng tuần chi tiết."
        },
        {
            "icon": "",
            "title": "Kỹ thuật lập trình",
            "desc": "Python là ngôn ngữ lập trình đầu tiên, cú pháp và logic lập trình cần nhiều thời gian để quen."
        },
        {
            "icon": "",
            "title": "Tìm kiếm tài liệu",
            "desc": "Phần lớn tài liệu chuyên ngành bằng tiếng Anh, phải rèn luyện thêm kỹ năng đọc hiểu tài liệu kỹ thuật."
        },
        {
            "icon": "",
            "title": "Làm việc nhóm online",
            "desc": "Phối hợp với các thành viên nhóm qua môi trường số đòi hỏi kỹ năng giao tiếp và tổ chức tốt hơn."
        }
    ],
    "future_plans": [
        "Học sâu hơn về Python và các thư viện Data Science (Pandas, NumPy, Matplotlib)",
        "Tìm hiểu về Machine Learning và xây dựng model AI đầu tiên",
        "Tham gia các cuộc thi lập trình sinh viên (ICPC, Google Code Jam)",
        "Thực tập tại công ty công nghệ vào năm 3",
        "Xây dựng portfolio với ít nhất 5 dự án thực tế trước khi tốt nghiệp",
        "Đạt chứng chỉ AWS Cloud Practitioner hoặc Google AI Certificate",
    ],
    "overall_grade": "9.0",
    "total_hours": "120+",
    "projects_completed": 6,
    "reflection": "Học kỳ đầu tiên là hành trình đầy thú vị và thách thức. Từ không biết gì về công nghệ số, tôi đã có được nền tảng kiến thức vững chắc và những kỹ năng thực tế giá trị. Điều quan trọng nhất tôi học được không chỉ là kiến thức kỹ thuật, mà còn là cách tư duy, cách học hỏi và cách thích nghi với môi trường công nghệ thay đổi nhanh chóng. Đây chỉ là bước đầu của một hành trình dài và đầy hứa hẹn!"
}


# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def index():
    """Trang chủ - Giới thiệu"""
    return render_template('index.html',
                           student=STUDENT_INFO,
                           page='home')


@app.route('/index')
@app.route('/home')
def index_alias():
    """Alias cho trang chủ"""
    return index()


@app.route('/projects')
@app.route('/projects/')
def projects():
    """Trang Dự án - Danh sách bài tập"""
    return render_template('projects.html',
                           student=STUDENT_INFO,
                           projects=PROJECTS,
                           page='projects')


@app.route('/projects/<slug>')
def project_detail(slug):
    """Trang chi tiết từng bài tập"""
    project = next((p for p in PROJECTS if p['slug'] == slug), None)
    if not project:
        return render_template('404.html'), 404
    return render_template('project_detail.html',
                           student=STUDENT_INFO,
                           project=project,
                           projects=PROJECTS,
                           page='projects')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/summary')
def summary():
    """Trang Tổng kết"""
    return render_template('summary.html',
                           student=STUDENT_INFO,
                           summary=SUMMARY,
                           page='summary')


# API endpoints để lấy dữ liệu JSON (tùy chọn)
@app.route('/api/student')
def api_student():
    return jsonify(STUDENT_INFO)


@app.route('/api/projects')
def api_projects():
    return jsonify(PROJECTS)


@app.route('/api/summary')
def api_summary():
    return jsonify(SUMMARY)


# ============================================================
# CHẠY ỨNG DỤNG
# ============================================================
if __name__ == '__main__':
    print("Portfolio Website đang khởi động...")
    print("Truy cập: http://127.0.0.1:5000")
    print("Nhấn Ctrl+C để dừng server")
    app.run(debug=True, host='0.0.0.0', port=5000)