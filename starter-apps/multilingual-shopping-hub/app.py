import streamlit as st
import requests
import json
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
from langchain.callbacks.base import BaseCallbackHandler

# Page configuration
st.set_page_config(
    page_title="Multilingual Shopping Hub",
    page_icon="🛍️",
    layout="wide"
)

# Define supported languages
languages = [
    "English", "Hindi", "Gujarati", "Bengali", "Tamil", 
    "Telugu", "Kannada", "Malayalam", "Punjabi", "Marathi", 
    "Urdu", "Assamese", "Odia", "Sanskrit", "Korean", 
    "Japanese", "Arabic", "French", "German", "Spanish", 
    "Portuguese", "Russian", "Chinese", "Vietnamese", "Thai", 
    "Indonesian", "Turkish", "Polish", "Ukrainian", "Dutch", 
    "Italian", "Greek", "Hebrew", "Persian", "Swedish", 
    "Norwegian", "Danish", "Finnish", "Czech", "Hungarian", 
    "Romanian", "Bulgarian", "Croatian", "Serbian", "Slovak", 
    "Slovenian", "Estonian", "Latvian", "Lithuanian", "Malay", 
    "Tagalog", "Swahili"
]

def get_stars(rating):
    full_stars = int(rating)
    half_star = rating % 1 >= 0.5
    empty_stars = 5 - full_stars - (1 if half_star else 0)
    
    stars = "★" * full_stars
    if half_star:
        stars += "⯨"
    stars += "☆" * empty_stars
    
    return stars

# Streaming callback handler for Sutra LLM
class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text
        self.run_id_ignore_token = None
    
    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)

# Initialize the ChatOpenAI model - base instance for caching
@st.cache_resource
def get_base_chat_model(api_key):
    return ChatOpenAI(
        api_key=api_key,
        base_url="https://api.two.ai/v2",
        model="sutra-v2",
        temperature=0.3,  # Lower temperature for more accurate translations
    )

