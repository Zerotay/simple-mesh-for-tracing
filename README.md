# 개요
서비스 메시 환경에서 중첩된 트래픽을 발생시킬 수 있는 서버.  


기껏 트레이싱하는데 기왕이면 여러 서버를 거치는 트레이스를 간단하게 확인할 방법이 있으면 좋겠다고 생각했다.  
그러다가 떠오른 생각이, 순전히 메시 내부에서 트레이싱을 위해 가동되는 테스트 서버가 있으면 좋겠다 싶었다.  
가령 `http://a/b/c`라고 요청을 보내면 a 서버가 요청을 받아서 이걸 `http://b/c`로 보내고, b 서버는 이걸 또 `http://c`로 보내는 방식으로 간단하게 url에 설정만 하는 것으로 트래픽을 마구 포워딩할 수 있는 테스트 환경을 구축하면, 트레이싱을 확인하는데 매우 유용할 것이다.  
## 간단 정리  
클러스터에서 활용할 수 있는 단일 웹 서버 바이너리를 개발한다.  
이 웹 서버들은 클러스터 내에서 고유한 네트워크 식별자를 통해 접근할 수 있으며, 이를 기반으로 서버 간 통신을 할 수 있다.  
# 핵심 기능 정의  
- 사용자는 임의의 웹서버에 임의의 서브패스를 넣어 요청을 날릴 수 있다.  
- 웹서버는 요청을 받고 서브패스의 값을 추출하여 자신이 요청을 날려야할 후속 웹 서버를 결정한다.  
	- 후속 웹 서버에 요청을 날리고, 돌아온 응답을 합쳐서 자신의 응답에 반영한다.  
- 서브패스에 더 이상 값이 없다면 웹서버는 바로 응답을 반환한다.  
- 웹서버는 `~`를 구분자로 자신이 요청을 날릴 웹 서버를 구분하여 복수의 요청을 날릴 수 있다.  

![image](https://github.com/user-attachments/assets/ffb9ee2b-02b6-4735-9b1b-88ce26b6576a)  
간단하게 사용자의 요청의 예시 플로우를 그려보았다.  
- `A/B~C/D`로 요청을 날리면 A서버로 요청이 날아간다.  
- A서버는 서브 패스로 `B~C/D`를 읽어내고, 여기에서 `~`를 구분자로 사용해 B와 C서버 후속 요청을 날린다.  
- B, C 서버는 다시금 서브 패스로 D를 받기 때문에 또 D에 요청을 날린다.  

url을 기반으로 그냥 후속 서버에 추가 요청을 날릴 수 있다면, 원하는 대로 서버를 띄우고 해당 서버끼리 통신을 하게 하는 트래픽을 매우 쉽게 만들어낼 수 있다.  
위 예시에서는 4개의 서버를 두었지만 서버를 얼마든지 늘려도 되고, 서버 간 트래픽이 순환하게 하는 것도 가능하다.  
## 추가 기능  
몇 가지 기능을 추가적으로 생각하고 정리해두었다.    
실제 기능 구현을 한 것도 있고, 안 한 것도 있다.  
- 환경 변수로 설정 주입(구현)  
	- 서버의 주소, 포트 등의 값을 컨테이너 환경 변수로 넣고 이를 기반으로 서버의 설정을 커스텀할 수 있다.  
- 일정 시간 지연 발생(구현)  
- 비동기 요청(미구현)   
	- 병렬적인 요청을 비동기로도 세팅할 수 있도록 한다.  
	- 사실 이 부분은 구체화가 안 된 것이, 처음에는 쿼리 파라미터로 전체 흐름을 세팅할 수 있게 할까 하다 말았다.  
- 헬름 세팅(미구현)  
	- 한 서버를 추가할 때마다 비슷한 양식을 반복적으로 작성해야 하는데, 아예 차트로 템플릿화시켜 세팅을 더 간편하게 할 수 있도록 한다.  
- 경로 상세 설정(미구현)  
	- 현재의 기능은 일방향적으로 작성하는데, 요청 분기가 일어나는 지점이 있으면 후속 서버는 분기된 서버마다 요청을 받게 된다.  
	- 좀 더 DAG 그래프를 자유롭게 만들 수 있도록 하는 url 세팅 방법이 당장 생각나지 않아 진행하지 않았다.  
# 개발  
![image.png](https://841lgfvhej.execute-api.ap-northeast-2.amazonaws.com/default/image?url=https://gist.githubusercontent.com/Zerotay/4ea4c657d8e35399250405e7fa7d56a9/raw/image.png)  
개발은 매우 단순하게 진행했다.  
[[uv]]를 이용해 환경 세팅을 하고 FastAPI로 서버를 구성했다.  
![image.png](https://841lgfvhej.execute-api.ap-northeast-2.amazonaws.com/default/image?url=https://gist.githubusercontent.com/Zerotay/3ccdf549f97acf866e322fcdeebca404/raw/image.png)  
모든 서버는 요청을 처리할 때 자신의 호스트 값, 그리고 자신이 요청을 처리하는데 걸린 시간을 응답으로 반환한다.  
환경 변수로 지연 시간이 전달되면 해당 값만큼 시간이 지연되도록 돼있다.  
![image.png](https://841lgfvhej.execute-api.ap-northeast-2.amazonaws.com/default/image?url=https://gist.githubusercontent.com/Zerotay/8350b41891d283b597efdf54ed1db908/raw/image.png)  
후속 서버로 간 요청은 `next_node` 필드에 담겨 결과적으로 처음 요청을 날린 클라이언트는 모든 서버의 요청을 받아볼 수 있게 된다.  

![image.png](https://841lgfvhej.execute-api.ap-northeast-2.amazonaws.com/default/image?url=https://gist.githubusercontent.com/Zerotay/4f364cd5ca53593c0174764c406d8181/raw/image.png)  
환경 변수에서 값을 받아오는 코드는 이렇게 생겼다.  
비동기 처리를 하려고 추가한 변수도 있는데, 실제로 사용하지는 않았다.  

![image.png](https://841lgfvhej.execute-api.ap-northeast-2.amazonaws.com/default/image?url=https://gist.githubusercontent.com/Zerotay/21913aa3a60ccbd4b2ffd0529290606b/raw/image.png)  
추가적으로 조금이나마 활용해먹을 상황이 있을 것 같아서 프로메테우스 메트릭 계측 라이브러리를 세팅했다.  


# 테스트

![image.png](https://841lgfvhej.execute-api.ap-northeast-2.amazonaws.com/default/image?url=https://gist.githubusercontent.com/Zerotay/074e0350cc674eb9c68bd4171b8701f1/raw/image.png)  
나는 a,b,c 서비스를 세우고 요청을 날려보았다.  
a는 0.5초, b는 1초, c는 1.5초의 지연이 발생하도록 세팅돼있다.  
그래서 합산한 값이 그대로 표시되는 것을 확인할 수 있다.  
![image.png](https://841lgfvhej.execute-api.ap-northeast-2.amazonaws.com/default/image?url=https://gist.githubusercontent.com/Zerotay/71d29bad971bcc206ee644eebf318d4c/raw/image.png)  
참고로 로그는 이런 식으로 남았다.  
fastapi에서 로그 설정하는 방법이 잘 기억이 안 나서 대충 세팅하니 내 커스텀 로그랑 겹쳐서 보이고 있다.  
아무튼 일단 자신의 호스트 정보를 남기고, 어디로 트래픽을 보내야 할지 명시한다.  
