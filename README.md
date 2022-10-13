# Dstagram


## 프로젝트 소개

Instagram 클론 프로젝트입니다. 

파이썬 웹 프로그래밍이라는 책의 카피 코딩으로 유저, 게시글 CRUD를 구현하였으며

그 이후 혼자 공부하며 개발하는 중입니다.

접속 주소: [https://dstagram-ec2.kro.kr/](https://dstagram-ec2.kro.kr/)

## 서버 구성
CloudFront - AWS ELB - Nginx - gunicorn(uvicorn) - Django

## 사용 기술

- Django, Python
- nginx, gunicorn
- Docker
- AWS EC2, S3, CloudFront, ELB
- AWS RDS MySQL 8.0
- javascript
- git
- github action


## 주요기능

- 회원 가입 및 로그인, 로그아웃
- 회원 정보 수정 및 탈퇴
- 이미지 다중 업로드(한 게시글에 최대 10개)
- 게시글 수정, 삭제
- 게시글 좋아요, 취소
- 게시글 공유(DM)
- 유저 팔로우, 취소
- 비동기 유저 검색
- DM(비동기 실시간 채팅)

## 변경 사항

### v1.0
- 서버 이전: 헤로쿠 -> AWS EC2
- DB변경: SQLite -> AWS RDS MySQL 
- github action과 docker compose를 이용한 ci/cd 파이프라인 구축
- CloudFront와 ACM 인증서를 이용한 무료 도메인 연결
- ACM 인증서를 이용한 https 통신
- Django Chanel을 이용한 비동기 실시간 채팅 구현
- 환경 변수 .env로 정리 및 git actions secrets 값으로 추가

### v0.9

- User Model 커스터마이징
- 프로필 이미지를 위한 `ImageField` 추가.
- username field 기본값을 email로 변경.
- 닉네임과 같은 용도의 tag 생성.

- 비동기 유저 검색 기능
- DRF serializer를 이용해 필요한 필드값만 응답

- 다중 파일 업로드
- 기존 Photo Model에서 Post, Photo 두개의 모델로 1:N 모델로 수정.
- imagekit app을 이용한 이미지 Resizing(2.07MB→21.7KB, 5.16MB→37.3KB ⇒ 약 99% 저장공간 절감)
- InlineFormSet 이용한 데이터 송수신.
- `TabularInline`를 이용해 Admin 페이지 수정.
- splider.js 라이브러리를 이용한 슬라이드로 게시글의 이미지를 보여줍니다.

- 팔로우
- Follow 모델 생성
- 메인 피드는 팔로우한 유저와 본인의 게시글만 보여줍니다.

- 좋아요
- Like 모델 생성
- 비동기로 좋아요 처리 후 현재 좋아요 수를 응답합니다.

- `secret_key.py` 헤로쿠 환경변수 처리
- Django `SECRET_KEY` 및 AWS S3 `ACCESS_KEY`

## 개발 예정

1. ~~실시간 채팅~~
2. 팔로우 할 유저 추천
3. 검색 페이지 추가
4. 해시태그
5. ~~게시글 공유~~
6. 게시글 우측 상단 점 세개 버튼 활성화
7. 댓글 기능 구현 (현재 DISQUS 사용)
8. 마이페이지 게시글 리스트 Grid Layout으로 변경
9. 동영상 업로드
10. 로그인 세션 보완
11. 회원 가입 유효성 검사 보완
12. 회원 가입 이메일과 휴대폰 인증
13. 코드와 파일 리팩토링
14. ~~AWS EC2로 서버 이전~~
15. 채팅 알람
16. 추후 생각나는 대로 추가 예정

## 모델 구조

**User**

| 필드명 | 타입 |
| --- | --- |
| email | EmailField |
| name | CharField |
| tag | CharField |
| birth_date | DateField |
| profile_pic | django_field.DefaultStaticImageField |
| self_intro | CharField |
| phone_num | CharField |
| created | DateTimeField |
| is_active | BooleanField |
| is_admin | BooleanField |

---

**Post**

| 필드명 | 타입 |
| --- | --- |
| id | AutoField |
| author | ForeignKey(User) |
| text | TextField |
| created | DateTimeField |
| updated | DateTimeField |

---

**Photo**

| 필드명 | 타입 |
| --- | --- |
| post | ForeignKey(Post) |
| photo | imagekit.models.ProcessedImageField |

---

**Follow**

| 필드명 | 타입 |
| --- | --- |
| id | AutoField |
| user | ForeignKey(User) |
| follow | ForeignKey(User) |
| created | DateTimeField |

---

**Like**

| 필드명 | 타입 |
| --- | --- |
| post | ForeignKey(Post) |
| user | ForeignKey(User) |
| created | DateTimeField |

---

**Room**

| 필드명 | 타입 |
| --- | --- |
| name | Charfield |
| users | ManyToManyField(User) |

---
**Message**

| 필드명 | 타입 |
| --- | --- |
| room | ForeignKey(Room) |
| user | ForeignKey(User) |
| content | Charfield |
| timestamp | DateTimeField |

---