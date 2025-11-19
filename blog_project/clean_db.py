import sqlite3

# 데이터베이스 파일 연결
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

target_user_id = 3

tables_to_clean = [
    'account_userprofile',        # 유저 프로필 (이미 지웠지만 확인 사살)
    'auth_user_groups',           # 유저-그룹 연결 (현재 에러 원인)
    'auth_user_user_permissions', # 유저-권한 연결 (잠재적 에러 원인 1)
    'django_admin_log',           # 관리자 작업 로그 (잠재적 에러 원인 2)
]

print(f"--- User ID {target_user_id} 관련 고아 데이터 삭제 시작 ---")

for table in tables_to_clean:
    try:
        # 해당 테이블에 user_id 컬럼이 있는지 확인 후 삭제
        query = f"DELETE FROM {table} WHERE user_id = {target_user_id}"
        cursor.execute(query)
        if cursor.rowcount > 0:
            print(f"[{table}] 테이블에서 {cursor.rowcount}개의 데이터를 삭제했습니다.")
        else:
            print(f"[{table}] 삭제할 데이터 없음.")
    except sqlite3.OperationalError:
        # 테이블이 없을 경우(예: 아직 마이그레이션 안된 경우) 넘어감
        print(f"[{table}] 테이블이 존재하지 않아 건너뜁니다.")

conn.commit()
conn.close()
print("--- 청소 완료 ---")