export const API_BASE_URL =
  window.location.hostname === "your-production-domain.com"
    ? "https://your-production-api.com"
    : "http://localhost:5000";