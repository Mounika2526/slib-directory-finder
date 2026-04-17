"""
seed_apis.py — Populates the SLIB Finder database with 100+ real API entries.

Usage:
    cd backend
    python seed_apis.py

This script connects to the same SQLite database used by app.py (apis.db)
and inserts 100+ well-known real-world APIs and microservices.
Each entry has ALL fields filled so cards show "✓ Complete".

Safe to run multiple times — skips entries that already exist.
"""

import os
import sys

# ── Make sure we can import from app.py ──────────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, ApiEntry

# ── 100+ Real API entries ─────────────────────────────────────────────────────
# Format: (name, category, description, version, developer,
#          language, framework, cost, latency, scalability,
#          design_pattern, risk_level, sample_code)

SEED_DATA = [
    # ── Payments ──────────────────────────────────────────────────────────────
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

    # ── Authentication ─────────────────────────────────────────────────────────
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

    # ── AI/ML ──────────────────────────────────────────────────────────────────
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

    # ── Cloud ──────────────────────────────────────────────────────────────────
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
     "DigitalOcean's API for managing droplets, databases, and cloud infrastructure.",
     "v2", "digitalocean", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const response = await fetch('https://api.digitalocean.com/v2/droplets', {\n  headers: { 'Authorization': 'Bearer YOUR_TOKEN' }\n});"),

    ("Vercel API", "Cloud",
     "Vercel's deployment and hosting API for managing projects and deployments.",
     "v9", "vercel", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const response = await fetch('https://api.vercel.com/v9/projects', {\n  headers: { 'Authorization': 'Bearer YOUR_TOKEN' }\n});"),

    ("Netlify API", "Cloud",
     "API for managing Netlify sites, deployments, forms, and serverless functions.",
     "v1", "netlify", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const NetlifyAPI = require('netlify');\nconst client = new NetlifyAPI('YOUR_TOKEN');\nconst sites = await client.listSites();"),

    # ── Database ───────────────────────────────────────────────────────────────
    ("Supabase API", "Database",
     "Open source Firebase alternative with PostgreSQL, auth, and realtime subscriptions.",
     "v1", "supabase", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { createClient } from '@supabase/supabase-js';\nconst supabase = createClient('YOUR_URL', 'YOUR_KEY');\nconst { data } = await supabase.from('users').select('*');"),

    ("Firebase Firestore", "Database",
     "Google's NoSQL cloud database with realtime sync for web and mobile apps.",
     "v9", "google", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { getFirestore, collection, getDocs } from 'firebase/firestore';\nconst db = getFirestore();\nconst querySnapshot = await getDocs(collection(db, 'users'));"),

    ("PlanetScale API", "Database",
     "Serverless MySQL platform API with branching and non-blocking schema changes.",
     "v1", "planetscale", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { connect } from '@planetscale/database';\nconst conn = connect({ url: process.env.DATABASE_URL });\nconst results = await conn.execute('SELECT * FROM users');"),

    ("MongoDB Atlas API", "Database",
     "MongoDB's cloud database API for managing clusters, data, and Atlas features.",
     "v2", "mongodb", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { MongoClient } = require('mongodb');\nconst client = new MongoClient(process.env.MONGODB_URI);\nawait client.connect();\nconst db = client.db('mydb');"),

    ("Redis Cloud API", "Database",
     "Redis managed cloud database API for caching, sessions, and pub/sub messaging.",
     "v1", "redis", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { createClient } from 'redis';\nconst client = createClient({ url: 'redis://localhost:6379' });\nawait client.connect();\nawait client.set('key', 'value');"),

    ("Neon API", "Database",
     "Serverless PostgreSQL API with branching, autoscaling, and instant provisioning.",
     "v2", "neon", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { neon } from '@neondatabase/serverless';\nconst sql = neon(process.env.DATABASE_URL);\nconst result = await sql`SELECT * FROM users`;"),

    # ── Communication ──────────────────────────────────────────────────────────
    ("Twilio SMS API", "API",
     "Cloud communications API for sending SMS, MMS, and voice calls programmatically.",
     "v2010", "twilio", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const twilio = require('twilio');\nconst client = twilio('ACCOUNT_SID', 'AUTH_TOKEN');\nawait client.messages.create({ body: 'Hello!', from: '+1234567890', to: '+0987654321' });"),

    ("SendGrid API", "API",
     "Email delivery API for sending transactional and marketing emails at scale.",
     "v3", "twilio", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const sgMail = require('@sendgrid/mail');\nsgMail.setApiKey(process.env.SENDGRID_API_KEY);\nawait sgMail.send({ to: 'user@example.com', from: 'sender@example.com', subject: 'Hello', text: 'World' });"),

    ("Mailgun API", "API",
     "Email API service for sending, receiving, and tracking emails programmatically.",
     "v3", "mailgun", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const formData = require('form-data');\nconst Mailgun = require('mailgun.js');\nconst mg = new Mailgun(formData);\nconst client = mg.client({ username: 'api', key: 'YOUR_KEY' });"),

    ("Postmark API", "API",
     "Transactional email API focused on fast delivery and detailed analytics.",
     "v1", "postmark", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const postmark = require('postmark');\nconst client = new postmark.ServerClient('SERVER_TOKEN');\nawait client.sendEmail({ From: 'sender@example.com', To: 'user@example.com', Subject: 'Hello', TextBody: 'World' });"),

    ("Vonage SMS API", "API",
     "Vonage (formerly Nexmo) API for SMS, voice, video, and messaging channels.",
     "v1", "vonage", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const Vonage = require('@vonage/server-sdk');\nconst vonage = new Vonage({ apiKey: 'YOUR_KEY', apiSecret: 'YOUR_SECRET' });\nvonage.message.sendSms('FROM', 'TO', 'Hello World');"),

    ("Resend API", "API",
     "Modern email API built for developers with React email template support.",
     "v1", "resend", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { Resend } from 'resend';\nconst resend = new Resend('YOUR_API_KEY');\nawait resend.emails.send({ from: 'you@example.com', to: 'user@example.com', subject: 'Hello', html: '<p>World</p>' });"),

    # ── Analytics ─────────────────────────────────────────────────────────────
    ("Google Analytics API", "Analytics",
     "Google Analytics Data API for querying and reporting on website traffic data.",
     "v1", "google", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "from google.analytics.data_v1beta import BetaAnalyticsDataClient\nclient = BetaAnalyticsDataClient()\nrequest = RunReportRequest(property=f'properties/YOUR_PROPERTY_ID')"),

    ("Mixpanel API", "Analytics",
     "Product analytics API for tracking user events, funnels, and retention.",
     "v2", "mixpanel", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import mixpanel from 'mixpanel-browser';\nmixpanel.init('YOUR_TOKEN');\nmixpanel.track('Button Clicked', { button: 'signup' });"),

    ("Amplitude API", "Analytics",
     "Digital analytics platform API for product intelligence and user behavior tracking.",
     "v2", "amplitude", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import * as amplitude from '@amplitude/analytics-browser';\namplitude.init('YOUR_API_KEY');\namplitude.track('Button Clicked');"),

    ("Segment API", "Analytics",
     "Customer data platform API for collecting, cleaning, and routing analytics data.",
     "v1", "segment", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const Analytics = require('analytics-node');\nconst analytics = new Analytics('YOUR_WRITE_KEY');\nanalytics.track({ userId: '123', event: 'Item Purchased' });"),

    ("Plausible API", "Analytics",
     "Privacy-friendly web analytics API — no cookies, GDPR compliant.",
     "v1", "plausible", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const response = await fetch('https://plausible.io/api/v1/stats/aggregate?site_id=YOUR_SITE', {\n  headers: { 'Authorization': 'Bearer YOUR_TOKEN' }\n});"),

    # ── Maps & Location ────────────────────────────────────────────────────────
    ("Google Maps API", "API",
     "Google Maps Platform API for maps, geocoding, directions, and places.",
     "v3", "google", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { Loader } from '@googlemaps/js-api-loader';\nconst loader = new Loader({ apiKey: 'YOUR_KEY', version: 'weekly' });\nawait loader.load();"),

    ("Mapbox API", "API",
     "Mapbox mapping and location API for custom maps, geocoding, and navigation.",
     "v1", "mapbox", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import mapboxgl from 'mapbox-gl';\nmapboxgl.accessToken = 'YOUR_TOKEN';\nconst map = new mapboxgl.Map({ container: 'map', style: 'mapbox://styles/mapbox/streets-v11' });"),

    ("OpenWeatherMap API", "API",
     "Weather data API providing current weather, forecasts, and historical data.",
     "v2.5", "openweather", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const response = await fetch(`https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_KEY`);\nconst data = await response.json();\nconsole.log(data.weather[0].description);"),

    ("HERE Maps API", "API",
     "HERE location platform API for maps, routing, and geocoding services.",
     "v8", "here", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const H = require('@here/maps-api-for-javascript');\nconst platform = new H.service.Platform({ apikey: 'YOUR_KEY' });"),

    ("ipapi API", "API",
     "IP address geolocation API returning country, city, timezone and ISP data.",
     "v1", "ipapi", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const response = await fetch('https://ipapi.co/json/');\nconst data = await response.json();\nconsole.log(data.country_name, data.city);"),

    # ── Social Media ───────────────────────────────────────────────────────────
    ("GitHub API", "API",
     "GitHub REST API for repositories, pull requests, issues, and user data.",
     "v3", "github", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Octokit } = require('@octokit/rest');\nconst octokit = new Octokit({ auth: 'YOUR_TOKEN' });\nconst { data } = await octokit.repos.listForUser({ username: 'octocat' });"),

    ("Twitter/X API", "API",
     "Twitter API v2 for posting tweets, searching content, and accessing user data.",
     "v2", "twitter", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { TwitterApi } from 'twitter-api-v2';\nconst client = new TwitterApi('BEARER_TOKEN');\nconst tweets = await client.v2.search('javascript');"),

    ("Instagram Graph API", "API",
     "Meta's Instagram Graph API for managing business accounts and media content.",
     "v18", "meta", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const response = await fetch(`https://graph.instagram.com/me/media?fields=id,caption&access_token=YOUR_TOKEN`);\nconst data = await response.json();"),

    ("Slack API", "API",
     "Slack API for building apps, sending messages, and managing workspace data.",
     "v1", "slack", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { WebClient } = require('@slack/web-api');\nconst client = new WebClient('YOUR_TOKEN');\nawait client.chat.postMessage({ channel: '#general', text: 'Hello World' });"),

    ("Discord API", "API",
     "Discord API for building bots, sending messages, and managing servers.",
     "v10", "discord", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const { Client, GatewayIntentBits } = require('discord.js');\nconst client = new Client({ intents: [GatewayIntentBits.Guilds] });\nclient.login('YOUR_BOT_TOKEN');"),

    ("LinkedIn API", "API",
     "LinkedIn API for profile data, job postings, and professional network integrations.",
     "v2", "linkedin", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const response = await fetch('https://api.linkedin.com/v2/me', {\n  headers: { 'Authorization': 'Bearer YOUR_TOKEN' }\n});"),

    # ── DevOps ─────────────────────────────────────────────────────────────────
    ("GitHub Actions API", "DevOps",
     "GitHub Actions REST API for managing CI/CD workflows, runs, and artifacts.",
     "v3", "github", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Octokit } = require('@octokit/rest');\nconst octokit = new Octokit({ auth: 'YOUR_TOKEN' });\nconst runs = await octokit.actions.listWorkflowRunsForRepo({ owner: 'org', repo: 'repo' });"),

    ("Docker Hub API", "DevOps",
     "Docker Hub API for managing repositories, images, and automated builds.",
     "v2", "docker", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const response = await fetch('https://hub.docker.com/v2/repositories/YOUR_USERNAME/', {\n  headers: { 'Authorization': 'Bearer YOUR_TOKEN' }\n});"),

    ("CircleCI API", "DevOps",
     "CircleCI API for triggering pipelines, managing jobs, and viewing build results.",
     "v2", "circleci", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const response = await fetch('https://circleci.com/api/v2/pipeline', {\n  headers: { 'Circle-Token': 'YOUR_TOKEN' }\n});"),

    ("Datadog API", "Monitoring",
     "Datadog monitoring API for metrics, logs, traces, and infrastructure monitoring.",
     "v1", "datadog", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "from datadog import initialize, api\ninitialize(api_key='YOUR_API_KEY', app_key='YOUR_APP_KEY')\napi.Metric.send(metric='my.metric', points=[(time.time(), 1.0)])"),

    ("PagerDuty API", "Monitoring",
     "Incident management API for alerting, on-call scheduling, and escalation policies.",
     "v2", "pagerduty", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const response = await fetch('https://api.pagerduty.com/incidents', {\n  headers: { 'Authorization': 'Token token=YOUR_TOKEN', 'Accept': 'application/vnd.pagerduty+json;version=2' }\n});"),

    ("Sentry API", "Monitoring",
     "Error tracking and performance monitoring API for capturing and resolving issues.",
     "v0", "sentry", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "High",
     "import * as Sentry from '@sentry/node';\nSentry.init({ dsn: 'YOUR_DSN' });\ntry { /* code */ } catch(e) { Sentry.captureException(e); }"),

    ("New Relic API", "Monitoring",
     "Full-stack observability API for APM, infrastructure, and browser monitoring.",
     "v2", "newrelic", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const newrelic = require('newrelic');\nnewrelic.recordMetric('Custom/MyMetric', 1.0);\nnewrelic.addCustomAttribute('userId', '123');"),

    # ── Search ─────────────────────────────────────────────────────────────────
    ("Algolia API", "Search",
     "Search-as-a-service API for fast, typo-tolerant full-text search experiences.",
     "v4", "algolia", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import algoliasearch from 'algoliasearch';\nconst client = algoliasearch('APP_ID', 'API_KEY');\nconst index = client.initIndex('products');\nconst results = await index.search('query');"),

    ("Elasticsearch API", "Search",
     "Elasticsearch REST API for full-text search, analytics, and log management.",
     "v8", "elastic", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const { Client } = require('@elastic/elasticsearch');\nconst client = new Client({ node: 'http://localhost:9200' });\nconst result = await client.search({ index: 'my-index', query: { match: { title: 'test' } } });"),

    ("Typesense API", "Search",
     "Fast, typo-tolerant open-source search engine API alternative to Algolia.",
     "v0.25", "typesense", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "High",
     "const Typesense = require('typesense');\nconst client = new Typesense.Client({ nodes: [{ host: 'localhost', port: 9108, protocol: 'http' }], apiKey: 'xyz' });"),

    ("MeiliSearch API", "Search",
     "Open-source, blazingly fast search API for building search experiences.",
     "v1", "meilisearch", "Multi-language", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const { MeiliSearch } = require('meilisearch');\nconst client = new MeiliSearch({ host: 'http://127.0.0.1:7700', apiKey: 'masterKey' });\nawait client.index('movies').search('Avengers');"),

    # ── Media & Files ──────────────────────────────────────────────────────────
    ("Cloudinary API", "API",
     "Cloud-based image and video management API with transformation and optimization.",
     "v1", "cloudinary", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const cloudinary = require('cloudinary').v2;\ncloudinary.config({ cloud_name: 'YOUR_CLOUD', api_key: 'YOUR_KEY', api_secret: 'YOUR_SECRET' });\nconst result = await cloudinary.uploader.upload('image.jpg');"),

    ("Imgix API", "API",
     "Real-time image processing and CDN API for dynamic image transformations.",
     "v1", "imgix", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "import ImgixClient from '@imgix/js-core';\nconst client = new ImgixClient({ domain: 'your-source.imgix.net' });\nconst url = client.buildURL('/path/to/image.jpg', { w: 400, h: 300 });"),

    ("Mux API", "API",
     "Video API for uploading, storing, encoding, and streaming video content.",
     "v1", "mux", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const Mux = require('@mux/mux-node');\nconst { video } = new Mux('TOKEN_ID', 'TOKEN_SECRET');\nconst asset = await video.assets.create({ input: 'https://example.com/video.mp4' });"),

    ("Uploadcare API", "API",
     "File uploading and processing API with CDN delivery and image transformations.",
     "v0.6", "uploadcare", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "High",
     "import { uploadFile } from '@uploadcare/upload-client';\nconst result = await uploadFile(file, { publicKey: 'YOUR_PUBLIC_KEY', store: 'auto' });"),

    # ── E-commerce ─────────────────────────────────────────────────────────────
    ("Shopify API", "API",
     "Shopify Admin API for managing products, orders, customers, and store data.",
     "v2024-01", "shopify", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const Shopify = require('shopify-api-node');\nconst shopify = new Shopify({ shopName: 'my-shop', apiKey: 'KEY', password: 'PASS' });\nconst products = await shopify.product.list();"),

    ("WooCommerce API", "API",
     "WooCommerce REST API for managing products, orders, and customers in WordPress.",
     "v3", "automattic", "PHP", "REST", "Open Source", "Low", "Medium", "REST", "Low",
     "const WooCommerceRestApi = require('@woocommerce/woocommerce-rest-api').default;\nconst api = new WooCommerceRestApi({ url: 'https://yourstore.com', consumerKey: 'ck_xxx', consumerSecret: 'cs_xxx', version: 'wc/v3' });"),

    ("Printful API", "API",
     "Print-on-demand and dropshipping API for creating and fulfilling custom products.",
     "v1", "printful", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const response = await fetch('https://api.printful.com/products', {\n  headers: { 'Authorization': 'Bearer YOUR_TOKEN' }\n});"),

    # ── Finance ────────────────────────────────────────────────────────────────
    ("Plaid API", "API",
     "Financial data API for connecting bank accounts, retrieving transactions, and verifying income.",
     "v1", "plaid", "Multi-language", "REST", "Paid/Premium", "Low", "High", "REST", "Low",
     "const { PlaidApi, Configuration, PlaidEnvironments } = require('plaid');\nconst config = new Configuration({ basePath: PlaidEnvironments.sandbox, baseOptions: { headers: { 'PLAID-CLIENT-ID': 'CLIENT_ID', 'PLAID-SECRET': 'SECRET' } } });"),

    ("Alpha Vantage API", "API",
     "Stock market and financial data API for equities, forex, and cryptocurrency.",
     "v1", "alphavantage", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const response = await fetch(`https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey=YOUR_KEY`);\nconst data = await response.json();"),

    ("CoinGecko API", "API",
     "Cryptocurrency data API for prices, market data, and coin information.",
     "v3", "coingecko", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd');\nconst data = await response.json();\nconsole.log(data.bitcoin.usd);"),

    # ── Microservices & Backend Frameworks ─────────────────────────────────────
    ("FastAPI", "Backend Framework",
     "Modern, fast Python web framework for building APIs with automatic OpenAPI docs.",
     "v0.109", "tiangolo", "Python", "REST", "Open Source", "Low", "High", "REST", "High",
     "from fastapi import FastAPI\napp = FastAPI()\n\n@app.get('/items/{item_id}')\nasync def read_item(item_id: int):\n    return {'item_id': item_id}"),

    ("Express.js", "Backend Framework",
     "Fast, unopinionated Node.js web framework for building APIs and web applications.",
     "v4.18", "expressjs", "JavaScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "const express = require('express');\nconst app = express();\napp.get('/api/users', (req, res) => {\n  res.json({ users: [] });\n});\napp.listen(3000);"),

    ("Django REST Framework", "Backend Framework",
     "Powerful toolkit for building Web APIs on top of Django.",
     "v3.14", "encode", "Python", "REST", "Open Source", "Low", "High", "REST", "Low",
     "from rest_framework import serializers, viewsets\nfrom .models import User\n\nclass UserSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = User\n        fields = '__all__'"),

    ("NestJS", "Backend Framework",
     "Progressive Node.js framework for building scalable server-side applications.",
     "v10", "nestjs", "TypeScript", "REST", "Open Source", "Low", "High", "MVC", "Low",
     "import { Controller, Get } from '@nestjs/common';\n\n@Controller('users')\nexport class UsersController {\n  @Get()\n  findAll() {\n    return [];\n  }\n}"),

    ("Spring Boot", "Backend Framework",
     "Java-based framework for building production-ready microservices and APIs.",
     "v3.2", "pivotal", "Java", "REST", "Open Source", "Low", "High", "MVC", "Low",
     "@RestController\n@RequestMapping('/api')\npublic class ApiController {\n  @GetMapping('/users')\n  public List<User> getUsers() {\n    return userService.findAll();\n  }\n}"),

    ("Flask", "Backend Framework",
     "Lightweight Python web framework for building simple APIs and microservices.",
     "v3.0", "pallets", "Python", "REST", "Open Source", "Low", "Medium", "REST", "Low",
     "from flask import Flask, jsonify\napp = Flask(__name__)\n\n@app.route('/api/users')\ndef get_users():\n    return jsonify({'users': []})\n\nif __name__ == '__main__':\n    app.run()"),

    ("Gin Framework", "Backend Framework",
     "High-performance HTTP web framework for Go, ideal for building REST APIs.",
     "v1.9", "gin-gonic", "Go", "REST", "Open Source", "Low", "High", "REST", "Low",
     "package main\nimport \"github.com/gin-gonic/gin\"\n\nfunc main() {\n  r := gin.Default()\n  r.GET('/users', func(c *gin.Context) {\n    c.JSON(200, gin.H{'users': []string{}})\n  })\n  r.Run()\n}"),

    ("Laravel API", "Backend Framework",
     "PHP web framework with elegant syntax for building REST APIs and web applications.",
     "v10", "laravel", "PHP", "REST", "Open Source", "Low", "High", "MVC", "Low",
     "Route::get('/api/users', function () {\n    return User::all();\n});\n\n// Or with a controller:\nRoute::apiResource('users', UserController::class);"),

    ("Ruby on Rails API", "Backend Framework",
     "Full-stack Ruby framework in API mode for building RESTful web services.",
     "v7.1", "rails", "Ruby", "REST", "Open Source", "Low", "High", "MVC", "Low",
     "class UsersController < ApplicationController\n  def index\n    users = User.all\n    render json: users\n  end\nend"),

    # ── Frontend ───────────────────────────────────────────────────────────────
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

    ("Next.js", "Microservice",
     "The React framework for production — SSR, SSG, API routes, and more.",
     "v14", "vercel", "JavaScript", "N/A", "Open Source", "Low", "High", "SSR", "Low",
     "// pages/api/users.js\nexport default function handler(req, res) {\n  res.status(200).json({ users: [] });\n}"),

    # ── GraphQL ────────────────────────────────────────────────────────────────
    ("Apollo GraphQL", "API",
     "GraphQL platform for building, managing, and scaling APIs with a supergraph.",
     "v4", "apollographql", "JavaScript", "GraphQL", "Open Source", "Low", "High", "GraphQL", "Low",
     "const { ApolloServer } = require('@apollo/server');\nconst server = new ApolloServer({\n  typeDefs,\n  resolvers,\n});\nawait server.start();"),

    ("Hasura API", "API",
     "Instant GraphQL API on PostgreSQL and other databases with real-time subscriptions.",
     "v2", "hasura", "Multi-language", "GraphQL", "Freemium", "Low", "High", "GraphQL", "Low",
     "const { gql, request } = require('graphql-request');\nconst query = gql`{ users { id name email } }`;\nconst data = await request('https://YOUR_PROJECT.hasura.app/v1/graphql', query);"),

    ("Contentful API", "API",
     "Headless CMS API with GraphQL and REST support for managing content.",
     "v10", "contentful", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const contentful = require('contentful');\nconst client = contentful.createClient({ space: 'YOUR_SPACE', accessToken: 'YOUR_TOKEN' });\nconst entries = await client.getEntries({ content_type: 'blogPost' });"),

    ("Sanity API", "API",
     "Headless CMS with real-time collaboration and GROQ query language.",
     "v3", "sanity", "JavaScript", "REST", "Freemium", "Low", "High", "REST", "Low",
     "import { createClient } from '@sanity/client';\nconst client = createClient({ projectId: 'YOUR_ID', dataset: 'production', useCdn: true });\nconst posts = await client.fetch(`*[_type == 'post']`);"),

    # ── Notifications ──────────────────────────────────────────────────────────
    ("OneSignal API", "API",
     "Push notification API for web, mobile, and email across all major platforms.",
     "v1", "onesignal", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const response = await fetch('https://onesignal.com/api/v1/notifications', {\n  method: 'POST',\n  headers: { 'Authorization': 'Basic YOUR_REST_API_KEY' },\n  body: JSON.stringify({ app_id: 'YOUR_APP_ID', contents: { en: 'Hello!' }, included_segments: ['All'] })\n});"),

    ("Pusher API", "API",
     "Real-time messaging API for adding live features — chat, notifications, collaboration.",
     "v8", "pusher", "Multi-language", "WebSocket", "Freemium", "Low", "High", "Pub/Sub", "Low",
     "const Pusher = require('pusher');\nconst pusher = new Pusher({ appId: 'APP_ID', key: 'KEY', secret: 'SECRET', cluster: 'mt1' });\nawait pusher.trigger('my-channel', 'my-event', { message: 'Hello!' });"),

    ("Ably API", "API",
     "Realtime messaging API for pub/sub, presence, and streaming at scale.",
     "v1.2", "ably", "Multi-language", "WebSocket", "Freemium", "Low", "High", "Pub/Sub", "Low",
     "const Ably = require('ably');\nconst client = new Ably.Realtime('YOUR_API_KEY');\nconst channel = client.channels.get('my-channel');\nawait channel.publish('greeting', 'Hello World');"),

    ("Socket.IO", "Microservice",
     "Bidirectional event-based communication library for real-time web applications.",
     "v4.7", "socketio", "JavaScript", "WebSocket", "Open Source", "Low", "High", "Event-Driven", "Low",
     "const { Server } = require('socket.io');\nconst io = new Server(httpServer);\nio.on('connection', (socket) => {\n  socket.emit('greeting', 'Hello!');\n  socket.on('message', (data) => console.log(data));\n});"),

    # ── Miscellaneous ──────────────────────────────────────────────────────────
    ("Airtable API", "API",
     "Airtable REST API for reading and writing data to Airtable bases and tables.",
     "v0", "airtable", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "High",
     "const Airtable = require('airtable');\nconst base = new Airtable({ apiKey: 'YOUR_KEY' }).base('YOUR_BASE_ID');\nconst records = await base('Users').select({ maxRecords: 100 }).firstPage();"),

    ("Notion API", "API",
     "Notion integration API for reading and writing pages, databases, and blocks.",
     "v1", "notion", "Multi-language", "REST", "Free", "Low", "High", "REST", "Low",
     "const { Client } = require('@notionhq/client');\nconst notion = new Client({ auth: process.env.NOTION_TOKEN });\nconst response = await notion.databases.query({ database_id: 'YOUR_DB_ID' });"),

    ("Zapier API", "API",
     "Workflow automation API for connecting apps and automating repetitive tasks.",
     "v1", "zapier", "Multi-language", "REST", "Freemium", "Medium", "High", "REST", "Low",
     "const response = await fetch('https://hooks.zapier.com/hooks/catch/YOUR_HOOK_ID/', {\n  method: 'POST',\n  body: JSON.stringify({ name: 'John', email: 'john@example.com' })\n});"),

    ("Calendly API", "API",
     "Scheduling automation API for embedding booking and managing calendar events.",
     "v2", "calendly", "Multi-language", "REST", "Freemium", "Low", "High", "REST", "Low",
     "const response = await fetch('https://api.calendly.com/users/me', {\n  headers: { 'Authorization': 'Bearer YOUR_TOKEN' }\n});"),

    ("Lottie API", "API",
     "Animation library API for rendering Adobe After Effects animations on web and mobile.",
     "v5.12", "airbnb", "JavaScript", "N/A", "Open Source", "Low", "High", "N/A", "Low",
     "import lottie from 'lottie-web';\nconst animation = lottie.loadAnimation({\n  container: document.getElementById('animation'),\n  renderer: 'svg',\n  loop: true,\n  autoplay: true,\n  path: 'animation.json'\n});"),

    ("PDFKit API", "API",
     "PDF generation library API for creating PDF documents programmatically in Node.js.",
     "v0.14", "foliojs", "JavaScript", "N/A", "Open Source", "Low", "High", "N/A", "High",
     "const PDFDocument = require('pdfkit');\nconst doc = new PDFDocument();\ndoc.pipe(fs.createWriteStream('output.pdf'));\ndoc.fontSize(25).text('Hello World', 100, 100);\ndoc.end();"),

    ("Axios", "Microservice",
     "Promise-based HTTP client for Node.js and browsers with request/response interceptors.",
     "v1.6", "axios", "JavaScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "import axios from 'axios';\nconst response = await axios.get('https://api.example.com/users', {\n  headers: { 'Authorization': `Bearer ${token}` }\n});\nconsole.log(response.data);"),

    ("GraphQL Yoga", "API",
     "Fully-featured GraphQL server with focus on easy setup and performance.",
     "v4", "the-guild", "TypeScript", "GraphQL", "Open Source", "Low", "High", "GraphQL", "Low",
     "import { createYoga } from 'graphql-yoga';\nimport { createServer } from 'node:http';\nconst yoga = createYoga({ schema });\nconst server = createServer(yoga);\nserver.listen(4000);"),

    ("tRPC", "API",
     "End-to-end typesafe APIs without code generation — TypeScript first.",
     "v10", "trpc", "TypeScript", "REST", "Open Source", "Low", "High", "REST", "Low",
     "import { initTRPC } from '@trpc/server';\nconst t = initTRPC.create();\nconst router = t.router({\n  getUser: t.procedure.query(() => ({ id: 1, name: 'Alice' }))\n});"),

    ("Prisma ORM", "Database",
     "Next-generation Node.js ORM with type-safe database access and migrations.",
     "v5", "prisma", "TypeScript", "N/A", "Open Source", "Low", "High", "N/A", "Low",
     "import { PrismaClient } from '@prisma/client';\nconst prisma = new PrismaClient();\nconst users = await prisma.user.findMany({\n  where: { active: true },\n  select: { id: true, name: true }\n});"),

    ("Drizzle ORM", "Database",
     "Lightweight TypeScript ORM with SQL-like query builder and full type safety.",
     "v0.29", "drizzle-team", "TypeScript", "N/A", "Open Source", "Low", "High", "N/A", "High",
     "import { drizzle } from 'drizzle-orm/node-postgres';\nimport { eq } from 'drizzle-orm';\nconst db = drizzle(pool);\nconst users = await db.select().from(usersTable).where(eq(usersTable.active, true));"),

    ("BullMQ", "Microservice",
     "Redis-based queue and job scheduling library for Node.js background processing.",
     "v4", "taskforce", "JavaScript", "N/A", "Open Source", "Low", "High", "Event-Driven", "Low",
     "import { Queue, Worker } from 'bullmq';\nconst queue = new Queue('emails');\nawait queue.add('sendWelcome', { to: 'user@example.com' });\nconst worker = new Worker('emails', async job => { /* send email */ });"),

    ("Kafka (Confluent)", "Microservice",
     "Apache Kafka API for high-throughput, fault-tolerant event streaming and messaging.",
     "v3.6", "apache", "Multi-language", "N/A", "Open Source", "Low", "High", "Event-Driven", "Low",
     "const { Kafka } = require('kafkajs');\nconst kafka = new Kafka({ clientId: 'my-app', brokers: ['localhost:9092'] });\nconst producer = kafka.producer();\nawait producer.send({ topic: 'events', messages: [{ value: 'Hello' }] });"),

    ("RabbitMQ API", "Microservice",
     "Message broker API for reliable message queuing between microservices.",
     "v3.12", "rabbitmq", "Multi-language", "AMQP", "Open Source", "Low", "High", "Pub/Sub", "Low",
     "const amqp = require('amqplib');\nconst conn = await amqp.connect('amqp://localhost');\nconst channel = await conn.createChannel();\nawait channel.assertQueue('tasks');\nchannel.sendToQueue('tasks', Buffer.from('Hello'));"),

    ("Temporal API", "Microservice",
     "Workflow orchestration platform API for reliable distributed application logic.",
     "v1.22", "temporal", "Multi-language", "gRPC", "Open Source", "Low", "High", "Event-Driven", "Low",
     "import { Client } from '@temporalio/client';\nconst client = new Client();\nawait client.workflow.start(myWorkflow, {\n  taskQueue: 'my-queue',\n  workflowId: 'workflow-001',\n  args: [{ name: 'Alice' }]\n});"),

    ("Inngest API", "Microservice",
     "Event-driven job scheduling API for background jobs, cron, and workflows in serverless.",
     "v2", "inngest", "TypeScript", "REST", "Freemium", "Low", "High", "Event-Driven", "Low",
     "import { Inngest } from 'inngest';\nconst inngest = new Inngest({ id: 'my-app' });\nconst fn = inngest.createFunction(\n  { id: 'send-welcome' },\n  { event: 'user/signup' },\n  async ({ event }) => { /* send email */ }\n);"),
]


def seed():
    """
    Insert all seed entries into the database.

    Called automatically by app.py on startup.
    Uses 'Stripe API' by 'stripe' as a sentinel —
    if it already exists, the database has been seeded
    and this function returns immediately without doing anything.

    Safe to call from app.py on every deploy.
    Safe to run manually: python seed_apis.py
    """
    # ── Sentinel check ───────────────────────────────────────────────────────
    # If Stripe API already exists, we have already seeded — skip everything.
    already_seeded = ApiEntry.query.filter_by(
        name="Stripe API", developer="stripe"
    ).first()

    if already_seeded:
        print("[SEED] Already seeded — skipping.")
        return

    # ── Insert entries ────────────────────────────────────────────────────────
    inserted = 0
    skipped = 0

    for row in SEED_DATA:
        (name, category, description, version, developer,
         language, framework, cost, latency, scalability,
         design_pattern, risk_level, sample_code) = row

        # Skip individual duplicates (handles partial seeds)
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
    # When run directly (python seed_apis.py), wrap in app context
    with app.app_context():
        db.create_all()
        seed()