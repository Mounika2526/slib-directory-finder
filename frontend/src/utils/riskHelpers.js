/**
 * riskHelpers.js — Risk level styling utilities for SLIB Finder
 *
 * Exports:
 *   getRiskBadgeClass — Tailwind classes for risk badge color
 *   getRiskColor      — Hex color for risk level (used in charts/compare)
 */

/**
 * getRiskBadgeClass
 * Returns Tailwind CSS classes for a risk level badge.
 *
 * @param {string} riskLevel - "High" | "Medium" | "Low"
 * @returns {string} Tailwind class string
 */
export function getRiskBadgeClass(riskLevel) {
    if (riskLevel === "High") return "bg-red-100 text-red-700";
    if (riskLevel === "Medium") return "bg-yellow-100 text-yellow-700";
    return "bg-emerald-100 text-emerald-700";
  }
  
  /**
   * getRiskColor
   * Returns a hex color string for a risk level.
   * Used in charts, compare modal, and card highlights.
   *
   * @param {string} risk - "High" | "Medium" | "Low"
   * @returns {string} Hex color string
   */
  export function getRiskColor(risk) {
    if (risk === "High") return "#dc2626";
    if (risk === "Medium") return "#d97706";
    return "#059669";
  }