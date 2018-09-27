# -*- coding: utf-8 -*-
# Create your views here.
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from .forms import *
from .models import *
from .serializers import *
from django.http import JsonResponse
import logging
from . import nounx

noun_extractor = nounx.NounX()


logger = logging.getLogger('test')

# class JSONResponse(HttpResponse):
#     """
#     An HttpResponse that renders its content into JSON.
#     """
#     def __init__(self, data, **kwargs):
#         content = JSONRenderer().render(data)
#         kwargs['content_type'] = 'application/json'
#         super(JSONResponse, self).__init__(content, **kwargs)

"""
버전 테이블 뷰셋
버전 생성, 삭제, 업데이트, 리스트 가능
"""
class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

    def list(self, request, *args, **kwargs):
        result = {}
        version = Version.objects.get(osType='android')

        result['result'] = 200
        result['osType'] = version.osType
        result['version'] = version.version
        return JsonResponse(result)
"""
유저 테이블 뷰셋
회원가입
"""
class SignupViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    #parser_classes = (JSONParser)

    def create(self, request, *args, **kwargs):

        userForm = UserJoinForm(request.POST)
        result = {}
        idMultipleObject = True

        if userForm.is_valid():
            try:
                UserModel.objects.get(id=userForm.data['id'])
                idMultipleObject = False
                UserModel.objects.get(email=userForm.data['email'])
            except MultipleObjectsReturned as e:
                logger.error('join create error : ' + str(e))

                if idMultipleObject:
                    result['result'] = 411
                    result['message'] = 'id 중복'
                else:
                    result['result'] = 412
                    result['message'] = 'email 중복'

                return JsonResponse(result)
            except ObjectDoesNotExist:
                pass

            user = userForm.save()
            result['result'] = 200
            result['id'] = user.id
            result['password'] = user.password
            result['email'] = user.email
            result['gender'] = user.gender

            return JsonResponse(result)
        else:
            logger.error('user join error : ')
            result['result'] = 410
            result['message'] = 'input form error'
            return JsonResponse(result)


"""
유저 테이블 뷰셋
로그인
"""
class LoginViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        result = {}
        id = request.POST['id']
        password = request.POST['password']

        try:
            user = UserModel.objects.get(id=id, password=password)
        except ObjectDoesNotExist:
            #messages.add_message(request, messages.INFO, '아이디 또는 비밀번호가 틀렸습니다')
            result['result'] = 410
            result['message'] = '아이디 또는 비밀번호가 틀렸습니다'
            return JsonResponse(result)

        result['result'] = 200
        result['id'] = user.id
        result['password'] = user.password
        result['email'] = user.email
        return JsonResponse(result)


"""
카테고리 테이블 읽기전용 뷰셋
카테고리 읽기 가능
"""
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


"""
게시판 테이블 뷰셋
게시판 생성, 삭제, 업데이트, 리스트 가능
등록자만 생성, 업데이트, 삭제 가능
"""
class PostModelViewSet(viewsets.ModelViewSet):
    queryset = PostModel.objects.all()
    serializer_class = PostModelSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ('name','content',)

   
"""
댓글 테이블 뷰셋
"""
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    filter_fields = ('PostModel', 'content', 'user',)

