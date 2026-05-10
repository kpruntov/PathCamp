// @trace TASK-013
// @trace TASK-039
import { useState, useEffect } from 'react'
import { UserManagement } from './components/UserManagement'
import { AuthForms } from './components/AuthForms'
import './App.css'

function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token);
    } else {
      localStorage.removeItem('token');
    }
  }, [token]);

  const handleLoginSuccess = (newToken: string) => {
    setToken(newToken);
  };

  const handleLogout = () => {
    setToken(null);
  };

  return (
    <div className="min-h-screen">
      {token && (
        <div className="p-4 flex justify-end">
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
      ) : (
        <UserManagement />
      )}
    </div>
  )
}

export default App
