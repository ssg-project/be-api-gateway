
# python 버전 선택
FROM python:3.9.19

WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . /app/

# Python 패키지 경로 설정
ENV PYTHONPATH=/app

# FastAPI 애플리케이션 실행
CMD ["python", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