"""
번역기 테이블 뷰셋
"""
class ChangeWordViewSet(viewsets.ModelViewSet):

    queryset = ChangeWordModel.objects.all()
    serializer_class = ChangeWordSerializer

    def create(self, request, *args, **kwargs):
        
        changeForm = ChangeWordForm(request.POST)
        result = {}

        dic = {'수도꼭지': '물꼭지', '연하다': '련하다', '원숭이': '원자', '육체': '륙체', '육체적': '륙체적', '이혼': '리혼', '잔디': '부사', '잔디밭': '부사밭', '여기': '녀기', '쪽': '머리쪽', '키보드': '자모건', '한밤': '정밤', '한밤중': '정밤', '개나리': '개나리꽃나무', '가끔': '가담가담', '가랑비': '안개비', '갈수': '구획가로수', '가르치다': '배워주다', '가발': '덧머리', '가위바위보': '가위주먹', '가정주부': '가두녀성', '각선미': '다리매', '간섭': '간참', '참견': '간참', '개고기': '단고기', '거스름돈': '각전', '거위': '게사니', '거짓말': '꽝포', '건널목': '철도건늠길', '건달': '날총각', '건망증': '잊음증', '검문소': '차단소', '게임': '껨', '견인차': '견인 운반차', '계단': '디대', '계모': '후어머니', '계집아이': '에미나이', '고종사촌': '고모사촌', '고함치다': '고아대다', '떠들다': '고아대다', '곡예': '교예', '골몰하다': '옴하다', '열중하다': '옴하다', '골밑 슛': '윤밑 던져 넣기', '골키퍼': '문지기', '공항': '항공역', '과일주': '우림술', '관광버스': '유람뻐스', '괜찮다': '괜치않다', '교도소': '교화소', '교미': '쌍붙이', '교점': '사귐점', '교탁': '강탁', '교통순경': '교통안전원', '교통경찰': '교통안전원', '구술시험': '구답시험', '국가 공무원': '국가 관리 일꾼', '공무원': '국가 관리 일꾼', '국가공무원': '국가 관리 일꾼', '국물': '마룩', '국민': '인민', '굳은살': '썩살', '굴착기': '기계삽', '궁리': '궁냥', '궐련': '마라초', '궤도': '자릿길', '그늘': '능쪽', '근방': '아근', '근처': '아근', '기르다': '자리우다', '기름지다': '노랑지다', '김매기': '김잡이', '꼭두새벽': '진새벽', '어둑새벽': '진새벽', '꾀병': '생병', '꿈나라': '꿈나락', '끼인각': '사이각', '남한': '남조선', '대한민국': '남조선', '한국': '남조선', '날씨': '일세', '네티즌': '망시민', '누리꾼': '망시민', '여자': '녀자', '노크': '손기척', '눌은밥': '가마치', '단무지': '겨절임', '달걀': '닭알', '대장': '굻은밸', '큰창자': '굵은밸', '대중가요': '군중가요', '덩크슛': '꽂아넣기', '데이터베이스': '자료묶음체계', '도넛': ' 가락지빵', '도시락': '곽밥', '돌기': '도드리', '돌풍': '갑작바람', '두통': '머리아픔', '드리블': '곱침', '들녘': '들옄', '라면': '꼬부랑 국수', '리듬 체조': '예술체조', '리듬체조': '예술체조', '리본': '댕기', '리본 체조': '댕기운동', '리본체조': '댕기 운동', '마네킹': '몸틀', '마라톤': '마라손', '마스카라': '눈썹먹', '만화': '이야기그림', '맞벌이 부부': '직장 세대', '맞벌이부 부': '직장 세대', '메리야스': '뜨게옷', '몽타주': '판조립', '뭊개': '색동다리', '뮤지컬': '가무이야기', '미소': '볼웃음', '미숙아': '달못찬아이', '미역국': '락제국', '밀썰물': '들날물', '바다표범': '물곰', '물범': '물곰', '반찬': '찔게', '발코니': '내 민대', '난간': '내민대', '배영': '누운 헤엄', '벌렁코': '발딱코', '벨트': '띠', '보푸라기': '보무라지', '보풀': '보무라지', ' 볶음밥': '기름밥', '볼펜': '원주필', '북한': '북조선', '한반도': '남북조선', '분유': '가루젓', '브래지어': '젖싸개', '빙수': ' 단얼음', '빨리': '날래', '삐삐': '주머니종', '상호': '호상', '선글라스': '채양안경', '셋방살이': '세방살이', '소꿉친구': '송아지 동무', '소등': '등불끄기', '소시지': '고기순대', '소파수술': '자궁강소파술', '소프라노': '녀성고음', '손자': '두벌자식', '수면제': '잠약', '수업': '상학', '수중발레': '예술헤염', '수화': '손가락말', '숨바꼭질': '숨을내기', '편두통': '쪽머리아픔', '평영': '가슴헤염', '표준어': '문화어', '프리킥': '벌차기', '피망': '사자고추', '필통': '연필갑', '한글': '조선글', '한약': ' 동약', '할머니': '할머니', '할아버지': '할아버지', '함박웃음': '함박꽃웃음', '합병증': '따라난병', '햄버거': '고기겹빵', '허들': '장애틀', '헌시': '드림시', '헬리콥터': '직승비행기', '혼잣말': '혼자말', '화들짝': '파들짝', '화장실': '위생실', '횡단로': '건늠길', '횡단도': '건늠길', '휴대 전화': '무선대화기', '휴대전화': '무선대화기', '이': '리', '유월': '류월', '골': '꼴', '노인': '로인', '영어': '령어', '바르다': '발그다', '막': '무대면막', '초': '초가락', '줄': '줄쇠', '집안': '집내', '죽이다': '해제끼다', '위': '우', '논리': '론리', '시각': '보는각', '내일': '래일', '수단': '백단', '이익': '리익', '논문': '론문', '혹시': '혹은', '양': '량', '이외': '리외', '외치다': '웨치다', '고장': '헛배부르기', '고르다': '고루다', '맡기다': '위하다', '상대방': '대방', '시골': '주곡', '연구하다': '년구하다', '라디오': '라지오', '금방': '가지', '남쪽': '앞쪽', '색깔': '색갈', '요리': '료리', '늘리다': '늘이다', '무릎': '근지부', '이용': '리용', '지난달': '간달', '올바르다': '옳바르다', '뛰어나다': '뛰여나다', '수도': '유도', '역': '력', '때리다': '쌔리다', '볶다': '닦다', '과학자': '과학가', '연기': '년기', '상처': '자병', '지하철': '지철', '현': '소리줄', '이어': '리어', '동료': '동참', '부족': '부아족', '달리다': '딸리다', '이러다': '이리다', '종': '장곡', '통합': '문장론적통합', '양식': '량식', '예전': '례전', '전기': '뎐기', '궁금하다': '궁겁다', '둘러싸다': '돌아싸다', '보도': '걸음길', '약하다': '략하다', '이쪽': '이켠', '행복하다': '복하다', '굽다': '구불다', '연습': '련습', '식량': '량료', '용기': '룡기', '정상': '정포', '화장품': '화장료', '내년': '래년', '이사': '니사', '화제': '그림제목', '물가': '물역', '압력': '압', '차량': '바곤', '약': '략', '구역': '구계', '아이고': '아이구', '생각나다': '생각히우다', '인상': '끌어올리기', '차갑다': '차겁다', '태아': '태아이', '드디어': '드디여', '여인': '녀인', '표': '빌레트', '싸다': '쌀다', '양파': '둥글파', '이상': '리상', '타다': '타개다', '가지': '가지나무', '어제': '물고기길구조물', '호랑이': '호랑', '영양': '령양', '초콜릿': '쵸콜레트', '감': '감새', '깨어지다': '깨여지다', '녹음하다': '록음하다', '마사지': '문지르기', '먹히다': ' 먹히우다', '비': '비틀자루', '사투리': '토배기사투리', '수저': '수저가락', '여대생': '녀대학생', '연기하 다': '련기하다', '외할머니': '외조할머니', '음악가': '악가', '이롭다': '리롭다', '입사': '립사', '제삿날': '제사날', '주름살': '살주름', '찻잔': '차잔', '칫솔': '이솔', '과거': '과업', '녹음': '록음', '빗방울': '비방울', '손뼉': '손벽', '저녁때': '주석', '지폐': '지표', '한데': '한지', '낚싯대': '낚시대', ' 냇물': '내물', '뛰어나오다': '뛰여나오다', '로터리': '로타리', '부잣집': '부자집', '상추': '부루', '씻기다': '씻기우다', '양배추': '가두배추', '여왕': '녀왕', '연기되다': '련기되다', '읽히다': '읽히우다', '초저녁': '아시저녁', '낚시꾼': '낚시군', '데려오다': '데리다', '속마음': '내속', '위아래': '우아래', '이발소': '리발소', '재작년': '재래년', '전구': '전기알', '코스모스': '길국화', '킬로': '키로', '페인트': '살짝공', '꽃씨': '꽃씨앗', '난방': '란방', '녹화': '록화', '농구': '롱구', '뒷골목': '뒤골목', '얼리다': '얼구다', '원피스': '달린옷', '이민': '리민', '이성': '다름성', '이혼하다': '리혼하다', '졸리다': '졸리우다', '졸음': '졸암', '한평생': '한당대', '무지개': '빛고리', '볼링': '보링경기', '인도': '덕성', '구': '문장론적구', '늦가을': '마가을', '지하 도': '건늠굴길', '튀김': '튀기', '미역': '해곽', '소포': '알쌈', '수영장': '헤염장', '작은아버지': '삼촌아버지', '장갑': '수갑', '냉면': '랭면', '비빔밥': '교반', '외할아버지': '외조할아버지', '요리하다': '료리하다', '체육관': '경기관', '칼국수': '밀제비국', '연락처': '련락처', '연세': '년세', '녹차': '푸른차', '독감': '독감기', '스케이트': '스케트', '노랫소리': '노래소리', '뒷문': '뒤문', '배꼽': '배구멍', '놀이터': '놀음터', '답장': '회안서', '무': '무우', '아랫사람': '아래사람', '영남': '령남', '지방': '방외', '팩시밀리': '자료전화', '고구마': '번서', '밥맛': '쌀구미', '배우자': '짝씨', '수입품': '입구품', '안': '아낙', '안부': '산안장부', '양주': '량주', '수': '수범주', '나': '라', '등': '잔등', '때': '까리', '속': '아낙', '원': '온', '그러다': '그리다', '좀': '좀벌레', '시간': '전점', '돈': '천원지방', '여성': '녀성', '지역': '구역', '길': '저고리지게', '그때': '그시', '교육': '격몽', '역사': '력사', '이제': '리제', '너무': '지내', '연구': '련구', '이유': '리유', '상황': '뽕나무혹버섯', '이후': '이래', '머리': '소리표머리', '이용하다': '리용하다', '곧': '선즉', '이거': '리거', '현상': '깨우기', '끝': '그망', '조사': '실꼬치', '영화': '령화', '하늘': '건상', '교수': '목매달기', '술': '술실', '고개': '목고개', '아내': '안해', '우선': '바른돌이', '바': '빠', '기관': '기줄', '입장': '립장', '예': '례', '방식': '삭음막이', '갑자기': '갑작', '마을': '마실', '노래': '로래', '노력': '로력', '모으다': '모두다', '이해하다': '리해하다', '옷': '의거', '전쟁': '병전', '노동': '로동', '발': '렴자', '은행': '저금소', '소설': '작은혀', '아기': '애기', '마지막': '마그막', '벌이다': '벌리다', '주로': '주장', '어른': '자란이', '차례': '아준위', '재산': '자화', '이념': '리념', '돌': '돌증', '성': '상', '불리다': '불구다', '땀': '뜸', '머릿속': '머리속', '마음속': '안가슴', '연결되다': '련결되다', '헤어지다': '헤여지다', '구입하다': '입구입하다', '시점': '눈점', '의사': '가짜죽음', '코드': '코드실', '온통': '전탕', '후춧가루': '후추가루', '연락': '련락', '정': '정대', '건너다': '건느다', '뛰어들다': '뛰여들다', '요금': '료금', '전자': '선자', '거칠다': '거치르다', '역사가': '력사가', '줄기': '줄금', '연결하다': '련결하다', '주머니': '패낭', '인연': '연인', '바위': '돌바위', '절반': '반판', '풍경': '바람종', '섞이다': '섞이우다', '이틀': '이발뼈', '예절': '례절', '부처': '중부처', '이마': '액', '청소': '청결', '햇살': '해살', '벗기다': '벗기우다', '서클': '써클단', '절': '범가', '양쪽': '량쪽', '예컨대': '례컨대', '운동장': '운동마당', '터뜨리다': '터치다', '영상': '령상', '영혼': '령혼', '잠깐': '잠간', '곳곳': '방방', '달려오다': '달아오다', '비교': '비김', '역사적': '력사적', '열차': '렬차', '정식': '온식', '즉시': '직시', '깔리다': '깔리우다', '연합': '련합', '장': '장군말', '논': '논구뎅이', '별': '별꽃', '잠기다': '잠기우다', '경고': '굳은고약', '논쟁': '론쟁', '뇌': '뢰', '손바닥': '손장심', '줍다': '줏다', '아무렇다': '아뭏다', '이용되다': '리용되다', '임시': '림시', '통': '세층', '두껍다': '두텁다', '유학': '류학', '농담': '롱담', '인': '린', '조각': '조박', '해석': '해석적증명법', '기차': '철차', '햇빛': '해빛', '논의하다': '론의하다', '바닷가': '바다가', '거꾸로': '곤두', '날짜': '날자', '아유': '아이유', '눈썹': '눈섭', '비율': '비률', '양국': '량국', '털': '털갗', '꺾다': '분지르다', '테이프': '테프', '품': '로동품', '연말': '년말', '줄곧': '줄창', '계좌': '돈자리', '당기다': '땅기다', '부자': '천금', '서쪽': '서켠', '일찍이': '일찌기', '자율': '자률', '천장': '천정', '화가': '그림버티개', '엉덩이': '엉뎅이', '전부': '전고', '질병': '와병', '각기': '각약', '귀신': '귀것', '나뭇가지': '나무가지', '무덤': '분굴', '밥상': '식안', '예외': '례외', '유리': '류리', '쥐': '쥐살', '팔리다': '팔리우다', '나침반': '라침기', '문장': '글토막', '여학생': '녀학생', '예방': '례방', '유리하다': '류리하다', '코스': '경주선', '날리다': '날리우다', '냉장고': '랭장고', '당근': '다홍무', '뛰어넘다': '뛰여넘다', '연속': '련속', '유물': '류물', '지난번': '간번', '판': '패', '화분': '가루씨', '배다': '배이다', '안쪽': '안녘', '전날': '간날', '흉내': '내', '결혼식': '례식', '계산기': '계산기계', '세다': '헤다', '애인': '어른님', '애초': '애저녁', '초반': '기초바닥', '파': '화', '헤매다': '헤매이다', '버터': '빠다', '뽑히다': '뽑히우다', '인근': '린근', '정기': '정패', '토마토': '도마도', '빛깔': '빛갈', '사방': '사군데', '유행': '류행', '이내': '인차', '부탁': '촉', '얼음': '얼음살', '쫓기다': '쫓기우다', '해안': '기슭바다', '갇히다': '갇히우다', '몸짓': '몸세', '스튜디오': '스타디오', '이상적': '리상적', '주방': '부엌방', '곤란하다': '곤난하다', '기대다': '기대이다', '깨어나다': '깨여나다', '먹이': '이료', '발레': '발레무용', '염려': '념려', '관광객': '관광자', '구별하다': '갈라보다', '미술관': '미술박물관', '반성': '반각', '소수': '씨수', '시어머니': '아고', '시집': '시가집', '연간': '년간', '조정': '물스키배', '그립다': '그리웁다', '논하다': '론하다', '동부': '넉줄당콩', '만만하다': '만문하다', '엿보다': '여수다', '유적': '류적', '잡아먹다': '해제끼다', '취향': '추향', '튀다': '튕기다', '머리카락': '머리오리', '시멘트': '세멘트', '양심': '량심', '이사장': '리사장', '이자': '리자', '지난날': '간날', '튀어나오다': '튀여나다', '도둑': '밤사람', '속이다': '떠넘기다', '수면': '물얼굴', '연락하다': '련락하다', '예의': '례의', '임금': '로력값', '냉동': '랭동', '녹다': '록다', '센터': '중심공격수', '승객': '차객', '여권': '녀권', '잠자리': '잘자리', '저마다': '저마끔', '포도주': '포도술', '화재': '그림감', '노선': '로선', '달려들다': '달아들다', '묶이다': '묶이우다', '유형': '류형', '청소하다': '청결하다', '넘어뜨리다': '넘어치다', '마찰': '쓸림', '쌍둥이': '쌍동이', '영하': '령하', '웬만하다': '웬간하다', '유행하다': '류행하다', '테러': '테로', '휴일': '휴식날', '달력': '력서장', '두께': '두터이', '시나리오': '영화문학', '신문지': '신문장', '용': '룡', '마스크': '얼굴가리개', '만장일치': '전원일치', '말다툼': '입다툼', '맞벌이 세대': '직장 세대', '매우 다급하다': '급해맞다', '맷돌': '망돌', '메어꽂다': '메여꼰지다', '멜빵': '멜바', '멜빵바지': '멜끈바지', '명란젓': '알밥젓', '멸균': '균깡그리죽이기', '명암': '검밝기', '모눈종이': '채눈종이', '모자이크': '쪽무늬그림', '목돈': '주먹돈', '묘책': '묘득', '무대 막': '주름막', '무상 교육': '면비교육', '무상교육': '면비교육', '무선 호출기': '주머니종', '무심결': '무중', '무안을 당하다': '꼴을 먹다', '문맹자': '글장님', '오리발': '발가락사이막', '물개': '바다개', '물에 만 밥': '무랍', '뭉게구름': '더미구름', '미풍': '가능바람', '미혼모': '해방처녀', '민간인': '사회사람', '민속놀이': '민간오락', '밑줄': '아래줄', '바로 정면으로': '면바로', '정면으로': '면바로', '박살나다': '박산나다', '반격': '반타격', '반딧불이': '물벌레', '반죽음': '얼죽음', '반환점': '돌아오는점', '방부제': '냄새막이약', '방음벽': '소리막이벽', '방직공장': '직포공장', '방화벽': '불막이벽', '배낭': '멜가방', '배드민턴': '바드민톤', '배수': '곱절수', '배웅하 다': '냄내다', '들창코': '발딱코', '벌집': '벌둥지', '베란다': '내민층대', '베어링': '축받치개', '벼락부자': '갑작부자', '벼 타작': '벼바심', '변태': '모습갈이', ' 보름달': '동근달', '보온성': '따슴성', '보온재': '열막이감', '보조개': '오목샘', '보증 수표': '지불행표', '보증수표': '지불행표', '보트': '젓기배', '복어': '보가지', '볶음밥': '기름밥', '부릅뜨다': '흡뜨다', '부산을 피우다': '설레발을 치다', '불도저': '평토기', '블라우스': '양복적삼', '비석': '비돌', '비염': '코염', '비중': '견줌무게', '빙설': '얼음눈', ' 빼아닮다': '먹고닮다', '호출기': '주머니종', '숙소': '초대소', '순환도로': '륜환도로', '스카이 라운지': '전망식당', '스카이라운지': '전망식당', '스카프': '목수건', '스커트': '양복치마', '스크랩북': '오림책', '스킨 로션': ' 살물결', '스타킹': '하루살이 양말', '스타 플레이어': '기둥선수', '스타플레이어': ' 기둥선수', '스튜어디스': '비행안내원', '스파이크': '순간타격', '슬리퍼': '끌신', ' 승려': '중선생', '승무': '중춤', '시동생': '적은이', '시디 플레이어': '레이자전축', '시디플레이어': '레이자전축', '시럽': '단물약', '시집간 딸': '집난이', '시집간딸': '집난이', '식혜': '밥감주', '신기록 보유자': '체육명수', '신기록보유자': '체육명수', '실격': '자격잃기', '실내화': '방안신', '싱크대': '가시대', '잔돈': '부스럭돈', '쓸개': '열주머니', '스킨로션': '살결물', '화장수': '살결물', '스트레이트': '곧추치기', '스프레이': '뿌무개', '분무기': '뿌무개', '분무': '뿌무개', '시범학교': '시험학교', '식단': '료리차림표', '차림표': '료리차림표', '요리차림표': '료리차림표', '개수대': '가시대', '설거지대': '가시대', '아리송하다': '새리새리하다', '아이스크림': '얼음보숭이', '안전벨트': '비행안전띠', '앞니': '앞이', '어묵': '튀긴고기떡', '에스컬레이터': '계단승강기', '자동계단': '계단승강기', '영역': '령역', '오페라': '가극물', '오프사이드': '공격어김', '외래어': '들어온말', '외래 어': '굳어진말', '우울증': '슬픔증', '우유': '소젖', '유모차': '애기차', '아기차': '애기차', '인터넷 검색': '망유람', '인터넷검색': '망유람', ' 자유형': '뺄헤염', '작은창자': '가는밸', '장난감': '놀이감', '장모': '가시어머니', '장인': '가시아버지', '접영': '나비헤염', '젤리': '단묵', '종착역': '마감역', '주민등록증': '공민증', '주차장': '차마당', '주스': '과일단물', '줄자': '타래자', '창자': '밸', '채소': '남새', '청력': '들을힘', '초등학교': '인 민학교', '출입문': '나들문', '치통': '이쏘기', '카스텔라': '설기과자', '컴퓨터': '전자계산기', '코너킥': '구석차기', '키워드': '열쇠단어', '타 임아웃': '분간휴식', '탁아소': '애기궁전', '토막글': '글토막', '토안': '눈알나오기', '투수': '넣는사람', '파스텔': '그림분필', '판다': '고양이곰', '판독기': '읽기장치', '페널티킥': '십일메터벌차기', '열정': '렬정', '추석': '추수절', '녹색': '록색', '벼': '나락', '쓸쓸하다': '서겁다', '이중': '리중', '목록': '등록부', '스위치': '전기여닫개', '연결': '련결', '연관': '련관', '육군': '륙군', '인분': '린분', '닫히다': '닫기다', '막걸리': '탁배기', '밀리다': '밀리우다', '예방하다': '례방하다', '유의하다': '류의하다', '이해되다': '리해되다', '잘리다': '잘리우다', '한순간': '한순', '가사': '가짜죽음', '넉넉하다': '두텁다', '밑바닥': '하바닥', '어쩌다': '어째다', '여': '녀', '연령': '년령', '예비': '례비', '이력서': '경력서', '퍽': '팍', '풍속': '바람속도', '한층': '한물', '난리': '란리', '열기': '렬기', '하룻밤': '하루밤', '빗물': '비물', '사위': '서랑자', '캠페인': '깜빠니야', '햇볕': '해볕', '건네다': '건늬다', '나뭇잎': '나무잎', '발자국': '발자욱', '뱉다': '배앝다', '소화': '불끄기', '연애': '련애', '내외': '내우', '중년': '중', '구입': '입구입', '꾸리다': '꿍지다', '낭비': '람비', '도리어': '됩다', '사상': '넘기기', '사춘기': '춘정기', '서점': '서쪽점', '수필': '붓떼기', '쓰다듬다': '얼쓸다', '알루미늄': '늄', '양말': '량말', '여우': '녀우', '잡아당기다': '잡아다리다', '낙엽': '락엽', '논리적': '론리적', '동창': '언상처', '두리번거리다': '두릿거리다', '맞은편': '맞은켠', '어젯밤': '어제밤', '여관': '녀관', '연습하다': '련습하다', '유산': '류산', '이따금': '가담가담', '하반기': '하반년', '힘겹다': '힘겨웁다', '감수성': '감수력', '건너편': '건넌편', '매': '응자', '냇물': '내물', '지하도': '건늠굴길', '육': '륙', '세탁소': '빨래집', '냉방': '랭방', '눈병': '눈앓이', '작은어머니': '삼촌어머니', '복사기': '복사촬영기', '내후년': '래후년', '육십': '륙십'}

        if changeForm.is_valid():

            user_sentence = changeForm['original_sentence']

            sentence = [ \
                u'' + user_sentence.value() + '', \
            ]

            for s in sentence:
                sentence = sentence[0]
                
                unicode_string2 = s.encode('utf8', 'ignore')
                unicode_string = unicode_string2.decode('utf-8')
                
                for n in noun_extractor.extract_noun(s):
                    utf8_string = n.encode('utf8', 'ignore')

                    unicode_string = utf8_string.decode('utf-8')
                    
                    try:
                        sentence = sentence.replace(unicode_string, dic[unicode_string])
                    except:
                        pass    

            

            def checkTrait(c):
                return (int((ord(c) - 0xAC00) % 28) != 0)

            res = ''
            for index, s in enumerate(sentence):
                if(s == "을" and checkTrait(sentence[index-1]) == False):
                    sentence = sentence[:index] + '를' + sentence[index+1:]
                if(s == "를" and checkTrait(sentence[index-1]) == True):
                    sentence = sentence[:index] + '을' + sentence[index+1:]
            res += sentence

            print(res)

            result['result'] = 200
            result['sentence'] = res.encode().decode()
            result['message'] = 'success'
                
           
            return JsonResponse(result)

            # except:
            #     result['result'] = 410
            #     result['sentence'] = "0"
            #     result['message'] = 'error'

            #     print(result)

            #     return JsonResponse(result)
