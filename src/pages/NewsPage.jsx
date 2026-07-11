import React, { useState } from 'react';
import { getLatestNewsFeed, getAllStates } from '../data/NewsData';

export default function NewsPage() {
  const [selectedState, setSelectedState] = useState('All');

  // Grab the automated chronologically sorted feed items
  const newsList = getLatestNewsFeed();
  const uniqueStates = getAllStates();

  // Filter items seamlessly depending on active state tabs
  const filteredNews = newsList.filter(item => {
    if (selectedState === 'All') return true;
    return item.state.toLowerCase() === selectedState.toLowerCase();
  });

  return (
    <div style={styles.container}>
      {/* Page Header */}
      <div style={styles.header}>
        <div style={styles.liveIndicator}>
          <span style={styles.liveDot} />
          <span style={styles.liveText}>LIVE UPDATES DESK</span>
        </div>
        <h1 style={styles.title}>South India Higher Education News</h1>
        <p style={styles.subtitle}>
          Real-time updates on allotments, schedules, and admissions across southern regions.
        </p>
      </div>

      {/* State Filter System */}
      <div style={styles.filterRow}>
        {uniqueStates.map((state) => (
          <button
            key={state}
            onClick={() => setSelectedState(state)}
            style={{
              ...styles.filterTab,
              ...(selectedState === state ? styles.activeTab : {})
            }}
          >
            {state === 'All' ? '🌐 All Regions' : `📍 ${state}`}
          </button>
        ))}
      </div>

      {/* Cards Stream Grid */}
      <div style={styles.grid}>
        {filteredNews.length === 0 ? (
          <div style={styles.noData}>No active alerts found for this region today.</div>
        ) : (
          filteredNews.map((news) => (
            <div key={news.id} style={styles.card}>
              <div style={styles.cardHeader}>
                <span style={{ ...styles.badge, backgroundColor: news.color, color: '#fff' }}>
                  {news.icon} {news.tag}
                </span>
                <span style={styles.stateLabel}>{news.state}</span>
              </div>
              
              <h3 style={styles.cardTitle}>{news.title}</h3>
              <p style={styles.cardDate}>🗓 Target Date: <strong>{news.date}</strong></p>
              <p style={styles.cardDesc}>{news.description}</p>
              
              <div style={styles.coursesRow}>
                {news.courses.map(course => (
                  <span key={course} style={styles.courseBadge}>{course}</span>
                ))}
              </div>

              {news.applyLink && (
                <a 
                  href={news.applyLink} 
                  target="_blank" 
                  rel="noreferrer" 
                  style={{ ...styles.portalBtn, backgroundColor: news.color }}
                >
                  Visit Official Authority Portal ↗
                </a>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

const styles = {
  container: { maxWidth: '1200px', margin: '0 auto', padding: '40px 20px', fontFamily: 'system-ui, sans-serif', color: '#1E293B' },
  header: { textAlign: 'center', marginBottom: '40px' },
  liveIndicator: { display: 'inline-flex', alignItems: 'center', gap: '8px', background: '#FEF2F2', padding: '6px 14px', borderRadius: '20px', marginBottom: '16px' },
  liveDot: { width: '8px', height: '8px', backgroundColor: '#EF4444', borderRadius: '50%', boxShadow: '0 0 8px #EF4444' },
  liveText: { fontSize: '11px', fontWeight: '800', color: '#EF4444', letterSpacing: '0.5px' },
  title: { fontSize: '32px', fontWeight: '800', margin: '0 0 10px 0', color: '#0F172A' },
  subtitle: { color: '#64748B', margin: 0, fontSize: '16px' },
  filterRow: { display: 'flex', gap: '10px', overflowX: 'auto', paddingBottom: '16px', marginBottom: '32px', borderBottom: '1px solid #E2E8F0' },
  filterTab: { padding: '8px 18px', borderRadius: '20px', border: '1px solid #E2E8F0', background: '#FFF', color: '#64748B', fontWeight: 600, cursor: 'pointer', fontSize: '14px', whiteSpace: 'nowrap' },
  activeTab: { background: '#0F172A', color: '#FFF', borderColor: '#0F172A' },
  grid: { display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: '24px' },
  card: { background: '#FFF', border: '1px solid #E2E8F0', borderRadius: '16px', padding: '24px', display: 'flex', flexDirection: 'column', gap: '12px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' },
  cardHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  badge: { padding: '4px 12px', borderRadius: '20px', fontSize: '11px', fontWeight: 700, textTransform: 'uppercase' },
  stateLabel: { fontSize: '12px', color: '#64748B', fontWeight: 600 },
  cardTitle: { fontSize: '18px', fontWeight: '700', color: '#0F172A', margin: 0, lineHeight: 1.4 },
  cardDate: { fontSize: '13px', color: '#475569', margin: 0 },
  cardDesc: { fontSize: '14px', color: '#475569', lineHeight: 1.6, margin: 0 },
  coursesRow: { display: 'flex', gap: '6px', flexWrap: 'wrap', marginTop: 'auto', paddingBottom: '8px' },
  courseBadge: { background: '#F1F5F9', padding: '4px 10px', borderRadius: '6px', fontSize: '12px', fontWeight: 600, color: '#475569' },
  portalBtn: { color: '#FFF', textDecoration: 'none', padding: '12px', borderRadius: '8px', textAlign: 'center', fontSize: '14px', fontWeight: 700, marginTop: '12px', display: 'block', boxShadow: '0 4px 6px rgba(0,0,0,0.05)' },
  noData: { gridColumn: '1/-1', textAlign: 'center', color: '#64748B', padding: '40px' }
};