import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import NewsPage from './pages/NewsPage';

// Simple fallback Home component for landing view demonstration
function HomePlaceholder() {
  return (
    <div style={{ textAlign: 'center', padding: '80px 20px' }}>
      <h2 style={{ fontSize: '28px', color: '#0F172A', marginBottom: '12px' }}>Welcome to Vidyabhyasam Portal</h2>
      <p style={{ color: '#64748B', marginBottom: '24px' }}>Discover colleges, verify admissions, and explore live tracking feeds.</p>
      <Link to="/news" style={{ background: '#1B6CA8', color: '#fff', textDecoration: 'none', padding: '12px 24px', borderRadius: '8px', fontWeight: 700 }}>
        Open News Board →
      </Link>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <div style={appStyles.layout}>
        
        {/* Navigation Headbar */}
        <nav style={appStyles.navbar}>
          <div style={appStyles.navInner}>
            <Link to="/" style={appStyles.logo}>
              🎓 Vidyabhyasam <span style={{ color: '#E8470A' }}>Portal</span>
            </Link>
            <div style={appStyles.links}>
              <Link to="/" style={appStyles.link}>Home</Link>
              <Link to="/news" style={appStyles.link}>News Alerts</Link>
            </div>
          </div>
        </nav>

        {/* Dynamic Route Viewport Content */}
        <main style={appStyles.main}>
          <Routes>
            <Route path="/" element={<HomePlaceholder />} />
            <Route path="/news" element={<NewsPage />} />
          </Routes>
        </main>

        {/* Global Structural Footer */}
        <footer style={appStyles.footer}>
          <p>© 2026 Vidyabhyasam Portal. Built with React & Vite. All rights reserved.</p>
        </footer>

      </div>
    </Router>
  );
}

const appStyles = {
  layout: { display: 'flex', flexDirection: 'column', minHeight: '100vh', background: '#F8FAFC' },
  navbar: { height: '64px', background: '#0F172A', borderBottom: '1px solid #1E293B', display: 'flex', alignItems: 'center', padding: '0 20px', position: 'sticky', top: 0, zIndex: 999 },
  navInner: { width: '100%', maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  logo: { color: '#FFF', textDecoration: 'none', fontSize: '18px', fontWeight: '800' },
  links: { display: 'flex', gap: '20px' },
  link: { color: '#94A3B8', textDecoration: 'none', fontSize: '14px', fontWeight: '600', transition: 'color 0.2s' },
  main: { flex: 1 },
  footer: { background: '#0F172A', color: '#64748B', textAlign: 'center', padding: '20px', fontSize: '13px', borderTop: '1px solid #1E293B' }
};