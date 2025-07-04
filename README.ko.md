<div align="right">
  <a href="README.md">English</a> |
  <a href="README.hi.md">हिंदी (Hindi)</a> |
  <a href="README.ko.md">한국어 (Korean)</a> |
  <a href="README.es.md">Español (Spanish)</a>
</div>

<p align="center">
  <img src="https://github.com/Shubhwithai/Sutra_Cookbooks/blob/main/images/SUTRA%20Cookbooks%20(1).svg" alt="SUTRA Banner" width="800"/>
</p>

<p align="center">
  <a href="https://developer.two.ai/"><img src="https://img.shields.io/badge/API-Active-success.svg" alt="API 상태"></a>
  <a href="https://docs.two.ai/"><img src="https://img.shields.io/badge/Docs-Available-blue.svg" alt="문서"></a>
  <a href="https://www.two.ai/sutra"><img src="https://img.shields.io/badge/Languages-50%2B-orange.svg" alt="언어"></a>
  <a href="https://x.com/sutra_dev"><img src="https://img.shields.io/twitter/follow/sutra_dev?style=social" alt="Twitter 팔로우"></a>
  <a href="https://discord.com/invite/NK9h6MFpxF"><img src="https://img.shields.io/badge/Discord-Join%20Us-7289DA?logo=discord&logoColor=white" alt="Discord"></a>
</p>

## 개요

SUTRA는 [TWO AI](https://www.two.ai)에서 개발한 대규모 다국어 언어 모델(LMLM) 제품군입니다. SUTRA의 이중 트랜스포머 아키텍처는 MoE(Mixture of Experts)와 Dense AI 언어 모델 접근 방식의 장점을 결합하여 50개 이상의 언어에 걸쳐 비용 효율적인 다국어 기능을 제공합니다.

## 이 저장소에서 찾을 수 있는 내용

| 섹션 | 설명 |
|---------|-------------|
| **Get Started** | 입문 튜토리얼, 기본 사용 패턴 및 설정 가이드 |
| **Multilingual** | SUTRA의 50개 이상 언어에 걸친 기능을 보여주는 코드 샘플 |
| **Integration Guides** | 인기 있는 프레임워크 및 도구와 SUTRA를 통합하는 지침 |
| **Chat with Data** | 지식 집약적 작업을 위한 검색 증강 생성(RAG) 예제 |
| **Agent Building** | 대화형 에이전트 및 어시스턴트 생성에 관한 튜토리얼 |
| **Starter Apps** | 개발을 빠르게 시작할 수 있는 사용 가능한 애플리케이션 템플릿 |
| **Examples** | 추가 코드 예제 및 구현 |

## Sutra 시작 가이드

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1j7B8mDIU8KMZ_IB-oaL_qLqXmWYYh0Xu)


## API 키 얻기

[TWO AI의 SUTRA API 페이지](https://developer.two.ai/)를 방문하여 API 키를 얻으세요.

⚠️ **보안 참고 사항:** API 키를 안전하게 보관하세요! 클라이언트 측 코드나 공개 저장소에 노출하지 마세요.

### API 엔드포인트

```
https://api.two.ai/v2/chat/completions
```

## 빠른 시작

### 샘플 코드

#### cURL

```bash
curl -X POST "https://api.two.ai/v2/chat/completions" \
  -H "Authorization: Bearer $SUTRA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept text/event-stream" \
  -d '{
  "model": "sutra-v2",
  "messages": [
    {"role": "user", "content": "화성에 대한 5개의 단락을 알려주세요"}
  ]
}'
```

#### Python

```python
import os
from openai import OpenAI

url = 'https://api.two.ai/v2'

client = OpenAI(base_url=url,
                api_key=os.environ.get("SUTRA_API_KEY"))

response = client.chat.completions.create(
    model='sutra-v2',
    messages=[{"role": "user", "content": "화성에 대한 5개의 단락을 알려주세요"}],
    max_tokens=1024,
    temperature=0
)

print(response.choices[0].message.content)
```

#### JavaScript/Node.js

```javascript
import { OpenAI } from 'openai';

async function testSutra() {
    const url = 'https://api.two.ai/v2';

    const client = new OpenAI({
        apiKey: process.env.SUTRA_API_KEY,
        baseURL: url,
    })

    const response = await client.chat.completions.create(
        {
            model: 'sutra-v2',
            messages: [{ role: 'user', content: '화성에 대한 5개의 단락을 알려주세요' }],
            max_tokens: 1024,
            temperature: 0
        }
    );

    console.log(response.choices[0].message.content);
}

(async () => { 
    await testSutra(); 
    process.exit(0); 
})();
```

## 특징

- **다국어 지원**: 50개 이상의 언어에 대한 기본 지원
- **OpenAI 호환 API**: 기존 OpenAI 기반 애플리케이션과 쉽게 통합
- **이중 트랜스포머 아키텍처**: MoE와 Dense AI 접근 방식의 장점 결합
- **높은 성능**: 다양한 사용 사례와 도메인에 최적화
- **스트리밍 지원**: 실시간 응답 스트리밍 기능

## 리소스

- 실시간 지원 및 토론을 위한 [Discord](https://discord.com/invite/NK9h6MFpxF) 커뮤니티에 가입하세요
- [Chat with SUTRA](https://chat.two.ai/)에서 대화하세요
- 업데이트를 위해 Twitter에서 [SUTRA](https://twitter.com/sutra_dev)를 팔로우하세요


## 지원 받기

- 자세한 정보는 [TWO AI 웹사이트](https://www.two.ai)를 방문하세요
- 연락처: hello@two.ai


### 비디오 튜토리얼

[![비디오 보기](https://img.youtube.com/vi/c_eKp1E48DE/maxresdefault.jpg)](https://www.youtube.com/watch?v=c_eKp1E48DE)

## 기여하기

SUTRA Cookbooks 저장소에 기여를 환영합니다! 기여하려면:

1. 저장소를 포크하고 클론하세요
2. 변경 사항을 위한 새 브랜치를 만드세요
3. 문서 표준에 따라 변경 사항을 만드세요
4. 예제를 철저히 테스트하세요
5. 풀 리퀘스트를 제출하세요

주요 변경 사항의 경우, 먼저 이슈를 열어 아이디어를 논의해 주세요.


## 법률

- [개인정보 보호정책](https://two.ai/legal/privacy)
- [서비스 약관](https://two.ai/legal/terms)

---

 2025 TWO AI | 모든 권리 보유
