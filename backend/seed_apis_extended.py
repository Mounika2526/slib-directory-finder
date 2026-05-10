"""
seed_apis_extended.py — Adds ~360 additional real API entries to SLIB Finder.

Usage:
    cd backend
    python seed_apis_extended.py

Safe to run multiple times — skips entries that already exist.
All entries have ALL fields filled so cards show "✓ Complete".
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, ApiEntry

SEED_DATA_EXTENDED = [

    # ── Payments ──────────────────────────────────────────────────────────────
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

    # ── Authentication ─────────────────────────────────────────────────────────
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

    # ── AI/ML ──────────────────────────────────────────────────────────────────
    ("Cohere API", "AI/ML",
     "NLP API for text generation, classification, embedding, and semantic search.",
     "v1", "cohere", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { CohereClient } = require('cohere-ai');\nconst cohere = new CohereClient({ token: 'YOUR_API_KEY' });\nconst response = await cohere.generate({ model: 'command', prompt: 'Write a story about', maxTokens: 200 });"),

    ("Mistral AI API", "AI/ML",
     "High performance open source large language model API for text generation.",
     "v1", "mistral", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst response = await axios.post('https://api.mistral.ai/v1/chat/completions', { model: 'mistral-tiny', messages: [{ role: 'user', content: 'Hello!' }] }, { headers: { Authorization: 'Bearer YOUR_API_KEY' } });"),

    ("Gemini API", "AI/ML",
     "Google's multimodal AI API for text, image, audio, and video understanding.",
     "v1", "google", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { GoogleGenerativeAI } = require('@google/generative-ai');\nconst genAI = new GoogleGenerativeAI('YOUR_API_KEY');\nconst model = genAI.getGenerativeModel({ model: 'gemini-pro' });\nconst result = await model.generateContent('Tell me a joke');"),

    ("Replicate API", "AI/ML",
     "Run machine learning models in the cloud with a simple API call.",
     "v1", "replicate", "Multi-language", "REST", "Paid/Premium", "Medium", "High", "REST", "Low",
     "import replicate from 'replicate';\nconst output = await replicate.run('stability-ai/stable-diffusion', { input: { prompt: 'A futuristic city' } });"),

    ("Runway ML API", "AI/ML",
     "Creative AI API for video generation, image editing, and visual effects.",
     "v1", "runwayml", "Multi-language", "REST", "Paid/Premium", "Medium", "High", "REST", "Low",
     "const axios = require('axios');\nconst response = await axios.post('https://api.runwayml.com/v1/image_to_video', { promptImage: 'https://example.com/image.jpg', model: 'gen3a_turbo' }, { headers: { Authorization: 'Bearer YOUR_API_KEY' } });"),

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

    ("Together AI API", "AI/ML",
     "API platform for running open source AI models with fast inference.",
     "v1", "togetherai", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst response = await axios.post('https://api.together.xyz/inference', { model: 'togethercomputer/llama-2-70b', prompt: 'Hello!', max_tokens: 512 }, { headers: { Authorization: 'Bearer YOUR_API_KEY' } });"),

    ("Groq API", "AI/ML",
     "Ultra-fast AI inference API for LLMs with low latency responses.",
     "v1", "groq", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const Groq = require('groq-sdk');\nconst groq = new Groq({ apiKey: 'YOUR_API_KEY' });\nconst completion = await groq.chat.completions.create({ messages: [{ role: 'user', content: 'Hello!' }], model: 'llama3-8b-8192' });"),

    ("Whisper API", "AI/ML",
     "OpenAI's speech-to-text API for accurate audio transcription.",
     "v1", "openai", "Multi-language", "REST", "Paid/Premium", "Medium", "High", "REST", "Low",
     "const OpenAI = require('openai');\nconst openai = new OpenAI({ apiKey: 'YOUR_API_KEY' });\nconst transcription = await openai.audio.transcriptions.create({ file: fs.createReadStream('audio.mp3'), model: 'whisper-1' });"),

    ("Midjourney API", "AI/ML",
     "AI image generation API for creating stunning visuals from text prompts.",
     "v6", "midjourney", "Multi-language", "REST", "Paid/Premium", "High", "High", "REST", "Medium",
     "const axios = require('axios');\nconst response = await axios.post('https://api.midjourney.com/v1/imagine', { prompt: 'A beautiful sunset over mountains', aspect_ratio: '16:9' }, { headers: { Authorization: 'Bearer YOUR_API_KEY' } });"),

    ("Anthropic Claude API", "AI/ML",
     "Powerful AI API for text generation, analysis, and reasoning tasks.",
     "v1", "anthropic", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const Anthropic = require('@anthropic-ai/sdk');\nconst client = new Anthropic({ apiKey: 'YOUR_API_KEY' });\nconst message = await client.messages.create({ model: 'claude-opus-4-5', max_tokens: 1024, messages: [{ role: 'user', content: 'Hello!' }] });"),

    # ── Cloud ──────────────────────────────────────────────────────────────────
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

    ("Linode API", "Cloud",
     "Cloud infrastructure API for managing virtual machines and Kubernetes clusters.",
     "v4", "akamai", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst linodes = await axios.get('https://api.linode.com/v4/linode/instances', { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

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

    ("Fly.io API", "Cloud",
     "Edge cloud platform API for deploying full-stack apps close to users.",
     "v1", "fly", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst apps = await axios.get('https://api.fly.io/v1/apps', { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    ("Render API", "Cloud",
     "Cloud platform API for deploying web services, databases, and static sites.",
     "v1", "render", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst services = await axios.get('https://api.render.com/v1/services', { headers: { Authorization: 'Bearer YOUR_API_KEY' } });"),

    ("Railway API", "Cloud",
     "Infrastructure platform API for deploying apps and databases instantly.",
     "v2", "railway", "Multi-language", "GraphQL", "Freemium", "Low", "High", "GraphQL", "Low",
     "const axios = require('axios');\nconst response = await axios.post('https://backboard.railway.app/graphql/v2', { query: '{ me { name email projects { edges { node { id name } } } } }' }, { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    # ── Database ──────────────────────────────────────────────────────────────
    ("PlanetScale API", "Database",
     "MySQL-compatible serverless database API with branching and schema changes.",
     "v1", "planetscale", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst databases = await axios.get('https://api.planetscale.com/v1/organizations/YOUR_ORG/databases', { headers: { Authorization: 'Basic YOUR_TOKEN' } });"),

    ("Supabase Database API", "Database",
     "PostgreSQL database API with real-time subscriptions and auto-generated REST API.",
     "v1", "supabase", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { createClient } from '@supabase/supabase-js';\nconst supabase = createClient('YOUR_URL', 'YOUR_KEY');\nconst { data, error } = await supabase.from('users').select('*').eq('status', 'active');"),

    ("Neon API", "Database",
     "Serverless PostgreSQL API with branching, autoscaling, and instant provisioning.",
     "v2", "neon", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Pool } = require('@neondatabase/serverless');\nconst pool = new Pool({ connectionString: process.env.DATABASE_URL });\nconst result = await pool.query('SELECT * FROM users WHERE active = $1', [true]);"),

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

    ("Firestore API", "Database",
     "Google's NoSQL document database API with real-time sync.",
     "v1", "google", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { getFirestore, collection, getDocs } from 'firebase/firestore';\nconst db = getFirestore();\nconst querySnapshot = await getDocs(collection(db, 'users'));\nquerySnapshot.forEach(doc => console.log(doc.id, doc.data()));"),

    ("Upstash Redis API", "Database",
     "Serverless Redis API with REST interface and global replication.",
     "v1", "upstash", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Redis } = require('@upstash/redis');\nconst redis = new Redis({ url: 'YOUR_URL', token: 'YOUR_TOKEN' });\nawait redis.set('key', 'value', { ex: 3600 });\nconst value = await redis.get('key');"),

    ("MongoDB Atlas API", "Database",
     "Fully managed cloud database API for MongoDB with global clusters.",
     "v2", "mongodb", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { MongoClient } = require('mongodb');\nconst client = new MongoClient(process.env.MONGODB_URI);\nawait client.connect();\nconst db = client.db('mydb');\nconst users = await db.collection('users').find({}).toArray();"),

    ("Xata API", "Database",
     "Serverless database API with branching, search, and analytics built-in.",
     "v1", "xata", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { XataClient } = require('./xata');\nconst xata = new XataClient({ apiKey: 'YOUR_API_KEY' });\nconst users = await xata.db.users.getAll();"),

    # ── DevOps ─────────────────────────────────────────────────────────────────
    ("GitLab API", "DevOps",
     "Complete DevOps platform API for source control, CI/CD, and project management.",
     "v4", "gitlab", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst projects = await axios.get('https://gitlab.com/api/v4/projects', { headers: { 'PRIVATE-TOKEN': 'YOUR_TOKEN' } });"),

    ("Bitbucket API", "DevOps",
     "Atlassian's Git repository API with built-in CI/CD pipelines.",
     "v2", "atlassian", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst repos = await axios.get('https://api.bitbucket.org/2.0/repositories/YOUR_WORKSPACE', { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    ("Travis CI API", "DevOps",
     "Continuous integration API for testing and deploying code from GitHub.",
     "v3", "travis", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst builds = await axios.get('https://api.travis-ci.com/repo/YOUR_REPO/builds', { headers: { Authorization: 'token YOUR_TOKEN', 'Travis-API-Version': '3' } });"),

    ("Jenkins API", "DevOps",
     "Open source automation API for building, testing, and deploying software.",
     "v2", "jenkins", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst jobs = await axios.get('http://localhost:8080/api/json?tree=jobs[name,url,color]', { auth: { username: 'admin', password: 'YOUR_TOKEN' } });"),

    ("ArgoCD API", "DevOps",
     "Declarative GitOps continuous delivery API for Kubernetes.",
     "v2", "argoproj", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst apps = await axios.get('https://argocd.example.com/api/v1/applications', { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    ("Terraform Cloud API", "DevOps",
     "Infrastructure as code API for managing cloud resources declaratively.",
     "v2", "hashicorp", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst workspaces = await axios.get('https://app.terraform.io/api/v2/organizations/YOUR_ORG/workspaces', { headers: { Authorization: 'Bearer YOUR_TOKEN', 'Content-Type': 'application/vnd.api+json' } });"),

    ("Ansible API", "DevOps",
     "IT automation API for configuration management and application deployment.",
     "v2", "redhat", "Python", "REST", "Open Source", "Low", "High", "REST", "Low",
     "import requests\nresponse = requests.get('http://localhost:8013/api/v2/jobs/', headers={'Authorization': 'Bearer YOUR_TOKEN'})\njobs = response.json()"),

    ("Kubernetes API", "DevOps",
     "Container orchestration API for automating deployment and scaling of applications.",
     "v1", "cncf", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const k8s = require('@kubernetes/client-node');\nconst kc = new k8s.KubeConfig();\nkc.loadFromDefault();\nconst k8sApi = kc.makeApiClient(k8s.CoreV1Api);\nconst pods = await k8sApi.listNamespacedPod('default');"),

    ("Docker Hub API", "DevOps",
     "Container registry API for managing Docker images and automated builds.",
     "v2", "docker", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst token = await axios.post('https://hub.docker.com/v2/users/login', { username: 'user', password: 'pass' });\nconst repos = await axios.get('https://hub.docker.com/v2/repositories/YOUR_USERNAME', { headers: { Authorization: `Bearer ${token.data.token}` } });"),

    ("Datadog CI API", "DevOps",
     "CI/CD visibility API for monitoring pipelines and test results.",
     "v2", "datadog", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst pipelines = await axios.get('https://api.datadoghq.com/api/v2/ci/pipelines', { headers: { 'DD-API-KEY': 'YOUR_KEY', 'DD-APPLICATION-KEY': 'YOUR_APP_KEY' } });"),

    ("Semaphore CI API", "DevOps",
     "Fast continuous integration API with Docker support and parallel jobs.",
     "v1alpha", "semaphoreci", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst workflows = await axios.get('https://api.semaphoreci.com/v1alpha/plumber-workflows', { headers: { Authorization: 'Token YOUR_TOKEN' } });"),

    # ── Analytics ──────────────────────────────────────────────────────────────
    ("Google Analytics API", "Analytics",
     "Web analytics API for tracking website traffic, user behavior, and conversions.",
     "v4", "google", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const { BetaAnalyticsDataClient } = require('@google-analytics/data');\nconst analyticsDataClient = new BetaAnalyticsDataClient();\nconst [response] = await analyticsDataClient.runReport({ property: 'properties/YOUR_PROPERTY_ID', dateRanges: [{ startDate: '30daysAgo', endDate: 'today' }], metrics: [{ name: 'activeUsers' }] });"),

    ("Mixpanel API", "Analytics",
     "Product analytics API for tracking user interactions and funnels.",
     "v2", "mixpanel", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const Mixpanel = require('mixpanel');\nconst mixpanel = Mixpanel.init('YOUR_TOKEN');\nmixpanel.track('Sign Up', { distinct_id: 'user123', plan: 'Premium' });"),

    ("Segment API", "Analytics",
     "Customer data platform API for collecting, cleaning, and routing analytics data.",
     "v1", "twilio", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Analytics } = require('@segment/analytics-node');\nconst analytics = new Analytics({ writeKey: 'YOUR_WRITE_KEY' });\nanalytics.track({ userId: 'user123', event: 'Item Purchased', properties: { price: 29.99, item: 'Pro Plan' } });"),

    ("Amplitude API", "Analytics",
     "Product analytics API for understanding user behavior and digital products.",
     "v2", "amplitude", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nawait axios.post('https://api2.amplitude.com/2/httpapi', { api_key: 'YOUR_API_KEY', events: [{ user_id: 'user123', event_type: 'button_click', event_properties: { button_name: 'signup' } }] });"),

    ("PostHog API", "Analytics",
     "Open source product analytics API with feature flags and session recording.",
     "v1", "posthog", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { PostHog } = require('posthog-node');\nconst client = new PostHog('YOUR_API_KEY', { host: 'https://app.posthog.com' });\nclient.capture({ distinctId: 'user123', event: 'user signed up' });"),

    ("Heap Analytics API", "Analytics",
     "Automatic event tracking API that captures all user interactions without code.",
     "v1", "heap", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nawait axios.post('https://heapanalytics.com/api/track', { app_id: 'YOUR_APP_ID', identity: 'user@example.com', event: 'Clicked Button', properties: { button: 'CTA' } });"),

    ("Plausible API", "Analytics",
     "Privacy-friendly web analytics API with no cookies and GDPR compliance.",
     "v1", "plausible", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst stats = await axios.get('https://plausible.io/api/v1/stats/summary', { params: { site_id: 'example.com', period: '30d' }, headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    ("Hotjar API", "Analytics",
     "User behavior analytics API with heatmaps, recordings, and feedback tools.",
     "v1", "hotjar", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst recordings = await axios.get('https://insights.hotjar.com/api/v1/sites/YOUR_SITE_ID/recordings', { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    ("Metabase API", "Analytics",
     "Open source business intelligence API for creating charts and dashboards.",
     "v0", "metabase", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst session = await axios.post('http://localhost:3000/api/session', { username: 'admin@example.com', password: 'password' });\nconst cards = await axios.get('http://localhost:3000/api/card', { headers: { 'X-Metabase-Session': session.data.id } });"),

    ("Looker API", "Analytics",
     "Business intelligence API for creating data models and embedded analytics.",
     "v4", "google", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const { Looker40SDK } = require('@looker/sdk');\nconst { NodeSession, NodeSettingsIniFile } = require('@looker/sdk-node');\nconst settings = new NodeSettingsIniFile();\nconst session = new NodeSession(settings);\nconst sdk = new Looker40SDK(session);"),

    ("Tableau API", "Analytics",
     "Data visualization platform API for creating interactive charts and dashboards.",
     "v3", "salesforce", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst auth = await axios.post('https://YOUR_SERVER/api/3.14/auth/signin', { credentials: { name: 'admin', password: 'password', site: { contentUrl: '' } } });\nconst token = auth.data.credentials.token;"),

    # ── Monitoring ─────────────────────────────────────────────────────────────
    ("Datadog API", "Monitoring",
     "Cloud monitoring and analytics API for infrastructure, applications, and logs.",
     "v2", "datadog", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const { v2 } = require('@datadog/datadog-api-client');\nconst configuration = v2.createConfiguration();\nconst apiInstance = new v2.MetricsApi(configuration);\nconst data = await apiInstance.queryScalarData({ body: { data: { attributes: { formulas: [{ formula: 'a' }], from: 1636629071000, queries: [{ data_source: 'metrics', name: 'a', query: 'avg:system.cpu.user{*}' }], to: 1636629671000 } } } });"),

    ("New Relic API", "Monitoring",
     "Full-stack observability API for monitoring applications and infrastructure.",
     "v2", "newrelic", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst response = await axios.post('https://api.newrelic.com/graphql', { query: '{ actor { account(id: YOUR_ACCOUNT_ID) { nrql(query: \"SELECT count(*) FROM Transaction SINCE 1 day ago\") { results } } } }' }, { headers: { 'API-Key': 'YOUR_KEY', 'Content-Type': 'application/json' } });"),

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
     "v0", "sentry", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const Sentry = require('@sentry/node');\nSentry.init({ dsn: 'YOUR_DSN', tracesSampleRate: 1.0 });\ntry {\n  doSomethingRisky();\n} catch (error) {\n  Sentry.captureException(error);\n}"),

    ("LogRocket API", "Monitoring",
     "Frontend monitoring API with session replay and performance tracking.",
     "v1", "logrocket", "JavaScript", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import LogRocket from 'logrocket';\nLogRocket.init('YOUR_APP_ID');\nLogRocket.identify('user123', { name: 'John Doe', email: 'john@example.com', subscriptionType: 'pro' });"),

    ("Uptime Robot API", "Monitoring",
     "Website monitoring API for tracking uptime and getting instant alerts.",
     "v2", "uptimerobot", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst monitors = await axios.post('https://api.uptimerobot.com/v2/getMonitors', new URLSearchParams({ api_key: 'YOUR_KEY', format: 'json' }));"),

    ("Elastic APM API", "Monitoring",
     "Application performance monitoring API built on the Elastic Stack.",
     "v1", "elastic", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const apm = require('elastic-apm-node').start({ serviceName: 'my-service', secretToken: 'YOUR_TOKEN', serverUrl: 'http://localhost:8200' });\nconst transaction = apm.startTransaction('my-transaction', 'request');"),

    ("Dynatrace API", "Monitoring",
     "AI-powered full-stack monitoring API for cloud infrastructure and applications.",
     "v2", "dynatrace", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst problems = await axios.get('https://YOUR_ENV.live.dynatrace.com/api/v2/problems', { headers: { Authorization: 'Api-Token YOUR_TOKEN' } });"),

    # ── Search ─────────────────────────────────────────────────────────────────
    ("Elasticsearch API", "Search",
     "Distributed search and analytics API for full-text and structured data.",
     "v8", "elastic", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Client } = require('@elastic/elasticsearch');\nconst client = new Client({ node: 'http://localhost:9200' });\nconst result = await client.search({ index: 'products', body: { query: { match: { name: 'laptop' } } } });"),

    ("Meilisearch API", "Search",
     "Open source, blazingly fast search API for building search experiences.",
     "v1", "meilisearch", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const { MeiliSearch } = require('meilisearch');\nconst client = new MeiliSearch({ host: 'http://localhost:7700', apiKey: 'YOUR_KEY' });\nconst index = client.index('products');\nconst results = await index.search('laptop', { limit: 10 });"),

    ("Solr API", "Search",
     "Enterprise search platform API based on Apache Lucene.",
     "v9", "apache", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst results = await axios.get('http://localhost:8983/solr/products/select', { params: { q: 'laptop', wt: 'json', rows: 10 } });"),

    ("Swiftype API", "Search",
     "Managed search API for adding site search and app search capabilities.",
     "v1", "elastic", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst results = await axios.get('https://api.swiftype.com/api/v1/engines/YOUR_ENGINE/search.json', { params: { auth_token: 'YOUR_TOKEN', q: 'laptop' } });"),

    ("Qdrant API", "Search",
     "Vector similarity search API for building AI-powered search applications.",
     "v1", "qdrant", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const { QdrantClient } = require('@qdrant/js-client-rest');\nconst client = new QdrantClient({ host: 'localhost', port: 6333 });\nconst results = await client.search('my_collection', { vector: [0.2, 0.1, 0.9], limit: 5 });"),

    ("Pinecone API", "Search",
     "Managed vector database API for semantic search and recommendation systems.",
     "v1", "pinecone", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Pinecone } = require('@pinecone-database/pinecone');\nconst pc = new Pinecone({ apiKey: 'YOUR_API_KEY' });\nconst index = pc.index('my-index');\nconst results = await index.query({ vector: [0.1, 0.2, 0.3], topK: 5 });"),

    ("Weaviate API", "Search",
     "Open source vector database API for semantic search and knowledge graphs.",
     "v1", "weaviate", "Multi-language", "REST", "Open Source", "Low", "High", "GraphQL", "Low",
     "import weaviate from 'weaviate-ts-client';\nconst client = weaviate.client({ scheme: 'http', host: 'localhost:8080' });\nconst result = await client.graphql.get().withClassName('Article').withFields('title content').withNearText({ concepts: ['machine learning'] }).withLimit(5).do();"),

    ("Typesense API", "Search",
     "Fast, typo-tolerant open-source search engine API alternative to Algolia.",
     "v0.25", "typesense", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const Typesense = require('typesense');\nconst client = new Typesense.Client({ nodes: [{ host: 'localhost', port: 8108, protocol: 'http' }], apiKey: 'YOUR_KEY' });\nconst results = await client.collections('products').documents().search({ q: 'laptop', query_by: 'name' });"),

    ("OpenSearch API", "Search",
     "Community-driven open source search and analytics API forked from Elasticsearch.",
     "v2", "amazon", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const { Client } = require('@opensearch-project/opensearch');\nconst client = new Client({ node: 'https://localhost:9200', auth: { username: 'admin', password: 'admin' } });\nconst result = await client.search({ index: 'movies', body: { query: { match: { title: 'Inception' } } } });"),

    # ── Microservice ───────────────────────────────────────────────────────────
    ("Kong Gateway API", "Microservice",
     "Open source API gateway and microservice management platform.",
     "v3", "kong", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst services = await axios.get('http://localhost:8001/services');\nconst newService = await axios.post('http://localhost:8001/services', { name: 'my-service', url: 'http://my-service:3000' });"),

    ("Istio API", "Microservice",
     "Service mesh API for connecting, securing, and monitoring microservices.",
     "v1", "google", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "kubectl apply -f - <<EOF\napiVersion: networking.istio.io/v1alpha3\nkind: VirtualService\nmetadata:\n  name: my-service\nspec:\n  hosts:\n  - my-service\n  http:\n  - route:\n    - destination:\n        host: my-service\n        port:\n          number: 9080\nEOF"),

    ("Consul API", "Microservice",
     "Service discovery and configuration API for distributed microservices.",
     "v1", "hashicorp", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst services = await axios.get('http://localhost:8500/v1/catalog/services');\nconst health = await axios.get('http://localhost:8500/v1/health/service/my-service?passing=true');"),

    ("Envoy Proxy API", "Microservice",
     "High-performance edge and service proxy API for cloud-native applications.",
     "v3", "cncf", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst stats = await axios.get('http://localhost:9901/stats?format=json');\nconst clusters = await axios.get('http://localhost:9901/clusters?format=json');"),

    ("NATS API", "Microservice",
     "High-performance messaging API for cloud-native microservices communication.",
     "v2", "nats", "Multi-language", "REST", "Open Source", "Low", "High", "Pub/Sub", "Low",
     "const { connect, StringCodec } = require('nats');\nconst nc = await connect({ servers: 'nats://localhost:4222' });\nconst sc = StringCodec();\nnc.publish('orders', sc.encode(JSON.stringify({ id: '123', total: 99.99 })));"),

    ("gRPC API", "Microservice",
     "High-performance remote procedure call API framework for microservices.",
     "v1", "google", "Multi-language", "gRPC", "Open Source", "Low", "High", "REST", "Low",
     "const grpc = require('@grpc/grpc-js');\nconst protoLoader = require('@grpc/proto-loader');\nconst packageDef = protoLoader.loadSync('service.proto');\nconst proto = grpc.loadPackageDefinition(packageDef);\nconst client = new proto.MyService('localhost:50051', grpc.credentials.createInsecure());"),

    ("Linkerd API", "Microservice",
     "Lightweight service mesh API for Kubernetes with automatic mTLS.",
     "v2", "buoyant", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst edges = await axios.get('http://localhost:8084/api/edges?resource_type=pod&namespace=default', { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    ("Dapr API", "Microservice",
     "Distributed application runtime API for building portable microservices.",
     "v1", "microsoft", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nawait axios.post('http://localhost:3500/v1.0/state/statestore', [{ key: 'order', value: { orderId: '123', total: 99.99 } }]);"),

    ("Temporal API", "Microservice",
     "Workflow orchestration API for building reliable distributed applications.",
     "v1", "temporal", "Multi-language", "REST", "Open Source", "Low", "High", "Event-Driven", "Low",
     "const { Connection, Client } = require('@temporalio/client');\nconst connection = await Connection.connect({ address: 'localhost:7233' });\nconst client = new Client({ connection });\nconst handle = await client.workflow.start(myWorkflow, { taskQueue: 'my-queue', workflowId: 'workflow-1' });"),

    ("Apache Kafka API", "Microservice",
     "Distributed event streaming API for high-throughput, fault-tolerant messaging.",
     "v3", "apache", "Multi-language", "REST", "Open Source", "Low", "High", "Event-Driven", "Low",
     "const { Kafka } = require('kafkajs');\nconst kafka = new Kafka({ clientId: 'my-app', brokers: ['localhost:9092'] });\nconst producer = kafka.producer();\nawait producer.connect();\nawait producer.send({ topic: 'orders', messages: [{ value: JSON.stringify({ orderId: '123' }) }] });"),

    # ── Frontend ───────────────────────────────────────────────────────────────
    ("Next.js API Routes", "Frontend",
     "Fullstack React framework with built-in API routes and server-side rendering.",
     "v14", "vercel", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "// pages/api/hello.ts\nimport type { NextApiRequest, NextApiResponse } from 'next';\nexport default function handler(req: NextApiRequest, res: NextApiResponse) {\n  res.status(200).json({ message: 'Hello World!' });\n}"),

    ("Remix API", "Frontend",
     "Full-stack web framework with nested routing and server-side data loading.",
     "v2", "shopify", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "// app/routes/api.users.ts\nimport { json } from '@remix-run/node';\nexport async function loader() {\n  const users = await db.user.findMany();\n  return json({ users });\n}"),

    ("SvelteKit API", "Frontend",
     "Full-stack Svelte framework with server endpoints and form actions.",
     "v2", "vercel", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "// src/routes/api/users/+server.ts\nimport { json } from '@sveltejs/kit';\nexport async function GET() {\n  const users = await db.getUsers();\n  return json(users);\n}"),

    ("Nuxt.js API", "Frontend",
     "Vue.js framework with server-side rendering and built-in API routes.",
     "v3", "nuxt", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "// server/api/users.get.ts\nexport default defineEventHandler(async (event) => {\n  const users = await db.getUsers();\n  return { users };\n});"),

    ("Astro API", "Frontend",
     "Static site builder with server endpoints and island architecture.",
     "v4", "astro", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "// src/pages/api/users.ts\nimport type { APIRoute } from 'astro';\nexport const GET: APIRoute = async ({ params, request }) => {\n  return new Response(JSON.stringify({ users: [] }), { status: 200 });\n};"),

    ("Tailwind CSS API", "Frontend",
     "Utility-first CSS framework with JIT compiler and design system integration.",
     "v3", "tailwindlabs", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "// tailwind.config.js\nmodule.exports = {\n  content: ['./src/**/*.{html,js,jsx,ts,tsx}'],\n  theme: {\n    extend: {\n      colors: { primary: '#3b82f6' }\n    }\n  },\n  plugins: [require('@tailwindcss/forms')]\n};"),

    ("React Query API", "Frontend",
     "Powerful data synchronization library for React with caching and background updates.",
     "v5", "tanstack", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "import { useQuery } from '@tanstack/react-query';\nconst { data, isLoading } = useQuery({ queryKey: ['users'], queryFn: async () => { const res = await fetch('/api/users'); return res.json(); } });"),

    ("Redux Toolkit API", "Frontend",
     "Official Redux state management API with simplified configuration and RTK Query.",
     "v2", "redux", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';\nexport const usersApi = createApi({ reducerPath: 'usersApi', baseQuery: fetchBaseQuery({ baseUrl: '/api' }), endpoints: (builder) => ({ getUsers: builder.query({ query: () => 'users' }) }) });"),

    ("GraphQL Yoga", "Frontend",
     "Fully featured GraphQL server with subscriptions and plugin system.",
     "v4", "the-guild", "TypeScript", "GraphQL", "Open Source", "Low", "High", "GraphQL", "Low",
     "import { createYoga } from 'graphql-yoga';\nimport { createServer } from 'http';\nconst yoga = createYoga({ schema });\nconst server = createServer(yoga);\nserver.listen(4000, () => { console.log('Server is running on http://localhost:4000/graphql'); });"),

    ("tRPC API", "Frontend",
     "End-to-end typesafe API framework for TypeScript fullstack applications.",
     "v11", "trpc", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "import { initTRPC } from '@trpc/server';\nconst t = initTRPC.create();\nexport const appRouter = t.router({ greeting: t.procedure.input(z.object({ name: z.string() })).query(({ input }) => { return { message: `Hello ${input.name}!` }; }) });"),

    ("Vite API", "Frontend",
     "Next-generation frontend build tool with hot module replacement and plugin API.",
     "v5", "vitejs", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "// vite.config.ts\nimport { defineConfig } from 'vite';\nimport react from '@vitejs/plugin-react';\nexport default defineConfig({ plugins: [react()], server: { proxy: { '/api': 'http://localhost:3000' } } });"),

    # ── Backend Framework ──────────────────────────────────────────────────────
    ("Hono API", "Backend Framework",
     "Ultrafast web framework API for the edge with zero dependencies.",
     "v4", "honojs", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "import { Hono } from 'hono';\nconst app = new Hono();\napp.get('/', (c) => c.text('Hello Hono!'));\napp.get('/users/:id', async (c) => { const id = c.req.param('id'); return c.json({ id }); });\nexport default app;"),

    ("Fastify API", "Backend Framework",
     "Fast and low overhead web framework API for Node.js.",
     "v4", "fastify", "JavaScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const fastify = require('fastify')({ logger: true });\nfastify.get('/users', async (request, reply) => {\n  return { users: await db.getUsers() };\n});\nawait fastify.listen({ port: 3000 });"),

    ("AdonisJS API", "Backend Framework",
     "Full-featured MVC framework API for Node.js with TypeScript support.",
     "v6", "adonisjs", "TypeScript", "REST", "Open Source", "Low", "High", "MVC", "Low",
     "import router from '@adonisjs/core/services/router';\nrouter.get('/users', [UsersController, 'index']);\nrouter.post('/users', [UsersController, 'store']);\nrouter.get('/users/:id', [UsersController, 'show']);"),

    ("Koa API", "Backend Framework",
     "Expressive middleware framework API for Node.js web applications.",
     "v2", "koajs", "JavaScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const Koa = require('koa');\nconst Router = require('@koa/router');\nconst app = new Koa();\nconst router = new Router();\nrouter.get('/users', async (ctx) => { ctx.body = await db.getUsers(); });\napp.use(router.routes());"),

    ("Feathers API", "Backend Framework",
     "Real-time application framework API with REST and WebSocket support.",
     "v5", "feathersjs", "JavaScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const { feathers } = require('@feathersjs/feathers');\nconst express = require('@feathersjs/express');\nconst app = express(feathers());\napp.use('/users', {\n  async find() { return db.getUsers(); }\n});"),

    ("Loopback API", "Backend Framework",
     "Highly extensible Node.js framework API for building REST and GraphQL services.",
     "v4", "ibm", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "import { get, response } from '@loopback/rest';\nexport class UserController {\n  @get('/users')\n  @response(200, { description: 'User list' })\n  async find(): Promise<User[]> {\n    return this.userRepository.find();\n  }\n}"),

    ("Strapi API", "Backend Framework",
     "Open source headless CMS API with customizable content types and REST/GraphQL.",
     "v4", "strapi", "JavaScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst articles = await axios.get('http://localhost:1337/api/articles', { headers: { Authorization: 'Bearer YOUR_TOKEN' } });\nconst newArticle = await axios.post('http://localhost:1337/api/articles', { data: { title: 'New Article', content: 'Content here' } }, { headers: { Authorization: 'Bearer YOUR_TOKEN' } });"),

    ("Directus API", "Backend Framework",
     "Open source data platform API with auto-generated REST and GraphQL endpoints.",
     "v10", "directus", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "import { createDirectus, rest, readItems } from '@directus/sdk';\nconst client = createDirectus('http://localhost:8055').with(rest());\nconst articles = await client.request(readItems('articles', { fields: ['*'], limit: 10 }));"),

    ("Payload CMS API", "Backend Framework",
     "TypeScript-first headless CMS API with built-in authentication and file management.",
     "v2", "payloadcms", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const payload = require('payload');\nawait payload.init({ secret: 'YOUR_SECRET', mongoURL: 'mongodb://localhost/payload' });\nconst users = await payload.find({ collection: 'users', limit: 10 });"),

    ("Hasura API", "Backend Framework",
     "GraphQL API engine that auto-generates APIs from your database schema.",
     "v2", "hasura", "Multi-language", "GraphQL", "Open Source", "Low", "High", "GraphQL", "Low",
     "const axios = require('axios');\nconst response = await axios.post('https://YOUR_APP.hasura.app/v1/graphql', { query: '{ users { id name email } }' }, { headers: { 'x-hasura-admin-secret': 'YOUR_SECRET' } });"),

    ("Flask API", "Backend Framework",
     "Lightweight Python web framework API for building REST services.",
     "v3", "pallets", "Python", "REST", "Open Source", "Low", "High", "REST", "Low",
     "from flask import Flask, jsonify, request\napp = Flask(__name__)\n@app.route('/users', methods=['GET'])\ndef get_users():\n    users = User.query.all()\n    return jsonify([u.to_dict() for u in users])\nif __name__ == '__main__':\n    app.run(debug=True)"),

    ("FastAPI Framework", "Backend Framework",
     "Modern, fast Python web framework API with automatic OpenAPI documentation.",
     "v0.110", "tiangolo", "Python", "REST", "Open Source", "Low", "High", "REST", "Low",
     "from fastapi import FastAPI\nfrom pydantic import BaseModel\napp = FastAPI()\nclass User(BaseModel):\n    name: str\n    email: str\n@app.get('/users')\nasync def get_users():\n    return await db.fetch_all('SELECT * FROM users')"),

    ("Django REST Framework", "Backend Framework",
     "Powerful toolkit for building Web APIs on top of Django.",
     "v3", "encode", "Python", "REST", "Open Source", "Low", "High", "REST", "Low",
     "from rest_framework import viewsets\nfrom .models import User\nfrom .serializers import UserSerializer\nclass UserViewSet(viewsets.ModelViewSet):\n    queryset = User.objects.all()\n    serializer_class = UserSerializer"),

    ("Laravel API", "Backend Framework",
     "PHP web framework API with elegant syntax and comprehensive ecosystem.",
     "v11", "laravel", "PHP", "REST", "Open Source", "Low", "High", "MVC", "Low",
     "<?php\nuse Illuminate\\Http\\Request;\nuse App\\Models\\User;\nRoute::get('/users', function () {\n    return User::all();\n});\nRoute::post('/users', function (Request $request) {\n    return User::create($request->validated());\n});"),

    ("Ruby on Rails API", "Backend Framework",
     "Full-stack web framework API with convention over configuration principles.",
     "v7", "rails", "Ruby", "REST", "Open Source", "Low", "High", "MVC", "Low",
     "class UsersController < ApplicationController\n  def index\n    @users = User.all\n    render json: @users\n  end\n  def create\n    @user = User.new(user_params)\n    if @user.save\n      render json: @user, status: :created\n    end\n  end\nend"),

    ("Spring Boot API", "Backend Framework",
     "Java-based framework API for building production-ready microservices and APIs.",
     "v3", "pivotal", "Java", "REST", "Open Source", "Low", "High", "REST", "Low",
     "@RestController\n@RequestMapping(\"/api/users\")\npublic class UserController {\n    @Autowired\n    private UserService userService;\n    @GetMapping\n    public List<User> getAllUsers() {\n        return userService.findAll();\n    }\n    @PostMapping\n    public User createUser(@RequestBody User user) {\n        return userService.save(user);\n    }\n}"),

    ("NestJS Framework", "Backend Framework",
     "Progressive Node.js framework API for building scalable server-side applications.",
     "v10", "nestjs", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "@Controller('users')\nexport class UsersController {\n  constructor(private readonly usersService: UsersService) {}\n  @Get()\n  findAll() {\n    return this.usersService.findAll();\n  }\n  @Post()\n  create(@Body() createUserDto: CreateUserDto) {\n    return this.usersService.create(createUserDto);\n  }\n}"),

    # ── API ────────────────────────────────────────────────────────────────────
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

    ("Mailchimp API", "API",
     "Email marketing API for managing subscribers, campaigns, and automation.",
     "v3", "mailchimp", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const mailchimp = require('@mailchimp/mailchimp_marketing');\nmailchimp.setConfig({ apiKey: 'YOUR_API_KEY', server: 'us21' });\nconst response = await mailchimp.lists.addListMember('LIST_ID', { email_address: 'user@example.com', status: 'subscribed' });"),

    ("Spotify API", "API",
     "Music streaming API for accessing tracks, playlists, and user listening data.",
     "v1", "spotify", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst tracks = await axios.get('https://api.spotify.com/v1/me/tracks', { headers: { Authorization: `Bearer ${accessToken}` } });\nconst search = await axios.get('https://api.spotify.com/v1/search', { params: { q: 'Bohemian Rhapsody', type: 'track' }, headers: { Authorization: `Bearer ${accessToken}` } });"),

    ("Twitter/X API", "API",
     "Social media API for posting tweets, reading timelines, and user management.",
     "v2", "twitter", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { TwitterApi } = require('twitter-api-v2');\nconst client = new TwitterApi('YOUR_BEARER_TOKEN');\nconst tweets = await client.v2.search('Hello World', { 'tweet.fields': ['author_id', 'created_at'] });"),

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

    ("YouTube Data API", "API",
     "Video platform API for searching, uploading, and managing YouTube content.",
     "v3", "google", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { google } = require('googleapis');\nconst youtube = google.youtube({ version: 'v3', auth: 'YOUR_API_KEY' });\nconst response = await youtube.search.list({ part: ['snippet'], q: 'JavaScript tutorial', type: ['video'], maxResults: 10 });"),

    ("NewsAPI", "API",
     "Breaking news and article search API from over 150,000 sources worldwide.",
     "v2", "newsapi", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst response = await axios.get('https://newsapi.org/v2/top-headlines', { params: { country: 'us', category: 'technology', apiKey: 'YOUR_API_KEY' } });"),

    ("CoinGecko API", "API",
     "Cryptocurrency data API for prices, market data, and coin information.",
     "v3", "coingecko", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst prices = await axios.get('https://api.coingecko.com/api/v3/simple/price', { params: { ids: 'bitcoin,ethereum', vs_currencies: 'usd' } });"),

    ("Alpha Vantage API", "API",
     "Stock market and financial data API for equities, forex, and cryptocurrency.",
     "v1", "alphavantage", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst quote = await axios.get('https://www.alphavantage.co/query', { params: { function: 'GLOBAL_QUOTE', symbol: 'AAPL', apikey: 'YOUR_API_KEY' } });"),

    ("NASA API", "API",
     "Space agency API for astronomical data, Mars rover photos, and near-earth objects.",
     "v1", "nasa", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst apod = await axios.get('https://api.nasa.gov/planetary/apod', { params: { api_key: 'YOUR_API_KEY', date: '2024-01-01' } });\nconst marsPhotos = await axios.get('https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos', { params: { sol: 1000, api_key: 'YOUR_API_KEY' } });"),

    ("OpenFDA API", "API",
     "FDA open data API for drug information, adverse events, and medical device reports.",
     "v1", "fda", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst drugs = await axios.get('https://api.fda.gov/drug/label.json', { params: { search: 'brand_name:aspirin', limit: 5 } });"),

    ("Open Library API", "API",
     "Internet Archive's book catalog API for book metadata and reading lists.",
     "v1", "internetarchive", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst book = await axios.get('https://openlibrary.org/api/books', { params: { bibkeys: 'ISBN:9780140449136', format: 'json', jscmd: 'data' } });"),

    ("PokeAPI", "API",
     "RESTful API for Pokémon data including species, moves, and abilities.",
     "v2", "pokeapi", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst pokemon = await axios.get('https://pokeapi.co/api/v2/pokemon/pikachu');\nconst { name, base_experience, height, weight, abilities } = pokemon.data;"),

    ("Rick and Morty API", "API",
     "RESTful API for Rick and Morty character, episode, and location data.",
     "v2", "rickandmortyapi", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst characters = await axios.get('https://rickandmortyapi.com/api/character', { params: { status: 'alive', species: 'Human' } });\nconsole.log(characters.data.results);"),

    ("JSONPlaceholder API", "API",
     "Free fake REST API for testing and prototyping frontend applications.",
     "v1", "jsonplaceholder", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst posts = await axios.get('https://jsonplaceholder.typicode.com/posts');\nconst newPost = await axios.post('https://jsonplaceholder.typicode.com/posts', { title: 'Test Post', body: 'Content', userId: 1 });"),

    ("REST Countries API", "API",
     "Public REST API providing information about countries, currencies, and languages.",
     "v3", "restcountries", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst countries = await axios.get('https://restcountries.com/v3.1/all');\nconst usa = await axios.get('https://restcountries.com/v3.1/name/united states');"),

    ("Unsplash API", "API",
     "High resolution photography API for accessing millions of free images.",
     "v1", "unsplash", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst photos = await axios.get('https://api.unsplash.com/photos', { params: { per_page: 10, order_by: 'popular' }, headers: { Authorization: 'Client-ID YOUR_ACCESS_KEY' } });"),

    ("Pexels API", "API",
     "Free stock photo and video API with millions of professionally curated assets.",
     "v1", "pexels", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst photos = await axios.get('https://api.pexels.com/v1/search', { params: { query: 'nature', per_page: 15 }, headers: { Authorization: 'YOUR_API_KEY' } });"),

    ("IPinfo API", "API",
     "IP address geolocation API for identifying user location and network information.",
     "v1", "ipinfo", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst info = await axios.get('https://ipinfo.io/8.8.8.8/json', { params: { token: 'YOUR_TOKEN' } });\nconsole.log(info.data.city, info.data.country);"),

    ("Abstract API", "API",
     "Suite of utility APIs for email validation, phone validation, and IP geolocation.",
     "v1", "abstractapi", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst validation = await axios.get('https://emailvalidation.abstractapi.com/v1/', { params: { api_key: 'YOUR_KEY', email: 'test@example.com' } });"),

    ("Hunter.io API", "API",
     "Email finder and verification API for finding professional email addresses.",
     "v2", "hunter", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst result = await axios.get('https://api.hunter.io/v2/domain-search', { params: { domain: 'example.com', api_key: 'YOUR_API_KEY' } });"),

    ("Clearbit API", "API",
     "Business intelligence API for enriching leads with company and contact data.",
     "v2", "clearbit", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const clearbit = require('clearbit')('YOUR_KEY');\nconst company = await clearbit.Company.find({ domain: 'github.com' });\nconst person = await clearbit.Person.find({ email: 'user@example.com' });"),

    ("Zendesk API", "API",
     "Customer service platform API for managing support tickets and help desk operations.",
     "v2", "zendesk", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst tickets = await axios.get('https://YOUR_SUBDOMAIN.zendesk.com/api/v2/tickets.json', { auth: { username: 'user@example.com/token', password: 'YOUR_TOKEN' } });"),

    ("Intercom API", "API",
     "Customer messaging platform API for support, engagement, and user management.",
     "v2", "intercom", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const { Client } = require('intercom-client');\nconst client = new Client({ tokenAuth: { token: 'YOUR_TOKEN' } });\nconst contact = await client.contacts.find({ id: 'CONTACT_ID' });"),

    ("HubSpot API", "API",
     "CRM and marketing platform API for contacts, deals, and marketing automation.",
     "v3", "hubspot", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const hubspot = require('@hubspot/api-client');\nconst hubspotClient = new hubspot.Client({ accessToken: 'YOUR_TOKEN' });\nconst contacts = await hubspotClient.crm.contacts.basicApi.getPage(10);"),

    ("Salesforce API", "API",
     "CRM platform API for managing sales, service, and marketing data.",
     "v59", "salesforce", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const jsforce = require('jsforce');\nconst conn = new jsforce.Connection({ loginUrl: 'https://login.salesforce.com' });\nawait conn.login('user@example.com', 'password+securitytoken');\nconst accounts = await conn.query('SELECT Id, Name FROM Account LIMIT 10');"),

    ("Airtable API", "API",
     "No-code database and spreadsheet API for managing structured data.",
     "v0", "airtable", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const Airtable = require('airtable');\nconst base = new Airtable({ apiKey: 'YOUR_KEY' }).base('YOUR_BASE_ID');\nconst records = await base('Table Name').select({ maxRecords: 10, view: 'Grid view' }).all();"),

    ("Notion API", "API",
     "Productivity platform API for reading and writing Notion pages and databases.",
     "v1", "notion", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const { Client } = require('@notionhq/client');\nconst notion = new Client({ auth: process.env.NOTION_TOKEN });\nconst response = await notion.databases.query({ database_id: 'YOUR_DATABASE_ID', filter: { property: 'Status', select: { equals: 'Done' } } });"),

    ("Figma API", "API",
     "Design collaboration API for accessing Figma files, components, and comments.",
     "v1", "figma", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst file = await axios.get('https://api.figma.com/v1/files/YOUR_FILE_KEY', { headers: { 'X-Figma-Token': 'YOUR_TOKEN' } });"),

    ("Linear API", "API",
     "Project management API for software teams with issues, cycles, and roadmaps.",
     "v1", "linear", "Multi-language", "GraphQL", "Freemium", "Low", "High", "GraphQL", "Low",
     "const { LinearClient } = require('@linear/sdk');\nconst client = new LinearClient({ apiKey: 'YOUR_API_KEY' });\nconst issues = await client.issues({ filter: { state: { name: { eq: 'In Progress' } } } });"),

    ("Jira API", "API",
     "Project tracking API for agile teams with sprints, issues, and workflows.",
     "v3", "atlassian", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst issues = await axios.get('https://YOUR_DOMAIN.atlassian.net/rest/api/3/search', { params: { jql: 'project = MYPROJECT AND status = \"In Progress\"' }, headers: { Authorization: `Basic ${Buffer.from('email:token').toString('base64')}` } });"),

    ("Asana API", "API",
     "Work management API for tasks, projects, and team collaboration.",
     "v1", "asana", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const asana = require('asana');\nconst client = asana.ApiClient.instance;\nclient.authentications['token'].accessToken = 'YOUR_TOKEN';\nconst tasksApi = new asana.TasksApi();\nconst tasks = await tasksApi.getTasks({ project: 'PROJECT_ID' });"),

    ("Trello API", "API",
     "Kanban board API for managing cards, lists, and team projects.",
     "v1", "atlassian", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst boards = await axios.get('https://api.trello.com/1/members/me/boards', { params: { key: 'YOUR_KEY', token: 'YOUR_TOKEN' } });"),

    ("Zoom API", "API",
     "Video conferencing API for managing meetings, webinars, and recordings.",
     "v2", "zoom", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst meetings = await axios.get('https://api.zoom.us/v2/users/me/meetings', { headers: { Authorization: `Bearer ${accessToken}` } });\nconst newMeeting = await axios.post('https://api.zoom.us/v2/users/me/meetings', { topic: 'Team Sync', type: 2, start_time: '2024-01-01T10:00:00Z' }, { headers: { Authorization: `Bearer ${accessToken}` } });"),

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
     "const { shopifyApi } = require('@shopify/shopify-api');\nconst shopify = shopifyApi({ apiKey: 'YOUR_KEY', apiSecretKey: 'YOUR_SECRET', scopes: ['read_products'], hostName: 'localhost:3000' });\nconst client = new shopify.clients.Rest({ session });"),

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

    ("Imgix API", "API",
     "Image processing and optimization API for real-time image transformations.",
     "v3", "imgix", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const ImgixClient = require('@imgix/js-core');\nconst client = new ImgixClient({ domain: 'YOUR_DOMAIN.imgix.net', secureURLToken: 'YOUR_TOKEN' });\nconst url = client.buildURL('/path/to/image.jpg', { w: 800, h: 600, fit: 'crop', auto: 'format' });"),

    ("Pusher API", "API",
     "Real-time WebSocket API for adding live features to web and mobile apps.",
     "v7", "pusher", "Multi-language", "REST", "Freemium", "Low", "High", "Pub/Sub", "Low",
     "const Pusher = require('pusher');\nconst pusher = new Pusher({ appId: 'YOUR_ID', key: 'YOUR_KEY', secret: 'YOUR_SECRET', cluster: 'mt1', useTLS: true });\npusher.trigger('my-channel', 'my-event', { message: 'Hello!' });"),

    ("Ably API", "API",
     "Real-time messaging API with pub/sub, presence, and history capabilities.",
     "v2", "ably", "Multi-language", "REST", "Freemium", "Low", "High", "Pub/Sub", "Low",
     "const Ably = require('ably');\nconst client = new Ably.Realtime('YOUR_API_KEY');\nconst channel = client.channels.get('my-channel');\nchannel.publish('event', { message: 'Hello!' });\nchannel.subscribe((message) => console.log(message.data));"),

    ("Liveblocks API", "API",
     "Real-time collaboration API for building multiplayer experiences.",
     "v2", "liveblocks", "TypeScript", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { createClient } from '@liveblocks/client';\nconst client = createClient({ publicApiKey: 'YOUR_KEY' });\nconst { room, leave } = client.enterRoom('my-room');\nconst storage = await room.getStorage();"),

    ("Socket.io API", "API",
     "Bidirectional real-time communication API for web applications.",
     "v4", "socketio", "JavaScript", "REST", "Open Source", "Low", "High", "Event-Driven", "Low",
     "const { Server } = require('socket.io');\nconst io = new Server(server, { cors: { origin: '*' } });\nio.on('connection', (socket) => {\n  socket.on('message', (data) => {\n    io.emit('message', data);\n  });\n});"),

    ("Postmark API", "API",
     "Transactional email API with fast delivery and detailed analytics.",
     "v1", "postmark", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const postmark = require('postmark');\nconst client = new postmark.ServerClient('YOUR_SERVER_TOKEN');\nawait client.sendEmail({ From: 'sender@example.com', To: 'recipient@example.com', Subject: 'Welcome!', TextBody: 'Hello!', HtmlBody: '<strong>Hello!</strong>' });"),

    ("Resend API", "API",
     "Modern email API built for developers with React email templates.",
     "v1", "resend", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { Resend } from 'resend';\nconst resend = new Resend('YOUR_API_KEY');\nawait resend.emails.send({ from: 'onboarding@resend.dev', to: 'user@example.com', subject: 'Hello World!', html: '<p>Welcome!</p>' });"),

    ("Vonage API", "API",
     "Communication API for SMS, voice, video, and messaging channels.",
     "v3", "vonage", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const Vonage = require('@vonage/server-sdk');\nconst vonage = new Vonage({ apiKey: 'YOUR_KEY', apiSecret: 'YOUR_SECRET' });\nawait vonage.sms.send({ to: '15551234567', from: 'Vonage', text: 'Hello from Vonage!' });"),

    ("MessageBird API", "API",
     "Cloud communication API for SMS, voice, email, and WhatsApp messaging.",
     "v2", "messagebird", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const messagebird = require('messagebird')('YOUR_ACCESS_KEY');\nmessagebird.messages.create({ originator: 'MessageBird', recipients: ['31612345678'], body: 'Hello World!' }, (err, response) => { if (err) console.log(err); });"),

    ("PDFkit API", "API",
     "PDF generation library API for creating PDF documents programmatically.",
     "v0.14", "foliojs", "JavaScript", "REST", "Open Source", "Low", "High", "REST", "High",
     "const PDFDocument = require('pdfkit');\nconst doc = new PDFDocument();\ndoc.pipe(fs.createWriteStream('output.pdf'));\ndoc.fontSize(25).text('Hello World!', 100, 100);\ndoc.end();"),

    ("Sharp API", "API",
     "High performance Node.js image processing API for resizing and converting images.",
     "v0.34", "lovell", "JavaScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const sharp = require('sharp');\nawait sharp('input.jpg')\n  .resize(800, 600, { fit: 'cover' })\n  .webp({ quality: 80 })\n  .toFile('output.webp');"),

    ("QR Code API", "API",
     "QR code generation API for creating customizable QR codes from URLs and text.",
     "v1", "qrserver", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst response = await axios.get('https://api.qrserver.com/v1/create-qr-code/', { params: { size: '200x200', data: 'https://example.com' }, responseType: 'arraybuffer' });\nfs.writeFileSync('qr.png', response.data);"),

    ("Currency API", "API",
     "Real-time currency exchange rate API with 170+ currencies supported.",
     "v3", "currencyapi", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst rates = await axios.get('https://api.currencyapi.com/v3/latest', { params: { apikey: 'YOUR_KEY', currencies: 'EUR,GBP,JPY', base_currency: 'USD' } });"),

    ("Giphy API", "API",
     "GIF and sticker search API with a library of millions of animated images.",
     "v1", "giphy", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst gifs = await axios.get('https://api.giphy.com/v1/gifs/search', { params: { api_key: 'YOUR_KEY', q: 'happy', limit: 10, rating: 'g' } });"),

    # ── Security ────────────────────────────────────────────────────────────────
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

    ("Cloudflare WAF API", "Security",
     "Web application firewall API for protecting applications from attacks.",
     "v4", "cloudflare", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst rules = await axios.get('https://api.cloudflare.com/client/v4/zones/YOUR_ZONE_ID/firewall/rules', { headers: { Authorization: 'Bearer YOUR_TOKEN', 'Content-Type': 'application/json' } });"),

    ("reCAPTCHA API", "Security",
     "Google's bot detection API for protecting websites from spam and abuse.",
     "v3", "google", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst verify = await axios.post('https://www.google.com/recaptcha/api/siteverify', new URLSearchParams({ secret: 'YOUR_SECRET_KEY', response: token, remoteip: req.ip }));\nif (!verify.data.success) throw new Error('reCAPTCHA failed');"),

    ("VirusTotal API", "Security",
     "File and URL scanning API for detecting malware and security threats.",
     "v3", "virustotal", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst analysis = await axios.get('https://www.virustotal.com/api/v3/urls/YOUR_URL_ID', { headers: { 'x-apikey': 'YOUR_API_KEY' } });"),

    ("Okta Threat Insight API", "Security",
     "Security intelligence API for detecting and preventing identity-based threats.",
     "v1", "okta", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst threats = await axios.get('https://YOUR_DOMAIN.okta.com/api/v1/threats/configuration', { headers: { Authorization: `SSWS ${process.env.OKTA_TOKEN}` } });"),

    ("Splunk API", "Security",
     "Security information and event management API for log analysis and threat detection.",
     "v9", "splunk", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst search = await axios.post('https://localhost:8089/services/search/jobs', new URLSearchParams({ search: 'search index=main | head 10', output_mode: 'json' }), { auth: { username: 'admin', password: 'YOUR_PASSWORD' }, httpsAgent: new https.Agent({ rejectUnauthorized: false }) });"),

    ("Auth Shield API", "Security",
     "Multi-factor authentication API with TOTP, SMS, and biometric verification.",
     "v2", "authshield", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst mfa = await axios.post('https://api.authshield.com/v2/verify', { userId: 'user123', token: '123456', method: 'totp' }, { headers: { Authorization: 'Bearer YOUR_API_KEY' } });"),

    # ── IoT ─────────────────────────────────────────────────────────────────────
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

    ("Hologram API", "IoT",
     "Cellular connectivity API for IoT devices with global SIM card management.",
     "v1", "hologram", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const axios = require('axios');\nconst devices = await axios.get('https://dashboard.hologram.io/api/1/devices', { params: { apikey: 'YOUR_API_KEY' } });\nconst sms = await axios.post('https://dashboard.hologram.io/api/1/sms/incoming', { apikey: 'YOUR_KEY', deviceid: 12345, data: 'Hello IoT device!' });"),

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
    with app.app_context():
        db.create_all()

        inserted = 0
        skipped = 0

        for row in SEED_DATA_EXTENDED:
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