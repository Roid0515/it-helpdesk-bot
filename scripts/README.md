# DB 스크립트

## helpdesk_db 테이블 생성 (MariaDB 12.1.x 호환)

1. DBeaver에서 **helpdesk_db**에 연결된 세션에서 `create_helpdesk_tables.sql` 열기
2. **첫 번째 CREATE TABLE** 블록만 드래그로 선택 → Ctrl+Enter 실행
3. **두 번째 CREATE TABLE** 블록만 드래그로 선택 → Ctrl+Enter 실행
4. Database Navigator에서 helpdesk_db → Tables **새로고침** → 테이블 확인

한 번에 전체 실행하지 말고, CREATE TABLE 두 개를 **각각 선택해서 따로 실행**해야 합니다.
