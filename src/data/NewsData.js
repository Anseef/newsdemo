import newsJson from './NewsData.json';

// Export the JSON array directly
export const newsItems = newsJson;

// ==========================================
// DATA RETRIEVAL & SORTING ENGINE
// ==========================================

/**
 * Safely look up an individual news entity by item ID.
 */
export const getNewsById = (id) => {
  return newsItems.find((item) => item.id === Number(id));
};

/**
 * Returns news items sorted chronologically by publishedAt (NEWEST items first).
 */
export const getLatestNewsFeed = () => {
  return [...newsItems].sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt));
};

/**
 * Filter news items by a specific tag/status, sorted by date.
 */
export const getNewsByTag = (tag) => {
  const filtered = newsItems.filter(item => item.tag.toLowerCase() === tag.toLowerCase());
  return filtered.sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt));
};

/**
 * Get all unique states available in the dataset (Required for Filter Tabs!)
 */
export const getAllStates = () => {
  const states = newsItems.map((item) => item.state);
  return ["All", ...new Set(states)];
};

/**
 * Get all unique tags available in the dataset
 */
export const getAllTags = () => {
  const tags = newsItems.map((item) => item.tag);
  return ["All", ...new Set(tags)];
};

export default newsItems;