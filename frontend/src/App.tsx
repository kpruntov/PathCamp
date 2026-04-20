import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { useAuth } from './hooks/useAuth';
import LoginView from './views/LoginView';
import RegistrationView from './views/RegistrationView';
import './App.css';

function Home() {
    const auth = useAuth();

    return (
        <div>
            <h2>Home</h2>
            {auth.user ? (
                <div>
                    <p>Welcome, {auth.user.username}!</p>
                    <button onClick={() => auth.logout()}>Logout</button>
                </div>
            ) : (
                <p>You are not logged in.</p>
            )}
        </div>
    );
}

function AppContent() {
  return (
      <div className="App">
          <nav>
              <ul>
                  <li>
                      <Link to="/">Home</Link>
                  </li>
                  <li>
                      <Link to="/login">Login</Link>
                  </li>
                  <li>
                      <Link to="/register">Register</Link>
                  </li>
              </ul>
          </nav>

          <main>
              <Routes>
                  <Route path="/" element={<Home />} />
                  <Route path="/login" element={<LoginView />} />
                  <Route path="/register" element={<RegistrationView />} />
                  <Route path="*" element={<Navigate to="/" />} />
              </Routes>
          </main>
      </div>
  );
}


function App() {
  return (
    <Router>
        <AuthProvider>
            <AppContent />
        </AuthProvider>
    </Router>
  );
}

export default App;

// @trace TASK-020
// @trace TASK-021
