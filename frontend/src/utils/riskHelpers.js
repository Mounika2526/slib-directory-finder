/**
 * riskHelpers.js — Risk level styling utilities for SLIB Finder
 *
 * Exports:
 *   getRiskBadgeClass — Tailwind classes for risk badge color
 *   getRiskColor      — Hex color for risk level (used in charts/compare)
 *
 * Risk levels: "Low" | "Medium" | "High"
 * These helpers ensure consistent risk styling across all components.
 */

/**
 * getRiskBadgeClass
 * Returns Tailwind CSS classes for a risk level badge.
 * Used on API cards to visually indicate stability.
 *
 * @param {string} riskLevel - "High" | "Medium" | "Low"
 * @returns {string} Tailwind class string
 */
export function getRiskBadgeClass(riskLevel) {
  // High risk — red badge (unstable/pre-release versions)
  if (riskLevel === "High") return "bg-red-100 text-red-700";

  // Medium risk — yellow badge (unknown or placeholder versions)
  if (riskLevel === "Medium") return "bg-yellow-100 text-yellow-700";

  // Low risk — green badge (stable, versioned releases)
  return "bg-emerald-100 text-emerald-700";
}

/**
 * getRiskColor
 * Returns a hex color string for a risk level.
 * Used in charts, compare modal highlights, and card color indicators.
 *
 * @param {string} risk - "High" | "Medium" | "Low"
 * @returns {string} Hex color string
 */
export function getRiskColor(risk) {
  if (risk === "High") return "#dc2626";   // red-600
  if (risk === "Medium") return "#d97706"; // amber-600
  return "#059669";                        // emerald-600
}