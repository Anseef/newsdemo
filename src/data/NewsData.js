import newsJson from './NewsData.json';

// Safe extraction with fallback array to prevent mapping errors
export const newsItems = Array.isArray(newsJson) ? newsJson : [];

export const getNewsById = (id) => {
  return newsItems.find((item) => item.id === Number(id));
};

export const getLatestNewsFeed = () => {
  return [...newsItems].sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt));
};

export const getNewsByTag = (tag) => {
  const filtered = newsItems.filter(item => item.tag?.toLowerCase() === tag.toLowerCase());
  return filtered.sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt));
};

export const getAllStates = () => {
  const states = newsItems.map((item) => item.state).filter(Boolean);
  return ["All", ...new Set(states)];
};

export default newsItems;