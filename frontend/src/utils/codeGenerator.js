/**
 * codeGenerator.js — Sample code template generator for SLIB Finder
 *
 * Exports:
 *   generateSampleCode — returns a language-specific code snippet string
 *
 * Supports: JavaScript, TypeScript, Python, Java, Go, Ruby, PHP,
 *           Rust, C#, Kotlin, Swift, and a cURL fallback default.
 */

// ─────────────────────────────────────────────
// CODE TEMPLATES
// Keyed by programming language (lowercase).
// Each template receives the API name as a parameter.
// ─────────────────────────────────────────────
const CODE_TEMPLATES = {
    javascript: (name) =>
  `// ${name} — JavaScript (fetch)
  const response = await fetch('https://api.example.com/v1/endpoint', {
    method: 'GET',
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY',
      'Content-Type': 'application/json'
    }
  });
  const data = await response.json();
  console.log(data);`,
  
    typescript: (name) =>
  `// ${name} — TypeScript (fetch)
  const response = await fetch('https://api.example.com/v1/endpoint', {
    method: 'GET',
    headers: {
      'Authorization': 'Bearer YOUR_API_KEY',
      'Content-Type': 'application/json'
    }
  });
  const data: Record<string, unknown> = await response.json();
  console.log(data);`,
  
    python: (name) =>
  `# ${name} — Python (requests)
  import requests
  
  headers = {
      "Authorization": "Bearer YOUR_API_KEY",
      "Content-Type": "application/json"
  }
  
  response = requests.get("https://api.example.com/v1/endpoint", headers=headers)
  data = response.json()
  print(data)`,
  
    java: (name) =>
  `// ${name} — Java (HttpClient)
  import java.net.http.*;
  import java.net.URI;
  
  HttpClient client = HttpClient.newHttpClient();
  HttpRequest request = HttpRequest.newBuilder()
      .uri(URI.create("https://api.example.com/v1/endpoint"))
      .header("Authorization", "Bearer YOUR_API_KEY")
      .GET()
      .build();
  
  HttpResponse<String> response = client.send(request,
      HttpResponse.BodyHandlers.ofString());
  System.out.println(response.body());`,
  
    go: (name) =>
  `// ${name} — Go (net/http)
  package main
  
  import (
      "fmt"
      "net/http"
      "io/ioutil"
  )
  
  req, _ := http.NewRequest("GET", "https://api.example.com/v1/endpoint", nil)
  req.Header.Set("Authorization", "Bearer YOUR_API_KEY")
  
  client := &http.Client{}
  resp, _ := client.Do(req)
  defer resp.Body.Close()
  
  body, _ := ioutil.ReadAll(resp.Body)
  fmt.Println(string(body))`,
  
    ruby: (name) =>
  `# ${name} — Ruby (Net::HTTP)
  require 'net/http'
  require 'json'
  
  uri = URI('https://api.example.com/v1/endpoint')
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = true
  
  request = Net::HTTP::Get.new(uri)
  request['Authorization'] = 'Bearer YOUR_API_KEY'
  
  response = http.request(request)
  puts JSON.parse(response.body)`,
  
    php: (name) =>
  `<?php
  // ${name} — PHP (cURL)
  $curl = curl_init();
  curl_setopt_array($curl, [
      CURLOPT_URL => "https://api.example.com/v1/endpoint",
      CURLOPT_RETURNTRANSFER => true,
      CURLOPT_HTTPHEADER => [
          "Authorization: Bearer YOUR_API_KEY",
          "Content-Type: application/json"
      ],
  ]);
  $response = curl_exec($curl);
  curl_close($curl);
  echo $response;`,
  
    rust: (name) =>
  `// ${name} — Rust (reqwest)
  use reqwest::header::{AUTHORIZATION, CONTENT_TYPE};
  
  let client = reqwest::Client::new();
  let response = client
      .get("https://api.example.com/v1/endpoint")
      .header(AUTHORIZATION, "Bearer YOUR_API_KEY")
      .header(CONTENT_TYPE, "application/json")
      .send()
      .await?;
  
  let data = response.text().await?;
  println!("{}", data);`,
  
    "c#": (name) =>
  `// ${name} — C# (HttpClient)
  using System.Net.Http;
  using System.Net.Http.Headers;
  
  var client = new HttpClient();
  client.DefaultRequestHeaders.Authorization =
      new AuthenticationHeaderValue("Bearer", "YOUR_API_KEY");
  
  var response = await client.GetAsync("https://api.example.com/v1/endpoint");
  var content = await response.Content.ReadAsStringAsync();
  Console.WriteLine(content);`,
  
    kotlin: (name) =>
  `// ${name} — Kotlin (OkHttp)
  val client = OkHttpClient()
  val request = Request.Builder()
      .url("https://api.example.com/v1/endpoint")
      .addHeader("Authorization", "Bearer YOUR_API_KEY")
      .build()
  
  client.newCall(request).execute().use { response ->
      println(response.body?.string())
  }`,
  
    swift: (name) =>
  `// ${name} — Swift (URLSession)
  var request = URLRequest(url: URL(string: "https://api.example.com/v1/endpoint")!)
  request.setValue("Bearer YOUR_API_KEY", forHTTPHeaderField: "Authorization")
  
  URLSession.shared.dataTask(with: request) { data, response, error in
      if let data = data {
          print(String(data: data, encoding: .utf8) ?? "")
      }
  }.resume()`,
  
    // Default fallback for any unrecognized language — uses curl (universal)
    default: (name) =>
  `# ${name} — cURL (universal)
  curl -X GET "https://api.example.com/v1/endpoint" \\
    -H "Authorization: Bearer YOUR_API_KEY" \\
    -H "Content-Type: application/json"`,
  };
  
  /**
   * generateSampleCode
   * Returns a language-specific code template for the given API name and language.
   *
   * @param {string} name     - API or library name (used in the comment header)
   * @param {string} language - Programming language (matched case-insensitively)
   * @returns {string} A formatted code snippet string
   */
  export function generateSampleCode(name, language) {
    const lang = (language || "").toLowerCase().trim();
    const templateFn = CODE_TEMPLATES[lang] || CODE_TEMPLATES["default"];
    return templateFn(name);
  }