from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from models import db, HelpDeskRequest, DailyInbox
from chatbot import ChatBot
from datetime import datetime, date
import os
import sys
import webbrowser
from threading import Timer
from dotenv import load_dotenv

load_dotenv()

# PyInstaller로 빌드된 경우 리소스 경로 처리
if getattr(sys, 'frozen', False):
    # 실행 파일로 실행된 경우
    base_path = sys._MEIPASS
    template_folder = os.path.join(base_path, 'templates')
    static_folder = os.path.join(base_path, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    # 일반 Python 스크립트로 실행된 경우
    app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///helpdesk.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# CORS 설정 (프론트엔드와 통신용)
CORS(app)

# 데이터베이스 초기화
db.init_app(app)

# 챗봇 인스턴스
chatbot = ChatBot()


# ==================== 사용자 챗봇 페이지 ====================
@app.route('/')
def index():
    """사용자용 챗봇 페이지"""
    return render_template('index.html')


# ==================== 챗봇 API ====================
@app.route('/api/chat', methods=['POST'])
def chat():
    """챗봇 메시지 처리 API"""
    data = request.json
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': '메시지가 없습니다.'}), 400
    
    # 챗봇 처리
    result = chatbot.process_message(user_message)
    
    return jsonify(result)


@app.route('/api/submit-request', methods=['POST'])
def submit_request():
    """요청사항 접수 API"""
    try:
        data = request.json
        
        # 필수 필드 확인
        if not data.get('title') or not data.get('content'):
            return jsonify({'error': '제목과 내용은 필수입니다.'}), 400
        
        # 요청사항 생성
        request_obj = HelpDeskRequest(
            user_name=data.get('user_name', '익명'),
            user_department=data.get('user_department'),
            user_contact=data.get('user_contact'),
            title=data.get('title'),
            content=data.get('content'),
            category=data.get('category'),
            request_date=date.today()
        )
        
        db.session.add(request_obj)
        db.session.commit()
        
        # 일일 접수함 확인 및 생성
        today = date.today()
        daily_inbox = DailyInbox.query.filter_by(inbox_date=today).first()
        if not daily_inbox:
            daily_inbox = DailyInbox(inbox_date=today)
            db.session.add(daily_inbox)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '요청사항이 접수되었습니다.',
            'request_id': request_obj.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'접수 중 오류가 발생했습니다: {str(e)}'}), 500


# ==================== 관리자 게시판 페이지 ====================
@app.route('/admin')
def admin():
    """관리자용 게시판 페이지"""
    return render_template('admin.html')


# ==================== 관리자 API ====================
@app.route('/api/admin/daily-inboxes', methods=['GET'])
def get_daily_inboxes():
    """일일 접수함 목록 조회"""
    try:
        inboxes = DailyInbox.query.order_by(DailyInbox.inbox_date.desc()).all()
        
        result = []
        for inbox in inboxes:
            # 해당 날짜의 요청사항 개수 조회
            request_count = HelpDeskRequest.query.filter_by(request_date=inbox.inbox_date).count()
            
            inbox_dict = inbox.to_dict()
            inbox_dict['request_count'] = request_count
            result.append(inbox_dict)
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'조회 중 오류가 발생했습니다: {str(e)}'}), 500


@app.route('/api/admin/requests', methods=['GET'])
def get_requests():
    """요청사항 목록 조회"""
    try:
        # 쿼리 파라미터
        date_filter = request.args.get('date')  # YYYY-MM-DD 형식
        status_filter = request.args.get('status')
        
        query = HelpDeskRequest.query
        
        # 날짜 필터
        if date_filter:
            try:
                filter_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
                query = query.filter_by(request_date=filter_date)
            except ValueError:
                return jsonify({'error': '날짜 형식이 올바르지 않습니다. (YYYY-MM-DD)'}), 400
        
        # 상태 필터
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        # 최신순 정렬
        requests = query.order_by(HelpDeskRequest.created_at.desc()).all()
        
        result = [req.to_dict() for req in requests]
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'조회 중 오류가 발생했습니다: {str(e)}'}), 500


@app.route('/api/admin/requests/<int:request_id>', methods=['GET'])
def get_request(request_id):
    """특정 요청사항 상세 조회"""
    try:
        request_obj = HelpDeskRequest.query.get_or_404(request_id)
        return jsonify(request_obj.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': f'조회 중 오류가 발생했습니다: {str(e)}'}), 500


@app.route('/api/admin/requests/<int:request_id>/status', methods=['PUT'])
def update_request_status(request_id):
    """요청사항 상태 업데이트"""
    try:
        request_obj = HelpDeskRequest.query.get_or_404(request_id)
        data = request.json
        
        new_status = data.get('status')
        if new_status not in ['pending', 'processing', 'completed']:
            return jsonify({'error': '올바른 상태값이 아닙니다.'}), 400
        
        request_obj.status = new_status
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '상태가 업데이트되었습니다.',
            'request': request_obj.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'업데이트 중 오류가 발생했습니다: {str(e)}'}), 500


@app.route('/api/admin/stats', methods=['GET'])
def get_stats():
    """통계 정보 조회"""
    try:
        total_requests = HelpDeskRequest.query.count()
        pending_requests = HelpDeskRequest.query.filter_by(status='pending').count()
        processing_requests = HelpDeskRequest.query.filter_by(status='processing').count()
        completed_requests = HelpDeskRequest.query.filter_by(status='completed').count()
        
        # 오늘의 요청 수
        today_requests = HelpDeskRequest.query.filter_by(request_date=date.today()).count()
        
        return jsonify({
            'total': total_requests,
            'pending': pending_requests,
            'processing': processing_requests,
            'completed': completed_requests,
            'today': today_requests
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'통계 조회 중 오류가 발생했습니다: {str(e)}'}), 500


def open_browser():
    """서버 시작 후 브라우저 자동 열기"""
    url = 'http://localhost:5000'
    webbrowser.open(url)


if __name__ == '__main__':
    with app.app_context():
        # 데이터베이스 테이블 생성
        db.create_all()
    
    # .exe로 실행된 경우에만 브라우저 자동 열기
    if getattr(sys, 'frozen', False):
        Timer(1.5, open_browser).start()
    
    # 디버그 모드는 .exe 빌드 시 False로 설정
    debug_mode = not getattr(sys, 'frozen', False)
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
