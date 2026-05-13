"""
seed_data.py — Populates the SLIB Finder database with all 306 API entries.

Usage:
    cd backend
    python seed_data.py

Safe to run multiple times — skips entries that already exist.
All entries have ALL fields filled so cards show "✓ Complete".
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, ApiEntry

# ── All API entries ───────────────────────────────────────────────────────────
# Format: (name, category, description, version, developer,
#          language, framework, cost, latency, scalability,
#          design_pattern, risk_level, sample_code)

SEED_DATA = [

    # ── PAYMENTS (15 entries) ─────────────────────────────────────────────────
    # Payment gateways and processing APIs for online and in-person transactions.
    # Covers global providers (Stripe, PayPal, Adyen), regional (Razorpay, Paytm),
    # and BNPL solutions (Klarna). All use REST with Paid/Premium pricing.
    ("Stripe API", "Payments",
     "Payment processing API for online businesses. Supports cards, wallets, and subscriptions.",
     "v1", "stripe", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const stripe = require('stripe')('sk_test_key');\nconst charge = await stripe.charges.create({\n  amount: 2000,\n  currency: 'usd',\n  source: 'tok_visa',\n});"),

    ("PayPal REST API", "Payments",
     "PayPal's REST API for accepting payments, managing transactions, and issuing refunds.",
     "v2", "paypal", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const paypal = require('@paypal/checkout-server-sdk');\nconst request = new paypal.orders.OrdersCreateRequest();\nrequest.requestBody({ intent: 'CAPTURE', purchase_units: [{ amount: { currency_code: 'USD', value: '10.00' } }] });"),

    ("Braintree API", "Payments",
     "Braintree payment gateway API supporting cards, PayPal, Venmo, and more.",
     "v1", "braintree", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const braintree = require('braintree');\nconst gateway = new braintree.BraintreeGateway({ environment: braintree.Environment.Sandbox });"),

    ("Square API", "Payments",
     "Square's API for payments, inventory, and point-of-sale integrations.",
     "v2", "square", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Client } = require('square');\nconst client = new Client({ accessToken: 'YOUR_TOKEN' });"),

    ("Razorpay API", "Payments",
     "India's leading payment gateway API for accepting online payments.",
     "v1", "razorpay", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const Razorpay = require('razorpay');\nconst instance = new Razorpay({ key_id: 'YOUR_KEY', key_secret: 'YOUR_SECRET' });"),

    ("Adyen API", "Payments",
     "Global payment platform API supporting 250+ payment methods and real-time data.",
     "v68", "adyen", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const { Client, Config, CheckoutAPI } = require('@adyen/api-library');\nconst config = new Config();\nconfig.apiKey = 'YOUR_API_KEY';\nconst client = new Client({ config });\nconst checkout = new CheckoutAPI(client);"),

    ("Mollie API", "Payments",
     "European payment gateway API supporting iDEAL, credit cards, and more.",
     "v2", "mollie", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const { createMollieClient } = require('@mollie/api-client');\nconst mollieClient = createMollieClient({ apiKey: 'test_xxxx' });\nconst payment = await mollieClient.payments.create({ amount: { currency: 'EUR', value: '10.00' }, description: 'Order' });"),

    ("Payoneer API", "Payments",
     "Global payment platform for cross-border payments and mass payouts.",
     "v4", "payoneer", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst response = await axios.post('https://api.payoneer.com/v4/programs/{program_id}/payees', { payee_id: 'id123' }, { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    ("Checkout.com API", "Payments",
     "Unified payment API for accepting online and in-person payments globally.",
     "v3", "checkout", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const { Checkout } = require('checkout-sdk-node');\nconst cko = new Checkout('YOUR_SECRET_KEY');\nconst payment = await cko.payments.request({ source: { type: 'card', number: '4242424242424242' }, currency: 'USD', amount: 1000 });"),

    ("PayU API", "Payments",
     "Payment gateway API for emerging markets including India, Latin America, and CEE.",
     "v2", "payu", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const crypto = require('crypto');\nconst hash = crypto.createHash('sha512').update(`${key}|${txnid}|${amount}|${productinfo}|${firstname}|${email}|||||||||||${salt}`).digest('hex');"),

    ("Klarna API", "Payments",
     "Buy now pay later API for e-commerce with flexible payment options.",
     "v1", "klarna", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst session = await axios.post('https://api.klarna.com/payments/v1/sessions', { purchase_country: 'US', purchase_currency: 'USD', order_amount: 10000, order_lines: [{ name: 'Product', quantity: 1, unit_price: 10000 }] });"),

    ("WePay API", "Payments",
     "Integrated payments API for platforms and marketplaces.",
     "v3", "wepay", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst account = await axios.post('https://api.wepay.com/v3/accounts', { name: 'My Store', description: 'Store payments' }, { headers: { 'App-Id': 'YOUR_APP_ID', 'App-Token': 'YOUR_TOKEN' } });"),

    ("Helcim API", "Payments",
     "Payment processing API with transparent pricing for small businesses.",
     "v2", "helcim", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst charge = await axios.post('https://api.helcim.com/v2/payment/purchase', { paymentType: 'purchase', amount: 100.00, currency: 'USD', cardData: { cardNumber: '4111111111111111' } }, { headers: { 'api-token': 'YOUR_TOKEN' } });"),

    ("Worldpay API", "Payments",
     "Global payment processing API for merchants and enterprises.",
     "v1", "worldpay", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst order = await axios.post('https://api.worldpay.com/v1/orders', { token: 'YOUR_TOKEN', orderDescription: 'My Order', amount: 1999, currencyCode: 'GBP' });"),

    ("Paytm API", "Payments",
     "India's leading digital payments API with UPI, wallet, and card support.",
     "v1", "paytm", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const PaytmChecksum = require('paytmchecksum');\nconst params = { MID: 'YOUR_MID', ORDER_ID: 'order123', CUST_ID: 'cust123', CHANNEL_ID: 'WEB', TXN_AMOUNT: '100.00', CURRENCY: 'INR', WEBSITE: 'WEBSTAGING', CALLBACK_URL: 'https://example.com/callback' };\nconst checksum = await PaytmChecksum.generateSignature(params, 'YOUR_MERCHANT_KEY');"),

    # ── AUTHENTICATION (15 entries) ───────────────────────────────────────────
    # Identity and access management APIs for user authentication and authorization.
    # Covers OAuth2/OIDC platforms (Auth0, Okta), passwordless (Magic, Stytch),
    # enterprise SSO (WorkOS, Ping Identity), and open source (Keycloak).
    ("Auth0 API", "Authentication",
     "Authentication and authorization platform with OAuth2, OIDC, and SAML support.",
     "v2", "auth0", "Multi-language", "REST", "Freemium", "Low", "High", "OAuth2", "Low",
     "const { auth } = require('express-openid-connect');\napp.use(auth({ issuerBaseURL: 'https://YOUR_DOMAIN.auth0.com' }));"),

    ("Firebase Authentication", "Authentication",
     "Google Firebase authentication supporting email, social logins, and phone auth.",
     "v1", "google", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { getAuth, signInWithEmailAndPassword } from 'firebase/auth';\nconst auth = getAuth();\nawait signInWithEmailAndPassword(auth, email, password);"),

    ("Okta API", "Authentication",
     "Enterprise identity management API with SSO, MFA, and lifecycle management.",
     "v1", "okta", "Multi-language", "REST", "Paid/Premium", "Low", "High", "OAuth2", "Low",
     "const { OktaAuth } = require('@okta/okta-auth-js');\nconst authClient = new OktaAuth({ issuer: 'https://YOUR_DOMAIN.okta.com/oauth2/default' });"),

    ("Clerk API", "Authentication",
     "Modern authentication API with drop-in UI components for React and Next.js.",
     "v1", "clerk", "JavaScript", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { ClerkProvider, SignIn } from '@clerk/nextjs';\nexport default function App() {\n  return <ClerkProvider><SignIn /></ClerkProvider>;\n}"),

    ("AWS Cognito", "Authentication",
     "Amazon's user authentication service with user pools and federated identities.",
     "v1", "amazon", "Multi-language", "REST", "Freemium", "Low", "High", "OAuth2", "Low",
     "import { CognitoUserPool } from 'amazon-cognito-identity-js';\nconst userPool = new CognitoUserPool({ UserPoolId: 'us-east-1_xxx', ClientId: 'xxx' });"),

    ("Keycloak API", "Authentication",
     "Open source identity and access management API with SSO and OAuth2.",
     "v21", "redhat", "Multi-language", "REST", "Open Source", "Low", "High", "OAuth2", "Low",
     "const axios = require('axios');\nconst token = await axios.post('http://localhost:8080/realms/myrealm/protocol/openid-connect/token', new URLSearchParams({ client_id: 'myclient', username: 'user', password: 'pass', grant_type: 'password' }));"),

    ("Supabase Auth", "Authentication",
     "Open source Firebase alternative with built-in authentication and row-level security.",
     "v2", "supabase", "JavaScript", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { createClient } from '@supabase/supabase-js';\nconst supabase = createClient('YOUR_URL', 'YOUR_KEY');\nconst { data, error } = await supabase.auth.signInWithPassword({ email: 'user@example.com', password: 'password' });"),

    ("OneLogin API", "Authentication",
     "Cloud-based identity management API with SSO and MFA capabilities.",
     "v2", "onelogin", "Multi-language", "REST", "Paid/Premium", "Low", "High", "OAuth2", "Low",
     "const axios = require('axios');\nconst token = await axios.post('https://api.us.onelogin.com/auth/oauth2/v2/token', { grant_type: 'client_credentials' }, { headers: { Authorization: 'client_id:client_secret' } });"),

    ("Ping Identity API", "Authentication",
     "Enterprise identity security API with adaptive MFA and zero trust capabilities.",
     "v1", "pingidentity", "Multi-language", "REST", "Paid/Premium", "Low", "High", "OAuth2", "Low",
     "const axios = require('axios');\nconst response = await axios.post('https://auth.pingone.com/{envId}/as/token', new URLSearchParams({ grant_type: 'client_credentials', client_id: 'YOUR_CLIENT_ID', client_secret: 'YOUR_SECRET' }));"),

    ("AWS IAM API", "Authentication",
     "Amazon's identity and access management API for controlling AWS resource access.",
     "v1", "amazon", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const { IAMClient, CreateUserCommand } = require('@aws-sdk/client-iam');\nconst client = new IAMClient({ region: 'us-east-1' });\nconst response = await client.send(new CreateUserCommand({ UserName: 'newuser' }));"),

    ("FusionAuth API", "Authentication",
     "Developer-focused authentication API with OAuth2, SAML, and passwordless login.",
     "v1", "fusionauth", "Multi-language", "REST", "Freemium", "Low", "High", "OAuth2", "Low",
     "const { FusionAuthClient } = require('@fusionauth/typescript-client');\nconst client = new FusionAuthClient('YOUR_API_KEY', 'http://localhost:9011');\nconst response = await client.login({ loginId: 'user@example.com', password: 'password', applicationId: 'YOUR_APP_ID' });"),

    ("Magic Link API", "Authentication",
     "Passwordless authentication API using magic links and Web3 wallet login.",
     "v1", "magic", "JavaScript", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { Magic } from 'magic-sdk';\nconst magic = new Magic('YOUR_PUBLISHABLE_KEY');\nawait magic.auth.loginWithMagicLink({ email: 'user@example.com' });"),

    ("Stytch API", "Authentication",
     "Modern authentication API with passwordless login, OTPs, and OAuth.",
     "v1", "stytch", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const stytch = require('stytch');\nconst client = new stytch.Client({ project_id: 'project-id', secret: 'secret' });\nawait client.magicLinks.email.loginOrCreate({ email: 'user@example.com' });"),

    ("Azure Active Directory API", "Authentication",
     "Microsoft's cloud identity platform API with enterprise SSO and MFA.",
     "v2", "microsoft", "Multi-language", "REST", "Freemium", "Low", "High", "OAuth2", "Low",
     "const { ConfidentialClientApplication } = require('@azure/msal-node');\nconst cca = new ConfidentialClientApplication({ auth: { clientId: 'YOUR_CLIENT_ID', clientSecret: 'YOUR_SECRET', authority: 'https://login.microsoftonline.com/YOUR_TENANT_ID' } });"),

    ("WorkOS API", "Authentication",
     "Enterprise authentication API with SSO, directory sync, and audit logs.",
     "v1", "workos", "Multi-language", "REST", "Freemium", "Low", "High", "OAuth2", "Low",
     "const WorkOS = require('@workos-inc/node');\nconst workos = new WorkOS('YOUR_API_KEY');\nconst url = workos.sso.getAuthorizationURL({ domain: 'example.com', redirectURI: 'https://app.example.com/callback', clientID: 'YOUR_CLIENT_ID' });"),

    # ── AI/ML (14 entries) ────────────────────────────────────────────────────
    # Artificial intelligence and machine learning APIs for text, image, and audio.
    # Covers LLM providers (OpenAI, Anthropic, Mistral, Groq), image generation
    # (Stability AI), speech (Whisper, AssemblyAI), and translation (DeepL).
    ("OpenAI API", "AI/ML",
     "Powerful AI API providing access to GPT-4, DALL-E, Whisper, and embeddings.",
     "v1", "openai", "Multi-language", "REST", "Paid/Premium", "Medium", "High", "REST", "Low",
     "import OpenAI from 'openai';\nconst client = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });\nconst completion = await client.chat.completions.create({ model: 'gpt-4', messages: [{ role: 'user', content: 'Hello!' }] });"),

    ("Anthropic Claude API", "AI/ML",
     "Anthropic's Claude AI API for text generation, analysis, and reasoning tasks.",
     "v1", "anthropic", "Multi-language", "REST", "Paid/Premium", "Medium", "High", "REST", "Low",
     "import Anthropic from '@anthropic-ai/sdk';\nconst client = new Anthropic();\nconst message = await client.messages.create({ model: 'claude-opus-4-6', max_tokens: 1024, messages: [{ role: 'user', content: 'Hello!' }] });"),

    ("Google Gemini API", "AI/ML",
     "Google's Gemini multimodal AI API for text, image, and code generation.",
     "v1", "google", "Multi-language", "REST", "Freemium", "Medium", "High", "REST", "Low",
     "import { GoogleGenerativeAI } from '@google/generative-ai';\nconst genAI = new GoogleGenerativeAI(API_KEY);\nconst model = genAI.getGenerativeModel({ model: 'gemini-pro' });"),

    ("Hugging Face API", "AI/ML",
     "Access thousands of pre-trained ML models for NLP, vision, and audio via API.",
     "v1", "huggingface", "Python", "REST", "Freemium", "Medium", "High", "REST", "Low",
     "import requests\nAPI_URL = 'https://api-inference.huggingface.co/models/gpt2'\nheaders = {'Authorization': 'Bearer YOUR_TOKEN'}\nresponse = requests.post(API_URL, headers=headers, json={'inputs': 'Hello world'})"),

    ("Stability AI API", "AI/ML",
     "Stable Diffusion image generation API for creating AI art and images.",
     "v1", "stabilityai", "Multi-language", "REST", "Paid/Premium", "High", "High", "REST", "Low",
     "import requests\nresponse = requests.post(\n  'https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image',\n  headers={'Authorization': 'Bearer YOUR_KEY'},\n  json={'text_prompts': [{'text': 'A lighthouse'}]}\n)"),

    ("Cohere API", "AI/ML",
     "NLP API for text generation, classification, embedding, and semantic search.",
     "v1", "cohere", "Multi-language", "REST", "Freemium", "Medium", "High", "REST", "Low",
     "import cohere\nco = cohere.Client('YOUR_API_KEY')\nresponse = co.generate(model='command', prompt='Write a tagline for an AI company')"),

    ("Replicate API", "AI/ML",
     "Run machine learning models in the cloud with a simple API call.",
     "v1", "replicate", "Multi-language", "REST", "Paid/Premium", "Medium", "High", "REST", "Low",
     "import replicate\noutput = replicate.run('stability-ai/stable-diffusion', input={'prompt': 'A futuristic city'})"),

    ("Mistral AI API", "AI/ML",
     "High performance open source large language model API for text generation.",
     "v1", "mistral", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst response = await axios.post('https://api.mistral.ai/v1/chat/completions', { model: 'mistral-tiny', messages: [{ role: 'user', content: 'Hello!' }] }, { headers: { Authorization: 'Bearer YOUR_API_KEY' } });"),

    ("ElevenLabs API", "AI/ML",
     "AI voice synthesis API for realistic text-to-speech and voice cloning.",
     "v1", "elevenlabs", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst response = await axios.post('https://api.elevenlabs.io/v1/text-to-speech/VOICE_ID', { text: 'Hello World', model_id: 'eleven_monolingual_v1' }, { headers: { 'xi-api-key': 'YOUR_API_KEY' }, responseType: 'arraybuffer' });"),

    ("AssemblyAI API", "AI/ML",
     "Speech recognition and audio intelligence API with transcription and analysis.",
     "v2", "assemblyai", "Multi-language", "REST", "Freemium", "Medium", "High", "REST", "Low",
     "const axios = require('axios');\nconst transcript = await axios.post('https://api.assemblyai.com/v2/transcript', { audio_url: 'https://example.com/audio.mp3' }, { headers: { authorization: 'YOUR_API_KEY' } });"),

    ("DeepL API", "AI/ML",
     "High quality machine translation API supporting 30+ languages.",
     "v2", "deepl", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst response = await axios.post('https://api-free.deepl.com/v2/translate', new URLSearchParams({ auth_key: 'YOUR_KEY', text: 'Hello World', target_lang: 'DE' }));"),

    ("Perplexity API", "AI/ML",
     "AI search and question answering API with real-time web access.",
     "v1", "perplexity", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst response = await axios.post('https://api.perplexity.ai/chat/completions', { model: 'pplx-7b-online', messages: [{ role: 'user', content: 'What is the latest news?' }] }, { headers: { Authorization: 'Bearer YOUR_API_KEY' } });"),

    ("Groq API", "AI/ML",
     "Ultra-fast AI inference API for LLMs with low latency responses.",
     "v1", "groq", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const Groq = require('groq-sdk');\nconst groq = new Groq({ apiKey: 'YOUR_API_KEY' });\nconst completion = await groq.chat.completions.create({ messages: [{ role: 'user', content: 'Hello!' }], model: 'llama3-8b-8192' });"),

    ("Whisper API", "AI/ML",
     "OpenAI's speech-to-text API for accurate audio transcription.",
     "v1", "openai", "Multi-language", "REST", "Paid/Premium", "Medium", "High", "REST", "Low",
     "const OpenAI = require('openai');\nconst openai = new OpenAI({ apiKey: 'YOUR_API_KEY' });\nconst transcription = await openai.audio.transcriptions.create({ file: fs.createReadStream('audio.mp3'), model: 'whisper-1' });"),

    # ── CLOUD (15 entries) ────────────────────────────────────────────────────
    # Cloud infrastructure and deployment APIs for storage, compute, and hosting.
    # Covers major providers (AWS, GCP, Azure), deployment platforms (Vercel,
    # Render, Railway, Heroku), and edge computing (Cloudflare Workers).
    ("AWS S3 API", "Cloud",
     "Amazon S3 object storage API for storing and retrieving files at scale.",
     "v4", "amazon", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const { S3Client, PutObjectCommand } = require('@aws-sdk/client-s3');\nconst client = new S3Client({ region: 'us-east-1' });\nawait client.send(new PutObjectCommand({ Bucket: 'my-bucket', Key: 'file.txt', Body: 'Hello' }));"),

    ("Google Cloud Storage", "Cloud",
     "Google's object storage API for storing and accessing data on Google infrastructure.",
     "v1", "google", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "from google.cloud import storage\nclient = storage.Client()\nbucket = client.bucket('my-bucket')\nblob = bucket.blob('file.txt')\nblob.upload_from_string('Hello World')"),

    ("Azure Blob Storage", "Cloud",
     "Microsoft Azure's object storage API for unstructured data storage.",
     "v12", "microsoft", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "from azure.storage.blob import BlobServiceClient\nclient = BlobServiceClient.from_connection_string('YOUR_CONN_STRING')\ncontainer = client.get_container_client('mycontainer')"),

    ("Cloudflare API", "Cloud",
     "API for managing DNS, CDN, firewall rules, and Workers on Cloudflare.",
     "v4", "cloudflare", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const response = await fetch('https://api.cloudflare.com/client/v4/zones', {\n  headers: { 'Authorization': 'Bearer YOUR_TOKEN' }\n});"),

    ("DigitalOcean API", "Cloud",
     "Cloud infrastructure API for managing droplets, databases, and cloud infrastructure.",
     "v2", "digitalocean", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst droplets = await axios.get('https://api.digitalocean.com/v2/droplets', { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    ("Vercel API", "Cloud",
     "Deployment and hosting API for managing projects and serverless functions.",
     "v9", "vercel", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst deployments = await axios.get('https://api.vercel.com/v6/deployments', { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    ("Netlify API", "Cloud",
     "Modern web hosting API for managing sites, deployments, forms, and serverless functions.",
     "v1", "netlify", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst sites = await axios.get('https://api.netlify.com/api/v1/sites', { headers: { Authorization: 'Bearer YOUR_ACCESS_TOKEN' } });"),

    ("AWS Lambda API", "Cloud",
     "Serverless compute API for running code without provisioning servers.",
     "v1", "amazon", "Multi-language", "REST", "Paid/Premium", "Low", "High", "Event-Driven", "Low",
     "const { LambdaClient, InvokeCommand } = require('@aws-sdk/client-lambda');\nconst client = new LambdaClient({ region: 'us-east-1' });\nconst response = await client.send(new InvokeCommand({ FunctionName: 'my-function', Payload: JSON.stringify({ key: 'value' }) }));"),

    ("AWS EC2 API", "Cloud",
     "Amazon Elastic Compute Cloud API for scalable virtual server management.",
     "v1", "amazon", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const { EC2Client, DescribeInstancesCommand } = require('@aws-sdk/client-ec2');\nconst client = new EC2Client({ region: 'us-east-1' });\nconst data = await client.send(new DescribeInstancesCommand({}));"),

    ("Google Cloud Run API", "Cloud",
     "Fully managed serverless platform API for containerized applications.",
     "v2", "google", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const { ServicesClient } = require('@google-cloud/run').v2;\nconst client = new ServicesClient();\nconst [service] = await client.getService({ name: 'projects/PROJECT/locations/us-central1/services/SERVICE' });"),

    ("Azure Functions API", "Cloud",
     "Microsoft's serverless API for event-driven cloud functions.",
     "v4", "microsoft", "Multi-language", "REST", "Paid/Premium", "Low", "High", "Event-Driven", "Low",
     "const { app } = require('@azure/functions');\napp.http('myFunction', { methods: ['GET', 'POST'], authLevel: 'anonymous', handler: async (request, context) => { return { body: 'Hello World!' }; } });"),

    ("Cloudflare Workers API", "Cloud",
     "Edge computing API for deploying serverless functions globally.",
     "v4", "cloudflare", "Multi-language", "REST", "Freemium", "Low", "High", "Event-Driven", "Low",
     "export default {\n  async fetch(request, env, ctx) {\n    return new Response('Hello World!', { headers: { 'content-type': 'text/plain' } });\n  }\n};"),

    ("Heroku Platform API", "Cloud",
     "Cloud platform API for deploying, managing, and scaling applications.",
     "v3", "heroku", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst apps = await axios.get('https://api.heroku.com/apps', { headers: { Authorization: `Bearer ${process.env.HEROKU_API_KEY}`, Accept: 'application/vnd.heroku+json; version=3' } });"),

    ("Render API", "Cloud",
     "Cloud platform API for deploying web services, databases, and static sites.",
     "v1", "render", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst services = await axios.get('https://api.render.com/v1/services', { headers: { Authorization: 'Bearer YOUR_API_KEY' } });"),

    ("Railway API", "Cloud",
     "Infrastructure platform API for deploying apps and databases instantly.",
     "v2", "railway", "Multi-language", "GraphQL", "Freemium", "Low", "High", "GraphQL", "Low",
     "const axios = require('axios');\nconst response = await axios.post('https://backboard.railway.app/graphql/v2', { query: '{ me { name email projects { edges { node { id name } } } } }' }, { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    # ── DATABASE (14 entries) ─────────────────────────────────────────────────
    # Database and ORM APIs for SQL, NoSQL, vector, and serverless storage.
    # Covers relational (Neon, PlanetScale, CockroachDB), document (MongoDB,
    # Firestore), key-value (Redis, Upstash), and ORM tools (Prisma, Drizzle).
    ("Supabase API", "Database",
     "Open source Firebase alternative with PostgreSQL, auth, and realtime subscriptions.",
     "v1", "supabase", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { createClient } from '@supabase/supabase-js';\nconst supabase = createClient('YOUR_URL', 'YOUR_KEY');\nconst { data } = await supabase.from('users').select('*');"),

    ("Firebase Firestore", "Database",
     "Google's NoSQL cloud database with realtime sync for web and mobile apps.",
     "v9", "google", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { getFirestore, collection, getDocs } from 'firebase/firestore';\nconst db = getFirestore();\nconst querySnapshot = await getDocs(collection(db, 'users'));"),

    ("PlanetScale API", "Database",
     "MySQL-compatible serverless database API with branching and schema changes.",
     "v1", "planetscale", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { connect } from '@planetscale/database';\nconst conn = connect({ url: process.env.DATABASE_URL });\nconst results = await conn.execute('SELECT * FROM users');"),

    ("MongoDB Atlas API", "Database",
     "Fully managed cloud database API for MongoDB with global clusters.",
     "v2", "mongodb", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { MongoClient } = require('mongodb');\nconst client = new MongoClient(process.env.MONGODB_URI);\nawait client.connect();\nconst db = client.db('mydb');\nconst users = await db.collection('users').find({}).toArray();"),

    ("Redis Cloud API", "Database",
     "Redis managed cloud database API for caching, sessions, and pub/sub messaging.",
     "v1", "redis", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { createClient } from 'redis';\nconst client = createClient({ url: 'redis://localhost:6379' });\nawait client.connect();\nawait client.set('key', 'value');"),

    ("Neon API", "Database",
     "Serverless PostgreSQL API with branching, autoscaling, and instant provisioning.",
     "v2", "neon", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { neon } from '@neondatabase/serverless';\nconst sql = neon(process.env.DATABASE_URL);\nconst result = await sql`SELECT * FROM users`;"),

    ("CockroachDB API", "Database",
     "Distributed SQL database API with global scaling and strong consistency.",
     "v23", "cockroachlabs", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Pool } = require('pg');\nconst pool = new Pool({ connectionString: process.env.DATABASE_URL, ssl: { rejectUnauthorized: false } });\nconst result = await pool.query('SELECT * FROM orders LIMIT 10');"),

    ("FaunaDB API", "Database",
     "Distributed document-relational database API with strong consistency.",
     "v10", "fauna", "Multi-language", "GraphQL", "Freemium", "Low", "High", "GraphQL", "Low",
     "const { Client, fql } = require('fauna');\nconst client = new Client({ secret: 'YOUR_SECRET' });\nconst result = await client.query(fql`Collection.all().take(10)`);"),

    ("Turso API", "Database",
     "Edge SQLite database API with global distribution and low latency.",
     "v1", "turso", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { createClient } from '@libsql/client';\nconst client = createClient({ url: 'libsql://YOUR_DB.turso.io', authToken: 'YOUR_TOKEN' });\nconst result = await client.execute('SELECT * FROM users');"),

    ("DynamoDB API", "Database",
     "Amazon's NoSQL database API with single-digit millisecond performance.",
     "v1", "amazon", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const { DynamoDBClient, GetItemCommand } = require('@aws-sdk/client-dynamodb');\nconst client = new DynamoDBClient({ region: 'us-east-1' });\nconst data = await client.send(new GetItemCommand({ TableName: 'Users', Key: { id: { S: '123' } } }));"),

    ("Upstash Redis API", "Database",
     "Serverless Redis API with REST interface and global replication.",
     "v1", "upstash", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Redis } = require('@upstash/redis');\nconst redis = new Redis({ url: 'YOUR_URL', token: 'YOUR_TOKEN' });\nawait redis.set('key', 'value', { ex: 3600 });\nconst value = await redis.get('key');"),

    ("Xata API", "Database",
     "Serverless database API with branching, search, and analytics built-in.",
     "v1", "xata", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { XataClient } = require('./xata');\nconst xata = new XataClient({ apiKey: 'YOUR_API_KEY' });\nconst users = await xata.db.users.getAll();"),

    ("Prisma ORM", "Database",
     "Next-generation Node.js ORM with type-safe database access and migrations.",
     "v5", "prisma", "TypeScript", "N/A", "Open Source", "Low", "High", "N/A", "Low",
     "import { PrismaClient } from '@prisma/client';\nconst prisma = new PrismaClient();\nconst users = await prisma.user.findMany({\n  where: { active: true },\n  select: { id: true, name: true }\n});"),

    ("Drizzle ORM", "Database",
     "Lightweight TypeScript ORM with SQL-like query builder and full type safety.",
     "v0.29", "drizzle-team", "TypeScript", "N/A", "Open Source", "Low", "High", "N/A", "High",
     "import { drizzle } from 'drizzle-orm/node-postgres';\nimport { eq } from 'drizzle-orm';\nconst db = drizzle(pool);\nconst users = await db.select().from(usersTable).where(eq(usersTable.active, true));"),

    # ── DEVOPS (8 entries) ────────────────────────────────────────────────────
    # CI/CD and infrastructure APIs for building, deploying, and orchestrating apps.
    # Covers version control (GitHub, GitLab, Bitbucket), containers (Docker,
    # Kubernetes), CI pipelines (CircleCI), and infrastructure-as-code (Terraform, ArgoCD).
    ("GitHub Actions API", "DevOps",
     "GitHub Actions REST API for managing CI/CD workflows, runs, and artifacts.",
     "v3", "github", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Octokit } = require('@octokit/rest');\nconst octokit = new Octokit({ auth: 'YOUR_TOKEN' });\nconst runs = await octokit.actions.listWorkflowRunsForRepo({ owner: 'org', repo: 'repo' });"),

    ("GitLab API", "DevOps",
     "Complete DevOps platform API for source control, CI/CD, and project management.",
     "v4", "gitlab", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst projects = await axios.get('https://gitlab.com/api/v4/projects', { headers: { 'PRIVATE-TOKEN': 'YOUR_TOKEN' } });"),

    ("Bitbucket API", "DevOps",
     "Atlassian's Git repository API with built-in CI/CD pipelines.",
     "v2", "atlassian", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst repos = await axios.get('https://api.bitbucket.org/2.0/repositories/YOUR_WORKSPACE', { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    ("CircleCI API", "DevOps",
     "CircleCI API for triggering pipelines, managing jobs, and viewing build results.",
     "v2", "circleci", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const response = await fetch('https://circleci.com/api/v2/pipeline', {\n  headers: { 'Circle-Token': 'YOUR_TOKEN' }\n});"),

    ("Docker Hub API", "DevOps",
     "Container registry API for managing Docker images and automated builds.",
     "v2", "docker", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst token = await axios.post('https://hub.docker.com/v2/users/login', { username: 'user', password: 'pass' });\nconst repos = await axios.get('https://hub.docker.com/v2/repositories/YOUR_USERNAME', { headers: { Authorization: `Bearer ${token.data.token}` } });"),

    ("Kubernetes API", "DevOps",
     "Container orchestration API for automating deployment and scaling of applications.",
     "v1", "cncf", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const k8s = require('@kubernetes/client-node');\nconst kc = new k8s.KubeConfig();\nkc.loadFromDefault();\nconst k8sApi = kc.makeApiClient(k8s.CoreV1Api);\nconst pods = await k8sApi.listNamespacedPod('default');"),

    ("Terraform Cloud API", "DevOps",
     "Infrastructure as code API for managing cloud resources declaratively.",
     "v2", "hashicorp", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst workspaces = await axios.get('https://app.terraform.io/api/v2/organizations/YOUR_ORG/workspaces', { headers: { Authorization: 'Bearer YOUR_TOKEN', 'Content-Type': 'application/vnd.api+json' } });"),

    ("ArgoCD API", "DevOps",
     "Declarative GitOps continuous delivery API for Kubernetes.",
     "v2", "argoproj", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst apps = await axios.get('https://argocd.example.com/api/v1/applications', { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    # ── ANALYTICS (8 entries) ─────────────────────────────────────────────────
    # Product and web analytics APIs for tracking user behavior and events.
    # Covers web analytics (Google Analytics, Plausible), product analytics
    # (Mixpanel, Amplitude, PostHog), and behavior tools (Hotjar, Heap).
    ("Google Analytics API", "Analytics",
     "Web analytics API for tracking website traffic, user behavior, and conversions.",
     "v4", "google", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const { BetaAnalyticsDataClient } = require('@google-analytics/data');\nconst analyticsDataClient = new BetaAnalyticsDataClient();\nconst [response] = await analyticsDataClient.runReport({ property: 'properties/YOUR_PROPERTY_ID', dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }], metrics: [{ name: 'activeUsers' }] });"),

    ("Mixpanel API", "Analytics",
     "Product analytics API for tracking user interactions and funnels.",
     "v2", "mixpanel", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const Mixpanel = require('mixpanel');\nconst mixpanel = Mixpanel.init('YOUR_TOKEN');\nmixpanel.track('Sign Up', { distinct_id: 'user123', plan: 'Premium' });"),

    ("Amplitude API", "Analytics",
     "Product analytics API for understanding user behavior and digital products.",
     "v2", "amplitude", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nawait axios.post('https://api2.amplitude.com/2/httpapi', { api_key: 'YOUR_API_KEY', events: [{ user_id: 'user123', event_type: 'button_click', event_properties: { button_name: 'signup' } }] });"),

    ("Segment API", "Analytics",
     "Customer data platform API for collecting, cleaning, and routing analytics data.",
     "v1", "twilio", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Analytics } = require('@segment/analytics-node');\nconst analytics = new Analytics({ writeKey: 'YOUR_WRITE_KEY' });\nanalytics.track({ userId: 'user123', event: 'Item Purchased', properties: { price: 29.99, item: 'Pro Plan' } });"),

    ("PostHog API", "Analytics",
     "Open source product analytics API with feature flags and session recording.",
     "v1", "posthog", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { PostHog } = require('posthog-node');\nconst client = new PostHog('YOUR_API_KEY', { host: 'https://app.posthog.com' });\nclient.capture({ distinctId: 'user123', event: 'user signed up' });"),

    ("Plausible API", "Analytics",
     "Privacy-friendly web analytics API with no cookies and GDPR compliance.",
     "v1", "plausible", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst stats = await axios.get('https://plausible.io/api/v1/stats/summary', { params: { site_id: 'example.com', period: '30d' }, headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    ("Hotjar API", "Analytics",
     "User behavior analytics API with heatmaps, recordings, and feedback tools.",
     "v1", "hotjar", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst recordings = await axios.get('https://insights.hotjar.com/api/v1/sites/YOUR_SITE_ID/recordings', { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    ("Heap Analytics API", "Analytics",
     "Automatic event tracking API that captures all user interactions without code.",
     "v1", "heap", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nawait axios.post('https://heapanalytics.com/api/track', { app_id: 'YOUR_APP_ID', identity: 'user@example.com', event: 'Clicked Button', properties: { button: 'CTA' } });"),

    # ── MONITORING (8 entries) ────────────────────────────────────────────────
    # Observability and incident management APIs for tracking system health.
    # Covers APM (Datadog, New Relic, Dynatrace), open source (Grafana,
    # Prometheus), error tracking (Sentry), alerting (PagerDuty), and uptime (Uptime Robot).
    ("Datadog API", "Monitoring",
     "Cloud monitoring and analytics API for infrastructure, applications, and logs.",
     "v2", "datadog", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const { v2 } = require('@datadog/datadog-api-client');\nconst configuration = v2.createConfiguration();\nconst apiInstance = new v2.MetricsApi(configuration);"),

    ("New Relic API", "Monitoring",
     "Full-stack observability API for monitoring applications and infrastructure.",
     "v2", "newrelic", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const newrelic = require('newrelic');\nnewrelic.recordMetric('Custom/MyMetric', 1.0);\nnewrelic.addCustomAttribute('userId', '123');"),

    ("Grafana API", "Monitoring",
     "Open source observability platform API for metrics, logs, and traces.",
     "v1", "grafana", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst dashboards = await axios.get('http://localhost:3000/api/search?type=dash-db', { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    ("Prometheus API", "Monitoring",
     "Open source monitoring API for collecting and querying time-series metrics.",
     "v1", "cncf", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst result = await axios.get('http://localhost:9090/api/v1/query', { params: { query: 'up', time: Date.now() / 1000 } });"),

    ("PagerDuty API", "Monitoring",
     "Incident management API for alerting, on-call scheduling, and post-mortems.",
     "v2", "pagerduty", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst incident = await axios.post('https://api.pagerduty.com/incidents', { incident: { type: 'incident', title: 'Server Down', service: { id: 'YOUR_SERVICE_ID', type: 'service_reference' } } }, { headers: { Authorization: 'Token token=YOUR_TOKEN', From: 'user@example.com' } });"),

    ("Sentry API", "Monitoring",
     "Application error tracking API for monitoring and fixing crashes in real time.",
     "v0", "sentry", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "High",
     "import * as Sentry from '@sentry/node';\nSentry.init({ dsn: 'YOUR_DSN' });\ntry { /* code */ } catch(e) { Sentry.captureException(e); }"),

    ("Uptime Robot API", "Monitoring",
     "Website monitoring API for tracking uptime and getting instant alerts.",
     "v2", "uptimerobot", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst monitors = await axios.post('https://api.uptimerobot.com/v2/getMonitors', new URLSearchParams({ api_key: 'YOUR_KEY', format: 'json' }));"),

    ("Dynatrace API", "Monitoring",
     "AI-powered full-stack monitoring API for cloud infrastructure and applications.",
     "v2", "dynatrace", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst problems = await axios.get('https://YOUR_ENV.live.dynatrace.com/api/v2/problems', { headers: { Authorization: 'Api-Token YOUR_TOKEN' } });"),

    # ── SEARCH (8 entries) ────────────────────────────────────────────────────
    # Full-text and vector search APIs for building fast search experiences.
    # Covers managed search (Algolia), open source (Elasticsearch, Meilisearch,
    # Typesense, OpenSearch), and vector/semantic search (Pinecone, Qdrant, Weaviate).
    ("Algolia API", "Search",
     "Search-as-a-service API for fast, typo-tolerant full-text search experiences.",
     "v4", "algolia", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import algoliasearch from 'algoliasearch';\nconst client = algoliasearch('APP_ID', 'API_KEY');\nconst index = client.initIndex('products');\nconst results = await index.search('query');"),

    ("Elasticsearch API", "Search",
     "Distributed search and analytics API for full-text and structured data.",
     "v8", "elastic", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Client } = require('@elastic/elasticsearch');\nconst client = new Client({ node: 'http://localhost:9200' });\nconst result = await client.search({ index: 'products', body: { query: { match: { name: 'laptop' } } } });"),

    ("Meilisearch API", "Search",
     "Open source, blazingly fast search API for building search experiences.",
     "v1", "meilisearch", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const { MeiliSearch } = require('meilisearch');\nconst client = new MeiliSearch({ host: 'http://localhost:7700', apiKey: 'YOUR_KEY' });\nconst index = client.index('products');\nconst results = await index.search('laptop', { limit: 10 });"),

    ("Typesense API", "Search",
     "Fast, typo-tolerant open-source search engine API alternative to Algolia.",
     "v0.25", "typesense", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const Typesense = require('typesense');\nconst client = new Typesense.Client({ nodes: [{ host: 'localhost', port: 8108, protocol: 'http' }], apiKey: 'YOUR_KEY' });\nconst results = await client.collections('products').documents().search({ q: 'laptop', query_by: 'name' });"),

    ("Pinecone API", "Search",
     "Managed vector database API for semantic search and recommendation systems.",
     "v1", "pinecone", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Pinecone } = require('@pinecone-database/pinecone');\nconst pc = new Pinecone({ apiKey: 'YOUR_API_KEY' });\nconst index = pc.index('my-index');\nconst results = await index.query({ vector: [0.1, 0.2, 0.3], topK: 5 });"),

    ("Qdrant API", "Search",
     "Vector similarity search API for building AI-powered search applications.",
     "v1", "qdrant", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const { QdrantClient } = require('@qdrant/js-client-rest');\nconst client = new QdrantClient({ host: 'localhost', port: 6333 });\nconst results = await client.search('my_collection', { vector: [0.2, 0.1, 0.9], limit: 5 });"),

    ("Weaviate API", "Search",
     "Open source vector database API for semantic search and knowledge graphs.",
     "v1", "weaviate", "Multi-language", "REST", "Open Source", "Low", "High", "GraphQL", "Low",
     "import weaviate from 'weaviate-ts-client';\nconst client = weaviate.client({ scheme: 'http', host: 'localhost:8080' });\nconst result = await client.graphql.get().withClassName('Article').withFields('title content').withNearText({ concepts: ['machine learning'] }).withLimit(5).do();"),

    ("OpenSearch API", "Search",
     "Community-driven open source search and analytics API forked from Elasticsearch.",
     "v2", "amazon", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const { Client } = require('@opensearch-project/opensearch');\nconst client = new Client({ node: 'https://localhost:9200', auth: { username: 'admin', password: 'admin' } });\nconst result = await client.search({ index: 'movies', body: { query: { match: { title: 'Inception' } } } });"),

    # ── MICROSERVICE (12 entries) ─────────────────────────────────────────────
    # Messaging, orchestration, and service communication APIs for distributed systems.
    # Covers message brokers (Kafka, RabbitMQ, NATS), API gateways (Kong),
    # workflow engines (Temporal), real-time (Socket.IO), and job queues (BullMQ).
    ("Kong Gateway API", "Microservice",
     "Open source API gateway and microservice management platform.",
     "v3", "kong", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst services = await axios.get('http://localhost:8001/services');\nconst newService = await axios.post('http://localhost:8001/services', { name: 'my-service', url: 'http://my-service:3000' });"),

    ("Apache Kafka API", "Microservice",
     "Distributed event streaming API for high-throughput, fault-tolerant messaging.",
     "v3", "apache", "Multi-language", "REST", "Open Source", "Low", "High", "Event-Driven", "Low",
     "const { Kafka } = require('kafkajs');\nconst kafka = new Kafka({ clientId: 'my-app', brokers: ['localhost:9092'] });\nconst producer = kafka.producer();\nawait producer.connect();\nawait producer.send({ topic: 'orders', messages: [{ value: JSON.stringify({ orderId: '123' }) }] });"),

    ("RabbitMQ API", "Microservice",
     "Message broker API for reliable message queuing between microservices.",
     "v3.12", "rabbitmq", "Multi-language", "AMQP", "Open Source", "Low", "High", "Pub/Sub", "Low",
     "const amqp = require('amqplib');\nconst conn = await amqp.connect('amqp://localhost');\nconst channel = await conn.createChannel();\nawait channel.assertQueue('tasks');\nchannel.sendToQueue('tasks', Buffer.from('Hello'));"),

    ("gRPC API", "Microservice",
     "High-performance remote procedure call API framework for microservices.",
     "v1", "google", "Multi-language", "gRPC", "Open Source", "Low", "High", "REST", "Low",
     "const grpc = require('@grpc/grpc-js');\nconst protoLoader = require('@grpc/proto-loader');\nconst packageDef = protoLoader.loadSync('service.proto');\nconst proto = grpc.loadPackageDefinition(packageDef);\nconst client = new proto.MyService('localhost:50051', grpc.credentials.createInsecure());"),

    ("Dapr API", "Microservice",
     "Distributed application runtime API for building portable microservices.",
     "v1", "microsoft", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nawait axios.post('http://localhost:3500/v1.0/state/statestore', [{ key: 'order', value: { orderId: '123', total: 99.99 } }]);"),

    ("Temporal API", "Microservice",
     "Workflow orchestration API for building reliable distributed applications.",
     "v1", "temporal", "Multi-language", "REST", "Open Source", "Low", "High", "Event-Driven", "Low",
     "const { Connection, Client } = require('@temporalio/client');\nconst connection = await Connection.connect({ address: 'localhost:7233' });\nconst client = new Client({ connection });\nconst handle = await client.workflow.start(myWorkflow, { taskQueue: 'my-queue', workflowId: 'workflow-1' });"),

    ("BullMQ", "Microservice",
     "Redis-based queue and job scheduling library for Node.js background processing.",
     "v4", "taskforce", "JavaScript", "N/A", "Open Source", "Low", "High", "Event-Driven", "Low",
     "import { Queue, Worker } from 'bullmq';\nconst queue = new Queue('emails');\nawait queue.add('sendWelcome', { to: 'user@example.com' });\nconst worker = new Worker('emails', async job => { /* send email */ });"),

    ("Inngest API", "Microservice",
     "Event-driven job scheduling API for background jobs, cron, and workflows in serverless.",
     "v2", "inngest", "TypeScript", "REST", "Freemium", "Low", "High", "Event-Driven", "Low",
     "import { Inngest } from 'inngest';\nconst inngest = new Inngest({ id: 'my-app' });\nconst fn = inngest.createFunction(\n  { id: 'send-welcome' },\n  { event: 'user/signup' },\n  async ({ event }) => { /* send email */ }\n);"),

    ("Socket.IO", "Microservice",
     "Bidirectional event-based communication library for real-time web applications.",
     "v4.7", "socketio", "JavaScript", "WebSocket", "Open Source", "Low", "High", "Event-Driven", "Low",
     "const { Server } = require('socket.io');\nconst io = new Server(httpServer);\nio.on('connection', (socket) => {\n  socket.emit('greeting', 'Hello!');\n  socket.on('message', (data) => console.log(data));\n});"),

    ("Axios", "Microservice",
     "Promise-based HTTP client for Node.js and browsers with request/response interceptors.",
     "v1.6", "axios", "JavaScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "import axios from 'axios';\nconst response = await axios.get('https://api.example.com/users', {\n  headers: { 'Authorization': `Bearer ${token}` }\n});\nconsole.log(response.data);"),

    ("Consul API", "Microservice",
     "Service discovery and configuration API for distributed microservices.",
     "v1", "hashicorp", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst services = await axios.get('http://localhost:8500/v1/catalog/services');\nconst health = await axios.get('http://localhost:8500/v1/health/service/my-service?passing=true');"),

    ("NATS API", "Microservice",
     "High-performance messaging API for cloud-native microservices communication.",
     "v2", "nats", "Multi-language", "REST", "Open Source", "Low", "High", "Pub/Sub", "Low",
     "const { connect, StringCodec } = require('nats');\nconst nc = await connect({ servers: 'nats://localhost:4222' });\nconst sc = StringCodec();\nnc.publish('orders', sc.encode(JSON.stringify({ id: '123', total: 99.99 })));"),

    # ── BACKEND FRAMEWORK (12 entries) ───────────────────────────────────────
    # Server-side web frameworks for building REST and GraphQL APIs.
    # Covers Python (Flask, FastAPI, Django REST), JavaScript (Express, NestJS,
    # Fastify, Hono), and others (Spring Boot, Laravel, Rails, Strapi, Hasura).
    ("Flask", "Backend Framework",
     "Lightweight Python web framework for building simple APIs and microservices.",
     "v3", "pallets", "Python", "REST", "Open Source", "Low", "High", "REST", "Low",
     "from flask import Flask, jsonify\napp = Flask(__name__)\n\n@app.route('/api/users')\ndef get_users():\n    return jsonify({'users': []})\n\nif __name__ == '__main__':\n    app.run()"),

    ("FastAPI Framework", "Backend Framework",
     "Modern, fast Python web framework API with automatic OpenAPI documentation.",
     "v0.110", "tiangolo", "Python", "REST", "Open Source", "Low", "High", "REST", "Low",
     "from fastapi import FastAPI\nfrom pydantic import BaseModel\napp = FastAPI()\nclass User(BaseModel):\n    name: str\n    email: str\n@app.get('/users')\nasync def get_users():\n    return await db.fetch_all('SELECT * FROM users')"),

    ("Django REST Framework", "Backend Framework",
     "Powerful toolkit for building Web APIs on top of Django.",
     "v3", "encode", "Python", "REST", "Open Source", "Low", "High", "REST", "Low",
     "from rest_framework import viewsets\nfrom .models import User\nfrom .serializers import UserSerializer\nclass UserViewSet(viewsets.ModelViewSet):\n    queryset = User.objects.all()\n    serializer_class = UserSerializer"),

    ("Express.js", "Backend Framework",
     "Fast, unopinionated Node.js web framework for building APIs and web applications.",
     "v4.18", "expressjs", "JavaScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const express = require('express');\nconst app = express();\napp.get('/api/users', (req, res) => {\n  res.json({ users: [] });\n});\napp.listen(3000);"),

    ("NestJS Framework", "Backend Framework",
     "Progressive Node.js framework API for building scalable server-side applications.",
     "v10", "nestjs", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "@Controller('users')\nexport class UsersController {\n  constructor(private readonly usersService: UsersService) {}\n  @Get()\n  findAll() {\n    return this.usersService.findAll();\n  }\n  @Post()\n  create(@Body() createUserDto: CreateUserDto) {\n    return this.usersService.create(createUserDto);\n  }\n}"),

    ("Spring Boot API", "Backend Framework",
     "Java-based framework API for building production-ready microservices and APIs.",
     "v3", "pivotal", "Java", "REST", "Open Source", "Low", "High", "REST", "Low",
     "@RestController\n@RequestMapping(\"/api/users\")\npublic class UserController {\n    @Autowired\n    private UserService userService;\n    @GetMapping\n    public List<User> getAllUsers() {\n        return userService.findAll();\n    }\n}"),

    ("Laravel API", "Backend Framework",
     "PHP web framework API with elegant syntax and comprehensive ecosystem.",
     "v11", "laravel", "PHP", "REST", "Open Source", "Low", "High", "MVC", "Low",
     "<?php\nuse Illuminate\\Http\\Request;\nuse App\\Models\\User;\nRoute::get('/users', function () {\n    return User::all();\n});"),

    ("Ruby on Rails API", "Backend Framework",
     "Full-stack web framework API with convention over configuration principles.",
     "v7", "rails", "Ruby", "REST", "Open Source", "Low", "High", "MVC", "Low",
     "class UsersController < ApplicationController\n  def index\n    @users = User.all\n    render json: @users\n  end\nend"),

    ("Hono API", "Backend Framework",
     "Ultrafast web framework API for the edge with zero dependencies.",
     "v4", "honojs", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "import { Hono } from 'hono';\nconst app = new Hono();\napp.get('/', (c) => c.text('Hello Hono!'));\napp.get('/users/:id', async (c) => { const id = c.req.param('id'); return c.json({ id }); });\nexport default app;"),

    ("Fastify API", "Backend Framework",
     "Fast and low overhead web framework API for Node.js.",
     "v4", "fastify", "JavaScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const fastify = require('fastify')({ logger: true });\nfastify.get('/users', async (request, reply) => {\n  return { users: await db.getUsers() };\n});\nawait fastify.listen({ port: 3000 });"),

    ("Strapi API", "Backend Framework",
     "Open source headless CMS API with customizable content types and REST/GraphQL.",
     "v4", "strapi", "JavaScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst articles = await axios.get('http://localhost:1337/api/articles', { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    ("Hasura API", "Backend Framework",
     "GraphQL API engine that auto-generates APIs from your database schema.",
     "v2", "hasura", "Multi-language", "GraphQL", "Open Source", "Low", "High", "GraphQL", "Low",
     "const axios = require('axios');\nconst response = await axios.post('https://YOUR_APP.hasura.app/v1/graphql', { query: '{ users { id name email } }' }, { headers: { 'x-hasura-admin-secret': 'YOUR_SECRET' } });"),

    # ── FRONTEND (8 entries) ──────────────────────────────────────────────────
    # Frontend frameworks and libraries for building user interfaces and fullstack apps.
    # Covers UI frameworks (React, Vue, Angular, Svelte), fullstack (Next.js),
    # data fetching (React Query), state management (Redux Toolkit), and tRPC.
    ("React", "Frontend",
     "The library for building user interfaces with component-based architecture.",
     "v19.2.5", "facebook", "JavaScript", "N/A", "Open Source", "Low", "High", "Component", "Low",
     "import { useState } from 'react';\n\nfunction Counter() {\n  const [count, setCount] = useState(0);\n  return (\n    <button onClick={() => setCount(count + 1)}>\n      Count: {count}\n    </button>\n  );\n}"),

    ("Vue.js", "Frontend",
     "Progressive JavaScript framework for building interactive user interfaces.",
     "v3.4", "vuejs", "JavaScript", "N/A", "Open Source", "Low", "High", "Component", "Low",
     "<template>\n  <button @click='count++'>Count: {{ count }}</button>\n</template>\n<script setup>\nimport { ref } from 'vue'\nconst count = ref(0)\n</script>"),

    ("Angular", "Frontend",
     "TypeScript-based framework by Google for building scalable enterprise web apps.",
     "v17", "google", "TypeScript", "N/A", "Open Source", "Low", "High", "MVC", "Low",
     "import { Component } from '@angular/core';\n\n@Component({\n  selector: 'app-root',\n  template: '<h1>Hello {{ title }}</h1>',\n})\nexport class AppComponent {\n  title = 'My App';\n}"),

    ("Svelte", "Frontend",
     "Cybernetically enhanced web apps — compiles components to vanilla JS at build time.",
     "v4", "svelte", "JavaScript", "N/A", "Open Source", "Low", "High", "Component", "Low",
     "<script>\n  let count = 0;\n</script>\n\n<button on:click={() => count++}>\n  Clicked {count} times\n</button>"),

    ("Next.js API Routes", "Frontend",
     "Fullstack React framework with built-in API routes and server-side rendering.",
     "v14", "vercel", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "// pages/api/hello.ts\nimport type { NextApiRequest, NextApiResponse } from 'next';\nexport default function handler(req: NextApiRequest, res: NextApiResponse) {\n  res.status(200).json({ message: 'Hello World!' });\n}"),

    ("React Query API", "Frontend",
     "Powerful data synchronization library for React with caching and background updates.",
     "v5", "tanstack", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "import { useQuery } from '@tanstack/react-query';\nconst { data, isLoading } = useQuery({ queryKey: ['users'], queryFn: async () => { const res = await fetch('/api/users'); return res.json(); } });"),

    ("Redux Toolkit API", "Frontend",
     "Official Redux state management API with simplified configuration and RTK Query.",
     "v2", "redux", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';\nexport const usersApi = createApi({ reducerPath: 'usersApi', baseQuery: fetchBaseQuery({ baseUrl: '/api' }), endpoints: (builder) => ({ getUsers: builder.query({ query: () => 'users' }) }) });"),

    ("tRPC API", "Frontend",
     "End-to-end typesafe API framework for TypeScript fullstack applications.",
     "v11", "trpc", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "import { initTRPC } from '@trpc/server';\nconst t = initTRPC.create();\nexport const appRouter = t.router({ greeting: t.procedure.input(z.object({ name: z.string() })).query(({ input }) => { return { message: `Hello ${input.name}!` }; }) });"),

    # ── API / GENERAL (47 entries) ────────────────────────────────────────────
    # General-purpose APIs across communication, data, media, and productivity.
    # Covers maps (Google Maps, Mapbox), weather (OpenWeatherMap), communication
    # (Twilio, SendGrid), social (GitHub, Slack, Discord, Spotify, Twitter/X),
    # e-commerce (Shopify, WooCommerce), CMS (Contentful, Sanity), CRM (HubSpot,
    # Salesforce), productivity (Notion, Airtable, Zoom), media (Cloudinary,
    # Pusher, Ably), finance (CoinGecko, Alpha Vantage), and public/free APIs.
    ("OpenWeatherMap API", "API",
     "Weather data API providing current, forecast, and historical weather information.",
     "v3", "openweather", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst weather = await axios.get('https://api.openweathermap.org/data/3.0/onecall', { params: { lat: 40.7128, lon: -74.0060, appid: 'YOUR_API_KEY', units: 'metric' } });"),

    ("Google Maps API", "API",
     "Mapping and location services API for embedding maps and geocoding.",
     "v3", "google", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Client } = require('@googlemaps/google-maps-services-js');\nconst client = new Client();\nconst result = await client.geocode({ params: { address: '1600 Amphitheatre Pkwy, Mountain View, CA', key: 'YOUR_API_KEY' } });"),

    ("Mapbox API", "API",
     "Location platform API for maps, navigation, and spatial analysis.",
     "v6", "mapbox", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import mapboxgl from 'mapbox-gl';\nmapboxgl.accessToken = 'YOUR_TOKEN';\nconst map = new mapboxgl.Map({ container: 'map', style: 'mapbox://styles/mapbox/streets-v12', center: [-74.5, 40], zoom: 9 });"),

    ("Twilio SMS API", "API",
     "Cloud communication API for SMS, voice calls, and messaging.",
     "v2010", "twilio", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const twilio = require('twilio');\nconst client = twilio('YOUR_ACCOUNT_SID', 'YOUR_AUTH_TOKEN');\nconst message = await client.messages.create({ body: 'Hello from Twilio!', from: '+1234567890', to: '+0987654321' });"),

    ("SendGrid API", "API",
     "Email delivery API for transactional and marketing email sending.",
     "v3", "twilio", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const sgMail = require('@sendgrid/mail');\nsgMail.setApiKey(process.env.SENDGRID_API_KEY);\nawait sgMail.send({ to: 'user@example.com', from: 'sender@example.com', subject: 'Hello!', text: 'Welcome!', html: '<strong>Welcome!</strong>' });"),

    ("GitHub API", "API",
     "Repository hosting API for managing code, issues, pull requests, and more.",
     "v4", "github", "Multi-language", "GraphQL", "Freemium", "Low", "High", "REST", "Low",
     "const { Octokit } = require('@octokit/rest');\nconst octokit = new Octokit({ auth: 'YOUR_TOKEN' });\nconst { data } = await octokit.rest.repos.listForUser({ username: 'octocat', per_page: 10 });"),

    ("Slack API", "API",
     "Team communication API for sending messages, managing channels, and building bots.",
     "v2", "slack", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { WebClient } = require('@slack/web-api');\nconst client = new WebClient('YOUR_TOKEN');\nawait client.chat.postMessage({ channel: '#general', text: 'Hello from the bot!' });"),

    ("Discord API", "API",
     "Gaming and community platform API for building bots and integrations.",
     "v10", "discord", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const { Client, GatewayIntentBits } = require('discord.js');\nconst client = new Client({ intents: [GatewayIntentBits.Guilds] });\nclient.on('ready', () => console.log(`Logged in as ${client.user.tag}`));\nclient.login('YOUR_TOKEN');"),

    ("Spotify API", "API",
     "Music streaming API for accessing tracks, playlists, and user listening data.",
     "v1", "spotify", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst tracks = await axios.get('https://api.spotify.com/v1/me/tracks', { headers: { Authorization: `Bearer ${accessToken}` } });"),

    ("Twitter/X API", "API",
     "Social media API for posting tweets, reading timelines, and user management.",
     "v2", "twitter", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { TwitterApi } = require('twitter-api-v2');\nconst client = new TwitterApi('YOUR_BEARER_TOKEN');\nconst tweets = await client.v2.search('Hello World', { 'tweet.fields': ['author_id', 'created_at'] });"),

    ("YouTube Data API", "API",
     "Video platform API for searching, uploading, and managing YouTube content.",
     "v3", "google", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { google } = require('googleapis');\nconst youtube = google.youtube({ version: 'v3', auth: 'YOUR_API_KEY' });\nconst response = await youtube.search.list({ part: ['snippet'], q: 'JavaScript tutorial', type: ['video'], maxResults: 10 });"),

    ("Notion API", "API",
     "Productivity platform API for reading and writing Notion pages and databases.",
     "v1", "notion", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const { Client } = require('@notionhq/client');\nconst notion = new Client({ auth: process.env.NOTION_TOKEN });\nconst response = await notion.databases.query({ database_id: 'YOUR_DATABASE_ID', filter: { property: 'Status', select: { equals: 'Done' } } });"),

    ("Airtable API", "API",
     "No-code database and spreadsheet API for managing structured data.",
     "v0", "airtable", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "High",
     "const Airtable = require('airtable');\nconst base = new Airtable({ apiKey: 'YOUR_KEY' }).base('YOUR_BASE_ID');\nconst records = await base('Table Name').select({ maxRecords: 10, view: 'Grid view' }).all();"),

    ("HubSpot API", "API",
     "CRM and marketing platform API for contacts, deals, and marketing automation.",
     "v3", "hubspot", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const hubspot = require('@hubspot/api-client');\nconst hubspotClient = new hubspot.Client({ accessToken: 'YOUR_TOKEN' });\nconst contacts = await hubspotClient.crm.contacts.basicApi.getPage(10);"),

    ("Salesforce API", "API",
     "CRM platform API for managing sales, service, and marketing data.",
     "v59", "salesforce", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const jsforce = require('jsforce');\nconst conn = new jsforce.Connection({ loginUrl: 'https://login.salesforce.com' });\nawait conn.login('user@example.com', 'password+securitytoken');\nconst accounts = await conn.query('SELECT Id, Name FROM Account LIMIT 10');"),

    ("Jira API", "API",
     "Project tracking API for agile teams with sprints, issues, and workflows.",
     "v3", "atlassian", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst issues = await axios.get('https://YOUR_DOMAIN.atlassian.net/rest/api/3/search', { params: { jql: 'project = MYPROJECT AND status = \"In Progress\"' }, headers: { Authorization: `Basic ${Buffer.from('email:token').toString('base64')}` } });"),

    ("Zoom API", "API",
     "Video conferencing API for managing meetings, webinars, and recordings.",
     "v2", "zoom", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst meetings = await axios.get('https://api.zoom.us/v2/users/me/meetings', { headers: { Authorization: `Bearer ${accessToken}` } });"),

    ("Google Calendar API", "API",
     "Calendar management API for creating and managing events and schedules.",
     "v3", "google", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const { google } = require('googleapis');\nconst calendar = google.calendar({ version: 'v3', auth });\nconst events = await calendar.events.list({ calendarId: 'primary', timeMin: new Date().toISOString(), maxResults: 10, singleEvents: true, orderBy: 'startTime' });"),

    ("Microsoft Graph API", "API",
     "Unified API for accessing Microsoft 365 services including Office, Teams, and OneDrive.",
     "v1", "microsoft", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Client } = require('@microsoft/microsoft-graph-client');\nconst client = Client.initWithMiddleware({ authProvider });\nconst user = await client.api('/me').get();\nconst emails = await client.api('/me/messages').top(10).get();"),

    ("Shopify API", "API",
     "E-commerce platform API for managing products, orders, and customer data.",
     "v2024", "shopify", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const { shopifyApi } = require('@shopify/shopify-api');\nconst shopify = shopifyApi({ apiKey: 'YOUR_KEY', apiSecretKey: 'YOUR_SECRET', scopes: ['read_products'], hostName: 'localhost:3000' });"),

    ("WooCommerce API", "API",
     "WordPress e-commerce REST API for managing products, orders, and customers.",
     "v3", "automattic", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const WooCommerceRestApi = require('@woocommerce/woocommerce-rest-api').default;\nconst api = new WooCommerceRestApi({ url: 'https://example.com', consumerKey: 'YOUR_KEY', consumerSecret: 'YOUR_SECRET', version: 'wc/v3' });\nconst products = await api.get('products', { per_page: 20 });"),

    ("Contentful API", "API",
     "Headless CMS API for managing and delivering structured content.",
     "v10", "contentful", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const contentful = require('contentful');\nconst client = contentful.createClient({ space: 'YOUR_SPACE_ID', accessToken: 'YOUR_ACCESS_TOKEN' });\nconst entries = await client.getEntries({ content_type: 'blogPost', limit: 10 });"),

    ("Sanity API", "API",
     "Structured content platform API with real-time collaboration and GROQ queries.",
     "v2021", "sanity", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { createClient } from '@sanity/client';\nconst client = createClient({ projectId: 'YOUR_PROJECT_ID', dataset: 'production', apiVersion: '2024-01-01', useCdn: true });\nconst posts = await client.fetch('*[_type == \"post\"][0...10]');"),

    ("Cloudinary API", "API",
     "Media management API for image and video upload, transformation, and delivery.",
     "v1", "cloudinary", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const cloudinary = require('cloudinary').v2;\ncloudinary.config({ cloud_name: 'YOUR_CLOUD', api_key: 'YOUR_KEY', api_secret: 'YOUR_SECRET' });\nconst result = await cloudinary.uploader.upload('image.jpg', { folder: 'products', transformation: [{ width: 800, crop: 'scale' }] });"),

    ("Pusher API", "API",
     "Real-time WebSocket API for adding live features to web and mobile apps.",
     "v7", "pusher", "Multi-language", "REST", "Freemium", "Low", "High", "Pub/Sub", "Low",
     "const Pusher = require('pusher');\nconst pusher = new Pusher({ appId: 'YOUR_ID', key: 'YOUR_KEY', secret: 'YOUR_SECRET', cluster: 'mt1', useTLS: true });\npusher.trigger('my-channel', 'my-event', { message: 'Hello!' });"),

    ("Ably API", "API",
     "Real-time messaging API with pub/sub, presence, and history capabilities.",
     "v2", "ably", "Multi-language", "REST", "Freemium", "Low", "High", "Pub/Sub", "Low",
     "const Ably = require('ably');\nconst client = new Ably.Realtime('YOUR_API_KEY');\nconst channel = client.channels.get('my-channel');\nchannel.publish('event', { message: 'Hello!' });\nchannel.subscribe((message) => console.log(message.data));"),

    ("Resend API", "API",
     "Modern email API built for developers with React email templates.",
     "v1", "resend", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { Resend } from 'resend';\nconst resend = new Resend('YOUR_API_KEY');\nawait resend.emails.send({ from: 'onboarding@resend.dev', to: 'user@example.com', subject: 'Hello World!', html: '<p>Welcome!</p>' });"),

    ("Postmark API", "API",
     "Transactional email API with fast delivery and detailed analytics.",
     "v1", "postmark", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const postmark = require('postmark');\nconst client = new postmark.ServerClient('YOUR_SERVER_TOKEN');\nawait client.sendEmail({ From: 'sender@example.com', To: 'recipient@example.com', Subject: 'Welcome!', TextBody: 'Hello!', HtmlBody: '<strong>Hello!</strong>' });"),

    ("Vonage API", "API",
     "Communication API for SMS, voice, video, and messaging channels.",
     "v3", "vonage", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const Vonage = require('@vonage/server-sdk');\nconst vonage = new Vonage({ apiKey: 'YOUR_KEY', apiSecret: 'YOUR_SECRET' });\nawait vonage.sms.send({ to: '15551234567', from: 'Vonage', text: 'Hello from Vonage!' });"),

    ("Zapier API", "API",
     "Workflow automation API for connecting apps and automating repetitive tasks.",
     "v1", "zapier", "Multi-language", "REST", "Freemium", "Medium", "High", "REST", "Low",
     "const response = await fetch('https://hooks.zapier.com/hooks/catch/YOUR_HOOK_ID/', {\n  method: 'POST',\n  body: JSON.stringify({ name: 'John', email: 'john@example.com' })\n});"),

    ("NASA API", "API",
     "Space agency API for astronomical data, Mars rover photos, and near-earth objects.",
     "v1", "nasa", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst apod = await axios.get('https://api.nasa.gov/planetary/apod', { params: { api_key: 'YOUR_API_KEY', date: '2024-01-01' } });"),

    ("CoinGecko API", "API",
     "Cryptocurrency data API for prices, market data, and coin information.",
     "v3", "coingecko", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst prices = await axios.get('https://api.coingecko.com/api/v3/simple/price', { params: { ids: 'bitcoin,ethereum', vs_currencies: 'usd' } });"),

    ("Alpha Vantage API", "API",
     "Stock market and financial data API for equities, forex, and cryptocurrency.",
     "v1", "alphavantage", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst quote = await axios.get('https://www.alphavantage.co/query', { params: { function: 'GLOBAL_QUOTE', symbol: 'AAPL', apikey: 'YOUR_API_KEY' } });"),

    ("NewsAPI", "API",
     "Breaking news and article search API from over 150,000 sources worldwide.",
     "v2", "newsapi", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst response = await axios.get('https://newsapi.org/v2/top-headlines', { params: { country: 'us', category: 'technology', apiKey: 'YOUR_API_KEY' } });"),

    ("PokeAPI", "API",
     "RESTful API for Pokémon data including species, moves, and abilities.",
     "v2", "pokeapi", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst pokemon = await axios.get('https://pokeapi.co/api/v2/pokemon/pikachu');\nconst { name, base_experience, height, weight, abilities } = pokemon.data;"),

    ("Unsplash API", "API",
     "High resolution photography API for accessing millions of free images.",
     "v1", "unsplash", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst photos = await axios.get('https://api.unsplash.com/photos', { params: { per_page: 10, order_by: 'popular' }, headers: { Authorization: 'Client-ID YOUR_ACCESS_KEY' } });"),

    ("IPinfo API", "API",
     "IP address geolocation API for identifying user location and network information.",
     "v1", "ipinfo", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst info = await axios.get('https://ipinfo.io/8.8.8.8/json', { params: { token: 'YOUR_TOKEN' } });\nconsole.log(info.data.city, info.data.country);"),

    ("Figma API", "API",
     "Design collaboration API for accessing Figma files, components, and comments.",
     "v1", "figma", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst file = await axios.get('https://api.figma.com/v1/files/YOUR_FILE_KEY', { headers: { 'X-Figma-Token': 'YOUR_TOKEN' } });"),

    ("Linear API", "API",
     "Project management API for software teams with issues, cycles, and roadmaps.",
     "v1", "linear", "Multi-language", "GraphQL", "Freemium", "Low", "High", "GraphQL", "Low",
     "const { LinearClient } = require('@linear/sdk');\nconst client = new LinearClient({ apiKey: 'YOUR_API_KEY' });\nconst issues = await client.issues({ filter: { state: { name: { eq: 'In Progress' } } } });"),

    ("GraphQL Yoga", "API",
     "Fully featured GraphQL server with subscriptions and plugin system.",
     "v4", "the-guild", "TypeScript", "GraphQL", "Open Source", "Low", "High", "GraphQL", "Low",
     "import { createYoga } from 'graphql-yoga';\nimport { createServer } from 'http';\nconst yoga = createYoga({ schema });\nconst server = createServer(yoga);\nserver.listen(4000, () => { console.log('Server is running on http://localhost:4000/graphql'); });"),

    ("tRPC", "API",
     "End-to-end typesafe API framework for TypeScript fullstack applications.",
     "v11", "trpc", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "import { initTRPC } from '@trpc/server';\nconst t = initTRPC.create();\nexport const appRouter = t.router({ greeting: t.procedure.input(z.object({ name: z.string() })).query(({ input }) => { return { message: `Hello ${input.name}!` }; }) });"),

    ("Apollo GraphQL", "API",
     "GraphQL platform for building, managing, and scaling APIs with a supergraph.",
     "v4", "apollographql", "JavaScript", "GraphQL", "Open Source", "Low", "High", "GraphQL", "Low",
     "const { ApolloServer } = require('@apollo/server');\nconst server = new ApolloServer({\n  typeDefs,\n  resolvers,\n});\nawait server.start();"),

    ("PDFKit API", "API",
     "PDF generation library API for creating PDF documents programmatically in Node.js.",
     "v0.14", "foliojs", "JavaScript", "N/A", "Open Source", "Low", "High", "N/A", "High",
     "const PDFDocument = require('pdfkit');\nconst doc = new PDFDocument();\ndoc.pipe(fs.createWriteStream('output.pdf'));\ndoc.fontSize(25).text('Hello World', 100, 100);\ndoc.end();"),

    ("Giphy API", "API",
     "GIF and sticker search API with a library of millions of animated images.",
     "v1", "giphy", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst gifs = await axios.get('https://api.giphy.com/v1/gifs/search', { params: { api_key: 'YOUR_KEY', q: 'happy', limit: 10, rating: 'g' } });"),

    ("Currency API", "API",
     "Real-time currency exchange rate API with 170+ currencies supported.",
     "v3", "currencyapi", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst rates = await axios.get('https://api.currencyapi.com/v3/latest', { params: { apikey: 'YOUR_KEY', currencies: 'EUR,GBP,JPY', base_currency: 'USD' } });"),

    ("REST Countries API", "API",
     "Public REST API providing information about countries, currencies, and languages.",
     "v3", "restcountries", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst countries = await axios.get('https://restcountries.com/v3.1/all');\nconst usa = await axios.get('https://restcountries.com/v3.1/name/united states');"),

    ("JSONPlaceholder API", "API",
     "Free fake REST API for testing and prototyping frontend applications.",
     "v1", "jsonplaceholder", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst posts = await axios.get('https://jsonplaceholder.typicode.com/posts');\nconst newPost = await axios.post('https://jsonplaceholder.typicode.com/posts', { title: 'Test Post', body: 'Content', userId: 1 });"),

    # ── SECURITY (7 entries) ──────────────────────────────────────────────────
    # Security and vulnerability APIs for protecting applications and user data.
    # Covers vulnerability scanning (Snyk), breach detection (HaveIBeenPwned),
    # secrets management (Vault), bot protection (reCAPTCHA), malware detection
    # (VirusTotal), WAF (Cloudflare), and SIEM (Splunk).
    ("Snyk API", "Security",
     "Developer security API for finding and fixing vulnerabilities in code and dependencies.",
     "v1", "snyk", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst issues = await axios.post('https://api.snyk.io/v1/test/npm', { encoding: 'plain', files: { target: { contents: JSON.stringify(require('./package.json')) } } }, { headers: { Authorization: `token ${process.env.SNYK_TOKEN}` } });"),

    ("HaveIBeenPwned API", "Security",
     "Data breach checking API to verify if email addresses have been compromised.",
     "v3", "hibp", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst breaches = await axios.get('https://haveibeenpwned.com/api/v3/breachedaccount/test@example.com', { headers: { 'hibp-api-key': 'YOUR_KEY', 'user-agent': 'MyApp' } });"),

    ("Vault API", "Security",
     "HashiCorp's secrets management API for securely storing and accessing secrets.",
     "v1", "hashicorp", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst secret = await axios.get('http://localhost:8200/v1/secret/data/my-secret', { headers: { 'X-Vault-Token': 'YOUR_TOKEN' } });\nconsole.log(secret.data.data.data);"),

    ("reCAPTCHA API", "Security",
     "Google's bot detection API for protecting websites from spam and abuse.",
     "v3", "google", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst verify = await axios.post('https://www.google.com/recaptcha/api/siteverify', new URLSearchParams({ secret: 'YOUR_SECRET_KEY', response: token, remoteip: req.ip }));\nif (!verify.data.success) throw new Error('reCAPTCHA failed');"),

    ("VirusTotal API", "Security",
     "File and URL scanning API for detecting malware and security threats.",
     "v3", "virustotal", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst analysis = await axios.get('https://www.virustotal.com/api/v3/urls/YOUR_URL_ID', { headers: { 'x-apikey': 'YOUR_API_KEY' } });"),

    ("Cloudflare WAF API", "Security",
     "Web application firewall API for protecting applications from attacks.",
     "v4", "cloudflare", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst rules = await axios.get('https://api.cloudflare.com/client/v4/zones/YOUR_ZONE_ID/firewall/rules', { headers: { Authorization: 'Bearer YOUR_TOKEN', 'Content-Type': 'application/json' } });"),

    ("Splunk API", "Security",
     "Security information and event management API for log analysis and threat detection.",
     "v9", "splunk", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst search = await axios.post('https://localhost:8089/services/search/jobs', new URLSearchParams({ search: 'search index=main | head 10', output_mode: 'json' }), { auth: { username: 'admin', password: 'YOUR_PASSWORD' } });"),

    # ── IOT (9 entries) ───────────────────────────────────────────────────────
    # Internet of Things platform APIs for connecting and managing smart devices.
    # Covers cloud IoT platforms (AWS IoT, Azure IoT Hub, Google Cloud IoT),
    # maker/hobbyist platforms (Particle, Adafruit IO, Blynk), analytics
    # (ThingSpeak), enterprise (Losant), and industrial (Ubidots).
    ("AWS IoT API", "IoT",
     "Amazon's IoT platform API for connecting and managing IoT devices at scale.",
     "v1", "amazon", "Multi-language", "REST", "Paid/Premium", "Low", "High", "Event-Driven", "Low",
     "const { IoTClient, ListThingsCommand } = require('@aws-sdk/client-iot');\nconst client = new IoTClient({ region: 'us-east-1' });\nconst things = await client.send(new ListThingsCommand({ maxResults: 100 }));"),

    ("Azure IoT Hub API", "IoT",
     "Microsoft's IoT hub API for connecting, monitoring, and managing IoT devices.",
     "v1", "microsoft", "Multi-language", "REST", "Paid/Premium", "Low", "High", "Event-Driven", "Low",
     "const { Registry } = require('azure-iothub');\nconst registry = Registry.fromConnectionString(process.env.IOTHUB_CONNECTION_STRING);\nconst devices = await registry.list();\nconsole.log(devices.responseBody);"),

    ("Google Cloud IoT API", "IoT",
     "IoT device management API for securely connecting and managing edge devices.",
     "v1", "google", "Multi-language", "REST", "Paid/Premium", "Low", "High", "Event-Driven", "Low",
     "const { DeviceManagerClient } = require('@google-cloud/iot');\nconst client = new DeviceManagerClient();\nconst devices = await client.listDevices({ parent: 'projects/YOUR_PROJECT/locations/us-central1/registries/YOUR_REGISTRY' });"),

    ("Particle API", "IoT",
     "IoT platform API for building and managing connected hardware products.",
     "v1", "particle", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const Particle = require('particle-api-js');\nconst particle = new Particle();\nawait particle.login({ username: 'user@example.com', password: 'password' });\nconst devices = await particle.listDevices({ auth: token });"),

    ("ThingSpeak API", "IoT",
     "IoT analytics API for collecting, analyzing, and visualizing sensor data.",
     "v1", "mathworks", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nawait axios.get('https://api.thingspeak.com/update', { params: { api_key: 'YOUR_WRITE_KEY', field1: 23.5, field2: 65 } });\nconst data = await axios.get('https://api.thingspeak.com/channels/YOUR_CHANNEL/feeds.json', { params: { api_key: 'YOUR_READ_KEY', results: 10 } });"),

    ("Adafruit IO API", "IoT",
     "IoT platform API for connecting hardware projects to the internet.",
     "v2", "adafruit", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const Adafruit_IO = require('adafruit-io-client');\nconst aio = new Adafruit_IO('YOUR_USERNAME', 'YOUR_KEY');\nconst feed = await aio.feeds('temperature');\nawait aio.data.create('temperature', { value: 23.5 });"),

    ("Losant API", "IoT",
     "Enterprise IoT platform API for device management and workflow automation.",
     "v1", "losant", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { LosantApi } = require('losant-rest');\nconst api = LosantApi({ credentials: { accessKey: 'YOUR_KEY', accessSecret: 'YOUR_SECRET' } });\nconst devices = await api.devices.get({ applicationId: 'YOUR_APP_ID' });"),

    ("Ubidots API", "IoT",
     "Industrial IoT platform API for connecting devices and building dashboards.",
     "v2", "ubidots", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nawait axios.post('https://industrial.api.ubidots.com/api/v1.6/devices/YOUR_DEVICE', { temperature: 23.5, humidity: 65 }, { headers: { 'X-Auth-Token': 'YOUR_TOKEN' } });"),

    ("Blynk API", "IoT",
     "IoT platform API for building mobile apps to control hardware projects.",
     "v2", "blynk", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst value = await axios.get(`https://blynk.cloud/external/api/get?token=YOUR_TOKEN&V0`);\nawait axios.get(`https://blynk.cloud/external/api/update?token=YOUR_TOKEN&V0=1`);"),

]


def seed():
    """
    Insert all seed entries into the database.

    Called automatically by app.py on startup.
    Uses 'Stripe API' by 'stripe' as a sentinel —
    if it already exists, the database has been seeded
    and this function returns immediately without doing anything.

    Safe to call from app.py on every deploy.
    Safe to run manually: python seed_data.py
    """
    already_seeded = ApiEntry.query.filter_by(
        name="Stripe API", developer="stripe"
    ).first()

    if already_seeded:
        print("[SEED] Already seeded — skipping.")
        return

    inserted = 0
    skipped = 0

    for row in SEED_DATA:
        (name, category, description, version, developer,
         language, framework, cost, latency, scalability,
         design_pattern, risk_level, sample_code) = row

        exists = ApiEntry.query.filter(
            db.func.lower(ApiEntry.name) == name.lower(),
            db.func.lower(ApiEntry.developer) == developer.lower()
        ).first()

        if exists:
            skipped += 1
            continue

        db.session.add(ApiEntry(
            name=name,
            category=category,
            description=description,
            version=version,
            developer=developer,
            risk_level=risk_level,
            programming_language=language,
            framework=framework,
            cost=cost,
            latency=latency,
            scalability=scalability,
            design_pattern=design_pattern,
            sample_code=sample_code,
        ))
        inserted += 1

    db.session.commit()

    total = ApiEntry.query.count()
    print(f"[SEED] Done! Inserted {inserted}, skipped {skipped}, total {total} entries.")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed()