# 18-1st-baemin-store-backend
18기 김택향, 18기 안다민

## 배민_스토어 1차 프로젝트 Back-end 소개

- 국내 최대 배달앱에서 만든 소품샵 [배민문방구](https://store.baemin.com/) 모티브 프로젝트
- 짧은 프로젝트 기간동안 개발에 집중해야 하므로 디자인/기획 부분만 모티브로 제작했습니다.
- 개발은 초기 세팅부터 전부 직접 구현했으며 프론트앤드와 연결하여 실제 사용할 수 있는 서비스 수준으로 개발한 것입니다.

### 개발 인원 및 기간

- 개발기간 : 2021/3/15~ 2021/3/26
- 개발 인원 : 프론트엔드 3명, 백엔드 2명
- [백엔드 github 링크](https://github.com/wecode-bootcamp-korea/18-1st-baemin-store-backend)

### 프로젝트 선정이유

- 이 사이트는 커머스 사이트로 사용자 중심의 인터페이스를 갖추고 있어 직관적으로 되어 있습니다. 또한 재밌는 상품을 판매하는만큼 메인 페이지도 자동 움직임 가능한 메인이 장식되어 있어 재미를 줍니다.
백엔드 관점에서 볼 때는 다양한 커머스 상품들과 대/중분류 된 카테고리 별 상품을 데이터베이스로 관리해볼 수 있고, 각 상품마다 옵션이 있어 옵션마다 변경되는 데이터 출력 로직이 흥미롭게 다가왔습니다.

<br>
## 적용 기술 및 구현 기능

### 적용 기술

> - Back-End : Python, Django web framework, Bcrypt, , JWT, Transaction, MySQL
> - Common : AWS(EC2,RDS), RESTful API

### 구현 기능

#### 일반 로그인(내가 한 부분 : '로그인' 기능 담당)

- 회원가입 / 로그인 각각 api 호출하여 구현 
- 정규표현식 이용하여 유저가 입력한 데이터 유효성 검증 
- JWT 토큰 발행하여 인가 로직 구현


#### 메인페이지

- 잘 나가요, 새로 나왔어요, 지금은 할인중 구현 
- 잘나가요(상품 판매순) / 새로 나왔어요(상품 등록순) / 지금 할인중(할인 상품 필터링) 등 다양한 필터링 조건 구현
- 그 외 전체 / 상품 카테고리별 api 구현

#### 상품 상세 페이지(내가 한 부분 : 상품 상세 정보 출력)

- 상품 상세 페이지 입력 및 출력 각각 api 호출하여 구현 : 책, 물건에 따른 상품상세설명 변경(if문 활용)
- 상품에 조건을 주는 것과 조건이 없는 것(옵션) 차이에 따른 로직 미세 조정(수량 등)

#### 장바구니
- order_status를 구현하여 장바구니의 상태를 주문과 함꼐 관리
- 장바구니에 추가된 상품에서 선택하여 구매하는 로직 구현

#### 찜하기 (내가 한 부분)
- get_or_create 이용하여 유저가 찜한 상품이 중복될 경우 개수만 올라갈 수 있도록 로직 구현하는 api 구현

#### 쿠폰 (내가 한 부분)

- 쿠폰을 만들고 만든 쿠폰이 원하는 만큼의 리스트화 된 서브 카테고리에 모두 적용될 수 있는 api 구현
- 이를 통해 유저가 결제창에서 쿠폰이 얼마나 있든 그 서브 카테고리에 연결된 쿠폰만 나와서 결제에 적용할 수 있는 api로 구현.


#### 데이터 입력 및 배포
- csv 파일 제작 후 api 구성하여 데이터 한 번에 입력
- AWS 배포 통한 데이터베이스 배포 완료

### 3차 기업협업 이후 리팩토리 예정

#### 상품구매 후 리뷰 및 상품 후기 구현
- 구매 상품에 한하여 리뷰 및 상품후기를 등록할 수 있는 api 구축

#### 더 많은 브랜치 활용하여 프론트엔드와 협업

#### 검색 기능 api 구축

#### 주문 시 주문을 관리할 수 있는 주문번호 기능 추가

#### 마이페이지 구축
- 회원 정보 변경 api 추가
- 1:1 문의 게시판 api 추가
- 배송지 관리 api 추가

<br>

## Reference

- 이 프로젝트는 [배민문방구](https://store.baemin.com/) 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
- 이 프로젝트에서 사용하고 있는 사진 대부분은 위코드에서 구매한 것이므로 해당 프로젝트 외부인이 사용할 수 없습니다.
