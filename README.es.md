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
  <a href="https://www.two.ai/sutra/api"><img src="https://img.shields.io/badge/API-Active-success.svg" alt="Estado de API"></a>
  <a href="https://docs.two.ai/"><img src="https://img.shields.io/badge/Docs-Available-blue.svg" alt="Documentación"></a>
  <a href="https://www.two.ai/sutra"><img src="https://img.shields.io/badge/Languages-50%2B-orange.svg" alt="Idiomas"></a>
  <a href="https://x.com/sutra_dev"><img src="https://img.shields.io/twitter/follow/sutra_dev?style=social" alt="Seguir en Twitter"></a>
  <a href="https://discord.com/invite/NK9h6MFpxF"><img src="https://img.shields.io/badge/Discord-Join%20Us-7289DA?logo=discord&logoColor=white" alt="Discord"></a>
</p>

## Descripción General

SUTRA es una familia de modelos de lenguaje multilingües de gran escala (LMLM) desarrollados por [TWO AI](https://www.two.ai). La arquitectura de transformador dual de SUTRA extiende el poder de los enfoques de modelos de lenguaje MoE (Mixture of Experts) y Dense AI, ofreciendo capacidades multilingües rentables en más de 50 idiomas.

## Lo que Encontrarás en Este Repositorio

| Sección | Descripción |
|---------|-------------|
| **Get Started** | Tutoriales introductorios, patrones básicos de uso y guías de configuración |
| **Multilingual** | Ejemplos de código que muestran las capacidades de SUTRA en más de 50 idiomas |
| **Integration Guides** | Instrucciones para integrar SUTRA con marcos y herramientas populares |
| **Chat with Data** | Ejemplos de Generación Aumentada por Recuperación para tareas intensivas en conocimiento |
| **Agent Building** | Tutoriales sobre la creación de agentes conversacionales y asistentes |
| **Starter Apps** | Plantillas de aplicaciones listas para usar para impulsar tu desarrollo |
| **Examples** | Ejemplos de código adicionales e implementaciones |

## Guía de Inicio de Sutra

[![Abrir en Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1j7B8mDIU8KMZ_IB-oaL_qLqXmWYYh0Xu)


## Obtén Tu Clave API

Obtén tu clave API visitando la [página de API SUTRA de TWO AI](https://www.two.ai/sutra/api).

⚠️ **Nota de Seguridad:** ¡Mantén tu clave API segura! Nunca la expongas en código del lado del cliente o repositorios públicos.

### Punto de Acceso API

```
https://api.two.ai/v2/chat/completions
```

## Inicio Rápido

### Código de Ejemplo

#### cURL

```bash
curl -X POST "https://api.two.ai/v2/chat/completions" \
  -H "Authorization: Bearer $SUTRA_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept text/event-stream" \
  -d '{
  "model": "sutra-v2",
  "messages": [
    {"role": "user", "content": "Dame 5 párrafos sobre el planeta Marte"}
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
    messages=[{"role": "user", "content": "Dame 5 párrafos sobre el planeta Marte"}],
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
            messages: [{ role: 'user', content: 'Dame 5 párrafos sobre el planeta Marte' }],
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

## Características

- **Soporte Multilingüe**: Soporte integrado para más de 50 idiomas
- **API Compatible con OpenAI**: Fácil integración con aplicaciones existentes basadas en OpenAI
- **Arquitectura de Transformador Dual**: Combina el poder de los enfoques MoE y Dense AI
- **Alto Rendimiento**: Optimizado para diversos casos de uso y dominios
- **Soporte de Streaming**: Capacidades de streaming de respuestas en tiempo real

## Recursos

- Únete a nuestra comunidad de [Discord](https://discord.com/invite/NK9h6MFpxF) para soporte y discusiones en tiempo real
- Chatea con nosotros en [Chat with SUTRA](https://chat.two.ai/)
- Sigue a [SUTRA](https://twitter.com/sutra_dev) en Twitter para actualizaciones


## Obtener Soporte

- Visita el [sitio web de TWO AI](https://www.two.ai) para más información
- Contáctanos: hello@two.ai


### Tutorial en Video

[![Ver el video](https://img.youtube.com/vi/c_eKp1E48DE/maxresdefault.jpg)](https://www.youtube.com/watch?v=c_eKp1E48DE)

## Contribuir

¡Damos la bienvenida a contribuciones al repositorio SUTRA Cookbooks! Para contribuir:

1. Haz fork y clona el repositorio
2. Crea una nueva rama para tus cambios
3. Realiza tus cambios siguiendo nuestros estándares de documentación
4. Prueba tus ejemplos minuciosamente
5. Envía una solicitud de extracción

Para cambios importantes, por favor abre primero un issue para discutir tus ideas.


## Legal

- [Política de Privacidad](https://two.ai/legal/privacy)
- [Términos de Servicio](https://two.ai/legal/terms)

---

 2025 TWO AI | Todos los Derechos Reservados
