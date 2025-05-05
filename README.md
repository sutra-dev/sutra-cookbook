# SUTRA COOKBOOK by TWO AI

<div align="right">
  <a href="README.md">English</a> |
  <a href="README.hi.md">हिंदी (Hindi)</a>
</div>

<p align="center">
  <img src="https://github.com/Shubhwithai/Sutra_Cookbooks/blob/main/images/logo-.png" alt="TWO AI Logo" width="400"/>
</p>

[![API Status](https://img.shields.io/badge/API-Active-success.svg)](https://www.two.ai/sutra/api)
[![Documentation](https://img.shields.io/badge/Docs-Available-blue.svg)](https://docs.two.ai/version-2/docs/get-started-with-sutra)
[![Languages](https://img.shields.io/badge/Languages-50%2B-orange.svg)](https://www.two.ai/sutra)
[![Twitter Follow](https://img.shields.io/twitter/follow/two_platforms?style=social)](https://twitter.com/two_platforms)

## Overview

SUTRA is a family of large multi-lingual language models (LMLMs) developed by [TWO AI](https://www.two.ai). SUTRA's dual-transformer architecture extends the power of both MoE (Mixture of Experts) and Dense AI language model approaches, delivering cost-efficient multilingual capabilities across 50+ languages.

## What You'll Find in This Cookbook

| Section | Description |
|---------|-------------|
| **Get Started** | Introductory tutorials, basic usage patterns, and setup guides |
| **Multilingual** | Code samples showcasing SUTRA's capabilities across 50+ languages |
| **Integration Guides** | Instructions for integrating SUTRA with popular frameworks and tools |
| **Chat with Data** | Retrieval-Augmented Generation examples for knowledge-intensive tasks |
| **Agent Building** | Tutorials on creating conversational agents and assistants |
| **Starter Apps** | Ready-to-use application templates to jumpstart your development |
| **Examples** | Additional code examples and implementations |

## Sutra Starter Guide

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1j7B8mDIU8KMZ_IB-oaL_qLqXmWYYh0Xu)

## Get Your API Key

Get your API key by visiting [TWO AI's SUTRA API page](https://www.two.ai/sutra/api).


### API Endpoint

```
https://api.two.ai/v2/chat/completions
```

## Quick Start

### Sample Code

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

## Features

- **Multilingual Support**: Built-in support for 50+ languages
- **OpenAI-compatible API**: Easy integration with existing OpenAI-based applications
- **Dual-transformer Architecture**: Combines the power of MoE and Dense AI approaches
- **High Performance**: Optimized for various use cases and domains
- **Streaming Support**: Real-time response streaming capabilities

## Resources

- [API Reference](https://docs.two.ai/version-2/docs/get-started-with-sutra)
- [SUTRA Tokenizer on Hugging Face](https://huggingface.co/spaces/TWO/sutra-tokenizer-comparison)
- [Sample Applications](https://github.com/sutra-dev)

## Getting Support

- Follow [@two_platforms](https://twitter.com/two_platforms) on Twitter for updates
- Visit [TWO AI's website](https://www.two.ai) for more information

## Contributing

We welcome contributions to the SUTRA Cookbooks repository! To contribute:

1. Fork and clone the repository
2. Create a new branch for your changes
3. Make your changes following our documentation standards
4. Test your examples thoroughly
5. Submit a pull request

For major changes, please open an issue first to discuss your ideas.

## Legal

- [Privacy Policy](https://two.ai/legal/privacy)
- [Terms of Service](https://two.ai/legal/terms)

---

 2025 TWO AI | All Rights Reserved
