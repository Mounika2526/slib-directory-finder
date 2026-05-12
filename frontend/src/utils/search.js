/**
 * search.js — Search and relevance scoring utilities for SLIB Finder
 *
 * Exports:
 *   similarityScore  — bigram-based string similarity (0–1)
 *   fuzzyCharMatch   — character sequence match (typo tolerance)
 *   scoreApi         — full relevance score for an API entry vs a search term
 *
 * Scoring tiers (higher = more relevant):
 *   100 — exact name match
 *    80 — name starts with term
 *    60 — name contains term
 *    40 — high similarity score (typo tolerance)
 *    20 — fuzzy char sequence match on name
 *    10 — match on other fields (description, category, developer…)
 */

/**
 * similarityScore
 * Returns a 0–1 score of how similar two strings are.
 * Uses bigram (2-character pair) overlap — language-agnostic and
 * typo-tolerant. "fastify" vs "fatify" → ~0.72
 *
 * @param {string} a
 * @param {string} b
 * @returns {number} 0 (no similarity) to 1 (identical)
 */
export function similarityScore(a, b) {
    if (!a || !b) return 0;
    if (a === b) return 1;
  
    const getBigrams = (str) => {
      const bigrams = new Set();
      for (let i = 0; i < str.length - 1; i++) {
        bigrams.add(str.slice(i, i + 2));
      }
      return bigrams;
    };
  
    const bigramsA = getBigrams(a);
    const bigramsB = getBigrams(b);
  
    if (bigramsA.size === 0 || bigramsB.size === 0) {
      return a.includes(b) || b.includes(a) ? 0.5 : 0;
    }
  
    let intersection = 0;
    bigramsA.forEach((bg) => { if (bigramsB.has(bg)) intersection++; });
  
    return (2 * intersection) / (bigramsA.size + bigramsB.size);
  }
  
  /**
   * fuzzyCharMatch
   * Returns true if every character in `term` appears in `str` in order.
   * Used as a last-resort signal for very short terms.
   *
   * @param {string} str
   * @param {string} term
   * @returns {boolean}
   */
  export function fuzzyCharMatch(str, term) {
    if (!str || !term) return false;
    let ti = 0;
    for (let i = 0; i < str.length && ti < term.length; i++) {
      if (str[i] === term[ti]) ti++;
    }
    return ti === term.length;
  }
  
  /**
   * scoreApi
   * Returns a numeric relevance score for an API entry against a search term.
   * Score of 0 means no match — exclude from results.
   *
   * @param {object} api  - An ApiEntry object
   * @param {string} term - Lowercased, trimmed search query
   * @returns {number}
   */
  export function scoreApi(api, term) {
    if (!term) return 1; // empty search — everything passes with neutral score
  
    const name = (api.name || "").toLowerCase();
    const SIMILARITY_THRESHOLD = 0.4;
  
    // Tier 1: Exact name match
    if (name === term) return 100;
  
    // Tier 2: Name starts with term
    if (name.startsWith(term)) return 80;
  
    // Tier 3: Name contains term as substring
    if (name.includes(term)) return 60;
  
    // Tier 4: High similarity on name (typo tolerance)
    const nameSim = similarityScore(name, term);
    if (nameSim >= SIMILARITY_THRESHOLD) {
      return Math.round(40 + nameSim * 19);
    }
  
    // Tier 5: Fuzzy character sequence on name (min 3 chars)
    if (term.length >= 3 && fuzzyCharMatch(name, term)) return 20;
  
    // Tier 6: Match on other fields
    const otherFields = [
      api.category,
      api.description,
      api.developer,
      api.programming_language,
      api.framework,
      api.cost,
      api.design_pattern,
    ];
  
    for (const field of otherFields) {
      const f = (field || "").toLowerCase();
      if (f.includes(term)) return 10;
      if (similarityScore(f, term) >= SIMILARITY_THRESHOLD) return 8;
    }
  
    return 0;
  }