import axios from "axios";
const api = axios.create({ baseURL: "/api", timeout: 60000, headers: { "Content-Type": "application/json" } });
export default api;

export const launchToken = (data) => api.post("/token/launch", data);
export const getToken = (id) => api.get(`/token/${id}`);
export const listTokens = (status = null) => api.get("/token/", { params: status ? { status } : {} });
export const analyzeToken = (id) => api.post(`/token/${id}/analyze`);

export const buyToken = (data) => api.post("/trade/buy", data);
export const sellToken = (data) => api.post("/trade/sell", data);
export const getQuote = (tokenId, side, amount) =>
  api.get("/trade/quote", { params: { token_id: tokenId, side, amount } });
export const tradeHistory = (tokenId = null, limit = 50) =>
  api.get("/trade/history", { params: { ...(tokenId && { token_id: tokenId }), limit } });

export const feedTrending = () => api.get("/feed/trending");
export const feedNew = () => api.get("/feed/new");
export const feedGraduating = () => api.get("/feed/graduating");
export const feedGraduated = () => api.get("/feed/graduated");