# Function to fetch high-quality image using Serper Images API
def fetch_high_quality_image(query):
    url = "https://google.serper.dev/images"
    payload = json.dumps({
        "q": query,
        "num": 1  # We only need one image
    })
    headers = {
        'X-API-KEY': st.session_state.serper_api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()
        results = response.json()
        if results.get("images") and len(results["images"]) > 0:
            return results["images"][0].get("imageUrl")
        return None
    except Exception as e:
        st.warning(f"Error fetching high-quality image: {str(e)}")
        return None

# Function to fetch products using Serper API
def fetch_products(query, num_results=20, page=1):
    url = "https://google.serper.dev/shopping"
    payload = {
        "q": query,
        "num": num_results,  # Use the user's preferred number of results
        "page": page
    }
    
    payload = json.dumps(payload)
    headers = {
        'X-API-KEY': st.session_state.serper_api_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        response.raise_for_status()
        results = response.json()
        products = results.get("shopping", [])
        
        # Enhance products with high-quality images
        enhanced_products = []
        for item in products:
            # Try to get a high-quality image based on the title
            high_quality_image = fetch_high_quality_image(item.get('title', ''))
            if high_quality_image:
                item['imageUrl'] = high_quality_image
            enhanced_products.append(item)
        
        return enhanced_products
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching products: {str(e)}")
        return []

# Function to translate products using Sutra LLM
def translate_products(products, target_language, api_key):
    try:
        # Get base model (non-streaming) for translation
        model = get_base_chat_model(api_key)
        
        # Create a container for all products
        products_container = st.container()
        
        # Process each product individually
        translated_items = []
        for i, item in enumerate(products):
            # Store original image URL
            original_image_url = item.get('imageUrl')
            
            # Create a specific prompt for each product
            system_message = f"""
            You are a professional translator specializing in product translation. Translate the following product content to {target_language}.
            
            Translation Rules:
            1. Translate ONLY these fields:
               - title: Keep it concise and product-focused
               - source: Translate the store name if it has a common translation
               - delivery: Translate shipping information
            
            2. Translation Guidelines:
               - Ensure natural and fluent language
               - Maintain the original meaning and context
               - Keep any brand names, sizes, and product codes in their original form
               - Preserve any numbers, prices, and measurements
               - Keep any technical terms accurate
            
            3. Return ONLY the translated fields in this exact format:
            {{
                "title": "translated title",
                "source": "translated source",
                "delivery": "translated delivery"
            }}
            
            4. Important:
               - Do not add any explanations
               - Do not modify the JSON structure
               - Do not translate any other fields
               - Ensure the translation is culturally appropriate for {target_language} speakers
            """
            
            # Prepare only the fields that need translation
            fields_to_translate = {
                "title": item.get('title', ''),
                "source": item.get('source', ''),
                "delivery": item.get('delivery', '')
            }
            
            # Convert to JSON string
            item_json = json.dumps(fields_to_translate, ensure_ascii=False)
            
            # Generate response
            messages = [
                HumanMessage(content=f"{system_message}\n\nFields to translate:\n{item_json}")
            ]
            
            try:
                # Show processing status
                with st.spinner(f"Translating product {i+1} of {len(products)}..."):
                    response = model.invoke(messages)
                    result = response.content.strip()
                    
                    # Clean the response
                    result = result.replace('```json', '').replace('```', '').strip()
                    
                    # Parse the translated fields
                    translated_fields = json.loads(result)
                    
                    # Create new item with translated fields and original data
                    translated_item = {
                        **item,  # Keep all original fields
                        "title": translated_fields.get('title', item.get('title', '')),
                        "source": translated_fields.get('source', item.get('source', '')),
                        "delivery": translated_fields.get('delivery', item.get('delivery', '')),
                        "imageUrl": original_image_url  # Ensure original image is kept
                    }
                    
                    translated_items.append(translated_item)
                    
                    # Display the translated product with improved layout
                    with products_container:
                        rating_stars = get_stars(float(translated_item.get('rating', 0))) if translated_item.get('rating') else ""
                        st.markdown(f"""
                            <div class="product-card">
                                <div style="display: flex; gap: 20px;">
                                    <div style="flex: 3;">
                                        <h3 class="product-title">{i+1}. {translated_item['title']}</h3>
                                        <p class="product-info">🏪 <strong>Store:</strong> {translated_item['source']}</p>
                                        <p class="product-price">💰 <strong>Price:</strong> {translated_item['price']}</p>
                                        <p class="product-delivery">🚚 <strong>Delivery:</strong> {translated_item['delivery']}</p>
                                        {f'<p class="product-rating"><span class="stars">{rating_stars}</span> <strong>Rating:</strong> {translated_item["rating"]} ({translated_item.get("ratingCount", 0)} reviews)</p>' if translated_item.get('rating') else ''}
                                        <p><a href="{translated_item['link']}" class="product-link" target="_blank">🛒 View Product</a></p>
                                    </div>
                                    <div style="flex: 2;">
                                        <div class="image-container">
                                            <img src="{translated_item['imageUrl']}" alt="Product Image">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
            except json.JSONDecodeError as e:
                st.warning(f"Failed to parse translation of item {i+1}: {str(e)}. Using original.")
                translated_items.append(item)
            except Exception as e:
                st.warning(f"Error translating item {i+1}: {str(e)}. Using original.")
                translated_items.append(item)
        
        return translated_items
            
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return products

# Function to translate search query to English using Sutra LLM
def translate_query_to_english(query, api_key):
    try:
        # Get base model (non-streaming) for translation
        model = get_base_chat_model(api_key)
        
        system_message = """
        You are a professional translator specializing in product search queries. Translate the following search query to English.
        
        Translation Rules:
        1. Keep the translation concise and clear
        2. Maintain the search intent and product-related terminology
        3. Preserve any proper nouns (names, places)
        4. Keep any numbers, dates, and measurements
        5. Ensure the translation is natural and search-friendly
        6. For technical terms and product names, use standard English terminology
        7. If the query is already in English, return it as is
        
        Return ONLY the translated query without any explanations or additional text.
        """
        
        messages = [
            HumanMessage(content=f"{system_message}\n\nQuery to translate:\n{query}")
        ]
        
        response = model.invoke(messages)
        translated_query = response.content.strip()
        
        # Log the translation for debugging
        st.write(f"Debug - Original query: {query}")
        st.write(f"Debug - Translated query: {translated_query}")
        
        return translated_query
        
    except Exception as e:
        st.error(f"Error translating query: {str(e)}")
        st.warning("Using original query as fallback.")
        return query

# Initialize session state variables
if "serper_api_key" not in st.session_state:
    st.session_state.serper_api_key = ""
if "sutra_api_key" not in st.session_state:
    st.session_state.sutra_api_key = ""
if "products_data" not in st.session_state:
    st.session_state.products_data = []
if "search_query" not in st.session_state:
    st.session_state.search_query = "nike shoes"
if "num_results" not in st.session_state:
    st.session_state.num_results = 20  # Default value
if "min_price" not in st.session_state:
    st.session_state.min_price = 0
if "max_price" not in st.session_state:
    st.session_state.max_price = 1000

# Sidebar for settings
with st.sidebar:
    st.markdown(
        f'<h1>🛍️ Shopping Hub</h1>',
        unsafe_allow_html=True
    )
    
    # API Key sections
    st.markdown("### API Keys")
    st.markdown("**Serper API**")
    serper_api_key = st.text_input("Enter your Serper API Key:", 
                                   value=st.session_state.serper_api_key,
                                   type="password",
                                   label_visibility="collapsed")
    if serper_api_key:
        st.session_state.serper_api_key = serper_api_key
    
    st.markdown("**Sutra API**")
    st.markdown("Get your free API key from [SUTRA API](https://www.two.ai/sutra/api)")
    sutra_api_key = st.text_input("Enter your Sutra API Key:", 
                                  value=st.session_state.sutra_api_key,
                                  type="password",
                                  label_visibility="collapsed")
    if sutra_api_key:
        st.session_state.sutra_api_key = sutra_api_key
    
    # Number of results selector
    st.markdown("### Search Settings")
    num_results = st.slider("Number of products to display:", 
                           min_value=5, 
                           max_value=30, 
                           value=st.session_state.num_results, 
                           step=5,
                           help="Select how many products you want to see")
    st.session_state.num_results = num_results  # Store the user's preference
    
    # Price range selector
    st.markdown("### Price Range")
    col1, col2 = st.columns(2)
    with col1:
        min_price = st.number_input("Min Price ($)", 
                                  min_value=0, 
                                  max_value=10000, 
                                  value=st.session_state.min_price,
                                  step=10,
                                  help="Minimum price in dollars")
    with col2:
        max_price = st.number_input("Max Price ($)", 
                                  min_value=0, 
                                  max_value=10000, 
                                  value=st.session_state.max_price,
                                  step=10,
                                  help="Maximum price in dollars")
    
    # Update session state with price range
    st.session_state.min_price = min_price
    st.session_state.max_price = max_price
    
    # Language selector
    st.markdown("### Language Settings")
    selected_language = st.selectbox("Select language:", languages)
    
    st.divider()
    st.markdown(f"Currently viewing products in: **{selected_language}**")
    st.markdown(f"Price range: **${min_price} - ${max_price}**")
    
    # About section
    with st.expander("About Multilingual Shopping Hub"):
        st.markdown("""
        This app uses:
        - **Serper API** to fetch product information from around the world
        - **Sutra LLM** to translate product details into 50+ languages
        - **Streamlit** for the interactive web interface
        
        Search for any product and get details in your preferred language!
        """)

# Main content area
st.markdown(
    f'<h1><img src="https://framerusercontent.com/images/9vH8BcjXKRcC5OrSfkohhSyDgX0.png" width="60" style="vertical-align: middle;"/> Multilingual Shopping Hub <img src="https://img.pikbest.com/png-images/20191028/little-boy-pushing-a-shopping-cart-to-buy-things-gif_2515305.png!bw700" width="90" height="90" style="vertical-align: middle;"/></h1>',
    unsafe_allow_html=True
)

# Search bar
col1, col2 = st.columns([4, 1])
with col1:
    search_query = st.text_input("Search for products:", value=st.session_state.search_query)
with col2:
    search_button = st.button("Search", type="primary", use_container_width=True)

# Validate API keys before searching
if search_button or (not st.session_state.products_data and st.session_state.serper_api_key):
    if not st.session_state.serper_api_key:
        st.error("Please enter your Serper API key in the sidebar.")
    else:
        st.session_state.search_query = search_query
        
        # Translate query to English if needed
        if selected_language != "English" and st.session_state.sutra_api_key:
            with st.spinner("Translating search query to English..."):
                english_query = translate_query_to_english(search_query, st.session_state.sutra_api_key)
                if english_query != search_query:  # Only show if translation actually happened
                    st.info(f"Translated query: '{english_query}'")
        else:
            english_query = search_query
        
        # Show loading message
        with st.spinner(f"Fetching products for '{english_query}'..."):
            # Fetch products data
            products = fetch_products(
                query=english_query,
                num_results=st.session_state.num_results  # Use the stored user preference
            )
            
            if products:
                st.session_state.products_data = products
                st.success(f"Found {len(products)} products!")
            else:
                st.warning("No products found. Try a different search term.")

# Function to filter products by price
def filter_products_by_price(products, min_price, max_price):
    filtered_products = []
    for product in products:
        try:
            # Extract price from the price string (e.g., "$100.00" -> 100.00)
            price_str = product.get('price', '')
            if price_str:
                # Remove currency symbol and any text, keep only numbers
                price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_str)))
                if min_price <= price <= max_price:
                    filtered_products.append(product)
        except (ValueError, TypeError):
            continue
    return filtered_products

# Display products content
if st.session_state.products_data:
    # Filter products by price
    filtered_products = filter_products_by_price(
        st.session_state.products_data,
        st.session_state.min_price,
        st.session_state.max_price
    )
    
    if not filtered_products:
        st.warning(f"No products found in the price range ${st.session_state.min_price} - ${st.session_state.max_price}")
    else:
        # Check if translation is needed
        if selected_language != "English" and st.session_state.sutra_api_key:
            with st.spinner(f"Translating products to {selected_language}..."):
                translated_products = translate_products(
                    filtered_products, 
                    selected_language,
                    st.session_state.sutra_api_key
                )
        else:
            # Display English products (or show message if Sutra API key is missing)
            if selected_language != "English" and not st.session_state.sutra_api_key:
                st.warning("Please enter your Sutra API key in the sidebar to translate products.")
            
            # Format and display the original products with improved layout
            products_container = st.container()
            for i, product in enumerate(filtered_products):
                rating_stars = get_stars(float(product.get('rating', 0))) if product.get('rating') else ""
                st.markdown(f"""
                    <div class="product-card">
                        <div style="display: flex; gap: 20px;">
                            <div style="flex: 3;">
                                <h3 class="product-title">{i+1}. {product.get('title', 'No Title')}</h3>
                                <p class="product-info">🏪 <strong>Store:</strong> {product.get('source', 'Unknown')}</p>
                                <p class="product-price">💰 <strong>Price:</strong> {product.get('price', 'Price not available')}</p>
                                <p class="product-delivery">🚚 <strong>Delivery:</strong> {product.get('delivery', 'Delivery info not available')}</p>
                                {f'<p class="product-rating"><span class="stars">{rating_stars}</span> <strong>Rating:</strong> {product["rating"]} ({product.get("ratingCount", 0)} reviews)</p>' if product.get('rating') else ''}
                                <p><a href="{product.get('link', '#')}" class="product-link" target="_blank">🛒 View Product</a></p>
                            </div>
                            <div style="flex: 2;">
                                <div class="image-container">
                                    <img src="{product.get('imageUrl')}" alt="Product Image">
                                </div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
else:
    if not st.session_state.serper_api_key:
        st.info("Enter your Serper API key and search for products to get started.")
    else:
        st.info("No product data available. Try searching for a product.")

# Add custom CSS for product cards
st.markdown("""
    <style>
    /* Theme-aware styles */
    .product-card {
        background-color: var(--background-color);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid var(--border-color);
    }
    .product-title {
        color: var(--text-color);
        font-size: 1.5em;
        margin-bottom: 10px;
    }
    .product-info {
        color: var(--text-color-secondary);
        font-size: 1.1em;
        margin: 5px 0;
    }
    .product-price {
        color: var(--accent-color);
        font-size: 1.3em;
        font-weight: bold;
    }
    .product-rating {
        color: var(--text-color-secondary);
        font-size: 1.1em;
    }
    .product-delivery {
        color: var(--link-color);
        font-size: 1.1em;
    }
    .product-link {
        color: var(--link-color);
        text-decoration: none;
        font-weight: bold;
    }
    .product-link:hover {
        color: var(--link-hover-color);
        text-decoration: underline;
    }
    .image-container {
        height: 250px;
        overflow: hidden;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid var(--border-color);
    }
    .image-container img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .stars {
        color: #FFD700;  /* Gold color for stars */
        font-size: 1.2em;
        letter-spacing: 2px;
    }

    /* Light theme variables */
    [data-theme="light"] {
        --background-color: #ffffff;
        --text-color: #1f1f1f;
        --text-color-secondary: #4a4a4a;
        --border-color: #e0e0e0;
        --accent-color: #2e7d32;
        --rating-color: #f57c00;
        --link-color: #1565c0;
        --link-hover-color: #0d47a1;
    }

    /* Dark theme variables */
    [data-theme="dark"] {
        --background-color: #262730;
        --text-color: #ffffff;
        --text-color-secondary: #e0e0e0;
        --border-color: #3e3e3e;
        --accent-color: #4caf50;
        --rating-color: #ffb74d;
        --link-color: #90caf9;
        --link-hover-color: #42a5f5;
    }

    /* Additional theme-aware improvements */
    .stMarkdown {
        color: var(--text-color);
    }
    .stMarkdown strong {
        color: var(--text-color);
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: var(--text-color);
    }
    .stMarkdown a {
        color: var(--link-color);
    }
    .stMarkdown a:hover {
        color: var(--link-hover-color);
    }

    /* Ensure proper contrast for all text elements */
    .stTextInput > div > div > input {
        color: var(--text-color);
        background-color: var(--background-color);
    }
    .stSelectbox > div > div > select {
        color: var(--text-color);
        background-color: var(--background-color);
    }
    .stSlider > div > div > div {
        color: var(--text-color);
    }
    </style>
    """, unsafe_allow_html=True) 