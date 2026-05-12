// @trace TASK-013
// @trace TASK-039
// @trace TASK-040
// @trace TASK-018
import { useState, useEffect } from 'react'
import { UserManagement } from './components/UserManagement'
import { AuthForms } from './components/AuthForms'
import { CampaignForm } from './components/CampaignForm'
import './App.css'

interface User {
  id: number;
  username: string;
  email: string;
  status: string;
  role: string;
}

function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
      fetch('/auth/me', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      .then(res => {
        if (!res.ok) throw new Error('Invalid token');
        return res.json();
      })
      .then(data => setUser(data))
      .catch(() => {
        localStorage.removeItem('token');
        setToken(null);
        setUser(null);
      });
    } else {
      localStorage.removeItem('token');
      setUser(null);
    }
  }, [token]);

  const handleLoginSuccess = (newToken: string) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  return (
    <div className="min-h-screen">
      {token && user && (
        <div className="p-4 flex justify-between items-center">
          <div className="text-fantasy-accent font-bold">
            Welcome, {user.username} ({user.role})
          </div>
          <button 
            onClick={handleLogout}
            className="bg-fantasy-dark border border-fantasy-accent text-fantasy-accent px-4 py-2 rounded hover:bg-fantasy-accent hover:text-fantasy-dark transition-colors font-bold uppercase text-sm tracking-wide"
          >
            Logout
          </button>
        </div>
      )}
      
      {!token ? (
        <AuthForms onLoginSuccess={handleLoginSuccess} />
      ) : user?.role === 'Admin' ? (
        <UserManagement />
      ) : user ? (
        <div className="p-8">
          <h2 className="text-2xl font-bold mb-8 text-fantasy-text text-center">GM Dashboard</h2>
          <CampaignForm onSuccess={(id) => alert(`Campaign ${id} created!`)} />
        </div>
      ) : (
        <div className="p-8 text-center text-fantasy-accent animate-pulse">Loading...</div>
      )}
    </div>
  )
}

export default App
