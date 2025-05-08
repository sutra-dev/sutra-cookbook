
<div align="right">
  <a href="README.md">English</a> |
  <a href="README.hi.md">हिंदी (Hindi)</a>
</div>

<p align="center">
  <img src="https://github.com/Shubhwithai/Sutra_Cookbooks/blob/main/images/SUTRA%20Cookbooks%20(1).svg" alt="SUTRA Banner" width="800"/>
</p>

<p align="center">
  <a href="https://www.two.ai/sutra/api"><img src="https://img.shields.io/badge/API-Active-success.svg" alt="API Status"></a>
  <a href="https://docs.two.ai/version-2/docs/get-started-with-sutra"><img src="https://img.shields.io/badge/Docs-Available-blue.svg" alt="Documentation"></a>
  <a href="https://www.two.ai/sutra"><img src="https://img.shields.io/badge/Languages-50%2B-orange.svg" alt="Languages"></a>
  <a href="https://twitter.com/two_platforms"><img src="https://img.shields.io/twitter/follow/two_platforms?style=social" alt="Twitter Follow"></a>
  <a href="https://discord.gg/NjWD9GEm"><img src="https://img.shields.io/badge/Discord-Join%20Us-7289DA?logo=discord&logoColor=white" alt="Discord"></a>
</p>

## अवलोकन

SUTRA बड़े बहुभाषी भाषा मॉडल्स (LMLMs) का एक परिवार है जिसे [TWO AI](https://www.two.ai) द्वारा विकसित किया गया है। SUTRA की द्विगुणी-ट्रांसफॉर्मर आर्किटेक्चर MoE (एक्सपर्ट्स का मिश्रण) और डेंस AI भाषा मॉडल दृष्टिकोणों दोनों की शक्ति का विस्तार करती है, जो 50+ भाषाओं में लागत-कुशल बहुभाषी क्षमताएं प्रदान करती है।

## इस कुकबुक में आपको क्या मिलेगा

| अनुभाग | विवरण |
|---------|-------------|
| **आरंभ करें** | परिचयात्मक ट्यूटोरियल, बुनियादी उपयोग पैटर्न, और सेटअप गाइड |
| **बहुभाषी** | 50+ भाषाओं में SUTRA की क्षमताओं को प्रदर्शित करने वाले कोड नमूने |
| **एकीकरण गाइड** | लोकप्रिय फ्रेमवर्क और टूल के साथ SUTRA को एकीकृत करने के लिए निर्देश |
| **डेटा के साथ चैट** | ज्ञान-गहन कार्यों के लिए पुनर्प्राप्ति-संवर्धित जनरेशन उदाहरण |
| **एजेंट निर्माण** | संवादात्मक एजेंट और सहायकों को बनाने पर ट्यूटोरियल |
| **उपयोग के मामले** | उद्योग-विशिष्ट अनुप्रयोग और समाधान |
| **स्टार्टर ऐप्स** | आपके विकास को शुरू करने के लिए उपयोग के लिए तैयार एप्लिकेशन टेम्प्लेट |
| **उदाहरण** | अतिरिक्त कोड उदाहरण और कार्यान्वयन |

## सूत्र स्टार्टर गाइड

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1j7B8mDIU8KMZ_IB-oaL_qLqXmWYYh0Xu)

## अपनी API कुंजी प्राप्त करें

[TWO AI की SUTRA API पेज](https://www.two.ai/sutra/api) पर जाकर अपनी API कुंजी प्राप्त करें।

⚠️ **सुरक्षा नोट:** अपनी API कुंजी को सुरक्षित रखें! इसे कभी भी क्लाइंट-साइड कोड या सार्वजनिक रिपॉजिटरी में उजागर न करें।

### API एंडपॉइंट

```
https://api.two.ai/v2/chat/completions
```

## त्वरित आरंभ

### नमूना कोड

#### cURL

```bash
curl -X POST "https://api.two.ai/v2/chat/completions" \
  -H "Authorization: Bearer $SUTRA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept text/event-stream" \
  -d '{
  "model": "sutra-v2",
  "messages": [
    {"role": "user", "content": "मुझे मंगल ग्रह के बारे में 5 पैराग्राफ दीजिए"}
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
    messages=[{"role": "user", "content": "मुझे मंगल ग्रह के बारे में 5 पैराग्राफ दीजिए"}],
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
            messages: [{ role: 'user', content: 'मुझे मंगल ग्रह के बारे में 5 पैराग्राफ दीजिए' }],
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

## विशेषताएं

- **बहुभाषी समर्थन**: 50+ भाषाओं के लिए अंतर्निहित समर्थन
- **OpenAI-संगत API**: मौजूदा OpenAI-आधारित अनुप्रयोगों के साथ आसान एकीकरण
- **द्विगुणी-ट्रांसफॉर्मर आर्किटेक्चर**: MoE और डेंस AI दृष्टिकोणों की शक्ति को जोड़ता है
- **उच्च प्रदर्शन**: विभिन्न उपयोग मामलों और डोमेन के लिए अनुकूलित
- **स्ट्रीमिंग समर्थन**: रीयल-टाइम प्रतिक्रिया स्ट्रीमिंग क्षमताएं

## संसाधन

- [API संदर्भ](https://docs.two.ai/version-2/docs/get-started-with-sutra)
- [Hugging Face पर SUTRA टोकनाइज़र](https://huggingface.co/spaces/TWO/sutra-tokenizer-comparison)
- [नमूना अनुप्रयोग](https://github.com/sutra-dev)

## सहायता प्राप्त करना

- अपडेट के लिए Twitter पर [@two_platforms](https://twitter.com/two_platforms) का अनुसरण करें
- अधिक जानकारी के लिए [TWO AI की वेबसाइट](https://www.two.ai) पर जाएँ

## योगदान

हम SUTRA Cookbooks रिपॉजिटरी में योगदान का स्वागत करते हैं! योगदान करने के लिए:

1. रिपॉजिटरी को फोर्क करें और क्लोन करें
2. अपने परिवर्तनों के लिए एक नई शाखा बनाएँ
3. हमारे दस्तावेज़ीकरण मानकों का पालन करते हुए अपने परिवर्तन करें
4. अपने उदाहरणों का पूरी तरह से परीक्षण करें
5. पुल अनुरोध सबमिट करें

बड़े परिवर्तनों के लिए, कृपया पहले अपने विचारों पर चर्चा करने के लिए एक इश्यू खोलें।

## कानूनी

- [गोपनीयता नीति](https://two.ai/legal/privacy)
- [सेवा की शर्तें](https://two.ai/legal/terms)

---

 2025 TWO AI | सर्वाधिकार सुरक्षित
